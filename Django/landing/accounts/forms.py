from django import forms


class SubscriptionForm(forms.Form):
    """
    Subscription Form
    """
    email = forms.EmailField(
        max_length=200,
        required=True,
        help_text='Write your email address'
    )
