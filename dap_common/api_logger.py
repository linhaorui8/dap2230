import logging
import os
import time


def api_log():
    # sys_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # print(sys_path)
    # log_path = sys_path + '\log' + time.strftime('%Y-%m-%d', time.localtime()) + '.log'
    backPath = os.path.abspath(os.path.join(os.getcwd(), "..")) + "/log/"
    if not os.path.exists(backPath):
        os.mkdir(backPath)
    log_time = time.strftime("%Y_%m_%d")

    log_name = backPath + log_time + '.log'
    print(log_name)
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    # 设置FileHandler日志文件
    fh = logging.FileHandler(log_name, 'w',
                             encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # 设置控制台输出log
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log.addHandler(fh)
    log.addHandler(ch)
    # 添加下面一句，在记录日志之后移除句柄
    # log.removeHandler(ch)
    # log.removeHandler(fh)
    # 关闭文件
    fh.close()
    ch.close()
    return log


# if __name__ == '__main__':
#     logger = api_log()
#     logger.debug('123')
