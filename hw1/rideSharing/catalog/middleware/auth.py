from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info == "/catalog/login/":
            return
        if request.path_info == "/catalog/register/":
            return
        
        info_dict = request.session.get("info")
        if info_dict:
            return
        return redirect('/catalog/login/')