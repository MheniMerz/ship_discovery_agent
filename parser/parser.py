import textfsm
import os
import json

class Parser:
    def __init__(self):
        self.headers = []
        self.data = []
        self.json_data = {}

    def parse_query_result(self, query):
        template_name = query.cmd.replace(' ', '_')
        template_name = query.cmd.replace('"', '')
        template_path = os.path.join(os.path.dirname(__file__),'templates/'+template_name+'.template')
        with open(template_path) as template:
            fsm = textfsm.TextFSM(template)
            self.headers = fsm.header
            self.data = fsm.ParseText(query.result)
            self.parse_to_json()
            return self.json_data

    def parse_to_json(self):
        json_dict = {}
        json_dict['columns'] = self.headers
        json_dict['rows'] = self.data
        self.json_data = json.dumps(json_dict)