from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
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
                "payment"
            )  # Redirect to the home page or any other desired page
        else:
            # Display an error message or handle authentication failure
            return render(
                request, "login.html", {"error_message": "Invalid username or password"}
            )

    return render(request, "login.html")


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
