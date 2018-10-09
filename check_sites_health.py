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

if __name__ == '__main__':
    pass
