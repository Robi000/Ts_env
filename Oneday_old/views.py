from django.shortcuts import render
from .models import Stu_old
from datetime import date


# Create your views here.
def All_view(request):
    if request.method == "POST":
        student = request.POST.get("name")
        students = Stu_old.objects.filter(name__icontains=student)
        print(students)
        if len(students) == 1:
            stu = students[0]
            current_date = date.today()
            left = stu.expire_date - current_date
            if left.days > 0:
                left = f"This certefication will expire after {left.days} days"
            else:
                left.days = (
                    f"This certefication Already expired {-1 * left.days} days ago"
                )
            return render(request, "detail.html", {"stu": students[0], "left": left})
        elif len(students) == 0:
            return render(
                request, "index.html", {"Err": f"there is no student named {student}"}
            )
        else:
            return render(request, "list.html", {"students": students})
    else:
        return render(request, "index.html", {})


def student_detail(request, id):
    student = Stu_old.objects.get(id=id)
    current_date = date.today()
    left = student.expire_date - current_date
    if left.days > 0:
        left = f"This certefication will expire after {left.days} days"
    else:
        left.days = f"This certefication Already expired {-1 * left.days} days ago"
    return render(request, "detail.html", {"stu": student, "left": left})
