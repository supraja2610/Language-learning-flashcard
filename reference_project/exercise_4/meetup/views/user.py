from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required

from meetup.forms.user import UserCreateForm, UserUpdateForm
from meetup.forms.userProfile import UserProfileUpdateForm
from meetup.models import Group

tmpl = lambda *args: settings.CREATE_TEMPLATE_PATH('user', *args)

def user_login(request):
    context = {};
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        context['username'] = username
        valid = True

        if not username:
            context['usernameError'] = '* This field is required.'
            valid = False;

        if not password:
            context['passwordError'] = '* This field is required.'
            valid = False;

        if valid:
            user = authenticate(username=username, password=password)
            if user is None:
                # Return an 'invalid login' error message
                context['loginError'] = 'Your username or password is incorrect'
            elif not user.is_active:
                # Return a 'disabled account error' message
                context['loginError'] = 'The account has been deactived'
            else:
                # Redirect to a success page
                login(request, user)
                return redirect('meetup:user_dashboard')

    return render(request, tmpl('login.html'), context)

def user_create(request):
    context = {}
    if request.method != 'POST':
        form = UserCreateForm()
    else:
        form = UserCreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            get_user_model().objects.create_user(username=username,
                                                 password=password,
                                                 first_name=first_name,
                                                 last_name=last_name,
                                                 email=email)

            user = authenticate(username=username, password=password)
            login(request, user)

    context['form'] = form
    return render(request, tmpl('create.html'), context)


@login_required
def user_dashboard(request):
    context = {}
    if request.method != 'POST':
        userUpdateForm = UserUpdateForm(instance=request.user)
        userProfileUpdateForm = UserProfileUpdateForm(instance=request.user.get_profile())
    else:
        userUpdateForm = UserUpdateForm(request.POST, instance=request.user)
        if userUpdateForm.is_valid():
            userUpdateForm.save()
        userProfileUpdateForm = UserProfileUpdateForm(request.POST, instance=request.user.get_profile())
        if userProfileUpdateForm.is_valid():
            userProfileUpdateForm.save()

    context['userUpdateForm'] = userUpdateForm
    context['userProfileUpdateForm'] = userProfileUpdateForm
    context['groupsCreated'] = Group.objects.filter(creator__id=request.user.id)
    context['groupsJoined'] = Group.objects.filter(members__id=request.user.id).exclude(creator__id=request.user.id)

    return render(request, tmpl('dashboard.html'), context)
