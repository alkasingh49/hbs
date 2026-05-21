from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import SignupForm
from bookings.models import Booking


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('room_list')
    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user).select_related('room')

    return render(request, 'registration/profile.html', {'bookings': bookings})
