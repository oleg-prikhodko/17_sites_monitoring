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


def has_server_responded_with_ok(url):
    response = requests.get(url)
    return response.ok


def get_domain_expiration_date(domain_name):
    domain_info = whois.whois(domain_name)
    expiration_date = domain_info.expiration_date

    if expiration_date is None:
        return None

    registry_expiration_index = 0
    expiration_date = (
        expiration_date
        if isinstance(expiration_date, datetime)
        else expiration_date[registry_expiration_index]
    )
    return expiration_date


def get_domain_from_url(url):
    return urlsplit(url).netloc


def is_further_in_time(datetime_to_check, time_period_from_now):
    future_datetime = datetime.now() + time_period_from_now
    return datetime_to_check > future_datetime


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


def print_server_health_status(
    url, responded_with_ok, days, further_in_time=None
):
    status_message = "response {} OK".format(
        "is" if responded_with_ok else "is not"
    )
    if further_in_time is None:
        expiration_date_message = "expiry date is unknown"
    else:
        expiration_date_message = "expiry date is {} than {} days away".format(
            "more" if further_in_time else "less", days
        )
    message = "[{}] {}, {}".format(
        url, status_message, expiration_date_message
    )
    print(message)


if __name__ == "__main__":
    urls_filepath = load_urls_filepath_from_argument()
    average_days_in_month = 30
    month_period = timedelta(days=average_days_in_month)

    try:
        validate_urls_argument(urls_filepath)
        urls = load_urls_from_file(urls_filepath)

        for url in urls:
            responded_with_ok = has_server_responded_with_ok(url)
            expiration_date = get_domain_expiration_date(
                get_domain_from_url(url)
            )
            further_in_time = (
                is_further_in_time(expiration_date, month_period)
                if expiration_date is not None
                else None
            )
            print_server_health_status(
                url, responded_with_ok, average_days_in_month, further_in_time
            )

    except (requests.exceptions.RequestException, ValueError) as error:
        sys.exit(error)
