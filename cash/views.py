from .models import Allocation_history
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import io
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle, Image
from django.shortcuts import render, redirect
from .models import Departnment, Spending, Allocated_cash, Allocation_history
from staff.models import users
from django.db.models import Q
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.graphics.shapes import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
from django.db.models import Sum
from django.http import HttpResponse
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def departnment_list(request):
    if request.user.users.role == 'Admin':
        deps = Departnment.objects.all()
        context = {"deps": deps}
        return render(request, 'departnment_list.html', context)
    else:
        return render(request, 'Unautorized.html', {})


@login_required
def deparnment_create(request):
    if request.user.users.role == 'Admin':
        usrs = users.objects.all()

        context = {"usrs": usrs}

        if request.method == "POST":
            user = users.objects.get(id=int(request.POST["user"]))
            name = request.POST["name"]
            dept = Departnment.objects.create(name=name, head=user)
            context["dept"] = dept
            return redirect('dept_list')

        return render(request, 'deparnment_create.html', context)
    else:
        return render(request, 'Unautorized.html', {})


@login_required
def departnment_edit(request, id):
    if request.user.users.role == 'Admin':
        dept = Departnment.objects.get(id=id)
        usrs = users.objects.all()
        context = {"dept": dept, "usrs": usrs}
        if request.method == "POST":
            user = users.objects.get(id=int(request.POST["user"]))
            name = request.POST["name"]
            changed = False
            if dept.name != name:
                dept.name = name
                changed = True
            if dept.head != user:
                dept.head = user
                changed = True
            if changed:
                dept.save()
            context["msg"] = changed
            return redirect('dept_list')

        return render(request, 'departnment_edit.html', context)
    else:
        return render(request, 'Unautorized.html', {})


@login_required
def departnment_delete(request, id):
    if request.user.users.role == 'Admin':
        dept = Departnment.objects.get(id=id)

        context = {"dept": dept, "deleted": False}
        if request.method == "POST":
            dept.delete()
            context["deleted"] = True
            context["dept"] = False
            return redirect('dept_list')

        return render(request, 'departnment_delete.html', context)
    else:
        return render(request, 'Unautorized.html', {})


@login_required
def allocate(request, id):
    if request.user.users.role == 'Admin':
        print()
        dept = Departnment.objects.get(id=id)

        context = {"dept": dept}
        if request.method == "POST":
            user = request.user.users
            name = dept.name
            typ = request.POST["Type"]
            amount = int(request.POST.get("amount"))
            allocation_cash = dept.allocated_cash
            prev = allocation_cash.amount
            if typ == "add":
                allocation_cash.amount = allocation_cash.amount + amount
                Allocation_history.objects.create(
                    action="cash_allocation",
                    typ=typ,
                    amount=amount,
                    prev_amount=prev,
                    current_amount=allocation_cash.amount,
                    possesd_by=user.first_name + " " + user.Last_name,
                    department=dept,
                    department_name=name
                )
            else:
                allocation_cash.amount = allocation_cash.amount - amount
                if allocation_cash.amount < 0:
                    allocation_cash.amount = 0
                    amount = prev
                Allocation_history.objects.create(
                    action="cash_allocation",
                    typ=typ,
                    amount=amount,
                    prev_amount=prev,
                    current_amount=allocation_cash.amount,
                    possesd_by=user.first_name + " " + user.Last_name,
                    department=dept,
                    department_name=name
                )

            allocation_cash.save()
            return redirect('dept_list')

        return render(request, 'allocate.html', context)
    else:
        return render(request, 'Unautorized.html', {})


@login_required
def spending_list(request):
    user = request.user.users
    if not (request.user.users.role == 'Admin' or Departnment.objects.filter(
            head=request.user.users).exists()):
        return render(request, 'Unautorized.html', {})
    if request.user.users.role != 'Admin':
        spd_list = Spending.objects.filter(
            Q(departnment__head=user) & Q(Reviewd_by="** NOT_Reviewd **")).order_by('-created')
        clr_list = Spending.objects.filter(
            Q(departnment__head=user) & Q(
                Reviewd_by=user.first_name + " " + user.Last_name)
            & Q(cleared=False)
        ).order_by('-created')
    else:
        spd_list = Spending.objects.filter(
            Q(Reviewd_by="** NOT_Reviewd **")).order_by('-created')
        clr_list = Spending.objects.filter(
            Q(cleared=False)).order_by('-created').exclude(Reviewd_by="** NOT_Reviewd **")
    user = request.user.users
    context = {"spds": spd_list, "clrs": clr_list}
    return render(request, 'spending_list.html', context)


@login_required
def Spending_request(request):
    user = request.user.users
    tot = Spending.objects.filter(submitted_by_user=user).count()
    deps = Departnment.objects.all()
    context = {"deps": deps, "tot": tot}
    if request.method == "POST":
        reason = request.POST["reason"]
        amount = int(request.POST["amount"])
        detp_id = int(request.POST["department"])
        catagory = request.POST["catagory"]
        dept = Departnment.objects.get(id=detp_id)
        Spending.objects.create(
            spend_catagory=catagory,
            reason=reason,
            amount=amount,
            departnment=dept,
            departnment_name=dept.name,
            submitted_by=user.first_name + " " + user.Last_name,
            submitted_by_user=user
        )
    return render(request, 'Spending_request.html', context)


@login_required
def spending_review(request, id):
    user = request.user.users
    spd = Spending.objects.get(id=int(id))
    if spd.Reviewd_by != "** NOT_Reviewd **":
        return redirect('spend_list')
    departnment = spd.departnment
    if not (request.user.users.role == 'Admin' or user == departnment.head):
        return render(request, 'Unautorized.html', {})
    alocated_cash = departnment.allocated_cash
    possible = alocated_cash.amount >= spd.amount
    current = alocated_cash.amount
    After_transaction = alocated_cash.amount - spd.amount
    context = {"spd": spd, "possible": possible,
               "current": current, "at": After_transaction}

    if request.method == "POST" and possible:
        recpit = True if request.POST["Recpit"] == "yes" else False
        spd.accepted = True
        spd.Reviewd_by = user.first_name + " " + user.Last_name
        spd.A_or_R_day = timezone.now()
        spd.Reviewd_by_user = user
        spd.recpit_req = recpit
        suser = spd.submitted_by_user
        suser.dept = suser.dept + spd.amount
        suser.save()
        spd.save()
        Allocation_history.objects.create(
            action="Spending Accepted",
            amount=spd.amount,
            prev_amount=alocated_cash.amount,
            current_amount=alocated_cash.amount - spd.amount,
            possesd_by=user.first_name + " " + user.Last_name,
            possesd_for=spd.submitted_by,
            reason=spd.reason,
            department=spd.departnment,
            department_name=spd.departnment_name
        )
        alocated_cash.amount = alocated_cash.amount - spd.amount
        alocated_cash.save()
        return redirect('spend_list')

    return render(request, 'spending_review.html', context)


@login_required
def spending_clearance(request, id):
    user = request.user.users
    spd = Spending.objects.get(id=int(id))
    departnment = spd.departnment
    if not (request.user.users.role == 'Admin' or user == departnment.head):
        return render(request, 'Unautorized.html', {})

    if spd.Reviewd_by == "** NOT_Reviewd **" or spd.cleared == True:
        return redirect('spend_list')
    context = {"spd": spd}
    r_amount = spd.recpit_amount
    if r_amount != spd.amount:
        return_amount = spd.amount - r_amount
        context["r_amount"] = return_amount

    if request.method == "POST":
        departnment = spd.departnment
        alocated_cash = departnment.allocated_cash
        spd.cleared = True
        spd.Cleared_by = user.first_name + " " + user.Last_name
        spd.clerance_day = timezone.now()
        spd.Cleared_by_user = user
        if r_amount != spd.amount:
            spd.returned_amount = return_amount
            Allocation_history.objects.create(
                action="Cash return...",
                amount=return_amount,
                prev_amount=alocated_cash.amount,
                current_amount=alocated_cash.amount + return_amount,
                possesd_by=user.first_name + " " + user.Last_name,
                reason=spd.reason,
                department=spd.departnment,
                department_name=spd.departnment_name
            )
            alocated_cash.amount = alocated_cash.amount + return_amount
            alocated_cash.save()

        spd.save()
        user.dept = user.dept + spd.recpit_amount
        user.save()
        user = spd.submitted_by_user
        print("a"*30, user.dept)
        user.dept = user.dept - spd.amount
        user.save()
        return redirect('spend_list')

    return render(request, 'spending_clearance.html', context)


@login_required
def spending_delete(request, id):
    spd = Spending.objects.get(id=int(id))
    if spd.Reviewd_by != "** NOT_Reviewd **":
        return redirect('spend_list')
    context = {"spd": spd}
    if request.method == "POST":
        spd.delete()
        return redirect('spend_list')
    return render(request, 'spending_delete.html', context)


@login_required
def spending_report(request):
    user = request.user.users

    if not (request.user.users.role == 'Admin' or Departnment.objects.filter(head=user).exists() or request.user.users.role == 'Finance'):
        return render(request, 'Unautorized.html', {})
    clr_list = Spending.objects.filter(Q(cleared=True)).order_by('-created')
    heads_of_departments = users.objects.filter(departnment__isnull=False)
    if request.method == "POST":
        head = request.POST["head"]
        print(head)
        unclered = request.POST.get("unclered", False)
        from_date_str = request.POST.get('fromDate', False)
        to_date_str = request.POST.get('toDate', False)
        if from_date_str and to_date_str:
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

        if head != "All":
            clr_list = clr_list.filter(
                Cleared_by_user=users.objects.get(id=int(head)))
            head_name = users.objects.get(id=int(head))
            head_name = head_name.first_name.capitalize(
            ) + " " + head_name.Last_name.capitalize()
        if unclered:
            clr_list = clr_list.filter(finance_cleared=False)
        if from_date_str and to_date_str:
            clr_list = clr_list.filter(
                clerance_day__range=[from_date, to_date])
        total_gross = sum(log.recpit_amount for log in clr_list)
        print(total_gross)

        pdf = generate_pdf(clr_list, total_gross, True, head_name) if head != "All" else generate_pdf(
            clr_list, total_gross, False)
        # Create a HTTP response with the PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="spending_report.pdf"'
        response.write(pdf)

        return response
    context = {"spds": clr_list[:10], "heads": heads_of_departments}
    return render(request, 'spending_report.html', context)


@login_required
def spending_detail(request):

    if request.htmx:
        print("HELLO WORLD")
        name = request.POST.get('name', '')
        if name:
            id = code(process_string(name[3:]), False)
            print(id)
            obj = Spending.objects.filter(id=id)
            if obj.exists():
                spd = obj[0]
                r_amount = spd.recpit_amount
                context = {"spd": spd}
                if r_amount != spd.amount:
                    return_amount = spd.amount - r_amount
                    context["r_amount"] = return_amount
                return render(request, 'p/spending_detail.html', context)
            else:
                context = {"spd": None}
                return render(request, 'p/spending_detail.html', context)
        else:
            context = {"spd": None}
            return render(request, 'p/spending_detail.html', context)

    context = {}
    return render(request, 'spending_detail.html', context)


def process_string(input_string):
    # Remove non-alphabetic characters and numbers
    processed_string = ''.join(char for char in input_string if char.isalpha())
    # Capitalize the processed string
    processed_string = processed_string.upper()
    return processed_string


@login_required
def cash_over_view(request):
    context = {}
    return render(request, 'cash_over_view.html', context)


@login_required
def finance_clearance(request):
    if not (request.user.users.role == 'Admin' or request.user.users.role == 'Finance'):
        return render(request, 'Unautorized.html', {})
    heads_of_departments = users.objects.filter(departnment__isnull=False)

    context = {"Huser": heads_of_departments}

    return render(request, 'finance_clearance.html', context)


@login_required
def head_clear(request, id):

    head = users.objects.get(id=id)
    user = head
    name = user.first_name + " " + user.Last_name
    context = {"head": head}
    if request.method == "POST":
        if not (request.user.users.role == 'Finance'):
            return render(request, 'Unautorized.html', {})
        spends = Spending.objects.filter(
            Q(Cleared_by=name) & Q(finance_cleared=False))
        for spend in spends:
            head.dept -= spend.recpit_amount
            spend.finance_cleared = True
            spend.save()
        if head.dept < 0:
            head.dept = 0
        head.save()
        return redirect("finance_clearance")
    return render(request, 'head_clear.html', context)


@login_required
def employee_debet_list(request):
    if not (request.user.users.role == 'Admin' or request.user.users.role == 'Finance'):
        return render(request, 'Unautorized.html', {})
    heads_of_departments = users.objects.filter(departnment__isnull=False)
    other_users = users.objects.exclude(
        pk__in=heads_of_departments.values_list('pk', flat=True))
    context = {"Huser": heads_of_departments, "users": other_users}
    print(context)
    return render(request, 'employee_debet_list.html', context)


@login_required
def emp_req_list(request, id=None):
    user = request.user.users
    clrs = Spending.objects.filter(Q(submitted_by_user=user) & Q(
        Cleared_by="** NOT_CLEARED **")).exclude(Reviewd_by="** NOT_Reviewd **").order_by('-created')

    context = {"clrs": clrs}
    return render(request, 'emp_req_list.html', context)


@login_required
def emp_spd_form(request, id):
    user = request.user.users
    spd = Spending.objects.get(id=id)
    if user != spd.submitted_by_user:
        return render(request, 'Unautorized.html', {})

    if spd.submitted_by_user == user:
        context = {"spd": spd}

    if request.method == "POST":
        from_x = request.POST["from"]
        Ref = request.POST["Ref"]
        amount = request.POST["amount"]
        tin = request.POST["TIN"]
        from_date_str = request.POST.get('Date', False)
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        spd.recpit_ref_NO = Ref
        spd.recpit_from = from_x
        spd.recpit_TIN_no = tin
        spd.recpit_Date = from_date
        spd.recpit_amount = amount
        spd.save()
        return redirect("spd_self")

    return render(request, 'emp_spd_form.html', context)


# def generate_pdf(spendings, total_gross, Head=True):

#     # Create a BytesIO buffer to store PDF
#     buffer = BytesIO()

#     # Create a PDF document
#     # doc = SimpleDocTemplate(buffer, pagesize=letter)
#     doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
#     styles = getSampleStyleSheet()
#     style_heading = ParagraphStyle(
#         name='Heading1',
#         fontSize=16,
#         textColor=colors.black,
#         alignment=1
#     )
#     style_heading2 = ParagraphStyle(
#         name='Heading1',
#         fontSize=14,
#         textColor=colors.black,
#         alignment=1
#     )

#     elements = []

#     # Add logo and header
#     spacer = Spacer(1, -0.8*inch)  # Adjust the height as needed
#     elements.append(spacer)
#     logo_path = "CERT/img/Logo.jpg"  # Update with your logo path
#     logo = Image(logo_path, width=100, height=70)
#     elements.append(logo)
#     elements.append(
#         Paragraph("TS ENVIRONMENT TECHNOLOGY", style_heading))
#     elements.append(Spacer(1, 25))
#     elements.append(
#         Paragraph("Department Heads Financial Clearance Paper ", style_heading2))

#     # Add a spacer
#     elements.append(Spacer(1, 25))
#     elements.append(Paragraph("<br/>"*2, style_heading))

#     # Add data from Spending instances to the PDF
#     data = []

#     headings = ['Rec_From', 'Rec TIN', 'Reason', 'Cleared By', 'Amount', "Tax", "total"
#                 'Rec_Ref_No', 'Rec_Date',  'code']
#     data.append(headings)
#     for spending in spendings:
#         try:
#             clr_date = spending.recpit_Date.strftime('%Y-%m-%d')
#         except:
#             clr_date = "not cleared"
#         amount = spending.recpit_amount * 0.85
#         tax = spending.recpit_amount * 0.15

#         data.append([spending.recpit_from, spending.recpit_TIN_no, spending.reason, spending.Cleared_by, amount, tax, spending.recpit_amount,
#                      spending.recpit_ref_NO, clr_date, code(spending.id)])

#     # Create a table
#     table = Table(data)
#     # Adjust the width of the 5th column (indexing starts from 0)

#     table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                                ('GRID', (0, 0), (-1, -1), 1, colors.black),
#                                ('WORDWRAP', (0, 0), (-1, -1), 1)]))

#     elements.append(table)
#     elements.append(Paragraph("<br/>"*3, style_heading))
#     elements.append(
#         Paragraph(f"Total amount to be cleared: {total_gross}", style_heading))
#     if Head:
#         elements.append(Spacer(1, 25))
#         elements.append(Paragraph("<br/>"*10, style_heading))

#         style_heading = ParagraphStyle(
#             name='Heading1',
#             fontSize=16,
#             textColor=colors.black,
#             alignment=TA_RIGHT,
#             underline=True
#         )
#         elements.append(
#             Paragraph("Departnment Head (Name and signature)", style_heading))
#         elements.append(Paragraph("<br/>"*7, style_heading))
#         elements.append(
#             Paragraph("Finance (Name and signature)", style_heading))

#     # Build PDF
#     doc.build(elements)

#     # Get PDF data
#     pdf = buffer.getvalue()
#     buffer.close()

#     return pdf


# def generate_pdf(spendings, total_gross, Head=True):
#     # Create a BytesIO buffer to store PDF
#     buffer = BytesIO()

#     # Create a HTML string
#     html = f"""
#     <!DOCTYPE html>
#     <html>
#     <head>
#     <style>


#     </style>
#     </head>
#     <body>
#     <h1>TS ENVIRONMENT TECHNOLOGY</h1>
#     <h2>Department Heads Financial Clearance Paper</h2>
#     <table>
#         <tr>
#             <th>Rec_From</th>
#             <th>Rec TIN</th>
#             <th>Reason</th>
#             <th>Cleared By</th>
#             <th>Amount</th>
#             <th>Tax</th>
#             <th>total</th>
#             <th>Rec_Ref_No</th>
#             <th>Rec_Date</th>
#             <th>code</th>
#         </tr>
#     """

#     # Add data from Spending instances to the HTML
#     for spending in spendings:
#         try:
#             clr_date = spending.recpit_Date.strftime('%Y-%m-%d')
#         except:
#             clr_date = "not cleared"
#         amount = spending.recpit_amount * 0.85
#         tax = round(spending.recpit_amount * 0.15, 2)

#         html += f"""
#         <tr>
#             <td>{spending.recpit_from}</td>
#             <td>{spending.recpit_TIN_no}</td>
#             <td>{spending.reason}</td>
#             <td>{spending.Cleared_by}</td>
#             <td>{amount}</td>
#             <td>{tax}</td>
#             <td>{spending.recpit_amount}</td>
#             <td>{spending.recpit_ref_NO}</td>
#             <td>{clr_date}</td>
#             <td>{code(spending.id)}</td>
#         </tr>
#         """

#     html += f"""
#     </table>
#     <p>Total amount to be cleared: {total_gross}</p>
#     """

#     if Head:
#         html += """
#         <p>Department Head (Name and signature)</p>
#         <p>Finance (Name and signature)</p>
#         """

#     html += """
#     </body>
#     </html>
#     """

#     # Generate PDF from HTML
#     pisa_status = pisa.CreatePDF(html, dest=buffer)

#     # Check if PDF generation was successful
#     if pisa_status.err:
#         return b'PDF generation failed'
#     else:
#         pdf = buffer.getvalue()
#         buffer.close()
#         return pdf


def generate_pdf(spendings, total_gross, Head=True, head_name=""):
    # Create a BytesIO buffer to store PDF
    buffer = BytesIO()

    # Create a HTML string
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    @page {{
    size: letter landscape;
    margin: 2cm;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
    }}
    th {{
        background-color: black;
        color: white;
        padding: 8px;
        text-align: center;
    }}
    th, td {{
        border: 1px solid black;
        padding: 3px;
        text-align: center;
    }}
    th:nth-child(1), td:nth-child(1),
    th:nth-child(2), td:nth-child(2) {{
        width: 200px; /* Twice as large as other columns */
    }}
    </style>
    </head>
    <body>
    <h1>TS ENVIRONMENTAL TECHNOLOGY</h1>
    <h2>Financial Paper</h2>
    <table>
        <tr>
            <th style="width: 15%">Rec_From</th>
            <th style="width: 15%">Rec TIN</th>
            <th style="width: 20%">Reason</th>
            <th>Amount</th>
            <th>Tax</th>
            <th>total</th>
            <th>Rec_Ref_No</th>
            <th>Rec_Date</th>
            <th>code</th>
        </tr>
    """

    # Add data from Spending instances to the HTML
    for spending in spendings:
        try:
            clr_date = spending.recpit_Date.strftime('%Y-%m-%d')
        except:
            clr_date = "** unavilable **"
        amount = spending.recpit_amount * 0.85
        tax = round(spending.recpit_amount * 0.15, 2)

        html += f"""
        <tr>
            <td>{spending.recpit_from}</td>
            <td>{spending.recpit_TIN_no}</td>
            <td>{spending.reason}</td>
            <td>{amount}</td>
            <td>{tax}</td>
            <td>{spending.recpit_amount}</td>
            <td>{spending.recpit_ref_NO}</td>
            <td>{clr_date}</td>
            <td>{"Ts-" + code(spending.id)}</td>
        </tr>
        """

    if Head:
        html += f"""
        </table>
        <p>Total amount to be cleared: {total_gross}</p>
        """
        html += """</br>""" * 3
        html += f"""
        <p>Department Head (Name and signature)</p>
        <br>
        <p> {head_name}  ___________________________ </p>
        <p>Finance (Name and signature)</p>
        <br>
        <p>_______________________________ </p>
        """
    else:
        html += f"""
        </table>
        <p>Total amount : {total_gross}</p>
        """

    html += """
    </body>
    </html>
    """

    # Generate PDF from HTML
    pisa_status = pisa.CreatePDF(html, dest=buffer)

    # Check if PDF generation was successful
    if pisa_status.err:
        return b'PDF generation failed'
    else:
        pdf = buffer.getvalue()
        buffer.close()
        return pdf


def generate_pdf_response():
    # Generate the PDF
    pdf = generate_pdf()

    # Create a HTTP response with the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="spending_report.pdf"'
    response.write(pdf)

    return response


def code(num, code=True):
    if code:
        number_letter_mapping = {
            '0': 'AI', '1': 'BJ', '2': 'lm', '3': 'ok', '4': 'jr',
            '5': 'mk', '6': 'dm', '7': 'Hp', '8': 'Iq', '9': 'Jm'
        }

        num_str = str(num)
        letters = "".join([number_letter_mapping[digit].upper()
                          for digit in num_str])
        return letters[::-1]

    else:
        let_num = {'AI': '0', 'BJ': '1', 'LM': '2', 'OK': '3', 'JR': '4',
                   'MK': '5', 'DM': '6', 'HP': '7', 'IQ': '8', 'JM': '9'}
        num = num[::-1]
        data = []
        for i in range(0, len(num), 2):
            number = let_num.get(num[i:i+2], "0")
            data.append(number)
        num = "".join(data)
        return int(num)
