from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    ## owner
    path('ownerIndex/', views.ownerIndex, name='ownerIndex'),
    path('ownerUpdate/', views.ownerUpdate, name='ownerUpdate'),
    path('ownerNewRequest/', views.ownerNewRequest, name='ownerNewRequest'),
    # path('ownerRequest/<int:request_id>/', views.ownerRequest, name='currentRequst'),
    path('ownerCurrentRequest/', views.ownerCurrentRequest, name='ownerCurrentRequest'),
    path('ownerCurrentRequest/<int:request_id>/delete/', views.requestDelete, name='requestDelete'),
    path('ownerCurrentRequest/<int:request_id>/edit/', views.requestEdit, name='requestEdit'),
    path('ownerPassOrder/', views.ownerPassOrder, name='ownerPassOrder'),


    ## sharer
    path('sharerIndex/', views.sharerIndex, name='sharerIndex'),
    path('sharerSearch/', views.sharerSearch, name='sharerSearch'),
    path('sharerShareableRequests/', views.sharerShareableRequests, name='sharerShareableRequests'),
    path('sharerShareableRequests/<int:request_id>/join/', views.sharerShareableRequestsJoin, name='sharerShareableRequestsJoin'),
    path('sharerCurrentRequests/', views.sharerCurrentRequests, name='sharerCurrentRequests'),
    path('sharerShareableRequests/<int:request_id>/delete/', views.sharerShareableRequestsDelete, name='sharerShareableRequestsDelete'),
    path('sharerPassOrder/', views.sharerPassOrder, name='sharerPassOrder'),
    
    ## driver
    path('driverIndex/', views.driverIndex, name='driverIndex'),
    path('driverUpdate/', views.driverUpdate, name='driverUpdate'),
    path('driverSearch/', views.driverSearch, name='driverSearch'),
    path('driverSearch/<int:request_id>/confirmed/', views.driverSearchConfirmed, name='driverSearchConfirmed'),
    path('driverOrders/', views.driverOrders, name='driverOrders'),
    path('driverOrders/<int:request_id>/completed/', views.driverOrdersCompleted, name='driverOrdersCompleted'),
    path('driverPassOrders/', views.driverPassOrders, name='driverPassOrders'),
]
