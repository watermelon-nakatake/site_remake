import py_files.html_design

if __name__ == "__main__":
    category_li = {'works': '実績', 'company': '会社案内', 'making_site': 'サイト作成', 'contact': 'お問合せ',
                   'technology': 'web技術', 'policy': 'サイトポリシー'}
    unlock_l = ['all']
    py_files.html_design.main('wmelon', 'https://www.wmelon.co.jp', category_li, '株式会社ウォーターメロン', unlock_l)