import argparse
import os.path
import sys
from datetime import datetime, timedelta
from urllib.parse import urlsplit

import requests
import whois


def load_urls_from_file(path):
    with open(path) as urls_file:
        urls = [line.strip() for line in urls_file]
        return urls


def has_server_responded_with_200(url):
    response = requests.get(url)
    return response.ok


def get_domain_expiration_date(domain_name):
    domain_info = whois.whois(domain_name)
    expiration_date = domain_info.expiration_date

    if expiration_date is None:
        raise ValueError(
            "Could not get expiry date for [{}]".format(domain_name)
        )

    registry_expiration_index = 0
    expiration_date = (
        expiration_date
        if isinstance(expiration_date, datetime)
        else expiration_date[registry_expiration_index]
    )
    return expiration_date


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


def print_server_health_status(url, responded_with_ok, more_than_month_left):
    status_message = "response {} OK".format(
        "is" if responded_with_ok else "is not"
    )
    expiration_date_message = "expiry date is {} than month away".format(
        "more" if more_than_month_left else "less"
    )
    message = "[{}] {}, {}".format(
        url, status_message, expiration_date_message
    )
    print(message)


if __name__ == "__main__":
    urls_filepath = load_urls_filepath_from_argument()
    try:
        validate_urls_argument(urls_filepath)
        urls = load_urls_from_file(urls_filepath)

        for url in urls:
            responded_with_ok = has_server_responded_with_200(url)
            expiration_date = get_domain_expiration_date(
                get_domain_from_url(url)
            )
            more_than_month_left = is_month_away(expiration_date)
            print_server_health_status(
                url, responded_with_ok, more_than_month_left
            )
    except (requests.exceptions.RequestException, ValueError) as error:
        sys.exit(error)
