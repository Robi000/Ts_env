from django.urls import path
from .views import (departnment_list, deparnment_create, departnment_delete, departnment_edit, spending_clearance,
                    spending_delete, spending_list, spending_report, spending_review, allocate,  employee_debet_list, Spending_request,
                    emp_req_list, finance_clearance, head_clear, emp_spd_form, spending_detail,
                    )
urlpatterns = [
    path("head_clear/<int:id>", head_clear, name="aaaab"),
    path("dept", departnment_list, name="dept_list"),
    path("dept_create", deparnment_create, name="dept_create"),
    path("dept_delete/<int:id>", departnment_delete, name="dept_del"),
    path("dept_edit/<int:id>", departnment_edit, name="dept_edit"),
    path("allocate/<int:id>", allocate, name="allocate"),
    path("spend", spending_list, name="spend_list"),
    path("spend_req", Spending_request, name="spd_req"),
    path("spend_rev/<int:id>", spending_review, name="spd_rev"),
    path("spend_del/<int:id>", spending_delete, name="spd_del"),
    path("spend_cle/<int:id>", spending_clearance, name="spd_cle"),
    path("spend_form/<int:id>", emp_spd_form, name="spd_form"),
    path("spend_self", emp_req_list, name="spd_self"),
    path("spend_det", spending_detail, name="spd_det"),
    path("spend_rep", spending_report, name="f_report"),
    path("dept_emp", employee_debet_list, name="dept_emp"),
    path("finance_clearance", finance_clearance, name="finance_clearance"),
    # path("his", generate_allocation_history_pdf, name="his"),

]
