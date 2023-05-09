from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from . import models
from catalog.forms import LoginForm, RegisterModelForm, ownerUpdateModelForm, OrderModelForm, SharerSearchOrderForm, DriverUpdateForm
from datetime import datetime
from django.core.mail import send_mail

def index(request):
    return render(
        request,
        'index.html',
        {},
    )


def register(request):
    """Register a new user."""
    if request.method == 'GET':
        # Display blank registration form.
        form = RegisterModelForm()
        context = {'form': form}
        return render(request, 'register.html', context)

    # Process completed form.
    form = RegisterModelForm(data=request.POST)
    context = {'form': form}
    if form.is_valid():
        new_user = form.save()
        # Log the user in, and then redirect to home page.
        # authenticated_user = authenticate(username=new_user.username,
        #                                     password=request.POST['password1'])
        # login(request, authenticated_user)
        return redirect('/catalog/login/')
    return render(request, 'register.html', context)


def login(request):
    if request.method == 'GET':        
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    ## method == POST
    form = LoginForm(data=request.POST)
    if form.is_valid():
        ## the form is not empty
        # print(form.cleaned_data)
        admin_object = models.User.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "incorrect username or password")
            return render(request, 'login.html', {'form': form})
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}
        return render(request, 'index.html')
    return render(request, 'login.html', {'form': form})

def logout(request):
    request.session.clear()
    return redirect('/catalog/login/')

def ownerUpdate(request):
    """Register a new user."""
    nid = request.session['info']['id']  ## todo: 要和当前id匹配才行
    row_object = models.User.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/catalog/login/')
    
    if request.method == 'GET':
        # Display blank registration form.
        print(row_object)
        print(row_object.email)
        form = ownerUpdateModelForm(instance=row_object)
        context = {'form': form}
        return render(request, 'ownerEditProfile.html', context)

    # Process completed form.
    form = ownerUpdateModelForm(data=request.POST, instance=row_object)
    context = {'form': form}
    if form.is_valid():
        new_user = form.save()
        # Log the user in, and then redirect to home page.
        # authenticated_user = authenticate(username=new_user.username,
        #                                     password=request.POST['password1'])
        # login(request, authenticated_user)
        return redirect('/catalog/login/')
    return render(request, 'ownerEditProfile.html', context)


def ownerIndex(request):
    return render(request, 'ownerIndex.html')

def ownerNewRequest(request):
    if request.method == 'GET':
        form = OrderModelForm()
        # initial={'user': request.session['info']['id']}
        return render(request, 'ownerNewRequest.html', {'form': form})

    ## post request
    # request.POST['user': request.session['info']['id']]
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        new_request = form.save(commit=False)
        new_request.user_id = request.session['info']['id']
        new_request.save() ## added the username 
        return redirect('/catalog/ownerIndex/')
    return render(request, 'ownerNewRequest.html', {'form': form})


def ownerCurrentRequest(request):
    ## TODO: ordered list bullet
    owner_id = request.session['info']['id']
    currentRequest = models.Order.objects.filter(user_id=owner_id, is_completed=False)
    context = {'currentRequest': currentRequest} 
    return render(request, 'ownerCurrentRequest.html', context)

def requestDelete(request, request_id):
    ## todo check the user id is equal to the deleter
    owner_id = request.session['info']['id']
    models.Order.objects.filter(id=request_id).delete()
    currentRequest = models.Order.objects.filter(user_id=owner_id, is_completed=False)
    context = {'currentRequest': currentRequest} 
    return render(request, 'ownerCurrentRequest.html', context)

def requestEdit(request, request_id):
    editOrder = models.Order.objects.filter(id=request_id).first()
    
    if request.method == 'GET':
        form = OrderModelForm(instance=editOrder)
        context = {'form': form}
        return render(request, 'ownerNewRequest.html', {'form': form})

    # Process completed form.
    form = OrderModelForm(data=request.POST, instance=editOrder)
    context = {'form': form}
    if form.is_valid():
        editedOrder = form.save()
        # Log the user in, and then redirect to home page.
        # authenticated_user = authenticate(username=new_user.username,
        #                                     password=request.POST['password1'])
        # login(request, authenticated_user)
        return redirect('/catalog/ownerCurrentRequest/')
    return render(request, 'ownerNewRequest.html', context)

def ownerPassOrder(request):
    owner_id = request.session['info']['id']
    currentAvailableRequests = models.Order.objects.filter(user_id=owner_id, is_confirmed=True, is_completed=True)
    context = {'currentAvailableRequests': currentAvailableRequests} 
    return render(request, 'ownerPassOrder.html', context)  

def sharerIndex(request):
    return render(request, 'sharerIndex.html')


def sharerSearch(request):
    if request.method == 'GET':
        form = SharerSearchOrderForm()
        return render(request, 'sharerSearch.html', {'form': form})
    form = SharerSearchOrderForm(data=request.POST)
    if form.is_valid():
        destination = request.POST['destination']
        earliestTime = request.POST['earliestTime']
        latestTime = request.POST['latestTime']
        number_passengers = request.POST['number_passengers']
        currentShareableRequests = models.Order.objects.filter(arrival_time__gte=earliestTime, arrival_time__lte=latestTime, destination=destination, total_passanger=number_passengers, shareable=True, is_completed=False, is_confirmed=False)
        context = {'currentShareableRequests': currentShareableRequests} 
        return render(request, 'sharerShareableRequests.html', context)
    return render(request, 'sharerSearch.html', {'form': form})
    

def sharerShareableRequests(request):
    ## seems like useless function
    ## TODO: ordered list bullet
    ## show the shared people's usernam could not show it through .user
    currentShareableRequests = models.Order.objects.filter(shareable=True)
    context = {'currentShareableRequests': currentShareableRequests} 
    return render(request, 'sharerShareableRequests.html', context)


def sharerShareableRequestsJoin(request, request_id):
    currentRequest = models.Order.objects.filter(id=request_id)
    current_number = currentRequest.first().total_passanger ## currentRequest.first() is an object
    shared_people = request.session['info']['name']  ## todo: 要和当前id匹配才行
    shared_people_id = request.session['info']['id']
    currentRequest.update(total_passanger=current_number+1, shared_people=shared_people, shared_people_id=shared_people_id)
    return render(request, 'sharerIndex.html')

def sharerCurrentRequests(request):
    shared_people_id = request.session['info']['id']
    shared_people = request.session['info']['name']
    currentRequest = models.Order.objects.filter(shared_people=shared_people, shared_people_id=shared_people_id, is_completed=False, is_confirmed=False)
    context = {'currentRequest': currentRequest} 
    return render(request, 'sharerCurrentRequests.html', context)


def sharerShareableRequestsDelete(request, request_id):
    currentRequest = models.Order.objects.filter(id=request_id)
    current_number = currentRequest.first().total_passanger ## currentRequest.first() is an object
    currentRequest.update(total_passanger=current_number-1, shared_people=None, shared_people_id=None)
    return render(request, 'sharerIndex.html')

def sharerPassOrder(request):
    owner_id = request.session['info']['id']
    currentAvailableRequests = models.Order.objects.filter(shared_people_id=owner_id, is_confirmed=True, is_completed=True)
    context = {'currentAvailableRequests': currentAvailableRequests} 
    return render(request, 'sharerPassOrder.html', context)  


def driverIndex(request):
    return render(request, 'driverIndex.html')


def driverUpdate(request):
    ## TODO: show the original info of driver
    if request.method == 'GET':        
        form = DriverUpdateForm()
        return render(request, 'driverUpdate.html', {'form': form})
    ## method == POST
    form = DriverUpdateForm(data=request.POST)
    context = {'form': form}
    if form.is_valid():
        new_driver = form.save(commit=False)
        new_driver.driver_info = request.session['info']['id']
        new_driver.save() ## added the username 
        return render(request, 'driverIndex.html')
    return render(request, 'driverUpdate.html', context)


def driverSearch(request):
    # TODO: owner himself could both request order and search order
    driverId = request.session['info']['id']
    # print(driverId)
    # driver_object = request.user.driver
    driver_object = models.Driver.objects.filter(driver_info=driverId).first()
    vehicle_type = driver_object.vehicle_type
    maxslot = driver_object.maxslot
    currentAvailableRequests = models.Order.objects.filter(total_passanger__lte=maxslot, vehicle_type=vehicle_type, is_confirmed=False)
    context = {'currentAvailableRequests': currentAvailableRequests} 
    return render(request, 'driverSearch.html', context)


def driverSearchConfirmed(request, request_id):
    driverId = request.session['info']['id']
    driver_object = models.Driver.objects.filter(driver_info=driverId).first()
    print(driver_object)
    vehicle_type = driver_object.vehicle_type
    plate_number = driver_object.plate_number
    confirmed_order_obejct = models.Order.objects.filter(id=request_id).first()
    confirmed_order_obejct_instance = models.Order.objects.filter(id=request_id)
    email_reception = []
    user_object = models.User.objects.filter(id=confirmed_order_obejct.user_id).first()
    user_object_email = user_object.email
    email_reception.append(user_object_email)
    if confirmed_order_obejct.shared_people_id != None:
        sharer_object = models.User.objects.filter(id=confirmed_order_obejct.shared_people_id).first()
        sharer_object_email = sharer_object.email
        email_reception.append(sharer_object_email)

    confirmed_order_obejct_instance.update(is_confirmed=True, plate_number=plate_number, vehicle_type=vehicle_type)
    send_mail(
        subject='rideSharing App Confirmed Email',
        message='Your order has been order',
        from_email='walterjiang726@gmail.com',
        recipient_list=email_reception,
        fail_silently=False
    )
    return render(request, 'driverIndex.html')

def driverOrders(request):
    driverId = request.session['info']['id']
    driver_object = models.Driver.objects.filter(driver_info=driverId).first()
    vehicle_type = driver_object.vehicle_type
    plate_number = driver_object.plate_number
    is_confirmed=True
    print(driver_object)
    currentAvailableRequests = models.Order.objects.filter(vehicle_type=vehicle_type, plate_number=plate_number, is_confirmed=is_confirmed, is_completed=False)
    context = {'currentAvailableRequests': currentAvailableRequests} 
    return render(request, 'driverOrders.html', context)

def driverOrdersCompleted(request, request_id):
    driverId = request.session['info']['id']
    driver_object = models.Driver.objects.filter(driver_info=driverId).first()
    completed_order_obejct = models.Order.objects.filter(id=request_id)
    completed_order_obejct.update(is_completed=True, completed_time=datetime.now())
    return render(request, 'driverIndex.html')


def driverPassOrders(request):
    driverId = request.session['info']['id']
    driver_object = models.Driver.objects.filter(driver_info=driverId).first()
    vehicle_type = driver_object.vehicle_type
    plate_number = driver_object.plate_number
    is_confirmed=True
    print(driver_object)
    currentAvailableRequests = models.Order.objects.filter(vehicle_type=vehicle_type, plate_number=plate_number, is_confirmed=is_confirmed, is_completed=True)
    context = {'currentAvailableRequests': currentAvailableRequests} 
    return render(request, 'driverPassOrders.html', context)