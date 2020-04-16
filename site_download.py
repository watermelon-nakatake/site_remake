from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.request import urlretrieve
from os import makedirs
import os.path
import time
import re
import chardet
import pickle
from html_design import this_case
from html_design import target_url


def download_site(url, save_name):
    test_files = {}
    row_str = {}
    if not re.search(r'.html$', url) and not re.search(r'.htm$', url) and not re.search(r'/$', url):
        url = url + '/'
    test_files, row_str = analyze_html(url, url, test_files, save_name, row_str)
    # print('result : ', test_files)
    old_str = '***************************'.join([x + '\n\n' + row_str[x] for x in row_str])
    with open('case_dir/' + save_name + '/md/old_text.txt', 'w', encoding='utf-8') as f:
        f.write(old_str)
    with open('case_dir/' + save_name + '/pickle_pot/old_text.pkl', 'wb') as p:
        pickle.dump(row_str, p)


def enum_links(html, base):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select("link[rel='stylesheet']")
    links += soup.select("a[href]")
    result = [urljoin(base, x.attrs['href']) for x in links]
    result += [urljoin(base, y.attrs['src']) for y in soup.select("img")]
    print('links : ', result)
    return result


def download_file(url, save_name):
    o = urlparse(url)
    save_path = 'case_dir/' + save_name + '/old_html/' + o.path
    if re.search(r"/$", save_path):
        save_path += "index.html"
    save_dir = os.path.dirname(save_path)
    if os.path.exists(save_path):
        return save_path
    if not os.path.exists(save_dir):
        print("mkdir : ", save_dir)
        makedirs(save_dir)
    try:
        print("download : ", url)
        urlretrieve(url, save_path)
        time.sleep(1)
        return save_path
    except Exception as e:
        print('ダウンロード失敗 : ', url, ' : ', e)
        return None


def analyze_html(url, root_url, test_files, save_name, row_str):
    save_path = download_file(url, save_name)
    if save_path is None or save_path in test_files:
        return test_files, row_str
    test_files[save_path] = True
    print("analyze_html :", url)
    with open(save_path, 'rb') as f:
        b = f.read()
        c_data = chardet.detect(b)
        c_code = c_data['encoding']
    html = open(save_path, "r", encoding=c_code).read()
    row_str[url] = remove_tag_from_old_site(html)
    links = enum_links(html, url)
    for link_url in links:
        if re.search(r".(html|htm)$", link_url) and root_url in link_url:
            test_files, row_str = analyze_html(link_url, root_url, test_files, save_name, row_str)
            continue
        elif re.search(r'.css$', link_url):
            analyze_css(link_url, save_name, root_url)
        download_file(link_url, save_name)
    print(test_files)
    return test_files, row_str


def analyze_css(css_path, save_name, root_url):
    save_path = download_file(css_path, save_name)
    with open(save_path, 'rb') as f:
        b = f.read()
        c_data = chardet.detect(b)
        c_code = c_data['encoding']
    with open(save_path, 'r', encoding=c_code) as g:
        c = g.read()
        images = re.findall(r'url\((.+?)\)', c)
        for i in images:
            img_path = i.strip()
            img_path = re.sub(r'^.*?/old_html/', '', img_path)
            img_path = urljoin(root_url, img_path)
            download_file(img_path, save_name)


# htmlの文字列からタグを削除して読みやすくする
def remove_tag_from_old_site(long_str):
    new_str = long_str.replace('<br>', '\n')
    new_str = new_str.replace('<br />', '\n')
    new_str = new_str.replace('<br/>', '\n')
    new_str = re.sub(r'<.+?>', '\n', new_str)
    new_str = re.sub(r'\n\s', '\n', new_str)
    new_str = re.sub(r'\n\n*', '\n\n', new_str)
    return new_str


if __name__ == "__main__":
    download_site(target_url, this_case)
