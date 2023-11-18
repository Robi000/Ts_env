from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import users
from django.views.decorators.csrf import csrf_exempt


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            return redirect(
                "auth_home"
            )  # Redirect to the home page or any other desired page
        else:
            # Display an error message or handle authentication failure
            return render(
                request, "login.html", {"error_message": "Invalid username or password"}
            )

    return render(request, "login.html")


def logout_view(request):
    context = {}
    logout(request)
    return redirect("auth_home")


def manage_user(request):
    userss = users.objects.all()
    # print(userss[0].id, userss[0].user.id)
    context = {"userss": userss}
    if request.htmx:
        return render(request, "manage.html", context)
    return render(request, "manage.html", context)


@csrf_exempt
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    userss = users.objects.all()
    # print(userss[0].id, userss[0].user.id)
    context = {"userss": userss}
    if request.htmx:
        return render(request, "manage.html", context)
    return render(request, "manage.html", context)


def edit_user(request, id):
    user = User.objects.get(id=id)
    context = {"user": user.users}
    if request.method == "POST":
        userr = user.users
        userr.first_name = request.POST["first_name"]
        userr.Last_name = request.POST["Last_name"]
        userr.email = request.POST["email"]
        userr.phone = request.POST["phone"]
        userr.role = request.POST["role"]
        if request.POST["password"]:
            print("hello world")
            context[
                "message"
            ] = "This notification serves to inform you that, henceforth, your password will no longer be displayed for security reasons.\
            It is imperative that you securely store and remember your password. In the event that you forget your password, kindly \
            reach out to your administrator, who will assist you in the password reset process.\
            It is important to note that, for security purposes, passwords are no longer visible, even to administrators.\
            <br>We are pleased to confirm that the edits to your profile have been successful. Welcome to our platform!"
            context["password"] = request.POST["password"]
            context["username"] = user.username
            user.set_password(request.POST["password"])
            user.save()
        userr.save()
        user = User.objects.get(id=id)
        context["user"] = user.users
        return render(request, "user_detail.html", context)
    return render(request, "edit_user.html", context)


def register(request):
    context = {}
    if request.method == "POST":
        dic = dict(request.POST)
        del dic["csrfmiddlewaretoken"]
        for x in dic:
            dic[x] = dic[x][0]
        user = users.objects.create(**dic)
        context = {"user": user}
        context[
            "message"
        ] = "This notification serves to inform you that, henceforth, your password will no longer be displayed for security reasons.\
            It is imperative that you securely store and remember your password. In the event that you forget your password, kindly \
            reach out to your administrator, who will assist you in the password reset process.\
            It is important to note that, for security purposes, passwords are no longer visible, even to administrators.\
            we are pleased to confirm that your registration was successful. Welcome to our platform!"
        context["password"] = dic["password"]
        context["username"] = user.user.username
        return render(request, "user_detail.html", context)

    return render(request, "registration.html", context)


def user_detail(request, id):
    user = User.objects.get(id=id)
    context = {"user": user.users}
    return render(request, "user_detail.html", context)


def home(request):
    context = {}
    return render(request, "home.html", context)
