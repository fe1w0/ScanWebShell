# coding:utf-8
# author: fe1w0
import joblib
from utils.utils import *

def check(file_name,cv,tf,gnb):
    """
    webshell 检测的主要函数 
    :param file_name:
    :param cv:
    :param tf:
    :param gnb:
    :return:
    """
    opcode = [load_php_opcode(file_name)]
    if opcode == [""]:
        return "Error!"
    opcode = cv.transform(opcode).toarray()
    opcode = tf.transform(opcode).toarray()

    # predict
    predict = gnb.predict(opcode)[-1]

    return predict

def file_check(dir):
    """
    对 dir 文件 进行 webshell 查杀
    :param dir:
    :return:
    """
    # init of CountVectorizer, TfidfTransformer and GaussianNB
    cv = joblib.load(r'./TrainedData/cv.pkl')
    tf = joblib.load(r'./TrainedData/tf.pkl')
    gnb = joblib.load(r'./TrainedData/gnb.pkl')
    response_result = []
    result = check(dir, cv, tf, gnb)
    if result != "Error!":
        response_result.append("{} is WebShell".format(dir))
    elif result == "Error!":
        response_result.append("Error!")
    else:
        response_result.append("{} is not WebShell".format(dir))
    return response_result


def folder_check(dir):
    """
    对目录下的文件进行webshell扫描
    :param dir:
    :return:
    """
    response_result = []
    # init of CountVectorizer, TfidfTransformer and GaussianNB
    cv = joblib.load(r'./TrainedData/cv.pkl')
    tf = joblib.load(r'./TrainedData/tf.pkl')
    gnb = joblib.load(r'./TrainedData/gnb.pkl')

    for root, dirs, files in os.walk(dir):
        for filename in files:
            if filename.endswith('.php') or filename.endswith('.php3') or filename.endswith('.php5') or filename.endswith('.phtml') or filename.endswith('.pht'):
                try:
                    full_path = os.path.join(root, filename)
                    result = check(full_path, cv, tf, gnb)
                    if result != "Error!":
                        response_result.append("{} is WebShell".format(full_path))
                except Exception as e:
                    print(e)
    return response_result

def webshellScan(php_file_name):
    """
    对文件进行 webshell 扫描
    :param php_file_name:
    :return:
    """
    if os.path.isdir(php_file_name):
        return folder_check(php_file_name)
    if os.path.isfile(php_file_name):
        return file_check(php_file_name)