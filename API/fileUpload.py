from __future__ import print_function
import os.path
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def uploadDrive(folder_id, drive_upload_list, target_file_path):

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
    
    #folder_id = '1DCig4Q3BojV6QDLk82kO_td8r-jy_BRn'
    
    #file_list = pd.read_csv(r"D:\ML\Musiio\PoCs\Roblox\Links\Roblox_drive_upload.csv")
    
    for index, row in drive_upload_list.iterrows():
        file_name = row['segment_file_name']
        file_path = row['segment_path']
        file_metadata = {
        'name': file_name,
        'parents': [folder_id]
        }
        media = MediaFileUpload(file_path,
                            mimetype='audio/mpeg',
                            resumable=True)
        file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        print('File ID: %s' % file.get('id'))
    
    query = f"parents = '{folder_id}' and trashed=false" 
    
    response = service.files().list(q=query, pageSize=1000, fields="nextPageToken, files(id, name, webViewLink)").execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')
    
    while nextPageToken:
        response = service.files().list(q=query).execute()
        files.extend(response.get('files'))
        nextPageToken = response.get('nextPageToken')
        
    df = pd.DataFrame(files)
    return df
    
    #df.to_csv(path_or_buf=target_file_path, sep=',', index=False, encoding='utf-8-sig')
          
    
#if __name__ == '__main__':
#    main()