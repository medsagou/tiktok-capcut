import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import yaml
import time


class GoogleSheet:
    def __init__(self):
        self.scope = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
            ]
        self.file_name = 'client.json'
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.file_name, self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open('pythonsheet').sheet1

    def update_sheet(self, n, value):
        self.sheet.update_cell(n, 1, value)
        # cell = self.sheet.cell(n, 1)
        print('Cell After Update: ', value)

    def save(self, value):
        fname = "config.yaml"
        stream = open(fname, 'r')
        data = yaml.load(stream=stream,  Loader=yaml.FullLoader)
        self.update_sheet(n=int(data['row']), value=value)
        data['row'] += 1
        with open(fname, 'w') as yaml_file:
            yaml_file.write( yaml.dump(data, default_flow_style=False))
