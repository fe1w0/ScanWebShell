import os
import subprocess
import re


def recursion_load_php_file_opcode(dir):
    """
    递归获取 php opcde
    :param dir: 目录文件
    :return:
    """
    files_list = []
    for root, dirs, files in os.walk(dir):
        for filename in files:
            if filename.endswith('.php') or filename.endswith('.php3') or filename.endswith('.php5') or filename.endswith('.phtml') or filename.endswith('.pht') :
                try:
                    full_path = os.path.join(root, filename)
                    file_content = load_php_opcode(full_path)
                    print("[Gen success] {}".format(full_path))
                    print('--' * 20)
                    if file_content != "":
                        files_list.append(file_content)
                except:
                    continue
    return files_list



def load_php_opcode(phpfilename):
    """
    获取php opcode 信息
    :param phpfilename:
    :return:
    """
    try:
        output = subprocess.check_output(['php', '-dvld.active=1', '-dvld.execute=0', phpfilename], stderr=subprocess.STDOUT).decode()
        tokens = re.findall(r'\s(\b[A-Z_]{2,}\b)\s', output)  # {2,} 至少匹配两次,规避一开始三个错误的结果
        t = " ".join(tokens)
        return t
    except BaseException as e :
        return ""

