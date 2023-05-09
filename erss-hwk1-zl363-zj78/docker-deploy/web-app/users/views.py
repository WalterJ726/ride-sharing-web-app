from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from .forms import UserRegistrationForm, UserUpdateForm, DriverRegistrationForm, RideRequestForm, RideSearchForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .models import User, RideOwner, RideDriver, RideSharer
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from datetime import datetime

# Create your views here.
def greet(request):
    return HttpResponse("Hello World!")

def home_page(request):
    return render(request, "home.html")

def create_user_account(request):
    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            
            name = register_form.cleaned_data.get('name')
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password1')
            email = register_form.cleaned_data.get('email')
            user = User(username=username, password=password, name=name, email=email)
            user.save()

            messages.success(request, "Your account is successfully created!")
            return HttpResponseRedirect(reverse('login'))
        else:
            messages.error(request, "Invalid registration. Please retry.")
    else:
        register_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': register_form})

@login_required
def update_profile(request):
    user = get_object_or_404(User, username=request.user)
    if (request.method == "POST"):
        update_form = UserUpdateForm(data=request.POST, instance=request.user)
        if update_form.is_valid():
            user.password = update_form.cleaned_data.get('password')
            user.email = update_form.cleaned_data.get('email')

            # simple check
            if len(user.password) < 8:
                messages.error(request, 'Password should be at least 8 characters long!')
                return redirect('update-profile')
            if user.password == user.username:
                messages.error(request, 'Password cannot be the same as the username!')
                return redirect('update-profile')
            
            user.save()

            _user = update_form.save(commit=False)
            _user.username = user.username
            request.user.set_password(user.password)
            _user.save()
            return redirect('home')
        else:
            messages.error(request, "failed to update your profile")
    else:
        update_form = UserUpdateForm()
    return render(request, 'registration/user_update.html', {'form': update_form})

# ------------ #
#    Driver    #
# ------------ #
def driver_home(request):
    return render(request, "driver_home.html")

@login_required
def register_driver(request):
    user = get_object_or_404(User, username=request.user.username)
    
    if request.method == "POST":
        register_form = DriverRegistrationForm(request.POST)
        if register_form.is_valid():
            driver = register_form.save(commit=False)
            driver.username = User.objects.get(username = request.user.username)
            driver.save()
            messages.success(request, "Congratulations! You have become a driver!")
            return redirect('driver-home')
        else:
            messages.error(request, "Invalid registration. Please retry.")
    else:
        register_form = DriverRegistrationForm()
    return render(request, 'registration/register_driver.html', {'form': register_form})


class RideDriverUnregister(ListView):
    model = RideDriver
    template_name = 'driver_confirm_delete.html'
    success_url = reverse_lazy('driver-home')

    def get_queryset(self):
        driver = get_object_or_404(RideDriver, username=self.request.user.username)
        return RideDriver.objects.filter(username__exact = driver.username)
    
    
@login_required
def delete_driver(request):
    driver = User.objects.get(username = request.user.username)
    RideDriver.objects.filter(username__exact = request.user.username).delete()
    orders = RideOwner.objects.filter(driver_name__exact = driver.name,
                                      status__exact = 'confirmed').exclude(username = driver.username)

    for ride in orders:
        ride.status = 'open'
        ride.driver_name = ''
        ride.plate_num = ''
        ride.save()

        rider = ride.username
        send_mail("Ride Cancellation",
              "One of your rides just got cancelled, please find a new ride",
              "",
              [rider.email], fail_silently=False)
        sharers = RideSharer.objects.filter(owner_id = ride.id)
        for sharer in sharers:
            send_mail("Ride Cancellation",
                      "One of your joined rides just got cancelled, please find a new ride",
                      "",
                      [sharer.username.email], fail_silently=False)
    
    return redirect('driver-home')

    
class RideDriverNewRides(ListView):
    template_name = 'driver_ride_list.html'

    def get_queryset(self):
        driver = get_object_or_404(RideDriver, username=self.request.user.username)
        return RideOwner.objects.filter(num_passenger__lte = driver.max_passengers,
                                        vehicle_type__exact = driver.vehicle_type,
                                        special_request__in = ['', driver.special_request],
                                        status__exact = 'open',
                                        arrival__gt = datetime.now()).exclude(username=driver.username).order_by('arrival')


class RideDriverEditRides(ListView):
    template_name = 'driver_edit_list.html'

    def get_queryset(self):
        driver = get_object_or_404(RideDriver, username=self.request.user.username)
        return RideOwner.objects.filter(status__exact = 'confirmed',
                                        driver_name = driver.username).exclude(username=driver.username).order_by('arrival')

    
class RideDriverPastRides(ListView):
    template_name = 'driver_past_list.html'

    def get_queryset(self):
        driver = get_object_or_404(RideDriver, username=self.request.user.username)
        return RideOwner.objects.filter(driver_name__exact = User.objects.get(username = self.request.user.username).name,
                                        status__exact = 'complete').order_by('-arrival')

    
@login_required
def driver_confirm(request, owner_id):
    rider = RideOwner.objects.filter(pk=owner_id, status='open').first()
    if not rider:
        return HttpResponseBadRequest("Selected ride order is no longer valid. Confirmation failed. Please go to pick anthoer one.")
    rider.status = "confirmed"
    rider.driver_name = User.objects.get(username = request.user.username).name
    rider.plate_num = RideDriver.objects.get(username = request.user.username).plate_num
    rider.save()
    
    send_mail("Ride Confirmation",
              "One of your rides just got confirmed!",
              "",
              [rider.username.email], fail_silently=False)
    sharers = RideSharer.objects.filter(owner_id = owner_id)
    for sharer in sharers:
        send_mail("Ride Confirmation",
                  "One of your joined rides just got confirmed!",
                  "",
                  [sharer.username.email], fail_silently=False)
    return redirect('driver-home')
    
@login_required
def driver_complete(request, owner_id):
    driver = get_object_or_404(RideDriver, username=request.user.username)
    rider = RideOwner.objects.filter(pk=owner_id, plate_num=driver.plate_num).first()
    rider.status = "complete"
    rider.save()
    return redirect('driver-home')
    
# ------------ #
#    Owner     #
# ------------ #    
def owner_home(request):
    return render(request, "owner_home.html")

@login_required
def request_ride(request):   
    if request.method == "POST":
        request_form = RideRequestForm(request.POST)
        if request_form.is_valid():
            new_ride = request_form.save(commit=False)
            new_ride.username = User.objects.get(username = request.user.username)
            new_ride.save()
            messages.success(request, "Congratulations! You have successfully request your ride!")
            return redirect('owner-home')
        else:
            messages.error(request, "Invalid request. Please retry.")
    else:
        request_form = RideRequestForm()
    return render(request, 'owner_request.html', {'form': request_form})

class OwnerEditRides(ListView):
    template_name = 'owner_edit_list.html'

    def get_queryset(self):
        return RideOwner.objects.filter(username__exact = self.request.user.username,
                                        status__in = ['open', 'confirmed']).order_by('arrival')


class OwnerUpdateRides(UpdateView):
    model = RideOwner
    template_name = 'owner_request.html'
    fields = ['dest_addr', 'arrival', 'num_passenger', 'vehicle_type', 'special_request', 'sharable']
    success_url = reverse_lazy('owner-home')

    def get_queryset(self):
        return RideOwner.objects.filter(id = self.kwargs['pk'],
                                        username = self.request.user.username)

        
class OwnerCancelRides(DeleteView):
    model = RideOwner
    template_name = 'rideowner_confirm_delete.html'
    success_url = reverse_lazy('owner-home')

    def form_valid(self, form):
        #response = super(OwnerCancelRides, self).delete(request, *args, **kwargs)
        sharers = RideSharer.objects.filter(owner_id = self.kwargs['pk'])
        for sharer in sharers:
            send_mail("Ride Cancellation",
                      "One of your joined rides just got cancelled, please find a new ride",
                      "",
                      [sharer.username.email], fail_silently=False)
        return super().form_valid(form)

    def get_queryset(self):
        return RideOwner.objects.filter(id = self.kwargs['pk'],
                                        username = self.request.user.username)

        
class OwnerPastRides(ListView):
    template_name = 'driver_past_list.html'

    def get_queryset(self):
        return RideOwner.objects.filter(username__exact = self.request.user.username,
                                        status__exact = 'complete').order_by('-arrival')


# ------------ #
#    Sharer    #
# ------------ #    
def sharer_home(request):
    return render(request, "sharer_home.html")

@login_required
def search_ride(request):   
    if request.method == "POST":
        search_form = RideSearchForm(request.POST)
        user = User.objects.get(username = request.user.username)

        if search_form.is_valid():
            
            if RideSharer.objects.filter(username=user, owner_id=-1).exists():
                sharer = RideSharer.objects.get(username=user, owner_id=-1)
                sharer.dest_addr = search_form.cleaned_data.get('dest_addr')
                sharer.arrival_start = search_form.cleaned_data.get('arrival_start')
                sharer.arrival_end = search_form.cleaned_data.get('arrival_end')
                sharer.num_passengers = search_form.cleaned_data['num_passengers']
            else:
                sharer = RideSharer(username = user,
                                    dest_addr = search_form.cleaned_data.get('dest_addr'),
                                    arrival_start = search_form.cleaned_data['arrival_start'],
                                    arrival_end = search_form.cleaned_data['arrival_end'],
                                    num_passengers = search_form.cleaned_data['num_passengers']
                                    )
            sharer.save()
            return redirect('search-result')
        else:
            messages.error(request, "Invalid request. Please retry.")
    else:
        search_form = RideSearchForm()
    return render(request, 'ridesharer_form.html', {'form': search_form})


    
class SharerSearchResults(ListView):
    template_name = 'ridesharer_search_result.html'
    model = RideOwner

    def get_queryset(self):
        sharer = get_object_or_404(RideSharer, username = self.request.user.username, owner_id = -1)
        return RideOwner.objects.filter(dest_addr__iexact = sharer.dest_addr,
                                        arrival__gte = sharer.arrival_start,
                                        arrival__lte = sharer.arrival_end,
                                        arrival__gt = datetime.now(),
                                        sharable__exact = True,
                                        status__exact = 'open').exclude(username = self.request.user.username).order_by('arrival')


@login_required
def sharer_join(request, owner_id):
    rider = RideOwner.objects.filter(pk=owner_id, sharable=True).first()
    sharer = RideSharer.objects.get(username=request.user.username, owner_id=-1)
    sharer.owner_id = owner_id;
    rider.num_sharer += sharer.num_passengers
    rider.num_passenger += sharer.num_passengers
    rider.save()
    sharer.save()
    messages.success(request, "Congratulations! You have successfully joined the ride!")
    return redirect('sharer-home')
    

class SharerEditRides(ListView):
    template_name = 'sharer_edit_list.html'

    def get_queryset(self):
        try:
            sharer = RideSharer.objects.filter(username = self.request.user.username,
                                               owner_id__gte = 0)
        except RideSharer.DoesNotExist:
            return RideOwner.objects.filter(id=-1)

        riders = RideOwner.objects.filter(status__exact = 'open', sharable = True)
        res = RideOwner.objects.none()
        for ride in sharer:
            res = res | riders.filter(id = ride.owner_id)
        return res.order_by('arrival')

        
class SharerUpdateRides(UpdateView):
    model = RideOwner
    template_name = 'sharer_update_request.html'
    fields = ['num_sharer']
    success_url = reverse_lazy('sharer-home')
    
    def form_valid(self, form):
        ID = self.kwargs['pk']
        sharer = RideSharer.objects.get(owner_id = ID)
        old_sharer_num = sharer.num_passengers
        new_sharer_num = form.cleaned_data.get('num_sharer')
        if (new_sharer_num <= 0):
            raise ValidationError("Invalid input. If you would like to cancel, please go back to cancel")
        sharer = form.save(commit=False)
        rider = RideOwner.objects.get(id = ID)
        new_num_passenger = rider.num_passenger + (new_sharer_num - old_sharer_num)
        new_num_sharer = rider.num_sharer + (new_sharer_num - old_sharer_num)
        RideOwner.objects.filter(id = ID).update(num_passenger=new_num_passenger, num_sharer=new_num_sharer)
        #rider.num_passenger += new_sharer_num - old_sharer_num
        #rider.num_sharer += new_sharer_num - old_sharer_num
        #rider.save(['num_passenger', 'num_sharer'])
        #rider.save()
        sharer.save()
        return super(SharerUpdateRides, self).form_valid(form)
        

@login_required
def sharer_cancel(request, owner_id):
    rider = RideOwner.objects.get(pk = owner_id, username = request.user.username)
    sharer = RideSharer.objects.get(owner_id = owner_id,
                                    username = request.user.username)
    rider.num_passenger -= sharer.num_passengers
    rider.num_sharer -= sharer.num_passengers
    rider.save()
    sharer.delete()
    return redirect('sharer-home')


class SharerPastRides(ListView):
    template_name = 'driver_past_list.html'

    def get_queryset(self):
        sharer = RideSharer.objects.filter(username = self.request.user.username,
                                           owner_id__gte = 0)
        riders = RideOwner.objects.filter(status__exact = 'complete',
                                          sharable = True,
                                          num_sharer__gt = 0)
        for record in sharer:
            riders.filter(id = record.owner_id)
        return riders.order_by('-arrival')
