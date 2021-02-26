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


def is_folder(path):
    return True if path[-1] == '\\' or path[-1] == '/' else False


def is_ubuntu(path):
    return True if path[0] == '\\' else False


def get_filename(path):
    return path.split('\\')[-1] if is_ubuntu(path) else os.path.basename(path)


# def files_append(file_list, folder):
#     with paramiko.SSHClient() as ssh:
#         ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
#         ssh.connect(hostname=hostname, port=port, username=username, password=password)
#         stdin, stdout, stderr = ssh.exec_command('ls ' + folder)


def transfer(input_file, output_folder, func='get'):
    """
    :param func:
        get: download
        put: upload
    """
    with paramiko.SSHClient() as ssh:
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
        with ssh.open_sftp() as sftp:
            if func == 'get':
                sftp.get(input_file, output_folder + get_filename(input_file))
            elif func == 'put':
                sftp.put(input_file, output_folder + get_filename(input_file))
            else:
                raise ValueError('only \'get\' or \'put\' for param func in transfer()')


if __name__ == '__main__':
    transfer(input_file, output_folder, 'put')
