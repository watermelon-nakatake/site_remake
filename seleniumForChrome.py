from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ブラウザのオプションを格納する変数をもらってきます。
op = Options()
op.headless = True

# ブラウザを起動する
driver = webdriver.Chrome(options=op)

# ブラウザでアクセスする
driver.get("https://www.kuma-kensetu.jp/index.htm")

# HTMLを文字コードをUTF-8に変換してから取得します。
html = driver.page_source.encode('utf-8')
driver.close()

# BeautifulSoupで扱えるようにパースします
soup = BeautifulSoup(html, "html.parser")


if __name__ == '__main__':
    print(soup.text)
