import datetime


class ScanStats:

    def __init__(self, url, parameters_dict, risk=None, total_voting=None, category=None, time=None):
        self.url = url
        self.parameters_dict = parameters_dict
        self.risk = risk
        self.total_voting = total_voting
        self.category = category
        self.time = time

    def set_datetime(self):
        """The function sets datetime to the attribute based on scan results"""
        self.time = datetime.datetime.now()

    def set_category(self):
        """The function sets category to the attribute based on scan results"""
        categories = self.parameters_dict['categories']
        category_dict = dict.fromkeys(categories.values(),0)
        for category in categories:
            category_dict[categories[category]] += 1
        self.category = str(sorted(category_dict)[0])

    def set_count_votes(self):
        """The function sets votes count to the attribute based on scan results"""
        total_votes = self.parameters_dict['votes']
        sum_of_votes = 0
        for vote in total_votes:
            sum_of_votes += total_votes[vote]
        self.total_voting = str(sum_of_votes)

    def set_risk(self):
        """The function sets risk level to the attribute based on scan results"""
        analysis_stats = self.parameters_dict['analysis']
        risk_count = 0
        for analysis in analysis_stats:
            if analysis in ("malicious", "phishing", "malware") and analysis_stats[analysis] > 0:
                risk_count += 1
        if risk_count > 0:
            self.risk = "risk"
        else:
            self.risk = "safe"
