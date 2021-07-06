import textfsm
import os
import json 

class Parser:
    def __init__(self):
        self.headers = []
        self.data = []
        self.json_data = {}

    def parse_show_arp(self, query_result: str):
        template_path = os.path.join(os.path.dirname(__file__),'templates/show_arp.template')
        with open(template_path) as template:
            fsm = textfsm.TextFSM(template)
            self.headers = fsm.header
            self.data = fsm.ParseText(query_result)
            self.parse_to_json()
            return self.json_data

    def parse_to_json(self):
        json_dict = {}
        json_dict['columns'] = self.headers
        json_dict['rows'] = self.data
        self.json_data = json.dumps(json_dict)

