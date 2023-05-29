from django.shortcuts import render

# Create your views here.
# calendar_integration/views.py

from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from google_auth_oauthlib.flow import Flow


class GoogleCalendarInitView(View):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            'path/to/client_secret.json',  # Path to your client_secret.json file obtained from Google API Console
            scopes=['https://www.googleapis.com/auth/calendar'],
            redirect_uri=request.build_absolute_uri(reverse('google-calendar-redirect'))
        )
        authorization_url, state = flow.authorization_url(access_type='offline', prompt='consent')
        request.session['google_auth_state'] = state
        return redirect(authorization_url)


class GoogleCalendarRedirectView(View):
    def get(self, request):
        code = request.GET.get('code')
        state = request.GET.get('state')
        if state != request.session.get('google_auth_state'):
            # Handle potential CSRF attack
            return redirect('/error')
        
        flow = Flow.from_client_secrets_file(
            'path/to/client_secret.json',  # Path to your client_secret.json file obtained from Google API Console
            scopes=['https://www.googleapis.com/auth/calendar'],
            redirect_uri=request.build_absolute_uri(reverse('google-calendar-redirect'))
        )
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # Now you can use the credentials to make API requests to Google Calendar
        # For example, to get a list of events:
        from googleapiclient.discovery import build
        
        service = build

