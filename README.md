# Paper Trading Application

## Project Overview
This is a Paper Trading Application built with Django, where users can test their trading skills by buying and selling financial instruments with virtual money. The application provides a simple interface to view available instruments, track transactions, and monitor the user's portfolio.

## Features
- **View Available Instruments**: Display a list of financial instruments with their prices.
- **Buy and Sell Instruments**: Users can buy or sell quantities of instruments.
- **Portfolio Tracking**: Displays the user’s current holdings and total balance.
- **Transaction History**: Shows the user's transaction history with details of each buy/sell action.
- **Historical Data**: View historical price trends for each instrument.

## Project Structure
- **paper_trader/**: The main Django project folder containing settings, URL configurations, etc.
- **trade_app/**: The Django app containing the core logic of the application.

## Technologies Used
- **Python**: Backend programming language.
- **Django**: Web framework for building the application.
- **SQLite**: Default database for storing user data.
- **yfinance**: Python library for retrieving financial data.

## Installation Instructions
1. Clone the repository:
   git clone https://github.com/anelsonf5c/paper-trading-app.git
cd paper-trading-app

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/anelsonf5c/paper-trading-app.git
   cd paper-trading-app
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

6. Visit `http://127.0.0.1:8000` to access the application.

## Technologies Used
- Python, Django, Django ORM
- Yahoo Finance API for financial data
- Matplotlib for data visualization
- Bootstrap for styling

## License
MIT License
