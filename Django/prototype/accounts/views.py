from django.shortcuts import render
from django.shortcuts import redirect
from accounts.forms import SubscriptionForm
from accounts.models import Profile


def account_subscribe(request):
    """
    Subscription page
    """
    form = SubscriptionForm()
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            """
            Form is valid, process saving
            """
            Profile.objects.create_profile_by_email(
                form.cleaned_data['email']
            )
            return redirect('/thanks')
        else:
            return redirect('/subscribe')

    return render(request, "landing/base.html", {
        'form': form,
        'action': '/subscribe/'
    })


def account_subscribe_after(request):
    """
    After subscription page
    """
    return render(request, "landing/after.html")
