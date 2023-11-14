from django.shortcuts import render, redirect
from .models import Student
from .forms import PaymentStatusForm
from django.db.models import Max


def Payment(request):
    max_value = Student.objects.aggregate(Max("Batch"))["Batch__max"]
    lis = list(range(max_value + 1))
    context = {"Batch": lis[1:]}

    if request.htmx:
        print(request.POST)
        Students = Student.objects.filter(Batch=int(request.POST["Batch"]))
        context["stus"] = Students
        context["Batch"] = int(request.POST["Batch"])
        return render(request, "p/payment.html", context)
    Students = Student.objects.filter(Batch=1)
    context["stus"] = Students
    return render(request, "payment.html", context)


def payment_handler(request):
    print("i was here")
    tuple_list = list(request.POST.items())
    context = {}
    print(tuple_list)
    Students = Student.objects.filter(Batch=int(request.POST["Batch"]))
    for stu in Students:
        print(stu.id)
        if stu.payment_status != request.POST.get(str(stu.id), stu.payment_status):
            stu.payment_status = request.POST.get(str(stu.id), stu.payment_status)
            print("changed")
            stu.save()
    context["stus"] = Students
    context["Batch"] = int(request.POST["Batch"])
    context["message"] = "scussessfully changed"
    context["id"] = True
    return render(request, "p/payment.html", context)
