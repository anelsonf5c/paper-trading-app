from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Instrument, Transaction, Portfolio
from .forms import BuyForm, SellForm
import yfinance as yf
import matplotlib.pyplot as plt
import io

# Home view - Displays the list of available instruments and their prices
def home(request):
    instruments = Instrument.objects.all()
    return render(request, 'trade_app/home.html', {'instruments': instruments})

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'trade_app/register.html', {'form': form})

# Portfolio view - Shows the user's portfolio, including balance and owned instruments
@login_required
def portfolio(request):
    # Retrieve only the transactions and portfolio of the logged-in user
    portfolio_items = Transaction.objects.filter(user=request.user, transaction_type='buy')
    total_balance = Portfolio.objects.filter(user=request.user).first().balance

    context = {
        'portfolio_items': portfolio_items,
        'balance': total_balance,
    }
    return render(request, 'trade_app/portfolio.html', context)

# Transaction history view - Shows the history of all transactions
@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'trade_app/history.html', {'transactions': transactions})

# Function to load data from Yahoo Finance and update the Instrument model
def load_data(symbol):
    data = yf.download(symbol, start="2022-01-01")
    if not data.empty:
        latest_price = data['Close'][-1]
        instrument, created = Instrument.objects.get_or_create(symbol=symbol)
        instrument.price = latest_price
        instrument.save()
    else:
        print("No data found for the symbol.")

# View to update the instrument data for a specific symbol by calling load_data
def update_instrument(request, symbol):
    load_data(symbol)
    return HttpResponse(f"Instrument data for {symbol} updated.")

# Buy instrument view - Allows the user to buy a specified quantity of an instrument
@login_required
def buy_instrument(request, symbol):
    instrument = get_object_or_404(Instrument, symbol=symbol)
    portfolio = Portfolio.objects.filter(user=request.user).first()
    form = BuyForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        quantity = form.cleaned_data['quantity']
        total_cost = instrument.price * quantity

        if portfolio.balance >= total_cost:
            portfolio.balance -= total_cost
            portfolio.save()

            Transaction.objects.create(
                user=request.user,
                instrument=instrument,
                quantity=quantity,
                transaction_type='buy'
            )
            return redirect('portfolio')
        else:
            return HttpResponse("Insufficient funds!")

    return render(request, 'trade_app/buy_instrument.html', {'instrument': instrument, 'form': form})

# Sell instrument view - Allows the user to sell a specified quantity of an instrument
@login_required
def sell_instrument(request, symbol):
    instrument = get_object_or_404(Instrument, symbol=symbol)
    portfolio = Portfolio.objects.filter(user=request.user).first()
    form = SellForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        quantity = form.cleaned_data['quantity']
        transactions = Transaction.objects.filter(user=request.user, instrument=instrument, transaction_type='buy')
        total_owned = sum([t.quantity for t in transactions])

        if total_owned >= quantity:
            portfolio.balance += instrument.price * quantity
            portfolio.save()

            Transaction.objects.create(
                user=request.user,
                instrument=instrument,
                quantity=-quantity,
                transaction_type='sell'
            )
            return redirect('portfolio')
        else:
            return HttpResponse("Insufficient quantity to sell!")

    return render(request, 'trade_app/sell_instrument.html', {'instrument': instrument, 'form': form})

# Historical data chart view - Displays historical price chart for a given instrument
def instrument_history(request, symbol):
    data = yf.download(symbol, start="2022-01-01")
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'])
    plt.title(f'{symbol} Price History')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return FileResponse(buffer, content_type='image/png')
