from django.urls import path

from contact_module import views

urlpatterns = [
    path('ticket/', views.TicketView.as_view(), name='ticket-page'),
]