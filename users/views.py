from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegistrationForm
from .models import UserAccount
from .token import account_activation_token


def register(request):
    if request.method == 'POST':
        registrationForm = RegistrationForm(request.POST)
        if registrationForm.is_valid():
            user = registrationForm.save(commit=False)
            user.email = registrationForm.cleaned_data['email']
            user.username = registrationForm.cleaned_data['username']
            user.first_name = registrationForm.cleaned_data['first_name']
            user.last_name = registrationForm.cleaned_data['last_name']
            user.set_password(registrationForm.cleaned_data['password'])
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('users/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('Successfully registered and activation sent')
    else:
        registrationForm = RegistrationForm()

    return render(request, 'users/registration/register.html', {'form': registrationForm})


def activate(request, uid64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = UserAccount.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('users:dashboard')
    else:
        return render(request, 'users/registration/activation_invalid.html')


@login_required
def dashboard(request):
    return render(request, 'users/user/dashboard.html')
