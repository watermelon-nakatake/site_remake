from ftplib import FTP
import os
import paramiko
import scp
import re
import datetime
import time
import html_design
import pathlib


def all_upload(case_name, domain_str, user_name, password_str, root_directory):
    today = datetime.date.today()
    backup_dir = 'case_dir/' + case_name + '/backup/' + re.sub(r'\D', '', str(today))
    if not os.path.isdir(backup_dir):
        first_backup(domain_str, user_name, password_str, root_directory, backup_dir)
    up_list = [x.replace('case_dir/' + case_name + '/product/', '')
               for x in file_pickup('case_dir/' + case_name + '/product')]
    up_list = pickup_mod_files('case_dir/' + case_name, up_list)
    print(up_list)
    # ftp_upload(case_name, domain_str, user_name, password_str, root_directory, up_list)
    scp_upload(case_name, domain_str, user_name, password_str, root_directory, up_list)


def pickup_mod_files(case_name, up_list):
    now = time.time()
    current_mod = html_design.read_pickle('up_time', case_name)
    result = [x for x in up_list if os.path.getmtime(case_name + '/product/' + x) > current_mod]
    html_design.save_data_to_pickle(now, 'up_time', case_name)
    return result


def scp_upload(case_name, domain_str, user_name, password_str, root_directory, up_file_list):
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=domain_str, port=22, username=user_name, password=password_str)
        # リモートのディレクトリ確認
        sftp_connection = ssh.open_sftp()
        remote_files = sftp_connection.listdir(root_directory)
        remote_dir = list(set([re.sub(r'/.+$', '', remote_file) for remote_file in remote_files]))
        local_dir_l = pickup_dir(up_file_list)
        # 必要なディレクトリを作成
        for local_dir in local_dir_l:
            if local_dir not in remote_dir:
                print('Make directory: ' + local_dir)
                stdin, stdout, stderr = ssh.exec_command('mkdir ' + root_directory + '/' + local_dir)
                print(stdin)
                print(stdout)
                print(stderr)
        # ファイルをアップロード
        with scp.SCPClient(ssh.get_transport()) as scpc:
            for up_file in up_file_list:
                print('upload: ' + up_file)
                if '/' in up_file:
                    up_dir = '/' + re.findall(r'^(.+)/', up_file)[0]
                else:
                    up_dir = ''
                scpc.put('case_dir/' + case_name + '/product/' + up_file,
                         root_directory + '/' + up_dir)


def pickup_dir(up_file_list):
    dir_list = []
    for file in up_file_list:
        if '/' in file:
            dir_str_l = re.findall(r'^(.+?)/', file)
            if dir_str_l:
                dir_str = dir_str_l[0]
                if dir_str not in dir_list:
                    dir_list.append(dir_str)
    return dir_list


def ftp_upload(case_name, domain_str, user_name, password_str, root_directory, up_file_list):
    """
    FTPでファイルをアップロード,ベースはドメイン直下
    :param case_name: 作業ディレクトリ
    :param domain_str: ドメイン
    :param user_name: ユーザー名
    :param password_str: サーバーパスワード
    :param root_directory: ファイルをいれる先のディレクトリ
    :param up_file_list: アップロードするファイルのリスト（product以降のpath）
    :return: none
    """
    with FTP(domain_str, passwd=password_str) as ftp:
        ftp.login(user=user_name, passwd=password_str)
        ftp.cwd(root_directory)
        # ftp.retrlines('LIST')
        for up_file_name in up_file_list:
            with open('case_dir/' + case_name + '/' + 'product' + '/' + up_file_name, 'rb') as fp:
                ftp.storbinary("STOR " + up_file_name, fp)
            print('upload: ' + up_file_name)
        ftp.close()
    return


def file_pickup(target_directory):
    result = []
    file_list = os.listdir(target_directory)
    for file_str in file_list:
        if '.' not in file_str and '_test' not in file_str:
            result.extend(file_pickup(target_directory + '/' + file_str))
        elif '_test' not in file_str and '_copy' not in file_str:
            result.append(target_directory + '/' + file_str)
    return result


def first_backup(domain_str, user_name, password_str, root_directory, backup_dir):
    os.makedirs(backup_dir)
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=domain_str, port=22, username=user_name, password=password_str)
        # リモートのディレクトリ確認
        sftp_connection = ssh.open_sftp()
        print(sftp_connection.listdir('www/wmelon'))
        remote_files = search_files_in_scp(root_directory, sftp_connection)
        print(remote_files)
        with scp.SCPClient(ssh.get_transport()) as scpc:
            for r_file in remote_files:
                r_file_name = r_file.replace(root_directory + '/', '')
                if not re.findall(r'/\.', r_file):
                    print('download: ' + r_file)
                    if '/' in r_file_name:
                        dir_name = re.findall(r'^(.+)/', r_file_name)[0]
                        if not os.path.isdir(backup_dir + '/' + dir_name):
                            os.makedirs(backup_dir + '/' + dir_name)
                    scpc.get(r_file, backup_dir + '/' + r_file_name)


def search_files_in_scp(directory_name, sftp_connection):
    result = []
    print(directory_name)
    remote_files = sftp_connection.listdir(directory_name)
    for remote_file in remote_files:
        if '.' in remote_file:
            result.append(directory_name + '/' + remote_file)
        else:
            result.extend(search_files_in_scp(directory_name + '/' + remote_file, sftp_connection))
    return result


def sample_page_upload(case_name):
    up_files = []
    p = pathlib.Path('case_dir/' + case_name + '/product')
    up_files = [y.as_posix().replace('case_dir/' + case_name + '/product/', '')
                for y in p.glob('**/*') if '.' in y.as_posix()]
    print(up_files)

    scp_upload(case_name, 'wmelon01.sakura.ne.jp', 'wmelon01', '4tmy3uap6y', 'www/wmelon/sample/kuma', up_files)


if __name__ == '__main__':
    # all_upload('wmelon', 'wmelon01.sakura.ne.jp', 'wmelon01', '4tmy3uap6y', 'www/wmelon')
    sample_page_upload('kuma')

    # first_backup('wmelon', 'wmelon01.sakura.ne.jp', 'wmelon01', '4tmy3uap6y', 'www/wmelon')

    # scp_upload('wmelon', 'wmelon01.sakura.ne.jp', 'wmelon01', '4tmy3uap6y', 'www/wmelon', ['contact/mail.php'])
    # ftp_upload('wmelon', 'wmelon01.sakura.ne.jp', 'wmelon01', '4tmy3uap6y', 'www/wmelon',
    # ['policy/index.html', 'css/base6.css'])
