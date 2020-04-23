import os


def change_sample_color(case_name, color_choice):
    with open('../case_dir/' + case_name + '/product/css/base_sample.css', 'r', encoding='utf-8') as f:
        css_str = f.read()


if __name__ == '__main__':
    change_color()