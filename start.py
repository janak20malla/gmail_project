from __future__ import print_function
import pprint
import os.path
from re import L

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_gmail_service():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return(service)


def get_emails_list():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    return results.get('messages', [])


def get_emails_content(message_id):
    service = get_gmail_service()
    data = service.users().messages().get(userId='me', id=message_id).execute()
    return data


if __name__ == '__main__':
    # messages = get_emails_list()

    # for messages in messages:
    #     print(messages['id'])
    # main()

    data = get_emails_content('17f7968364a119c9')
    print(data)
    print(data['snippet'])
