import html_design
from html_design import this_case
import os
import shutil
from PIL import Image


def make_new_sample_from_data(case_name):
    if not os.path.exists('case_dir/' + case_name):
        os.mkdir('case_dir/' + case_name)
        os.mkdir('case_dir/' + case_name + '/product')
        os.mkdir('case_dir/' + case_name + '/product/css')
        os.mkdir('case_dir/' + case_name + '/md')
        shutil.copyfile('main_temp/css/base_sample.css', 'case_dir/' + case_name + '/product/css/base_sample.css')
        shutil.copyfile('main_temp/data.txt', 'case_dir/' + case_name + '/data_' + case_name + '.txt')
        shutil.copyfile('main_temp/sample.htm', 'case_dir/' + case_name + '/product/test.html')
        shutil.copyfile('main_temp/md_tmp.md', 'case_dir/' + case_name + '/md/test.md')
    else:
        html_design.insert_cop_data_to_sample(case_name)
    resize_images(case_name)


def resize_images(case_name):
    img_dir = '/Users/nakataketetsuhiko/Downloads/site_remake/change_image'
    img_list = os.listdir(img_dir)
    if img_list:
        for img_path in img_list:
            img = Image.open(os.path.join(img_dir, img_path))
            img_resize = img.resize((2048, 1461), Image.LANCZOS)
            img_num = 1
            while os.path.exists('case_dir/' + case_name + '/product/images/t' + str(img_num) + '.jpg'):
                img_num += 1
            img_resize.save('case_dir/' + case_name + '/product/images/t' + str(img_num) + '.jpg')
            os.remove(os.path.join(img_dir, img_path))


if __name__ == '__main__':
    make_new_sample_from_data(this_case)
