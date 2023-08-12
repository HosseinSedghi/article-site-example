from django.shortcuts import render, redirect
from django.views import View

from contact_module.forms import TicketForm
from contact_module.models import Ticket


# Create your views here.


class TicketView(View):
    def get(self, request):
        ticket_form = TicketForm()
        return render(request, 'contact_module/ticket.html', {
            'ticket_form': ticket_form
        })

    def post(self, request):
        ticket_form = TicketForm(request.POST)
        if ticket_form.is_valid():
            name = ticket_form.cleaned_data.get('full_name')
            text = ticket_form.cleaned_data.get('text')
            if request.user.is_authenticated:
                new_ticket = Ticket(name=name, text=text, user_id=request.user.id)
            else:
                new_ticket = Ticket(name=name, text=text)
            new_ticket.save()
        return redirect('ticket-page')