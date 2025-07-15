import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_drive_service():
    creds = None
    if os.path.exists("token.json"):
        with open("token.json", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "wb") as token:
            pickle.dump(creds, token)
    return build("drive", "v3", credentials=creds)

def create_drive_folders(deliverables, parent_name="AI Project Folder"):
    service = get_drive_service()
    file_metadata = {
        'name': parent_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    parent = service.files().create(body=file_metadata, fields='id').execute()
    parent_id = parent.get('id')
    created = []

    for name in deliverables:
        folder_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        created.append(f"https://drive.google.com/drive/folders/{folder.get('id')}")

    return created