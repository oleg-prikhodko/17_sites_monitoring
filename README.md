# Sites Monitoring Utility

Program outputs server health status from given urls (taken from an arbitrary file) including: has server responded with status code 200 and is domain name registration expiry date is at least month away

# Quickstart

Program requires __python-whois__ in order to get registration info. Installation:

```bash
$ pip install -r requirements.txt
```

Example of script launch on Linux, Python 3.5:

```bash
$ python check_sites_health.py <urls file>
[http://yandex.ru] response is OK, expiry date is more than month away
[http://google.com] response is OK, expiry date is more than month away
[http://devman.org] response is OK, expiry date is more than month away
[http://python.org] response is OK, expiry date is more than month away
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
