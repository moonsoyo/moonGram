from django.http import JsonResponse
from django.views import View

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
    @method-decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')

        user = User.objects.create_user(username, email, password)

        return self.response({'user.id': user.id})