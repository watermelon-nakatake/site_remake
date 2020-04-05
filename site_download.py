from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.request import urlretrieve
from os import makedirs
import os.path
import time
import re


def download_site(url, save_name):
    test_files = {}
    analyze_html(url, url, test_files, save_name)
    print('result=', test_files)


def enum_links(html, base):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.select("link[rel='stylesheet']")
    links += soup.select("a[href]")
    return [urljoin(base, x.attrs['href']) for x in links if 'http://' in x or 'http://' in x]


def download_file(url, save_name):
    o = urlparse(url)
    save_path = 'case_dir/' + save_name + '/old_html/' + o.netloc + o.path
    if re.search(r"/$", save_path):
        save_path += "index.html"
    save_dir = os.path.dirname(save_path)
    if os.path.exists(save_path):
        return save_path
    if not os.path.exists(save_dir):
        print("mkdir=", save_dir)
        makedirs(save_dir)
    print("download=", url)
    urlretrieve(url, save_path)
    time.sleep(1)
    return save_path


def analyze_html(url, root_url, test_files, save_name):
    save_path = download_file(url, save_name)
    if save_path is None or save_path in test_files:
        return
    test_files[save_path] = True
    print("analyze_html=", url)
    html = open(save_path, "r", encoding="utf-8").read()
    links = enum_links(html, url)
    for link_url in links:
        if '.htm' in link_url:
            test_files = analyze_html(link_url, root_url, test_files, save_name)
            continue
        download_file(link_url, save_name)
    print(test_files)
    return test_files


if __name__ == "__main__":
    download_site('', '')
