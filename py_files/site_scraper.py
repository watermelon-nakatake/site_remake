from urllib import request
import requests
from bs4 import BeautifulSoup


def main():
    print('a')


def scraping_single_page(url):
    response = request.urlopen(url=url)
    soup = BeautifulSoup(response)


def mobile_friendly_test(url):
    api_url = 'https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run'
    payload = {'url': url}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        api_url + "?key=AIzaSyCKDowxisgmy3aNwnrijK7yae2fq_9XLPM", params=payload, headers=headers)
    print("URL=" + url)
    if '"mobileFriendliness": "MOBILE_FRIENDLY"' in response.text:
        result = True
        print('good!')
    else:
        result = False
        print('not mobile friendly')
        print("RESULT = " + response.text)
    return result


if __name__ == '__main__':
    print(mobile_friendly_test('http://www.attractable.net/'))
