from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.validators import validate_email, ValidationError
from django.contrib.auth import authenticate, login, logout

# BaseView class helps exchange JSON data when developing apis.
# If LogIn, LogOut, Sign up etc views inherit BaseView, JSON data can be exchanged.
class BaseView(View):
    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data': data,
            'message': message,
        }
        return JsonResponse(result, status)


class UserCreateView(BaseView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        username = request.POST.get('username', '')
        if not username:
            return self.response(message='Please put in your ID.', status=400)
        password = request.POST.get('password', '')
        if not password:
            return self.response(message='Please put in your password.', status=400)
        email = request.POST.get('email', '')
        try:
            validate_email(email)
        except ValidationError:
            self.response(message='Please put in your email in correct form.', status=400)

        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            return self.response(message='This ID already exists.', status=400)

        return self.response({'user.id': user.id})


class UserLoginView(BaseView):
    def post(self, request):
        username = request.POST.get('username', '')
        if not username:
            return self.response(message='Please put in the username', status=400)
        password = request.POST.get('password', '')
        if not password:
            return self.response(message='Please put in the password', status=400)
                
        user = authenticate(request, username=username, password=password)
        if user is None:
            return self.response(message='This user does not exist', status=400)
        login(request, user)

        return self.response()

    
class UserLogoutView(BaseView):
    def get(self, request):
        logout(request)
        return self.response()
