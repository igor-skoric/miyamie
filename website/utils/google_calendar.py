# utils/google_calendar.py
import json
import os

from django.shortcuts import render, redirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/calendar']
BASE_DIR = settings.BASE_DIR
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'credentials', 'client_secret.json')
REDIRECT_URI = 'http://localhost:8000/oauth2callback/'


def get_google_auth_flow():
    return Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )


def create_event(creds, event_data):
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': event_data['summary'],
        'description': event_data.get('description', ''),
        'start': {
            'dateTime': event_data['start'],
            'timeZone': 'Europe/Belgrade',
        },
        'end': {
            'dateTime': event_data['end'],
            'timeZone': 'Europe/Belgrade',
        },
    }

    return service.events().insert(calendarId='primary', body=event).execute()


def oauth2callback(request):
    state = request.session.get('oauth_state', None)
    flow = get_google_auth_flow()
    if state:
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=SCOPES,
            state=state,
            redirect_uri=REDIRECT_URI,
        )
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    creds = flow.credentials
    # Sačuvaj creds u sesiju ili bazi
    request.session['google_token'] = creds.to_json()

    print("request.session['google_token'] = creds.to_json()")
    print(creds.to_json())

    return render(request, 'website/pages/email.html')


def connect_google(request):
    flow = get_google_auth_flow()
    auth_url, state = flow.authorization_url(prompt='consent')
    request.session['oauth_state'] = state  # sačuvaj state u sesiju
    return redirect(auth_url)



def create_google_calendar_event(token_json, reservation):
    creds = Credentials.from_authorized_user_info(json.loads(token_json))
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': f'Reservation by {reservation.user.username}',
        'description': reservation.description or 'No description',
        'start': {
            'dateTime': reservation.start_time.isoformat(),
            'timeZone': 'Europe/Belgrade',
        },
        'end': {
            'dateTime': reservation.end_time.isoformat(),
            'timeZone': 'Europe/Belgrade',
        },
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event.get('id')
