import argparse
import os.path
import sys
from datetime import datetime, timedelta
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import urlopen

import whois


def load_urls_from_file(path):
    with open(path) as urls_file:
        urls = [line.strip() for line in urls_file]
        return urls


def has_server_responded_with_200(url):
    response = urlopen(url)
    return response.status == 200


def get_domain_expiration_date(domain_name):
    domain_info = whois.whois(domain_name)
    return domain_info.expiration_date


def get_domain_from_url(url):
    return urlsplit(url).netloc


def is_month_away(datetime_to_check):
    average_days_in_month = 30
    month_period = timedelta(days=average_days_in_month)
    month_from_now = datetime.now() + month_period
    return datetime_to_check > month_from_now


def load_urls_filepath_from_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("urls")
    arguments = parser.parse_args()
    return arguments.urls


def validate_urls_argument(urls_filepath):
    if not os.path.exists(urls_filepath):
        raise ValueError("File not exists")
    elif os.path.isdir(urls_filepath):
        raise ValueError("Directories not allowed")


if __name__ == "__main__":
    urls_filepath = load_urls_filepath_from_argument()
    try:
        validate_urls_argument(urls_filepath)
    except ValueError as error:
        sys.exit(error)

    urls = load_urls_from_file(urls_filepath)
    registry_expiration_index = 0

    for url in urls:
        expiration_date = get_domain_expiration_date(get_domain_from_url(url))
        expiration_date = (
            expiration_date
            if isinstance(expiration_date, datetime)
            else expiration_date[registry_expiration_index]
        )
        try:
            status_message = "response {} OK".format(
                "is" if has_server_responded_with_200(url) else "is not"
            )
        except URLError as error:
            sys.exit(error)

        expiration_date_message = "expiry date is {} than month away".format(
            "more" if is_month_away(expiration_date) else "less"
        )
        message = "[{}] {}, {}".format(
            url, status_message, expiration_date_message
        )
        print(message)
