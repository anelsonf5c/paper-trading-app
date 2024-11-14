from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('history/', views.transaction_history, name='transaction_history'),
    path('update/<str:symbol>/', views.update_instrument, name='update_instrument'),
    path('buy/<str:symbol>/', views.buy_instrument, name='buy_instrument'),
    path('sell/<str:symbol>/', views.sell_instrument, name='sell_instrument'),
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
    path('register/', views.register, name='register'),  # Custom registration view
]



