from django.core.mail import EmailMessage
from django.core.mail import send_mail, BadHeaderError

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from django.template import Context
from django.template.loader import get_template, render_to_string

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.urlpatterns import format_suffix_patterns

from django.views.decorators.csrf import csrf_exempt

from .serializers import *
from students.forms import *
from .models import *
from .forms import *

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .tokens import account_activation_token
#api permission to view users of the d.b

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from django.contrib.auth.views import login
from django.contrib.auth import views



# Create your views here.

def signup(request):
    if request.method =='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('acc_activate.html',
            {'user': user, 'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            # user.email_user(subject, message)
            toemail = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[toemail])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form':form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


email = EmailMessage('Hi!', 'Cool message for %recipient.first_name%', 'vanshergzie@gmail.com', ['jaywizzy34@gmail.com'])
email.extra_headers['recipient_variables'] = '{"joe@example.com":{"first_name":"Joe"}, "jane@example.com":{"first_name":"Jane"}}'
email.send()
# def register(request):
#     if request.method == 'POST':
#         form = StudentsForm(request.POST or None, request.FILES or None)
#         if form.is_valid():
#             create = Students()
#             create.first_name = form.cleaned_data['first_name']
#             create.last_name = form.cleaned_data['last_name']
#             create.username = form.cleaned_data['username']
#             create.email = form.cleaned_data['email']
#             create.date_of_birth = form.cleaned_data['date_of_birth']
#             create.gender = form.cleaned_data['gender']
#             create.profile_pic = form.cleaned_data['profile_pic']
#             create.password = form.cleaned_data['password']
#             create.save()
#             return HttpResponse('Thanks for registering')
#         else:
#             return HttpResponse('unable to create user')
#             # return messages.error(request, 'error creating user')
#     else:

#         form = StudentsForm()
#     return render(request, 'registration/register.html',{"form":form})

# def login(request):
#     if request.method == "POST":
#         form = StudentsLoginForm(request.POST or None)
#         if form.is_valid():

#             login = Students.objects.filter(
#                 form.cleaned_data['email'],
#                 form.cleaned_data['password']
#                 )
#             if login:
#                 return HttpResponse('you are successfully logged in')
#             else:
#                 return messages.error(request, 'invalid login details')
#     else:
#         form = StudentsLoginForm()
#     return render(request, 'login.html', {'form':form})

# @csrf_exempt
# def students_list(request):
#     if request.method == "GET":
#         students = Students.objects.all()
#         serializer = StudentsSerializer(students, many = True)
#         return JsonResponse(serializer.data, safe = False)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = StudentsSerializer(data = data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status = 201)
#         return JsonResponse(serializer.error, status = 400)

# def reg(request):
#     if request.method == "POST":
#         form = UserForm(request.POST or None)
#         if form.is_valid():
#             form.save()
#         else:
#             # return messages.error(request, "form not valid")
#             return HttpResponse('form not created')

#     else:
#         form = UserForm()
#     return render(request, 'registration/reg.html',{"form":form})

# def contact(request):
#     form_class = ContactForm
#     if request.method == 'POST':
#         form = form_class(data=request.POST)
#         if form.is_valid():
#             subject = request.POST.get('subject', '')
#             message = request.POST.get('message', '')
#             contact_email = request.POST.get('contact_email', '')

#             if subject and message and contact_email:
#                 try:
#                     send_mail(subject, message, contact_email, ['vanshergzie@gmail.com'])
#                 except BadHeaderError:
#                     return HttpResponse('Invalid header found.')
#                 return HttpResponse('thanks for contacting us')
#             else:
#                 # In reality we'd use a form class
#                 # to get proper validation errors.
#                 return HttpResponse('Make sure all fields are entered and valid.')

#     return render(request, 'contact.html', {"form":form_class})

#             # Email the profile with the
#             # contact information
#             # template =  get_template('contact_template.txt')
#             # context = Context({
#             #     'subject': subject,
#             #     'message': message,
#             #     'contact_email': contact_email,

#             # })
#             # content = template.render(context)

#             # email = EmailMessage(
#             #     # "New contact form submission",
#             #     # content,
#             #     # "Your website" +'',
#             #     # ['jaywizzy34@gmail.com'],
#             #     # headers = {'Reply-To': contact_email }
#             # )
#             # email.send()
#             # return redirect('contact')


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = StudentsSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = StudentsSerializer
