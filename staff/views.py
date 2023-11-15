from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


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
