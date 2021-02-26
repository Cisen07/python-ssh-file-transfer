# __author__: Cisen
# date: 2021/2/21

import os
import paramiko


hostname = '192.168.1.1'
username = 'root'
password = 'password'
port = 22

input_file = "path-to-a-file"
output_folder = "/path-to-a-folder/"


# verdict whether the path is a folder based on the name
def is_folder_name(path):
    return True if path[-1] == '\\' or path[-1] == '/' else False


def is_ubuntu(path):
    return True if path[0] == '/' else False


def get_filename(path):
    return path.split('/')[-1] if is_ubuntu(path) else os.path.basename(path)


def files_append(file_list, input_file, ssh):
    if is_folder_name(input_file):
        if is_ubuntu(input_file):
            stdin, stdout, stderr = ssh.exec_command('ls -F ' + input_file)  # -F: neglect folder of ubuntu
            out = stdout.readlines()
            for o in out:
                temp = input_file + o
                files_append(file_list, temp[:-1], ssh)  # get rid of the '\n' at ends
        else:
            out = os.listdir(input_file)
            for o in out:
                temp_path = input_file+o
                if os.path.isdir(input_file+o):  # neglect folder of win
                    pass
                else:
                    files_append(file_list, temp_path, ssh)
    else:
        file_list.append(input_file)


def transfer(input_file, output_folder, func='get'):
    """
    :param func:
        get: download
        put: upload
    """
    with paramiko.SSHClient() as ssh:
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
        file_list = []
        files_append(file_list, input_file, ssh)
        with ssh.open_sftp() as sftp:
            the_func = sftp.get if func == 'get' else sftp.put
            print("Transferred => ")
            for file in file_list:
                the_func(file, output_folder + get_filename(file))
                print(file)


if __name__ == '__main__':
    transfer(input_file, output_folder, 'get')
