from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from user.forms import SignupForm, ProfileForm


def signup(request):
    form = SignupForm()

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            # Save User Data
            form.save()

            # Authenticate User
            user_email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(email=user_email, password=raw_password)

            # Auto-login user
            login(request, user)

            return redirect("home:index")

    context = {"form": form}

    return render(request, "user/signup.html", context)


@login_required(login_url="user:login")
def profile(request):
    return render(request, "user/profile.html")


# Views for Change User Password
@login_required(login_url="user:login")
def change_password(request):
    from django.contrib.auth.forms import PasswordChangeForm
    from django.contrib.auth import update_session_auth_hash

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()  # This will update the password
            update_session_auth_hash(request, user)
            return redirect("user:profile")

    else:
        form = PasswordChangeForm(request.user)

    return render(request, "user/change-password.html", {"form": form})
