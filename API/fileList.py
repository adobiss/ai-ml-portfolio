from __future__ import print_function
import os.path
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():

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

    service = build('drive', 'v3', credentials=creds)
    
    folder_id = '18pkWF2plaxXV2rp2OJSHwGN_PMBV56w0'
    query = f"parents = '{folder_id}' and trashed=false" 
    
    response = service.files().list(q=query, pageSize=1000, fields="nextPageToken, files(id, name, webViewLink)").execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')
    
    
    #results = service.files().list(pageSize=10,fields="nextPageToken, files(id, name, webViewLink)").execute() 
    
    while nextPageToken:
        response = service.files().list(q=query).execute()
        files.extend(response.get('files'))
        nextPageToken = response.get('nextPageToken')
        
    df = pd.DataFrame(files)
    df.to_csv(path_or_buf=r"D:\ML\Musiio\PoCs\Roblox\Links\Roblox_drive_links.csv", sep=',', index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    main()