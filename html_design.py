import re
import pickle
import os
import markdown
import datetime
import shutil
import time

css_vars = ['wrapper_width', 'main_width_per', 'header_height', 'footer_height']


def main(case_name, domain_name, category_list, site_name, unlock_list):
    # new_case_preparation(case_name)
    case_name = 'case_dir/' + case_name
    md_list = pick_up_md_files(case_name, unlock_list)
    md_list = pickup_mod_md_files(case_name, md_list)
    print(md_list)
    if case_name + '/md/index.md' in md_list:
        import_from_markdown([case_name + '/md/index.md'],
                             case_name + '/template/top_tmp.html', domain_name, site_name,
                             category_list, case_name)
        md_list.remove(case_name + '/md/index.md')
    import_from_markdown(md_list, case_name + '/template/main_tmp.html', domain_name, site_name,
                         category_list, case_name)


def link_filter(long_str, new_path):
    if new_path.count('/') == 3:
        long_str = long_str.replace('../product/', '')
    else:
        long_str = long_str.replace('../product/', '../')
    return long_str


def new_case_preparation(case_name):
    for dir_name in ['product', 'product/css', 'template']:
        if not os.path.exists(case_name + '/' + dir_name):
            os.mkdir(case_name + '/' + dir_name)
    for file_name in ['main_tmp.html', 'top_tmp.html']:
        if not os.path.exists(case_name + '/template/' + file_name):
            shutil.copyfile(file_name, case_name + '/template/' + file_name.replace('base', 'tmp'))
    for file_name_c in ['css/base.css']:
        if not os.path.exists(case_name + '/' + file_name_c):
            shutil.copyfile(file_name_c, case_name + '/product/' + file_name_c)


def pickup_mod_md_files(case_name, md_list):
    now = time.time()
    current_mod = read_pickle('md_mod_time', case_name)
    result = [x for x in md_list if os.path.getmtime(x) > current_mod]
    save_data_to_pickle(now, 'md_mod_time', case_name)
    return result


def pick_up_md_files(directory, unlock_list):
    result = []
    md_list = os.listdir(directory)
    for file_name in md_list:
        if file_name not in ['images', 'css', 'template', 'product', 'test']:
            mk_dir_path = directory + '/' + file_name
            html_path = mk_dir_path.replace('/md/', '/product/').replace('.md', '.html')
            if '.' not in file_name:
                if not os.path.isdir(html_path):
                    os.mkdir(html_path)
                result.extend(pick_up_md_files(mk_dir_path, unlock_list))
            elif '.md' in file_name:
                if unlock_list[0] == 'all':
                    result.append(mk_dir_path)
                else:
                    if not os.path.exists(html_path) or html_path in unlock_list:
                        result.append(mk_dir_path)
            else:
                pass
    return result


def insert_split_list(long_str):
    for sp_num in ['2', '3']:
        if '%li' + sp_num in long_str:
            long_str = long_str.replace('<p>%li' + sp_num + '</p><ul>', '<ul class="split_li">')
            li3_str_l = re.findall(r'<ul class="split_li">(.+?)</ul>', long_str)
            for li3_str in li3_str_l:
                li3_str_r = li3_str.replace('<li>', '<li class="sp_li' + sp_num + '">')
                li3_l = re.findall(r'<a href=".+?">(.+?)</a>', li3_str_r)
                for x in li3_l:
                    if '%%' in x:
                        x_r = '<div class="sp_ti">' + x.replace('%%', '</div><span>') + '</span>'
                        li3_str_r = li3_str_r.replace(x, x_r)
                long_str = long_str.replace(li3_str, li3_str_r)
    return long_str


def import_from_markdown(md_file_list, template_file, domain_name, site_name, category_list, case_name):
    upload_list = []
    pk_dec = {}
    now = datetime.datetime.now()
    with open(template_file, 'r', encoding='utf-8') as t:
        tmp_str = t.read()
    for md_file_path in md_file_list:
        print('md to html :  ' + md_file_path)
        directory_l = re.findall(r'/md/(.+?)/', md_file_path)
        if directory_l:
            directory = directory_l[0]
            category_str = category_list[directory]
        else:
            directory = ''
            category_str = ''
        new_path = md_file_path.replace('/md/', '/product/').replace('.md', '.html')
        with open(md_file_path, 'r', encoding='utf-8') as f:
            plain_txt = f.read()
            description_l = re.findall(r'd::(.+?)\n', plain_txt)
            if description_l:
                description = description_l[0]
                if 'p::' in plain_txt:
                    pub_date = re.findall(r'p::(.+?)\n', plain_txt)[0]
                else:
                    pub_date = str(now)
                if 'k::' in plain_txt:
                    keyword_str = re.findall(r'k::(.+?)\n', plain_txt)[0]
                    keyword = keyword_str.split(' ')
                    if '' in keyword:
                        keyword.remove('')
                if 'id::' in plain_txt:
                    id_str = re.findall(r'id::(.+?)\n', plain_txt)[0]
                else:
                    id_str = ''
                title_l = re.findall(r't::(.+?)\n', plain_txt)
                if title_l:
                    title_str = title_l[0]
                else:
                    print('There is no title!!')
                if '%%fsp%%' in plain_txt:
                    fsp_str = re.findall(r'%%fsp%%([\s\S]*?)%', plain_txt)[0]
                    fsp_str = fsp_str.strip()
                    plain_txt = re.sub(r'%%fsp%%([\s\S])*$', '', plain_txt)
                else:
                    fsp_str = ''
                # コメントアウト削除
                plain_txt = re.sub(r'\(\)\[.*?\]\n', '', plain_txt)
                plain_txt = re.sub(r'\n(<!--.+?-->)\n', r'\n\1', plain_txt)
                plain_txt = re.sub(r'>[\s]+?<', '><', plain_txt)

                sb_str = re.findall(r'%sb%[\s\S]*?%%%', plain_txt)
                if sb_str:
                    sb_text = make_side_bar(sb_str[0])
                    tmp_str = tmp_str.replace('<!--side_bar-->', sb_text)
                    plain_txt = re.sub(r'%sb%[\s\S]*?%%%', '', plain_txt)
                    tmp_str = tmp_str.replace('<main role="main">', '<main role="main" id="sb_main">')
                else:
                    tmp_str = re.sub(r'</main>[\s\S]*?<!--e/side_bar-->', '</main>', tmp_str)

                # print(plain_txt)
                # print('markdown start!')
                con_str = markdown.markdown(plain_txt, extensions=['tables'])
                con_str = con_str.replace('\n', '')
                h1_text = re.findall(r'<h1>(.+?)</h1>', con_str)[0]
                con_str = re.sub(r'^[\s\S]*</h1>', '', con_str)
                # print(con_str)

                new_str = tmp_str.replace('<!--meta-key-->', ','.join(keyword))
                html_path = re.sub(r'^.*?/', '', md_file_path).replace('.md', '.html')
                url_str = domain_name + '/' + html_path
                new_str = new_str.replace('<!--file-path-->', url_str)
                new_str = re.sub(r'<article>[\s\S]*</article>', '<article><section class="z_m">' + con_str
                                 + '</section></article>', new_str)
                new_str = new_str.replace('<!--mod-date-->', str(now.date()))
                new_str = new_str.replace('<!--mod-date-j-->',
                                          str(now.year) + '/' + str(now.month) + '/' + str(now.day))
                if pub_date:
                    new_str = new_str.replace('<!--pub-date-->', pub_date)
                    new_str = new_str.replace('<!--pub-date-j-->', pub_date.replace('-', '/').replace('/0', '/'))
                else:
                    new_str = new_str.replace('<!--pub-date-->', str(now.date()))
                    new_str = new_str.replace('<!--pub-date-j-->',
                                              str(now.year) + '/' + str(now.month) + '/' + str(now.day))
                new_str = punctuation_filter(new_str)
                new_str = new_str.replace('<table>', '<table class="tb_n">')
                new_str = new_str.replace('<!--b_c-->', breadcrumb_maker(category_str, directory, md_file_path))
                new_str = new_str.replace('<!--title-->', title_str.replace('<br />', ''))
                new_str = new_str.replace('<!--description-->', description)
                new_str = new_str.replace('<!--h1_text-->', h1_text)
                if fsp_str:
                    new_str = new_str.replace('<!--free_script-->', fsp_str)
                if new_path.count('/') == 3:
                    new_str = new_str.replace('<link href="css/base.css"', '<link href="css/base.css"')
                elif new_path.count('/') == 4:
                    new_str = new_str.replace('<link href="css/base.css"', '<link href="../css/base.css"')
                new_str = new_str.replace('.md"', '.html"')
                new_str = link_filter(new_str, new_path)
                new_str = insert_anchor(new_str)
                new_str = insert_split_list(new_str)
                if id_str:
                    new_str = new_str.replace('<body>', '<body id="' + id_str + '">')
                if '<!--site_name-->' in new_str:
                    new_str = new_str.replace('<!--site_name-->', site_name)
                new_str = new_str.replace('<dl>', '<dl class="tbl_dl">')
                # print(new_str)

                with open(new_path, 'w', encoding='utf-8') as g:
                    g.write(new_str)
                    upload_list.append(new_path)

                new_data = [new_path, title_str, '', str(now.date()), directory, description]
                pk_dec = add_pickle_dec(pk_dec, new_data, case_name)
    return upload_list, pk_dec


def make_side_bar(sb_str):
    result = re.sub(r'%sb%(.+?)%%%', r'\1', sb_str)
    return result


def insert_anchor(long_str):
    h2_list = re.findall(r'<h2>.+?</h2>', long_str)
    for i in range(len(h2_list)):
        if '%%long' in h2_list[i]:
            long_str = long_str.replace(h2_list[i], '</section><section class="l_view"><a id="sec'
                                        + str(i + 1).zfill(2) + '" class="ach"></a>' + h2_list[i]).replace('%%long', '')
        else:
            long_str = long_str.replace(h2_list[i], '</section><section class="bc_view"><a id="sec'
                                        + str(i + 1).zfill(2) + '" class="ach"></a>' + h2_list[i])
    long_str = long_str.replace('<section class="z_m"></section>', '')
    long_str = long_str.replace('<h2>', '<h2><span>')
    long_str = long_str.replace('</h2>', '</span></h2>')
    return long_str


def punctuation_filter(long_str):
    new_str = long_str.replace('<br /></p>', '</p>')
    new_str = new_str.replace('。。<br />', '。</p><p>')
    new_str = new_str.replace('。。', '。</p><p>')
    new_str = new_str.replace('）。<br />', '）</p><p>')
    new_str = new_str.replace(')。<br />', ')</p><p>')
    new_str = new_str.replace(')。', ')</p><p>')
    new_str = new_str.replace('）。', '）</p><p>')
    new_str = new_str.replace('？。', '？<br />')
    new_str = new_str.replace('？。。', '？</p><p>')
    new_str = re.sub(r'([^>])。([^<])', r'\1。<br />\2', new_str)
    new_str = new_str.replace('。<a ', '。<br /><a ')
    new_str = new_str.replace('。<br />）', '。）')
    new_str = new_str.replace('。<br />)', '。)')
    new_str = new_str.replace('！。<br />', '！<br />')
    new_str = new_str.replace('。<br /></p>', '。</p>')
    new_str = new_str.replace('<li><p>', '<li>')
    new_str = new_str.replace('</p></li>', '</li>')
    return new_str


def breadcrumb_maker(category, directory, md_path):
    if directory:
        result = '<ol id="bread" itemscope itemtype="https://schema.org/BreadcrumbList">' \
               '<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem" class="brd1">' \
               '<a href="../" itemprop="item"><span itemprop="name">TOP</span></a>' \
               '<meta itemprop="position" content="1" /></li><li>></li>'
        if 'index.md' not in md_path:
            result += '<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem" class="brd2">' \
                      '<a href="../' + directory + '/" itemprop="item"><span itemprop="name">' + category\
                      + '</span></a><meta itemprop="position" content="2" /></li><li>>></li>'
            result += '<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem" class="brd3">' \
                      '<h1><span itemprop="name"><!--h1_text--></span></h1><meta itemprop="position" content="3" />' \
                      '</li>'
        else:
            result += '<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem" class="brd2">' \
                      '<h1><span itemprop="name">' + category + '</span></h1><meta itemprop="position" content="2" />' \
                      '</li>'
    else:
        result = '<ol id="bread" itemscope itemtype="https://schema.org/BreadcrumbList">' \
               '<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem" class="brd1">' \
               '<h1><span itemprop="name"><!--h1_text--></span></h1><meta itemprop="position" content="1" /></li>'
    return result + '</ol>'


def add_pickle_dec(pk_dec, new_data, case_name):
    path_list = [pk_dec[x][0] for x in pk_dec]
    if new_data[0] not in path_list:
        pk_dec[len(pk_dec)] = new_data
    else:
        for i in range(len(path_list)):
            if path_list[i] == new_data[0]:
                pk_dec[i] = new_data
    save_data_to_pickle(pk_dec, 'data_list', case_name)
    return pk_dec


def save_data_to_pickle(data, pickle_name, case_name):
    with open(case_name + '/pickle_pot/' + pickle_name + '.pkl', 'wb') as p:
        pickle.dump(data, p)


def read_pickle(pickle_name, case_name):
    with open(case_name + '/pickle_pot/' + pickle_name + '.pkl', 'rb') as f:
        pk_data = pickle.load(f)
    return pk_data


def css_setup(case_name, css_data):
    if len(css_vars) != len(css_data):
        print('the number of css is not equal!!')
        return
    with open('base_tmp.css', 'r', encoding='utf-8') as f:
        css_tmp = f.read()
        for css_num in range(len(css_vars)):
            if css_num in [1]:
                css_tmp = re.sub(r'/\*' + css_vars[css_num] + r'\*[\s\S]*?\*' + css_vars[css_num] + r'_e\*/',
                                 'width:' + str(css_data[css_num]) + '%;/*' + css_vars[css_num] + '*/', css_tmp)
            else:
                css_tmp = re.sub(r'/\*' + css_vars[css_num] + r'\*[\s\S]*?\*' + css_vars[css_num] + r'_e\*/',
                                 'width:' + str(css_data[css_num]) + 'px;/*' + css_vars[css_num] + '*/', css_tmp)
        side_bar_width = 100 - css_data[1]
        css_tmp = re.sub(r'/\*side_bar_width\*[\s\S]*?\*side_bar_width_e\*/',
                         'width:' + str(side_bar_width) + '%;/*side_bar_width*/', css_tmp)
        print(css_tmp)
    with open(case_name + '/base.css', 'w', encoding='utf-8') as g:
        g.write(css_tmp)


def gradation_maker(base_color):
    if '#' in base_color and len(base_color) == 7:
        r_hex = base_color[1:3]
        g_hex = base_color[3:4]
        b_hex = base_color[4:7]
        r_int = int(r_hex, 16)
        g_int = int(g_hex, 16)
        b_int = int(b_hex, 16)

        c_list = [r_int, g_int, b_int]
        max_i = c_list.index(max(c_list))
        
        print(r_int)
        print(max_i)


if __name__ == '__main__':
    category_li = {'works': '実績', 'company': '会社案内', 'making_site': 'サイト作成', 'contact': 'お問い合わせ',
                   'technology': 'web技術', 'policy': 'サイトポリシー'}
    unlock_l = ['all']
    main('wmelon', 'https://www.wmelon.co.jp', category_li, '株式会社ウォーターメロン', unlock_l)

    # css_setup('test_case', [1100, 75, 0, 0])
    # gradation_maker('#ffffff', 'a')
    # todo: 複数パターンのhtmlサンプルを一括作成　パラメータは色、サイズ、フォント等
