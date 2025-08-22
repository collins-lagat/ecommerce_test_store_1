from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from customer.forms import CompleteSignUp


@login_required
def complete_sign_up(request):
    if request.user.is_authenticated and request.user.phone_number:
        return redirect("/")

    if request.method == "POST":
        form = CompleteSignUp(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = CompleteSignUp(instance=request.user)
    return render(request, "customer-complete-signup.html", {"form": form})
