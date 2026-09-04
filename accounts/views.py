from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def profile_redirect(request):
    """Redirect logged-in users to their own dashboard or portfolio."""
    # This is a simple helper; dashboard routing will be expanded later.
    return redirect('dashboard:home')
