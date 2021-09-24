from __future__ import print_function
import base64
import os.path
from sys import _clear_type_cache
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from base64 import urlsafe_b64decode, urlsafe_b64encode
from bs4 import BeautifulSoup
from functions import *


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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

    # Call the Gmail API
    results = service.users().threads().list(userId='me',).execute()
    messages = service.users().messages().list(userId='me').execute()
    threadId = []

    id = '17c0ea35c36d6377'
    email =  service.users().messages().get(userId='me',id=id,format='full').execute()
    email_part = email['payload']
    t = gethtml(findType(email_part))
    print (t)
     
    def alternativeMIME(parts):
        part = parts['parts'][-1]
        data = part['body']['data']
        clean_text = base64.urlsafe_b64decode(data).decode('UTF-8')
        soup = BeautifulSoup(clean_text,'lxml')
        print (soup.get_text())

    for message in messages['messages']:
        info = service.users().messages().get(userId='me',id=message['id'],format='full').execute()
        if info['labelIds']:
            #make sure it is not a chat message
            if 'CHAT' not in info['labelIds']:
                mimeType = info['payload']['mimeType']
                if info['threadId'] not in threadId:
                    threadId.append(info['threadId'])
                    if mimeType == 'multipart/mixed':
                        #this has an attachment
                        print (mimeType)
                    elif mimeType == 'multipart/alternative':
                        
                        #this has alternative versions of the same content
                        #the one we will try to parse is the html version, 
                        #always the last part [-1]

                        alternativeMIME(info['payload'])

                    elif mimeType == 'multipart/related':
                        part = info['payload']['parts'][0]    
                        alternativeMIME(part)
                    elif mimeType == 'text/html':
                        data = info['payload']['body']['data']
                        clean_text = base64.urlsafe_b64decode(data).decode('UTF-8')
                        soup = BeautifulSoup(clean_text,'lxml')
                        print (soup.get_text())

                    else:
                        print (f'not yet implemented how to parse {mimeType}')

                print ('*'*10)

if __name__ == '__main__':
    main()