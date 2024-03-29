from django.urls import path
from .views import (
    Payment,
    payment_handler,
    complition,
    complition_handler,
    refund,
    refund_handler,
    unpaid,
    unpaid_handler,
    uncomplition,
    uncomplition_handler,
    student_detail_search,
    student_detail,
    batch_report,
    batch_report_handler,
    student_reg,
    Student_edit_search,
    student_edit_handler,
    single_student_report,
    single_student_report_handler,
    generate_excel,
)

urlpatterns = [
    path("", Payment, name="payment"),
    path("payment/", payment_handler),
    path("Register/", student_reg, name="register"),
    path("refund/", refund, name="refund"),
    path("refund/refund_handler/", refund_handler),
    path("unpaid/", unpaid, name="unpaid"),
    path("unpaid/unpaid_handler/", unpaid_handler),
    path("complition/", complition, name="student_status"),
    path("complition/complitionhandler/", complition_handler),
    path("uncomplition/", uncomplition, name="student_lag_status"),
    path("uncomplition/uncomplitionhandler/", uncomplition_handler),
    path("detail/", student_detail_search, name="stu_detail_search"),
    path("edit/", Student_edit_search, name="stu_edit_search"),
    path("edit/<int:id>", student_edit_handler, name="stu_edit"),
    path("detail/<int:id>", student_detail, name="stu_detail"),
    path("Batch_report/", batch_report, name="batch_report"),
    path("Batch_report/batch_report_handler/<int:batch>/",
         batch_report_handler, name="generate_pdf"),
    path("report/", single_student_report, name="single_student_report"),
    path("report/<int:id>", single_student_report_handler, name="SSRH"),
    path("excelgen/", generate_excel, name="generate_excel"),


]
