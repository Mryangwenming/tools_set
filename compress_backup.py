import datetime
import glob
import logging
import os
import time
import zipfile

logging.basicConfig(filename=os.path.join(os.getcwd(), 'backup.log'),
                    filemode='a',
                    level=logging.INFO,
                    format='%(asctime)s  %(filename)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def get_zip(files, zip_name):
    '''
    压缩文件
    :param files:
    :param zip_name:
    :return:
    '''
    zp = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for file in files:
        _, filename = os.path.split(file)
        zp.write(file, filename)
        logging.info("{} ADD {}".format(zip_name, file))
        os.remove(file)
    zp.close()


def timestamp_to_time(timestamp):
    '''
    时间戳转换成日期时间
    :param timestamp:
    :return:
    '''
    time_struct = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d", time_struct)


def time_to_timestamp(year, month, date):
    '''
    日期时间转换成时间戳
    :param year:
    :param month:
    :param date:
    :return:
    '''
    date = datetime.datetime(year, month, date)
    return date.timestamp()


def verify(file_path):
    '''
    将指定文件夹中的符合格式的图片的路径解析出来
    :param file_path:
    :return:
    '''
    r = "{}/*[.jpeg|.jpg|.png]".format(file_path)
    return glob.iglob(r)


def interval_backup(file_path, start_date, end_date=None):
    '''
    按照某个时间段, 根据指定路径压缩图片
    :param file_path: 图片所在路径
    :param start_date: 开始时间
    :param end_date: 结束时间
    :return:
    '''
    zip_list = []
    if not end_date:
        end_date = timestamp_to_time(time.time())
    # zip_name = os.path.join(os.curdir, start_date + "&" + end_date + ".zip")
    zip_name = os.path.join(file_path, start_date + "&" + end_date + ".zip")
    for path in verify(file_path):
        create_time = os.path.getmtime(path.encode("utf-8"))
        s_year, s_month, s_date = [int(i) for i in start_date.split("-")]
        e_year, e_month, e_date = [int(i) for i in end_date.split("-")]
        start = time_to_timestamp(s_year, s_month, s_date)
        end = time_to_timestamp(e_year, e_month, e_date)
        if start <= create_time <= end:
            zip_list.append(path)
    get_zip(zip_list, zip_name)
    print("压缩完成")


def period_backup(file_path, interval):
    '''
    按照间隔周期进行备份图片
    :param file_path: 图片所在路径
    :param interval: 间隔周期,以天为单位
    :return:
    '''
    zip_list = []
    now_time = timestamp_to_time(time.time())
    for path in verify(file_path):
        create_time = timestamp_to_time(os.path.getmtime(path.encode("utf-8")))
        c_year, c_month, c_day = [int(i) for i in create_time.split("-")]
        n_year, n_month, n_day = [int(i) for i in now_time.split("-")]
        if (datetime.datetime(n_year, n_month, n_day) - datetime.datetime(c_year, c_month, c_day)).days <= interval:
            zip_list.append(path)
    zip_name = os.path.join(file_path, now_time + ".zip")
    get_zip(zip_list, zip_name)
    print("压缩完成")


if __name__ == '__main__':
    # interval_backup("/home/ywm/Desktop/demo/photo", "2019-09-23", "2019-10-09")
    # interval_backup("/home/ywm/Desktop/demo/photo", "2019-05-23")
    period_backup("/home/ywm/Desktop/demo/photo", 30)

