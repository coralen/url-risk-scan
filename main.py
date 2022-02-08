import re
import datetime
from ScanHandler import ScanHandler as sh
from ScanStats import ScanStats as ss
from FilesEditor import FilesEditor as fe
config_file = 'config.yml'


def write_to_csv(ss_obj):
    """The function accepts parameters of a scan as a ScanStats object.
    Writes to a file the output of the scan
    :param ScanStats ss_obj: This object holds a scan parameters"""
    list_of_scan_parameters = [ss_obj.url, ss_obj.risk, ss_obj.total_voting,
                               ss_obj.category, ss_obj.time]
    fe_scan_records = fe(file_path='url_scan_records.csv', file_content=list_of_scan_parameters, file_type='csv')
    fe_scan_records.write_file()


def check_last_update(url, config_content):
    """The function accepts url and config content
    :param str url: The url needed to be checked for a scan
    :param yaml config_content: Configuration file content
    :returns Boolean: True If a scan is needed, False otherwise"""
    last_update_delta = config_content['LAST_SCAN']['MINUTES']
    last_update = config_content['LAST_SCAN']['URL_LAST_SCAN'][url]
    if last_update is None:
        return True
    try:
        config_last_update = datetime.datetime.now() - datetime.timedelta(minutes=last_update_delta)
        if last_update < config_last_update:
            return True
    except TypeError:
        print("Check the MINUTES configuration")
    return False


def last_update_dict(ss_obj, config_content):
    """The function accepts scan_parameters and config content
    :param canStats ss_obj: This object holds a scan parameters
    :param yaml config_content: Configuration file content"""
    config_content['LAST_SCAN']['URL_LAST_SCAN'][ss_obj.url] = ss_obj.time
    fe_update_config = fe(file_path=config_file, file_content=config_content, file_type='yaml')
    fe_update_config.write_file()


def main():
    """For each url, checks if a scan is needed and prints it out to a csv file.
    If an url has been scanned in the past 30 minutes, no scan is needed"""
    fe_urls = fe(file_path='urls.csv', file_type='csv')
    fe_urls.read_file()
    for url in fe_urls.file_content:
        try:
            url = re.sub(r"[\n\s]*", "", url)
        except ValueError:
            print("No need for substring")

        fe_config = fe(file_path=config_file, file_type='yaml')
        fe_config.read_file()
        config_content = fe_config.file_content
        if check_last_update(url, config_content) is True:
            sh_obj = sh(url=url, config_content=config_content)
            sh_obj.request_scan()
            sh_obj.parse_response()
            parameters_dict = sh_obj.parameters_dict
            ss_obj = ss(url=url, parameters_dict=parameters_dict)
            ss_obj.set_category()
            ss_obj.set_count_votes()
            ss_obj.set_risk()
            ss_obj.set_datetime()
            write_to_csv(ss_obj)
            last_update_dict(ss_obj, fe_config.file_content)


if __name__ == '__main__':
    main()

