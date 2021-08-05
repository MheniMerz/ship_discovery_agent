import requests

class jsonSend:
    def postRequest(self, url, filename):
        filedata = {'filedata': (filename, open(filename, 'rb'))}
        response = requests.post(url, files=filedata)
        return response.text
