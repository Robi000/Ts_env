from cash.models import Departnment


def my_custom_data(request):
    user_role = {}
    if request.user.is_authenticated:
        try:
            user_role["role"] = request.user.users.role
            user_role["Admin"] = request.user.users.role == "Admin"
            user_role["Finance"] = request.user.users.role == "Finance"
            user_role["depat"] = Departnment.objects.filter(
                head=request.user.users).exists()
        except:
            user_role["role"] = False
    else:
        user_role["role"] = False

    return user_role
