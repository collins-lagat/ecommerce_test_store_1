from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from customer.forms import CompleteSignUp


@login_required
def complete_sign_up(request):
    print(request.user)
    if request.method == "POST":
        form = CompleteSignUp(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse("profile"))
    else:
        form = CompleteSignUp(instance=request.user)
    return render(request, "customer-complete-signup.html", {"form": form})
