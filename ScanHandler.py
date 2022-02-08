import requests
from requests.structures import CaseInsensitiveDict


class ScanHandler:

    def __init__(self, url, config_content, resp=None, parameters_dict=None):
        self.url = url
        self.config_content = config_content
        self.resp = resp
        self.parameters_dict = parameters_dict

    def request_scan(self):
        """The function accepts url and scans it for potential harm
        :returns json resp: The response from the scan"""

        api = self.config_content['API_CONNECTION']['API'] + self.url
        headers = CaseInsensitiveDict()
        headers["x-apikey"] = self.config_content['API_CONNECTION']['API_KEY']
        resp = requests.get(api, headers=headers).json()
        self.resp = resp

    def parse_response(self):
        """The function accepts response json from the API scan requests
        :returns list parameters_dict: A list of the essential parameters including risk state, total voting and the domain's'category"""

        data_property = self.resp["data"][0]
        last_analysis_stats = data_property["attributes"]["last_analysis_stats"]
        total_votes = data_property["attributes"]["total_votes"]
        categories = data_property["attributes"]["categories"]
        parameters_dict = {'analysis': last_analysis_stats, 'votes': total_votes, 'categories': categories}
        self.parameters_dict = parameters_dict

