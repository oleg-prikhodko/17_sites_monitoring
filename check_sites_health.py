from urllib.request import urlopen

def load_urls4check(path):
    pass

def is_server_respond_with_200(url):
    response = urlopen(url)
    return response.status == 200

def get_domain_expiration_date(domain_name):
    pass

if __name__ == '__main__':
    pass
