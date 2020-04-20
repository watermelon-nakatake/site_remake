from py_files import html_design, site_download
from py_files.html_design import this_case
from py_files.html_design import target_url
import os


# 営業前の一連の準備
def first_action(case_name):
    if not os.path.exists('case_dir/' + case_name):
        html_design.new_case_preparation(case_name)
        print('make directory')
    else:
        print('Is new case is', case_name, '?')
        return
    if target_url:
        site_download.download_site(target_url, case_name)
        print('download old site')
    else:
        print('There is not target_url !')
        return


if __name__ == '__main__':
    print('This case is "', this_case, '"')
    first_action(this_case)
