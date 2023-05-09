from django.urls import path
from . import views
from .views import RideDriverUnregister, RideDriverNewRides, RideDriverEditRides, RideDriverPastRides, OwnerEditRides, OwnerUpdateRides, OwnerCancelRides, OwnerPastRides, SharerSearchResults, SharerEditRides, SharerUpdateRides, SharerPastRides
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home_page, name='home'),
    path('greeting/', views.greet, name='greet'),
    path('driver/', views.driver_home, name='driver-home'),
    path('driver/registerDriver/', views.register_driver, name='driver-reg'),
    path('driver/registerDriver/<user_id>/', views.register_driver, name='driver-reg'),
    path('driver/unregisterDriver/', login_required(RideDriverUnregister.as_view()), name='driver-unregister'),
    path('driver/deleteDriver/', views.delete_driver, name='delete-driver'),
    path('driver/newRidesList/', login_required(RideDriverNewRides.as_view()), name='driver-new-rides'),
    path('driver/currentRidesList/', login_required(RideDriverEditRides.as_view()), name='driver-edit-rides'),
    path('driver/pastRidesList/', login_required(RideDriverPastRides.as_view()), name='driver-past-rides'),
    path('driver/newRideslist/confirm/<owner_id>/', views.driver_confirm, name='driver-confirm'),
    path('driver/newRideslist/complete/<owner_id>/', views.driver_complete, name='driver-complete'),
    
    path('owner/', views.owner_home, name='owner-home'),
    path('owner/requestRide/', views.request_ride, name='request-ride'),
    path('owner/editRide/', login_required(OwnerEditRides.as_view()), name='owner-edit'),
    path('owner/updateRide/<int:pk>/', login_required(OwnerUpdateRides.as_view()), name='owner-update'),
    path('owner/cancelRide/<int:pk>/', login_required(OwnerCancelRides.as_view()), name='owner-cancel'),
    path('owner/pastRides/', login_required(OwnerPastRides.as_view()), name='owner-past-rides'),
    
    path('sharer/', views.sharer_home, name='sharer-home'),
    path('sharer/searchRide/', views.search_ride, name='search-ride'),
    path('sharer/searchResult/', login_required(SharerSearchResults.as_view()), name='search-result'),
    path('sharer/searchResult/join/<owner_id>/', views.sharer_join, name='sharer-join'),
    path('sharer/editRide/', login_required(SharerEditRides.as_view()), name='sharer-edit'),
    path('sharer/cancelRide/<owner_id>/', views.sharer_cancel, name='sharer-cancel'),
    path('sharer/pastRides/', login_required(SharerPastRides.as_view()), name='sharer-past-rides'),
]
