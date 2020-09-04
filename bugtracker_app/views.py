from django.shortcuts import render, HttpResponseRedirect, reverse
from bugtracker_app.models import CustomUser, Ticket
from bugtracker_app.forms import LoginForm, AddTicketForm
from django.contrib.auth import login, logout, authenticate
from bugtracker.settings import AUTH_USER_MODEL
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    tickets = Ticket.objects.all()
    new_tickets = Ticket.objects.filter(completion_status='New')
    inprogress_tickets = Ticket.objects.filter(completion_status='In Progress')
    completed_tickets = Ticket.objects.filter(completion_status='Done')
    invalid_tickets = Ticket.objects.filter(completion_status='Invalid')
    return render(request, "index.html", {"title": "Bug Tracker", "tickets": tickets, "new_tickets": new_tickets, "inprogress_tickets": inprogress_tickets, "completed_tickets": completed_tickets, "invalid_tickets": invalid_tickets})



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(
                request, username=data.get("username"), password=data.get("password")
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get("next",reverse("homepage")))

    form = LoginForm()
    return render(request, "generic_form.html", {"form": form})



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))



@login_required
def add_ticket_view(request):
    if request.method == "POST":
        form = AddTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.create(
                title=data.get("title"), 
                description=data.get("description"), 
                created_by=request.user,
            )
            return HttpResponseRedirect(reverse("homepage"))
    form = AddTicketForm()
    return render(request, "generic_form.html", {"form": form})



@login_required
def edit_ticket_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == "POST":
        form = AddTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ticket.title = data["title"]
            ticket.description = data["description"]
            ticket.save()
        return HttpResponseRedirect(reverse("ticket_details", args=[ticket.id]))
    data = {
        "title": ticket.title,
        "description": ticket.description
    }
    form = AddTicketForm(initial=data)
    return render(request, "generic_form.html", {"form": form})



@login_required
def ticket_detail_view(request, ticket_id):
    ticket = Ticket.objects.filter(id=ticket_id).first()
    return render(request, 'ticket_detail.html', {'ticket': ticket})



@login_required
def user_detail_view(request, user_id):
    bugtracker_user = CustomUser.objects.filter(id=user_id).first()
    tickets_by = Ticket.objects.filter(created_by=bugtracker_user)
    tickets_assigned = Ticket.objects.filter(assigned_to=bugtracker_user)
    tickets_completed = Ticket.objects.filter(completed_by=bugtracker_user)
    return render(request, "user_detail.html", {"bugtracker_user": bugtracker_user, "tickets_by": tickets_by, 'tickets_assigned': tickets_assigned, 'tickets_completed': tickets_completed})



@login_required
def in_progress_view(request, ticket_id):
    inprogress = Ticket.objects.get(id=ticket_id)
    inprogress.assigned_to = request.user
    inprogress.completion_status = 'In Progress'
    inprogress.save()
    return HttpResponseRedirect(reverse("ticket_details", args=[ticket_id]))
    


@login_required
def completed_view(request, ticket_id):
    completed = Ticket.objects.get(id=ticket_id)
    completed.completion_status = 'Done'
    completed.completed_by = request.user
    completed.assigned_to = None
    completed.save()
    return HttpResponseRedirect(reverse("ticket_details", args=[ticket_id]))



@login_required
def invalid_view(request, ticket_id):
    invalid = Ticket.objects.get(id=ticket_id)
    invalid.completion_status = 'Invalid'
    invalid.completed_by = None
    invalid.assigned_to = None
    invalid.save()
    return HttpResponseRedirect(reverse("ticket_details", args=[ticket_id]))