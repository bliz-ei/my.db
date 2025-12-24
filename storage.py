import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

class DriveStorage:
    def __init__(self, credentials_file, folder_id):
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_file, 
            scopes=['https://www.googleapis.com/auth/drive']
        )
        self.service = build('drive', 'v3', credentials=self.credentials)
        self.folder_id = folder_id

    def upload_file(self, file_path):
        file_metadata = {'name': os.path.basename(file_path), 'parents': [self.folder_id]}
        media = MediaIoBaseUpload(io.FileIO(file_path, 'rb'), mimetype='application/octet-stream')
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        return file.get('webViewLink')