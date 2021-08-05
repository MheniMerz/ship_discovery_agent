import requests

class Request:
    def __init__(self):
        self.url = ""
        self.filename = ""

    def postRequest(self, url, filename):
        filedata = {'filedata': (filename, open(filename, 'rb'))}
        response = requests.post(url, files=filedata)
        return response.text
