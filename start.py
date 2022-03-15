from __future__ import print_function
import pprint
import os.path
from re import L
import base64
import email


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_gmail_service():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    # The file jmalla_token.json stores the user's access and refresh jmalla_tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('jmalla_token.json'):
        creds = Credentials.from_authorized_user_file(
            'jmalla_token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_jmalla_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'jmalla_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('jmalla_token.json', 'w') as jmalla_token:
            jmalla_token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return(service)


def get_emails_list():
    service = get_gmail_service()
    results = service.users().messages().list(
        userId='me', maxResults=1, q='noreply@njtransit.com').execute()
    return results.get('messages', [])


def get_emails_content():
    service = get_gmail_service()
    data = service.users().messages().get(
        userId='me', id='17f7e5252b23f639', format='raw').execute()
    return data


if __name__ == '__main__':
    messages = get_emails_list()

    ids = messages[0]['id']
    # print(ids)

    content = get_emails_content()

    raw_content = content['raw']
    # print(raw_content)

    msg_str = base64.urlsafe_b64decode(raw_content)
    msg_str = str(msg_str, "utf-8")
    print(type(msg_str))
    # msg_str = base64.urlsafe_b64decode(raw_content.encode('ASCII'))
    # # print(msg_str)
    #print(" ")
    # mine_msg = email.message_from_bytes(msg_str)

    # print(mine_msg.get_payload())

    # print(mine_msg.get_content_maintype())  # Test how many parts does it have.

    # print(mine_msg.get_payload())

    # nj_transit_id = []  # To store the message id's

    # for messages in messages:
    #     # print(messages['id'])
    #     nj_transit_id.append(messages['id'])
    #     # print('\n')
    # # main()
    # print(len(nj_transit_id))
    # print(nj_transit_id)
    # data1 = get_emails_content('17f7e5252b23f639')
    # data2 = get_emails_content('17f7df9e193bb431')
