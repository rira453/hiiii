
from django.shortcuts import redirect
from django.urls import reverse

class PreventLoggedInAccessToLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = reverse('sing_in')  # Get the URL for the login view
        if request.user.is_authenticated and request.path == login_url:
            return redirect('index')  # Redirect authenticated users to the home page
        response = self.get_response(request)
        return response
