from django import forms


class PaymentStatusForm(forms.Form):
    payment_status = forms.ChoiceField(
        choices=[("pending", "Pending"), ("paid", "Paid")],
        widget=forms.Select(attrs={"class": "form-control"}),
    )
