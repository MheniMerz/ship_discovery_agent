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
        template_name = template_name.replace('"', '')

        template_path = os.path.join(os.path.dirname(__file__),'templates/'+template_name+'.template')
        with open(template_path) as template:
            fsm = textfsm.TextFSM(template)
            self.headers = fsm.header
            self.data = fsm.ParseText(query.result)
            if len(self.data) == 1:
                self.parse_single_row_to_json()
            else:
                self.parse_multiple_rows_to_json()
        return self.json_data
        
    def parse_multiple_rows_to_json(self):
        json_dict = {}
        json_dict['columns'] = self.headers
        json_dict['rows'] = self.data
        self.json_data = json_dict

    def parse_single_row_to_json(self):
        json_dict = {}
        for header in self.headers:
            json_dict[header] = self.data[0][self.headers.index(header)]
        self.json_data = json_dict