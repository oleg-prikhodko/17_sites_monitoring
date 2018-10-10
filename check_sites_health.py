from datetime import datetime
from urllib.parse import urlsplit
from urllib.request import urlopen

import whois


def load_urls4check(path):
    with open(path) as urls_file:
        urls = [line.strip() for line in urls_file]
        return urls


def is_server_respond_with_200(url):
    response = urlopen(url)
    return response.status == 200


def get_domain_expiration_date(domain_name):
    domain_info = whois.whois(domain_name)
    return domain_info.expiration_date


def get_domain_from_url(url):
    return urlsplit(url).netloc


if __name__ == "__main__":
    urls = load_urls4check("urls.txt")
    for url in urls:
        expiration_date = get_domain_expiration_date(get_domain_from_url(url))
        registry_expiration_index = 0
        expiration_date = (
            expiration_date
            if isinstance(expiration_date, datetime)
            else expiration_date[registry_expiration_index]
        )
        message = "[{}] status ok: {}, expiration date: {}".format(
            url, is_server_respond_with_200(url), expiration_date
        )
        print(message)
