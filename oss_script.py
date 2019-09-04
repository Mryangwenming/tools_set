import oss2
import sys
from datetime import datetime
from prettytable import PrettyTable


class OssOwnerManage:
    def __init__(self):
        self.endpoint = "<your endpoint>"
        self.bucket_name = "<your bucket_name>"
        self.access_key_id = "<your access_key_id>"
        self.access_key_secret = "<your access_key_secret>"
        self.bucket = oss2.Bucket(oss2.Auth(self.access_key_id, self.access_key_secret), self.endpoint, self.bucket_name)
        self.tb = PrettyTable()
        self.tb.field_names = ["Filename", "Size", "Tag", "Last_modified"]


    @staticmethod
    def formatSize(bytes):
        try:
            bytes = float(bytes)
            kb = bytes / 1024
        except:
            print("传入的字节格式不对")
            return "Error"

        if kb >= 1024:
            M = kb / 1024
            if M >= 1024:
                G = M / 1024
                return "%fG" % (G)
            else:
                return "%fM" % (M)
        else:
            return "%fkb" % (kb)

    @staticmethod
    def percentage(consumed_bytes, total_bytes):
        """进度条回调函数，计算当前完成的百分比
        :param consumed_bytes: 已经上传/下载的数据量
        :param total_bytes: 总数据量
        """
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            sys.stdout.write("\r当前传输进度: {}% ".format(rate))
            sys.stdout.flush()

    def get_bucket_status(self):
        # 获取bucket相关信息
        bucket_info = self.bucket.get_bucket_info()
        print('name: ' + bucket_info.name)
        print('storage class: ' + bucket_info.storage_class)
        print('creation date: ' + bucket_info.creation_date)

        # 查看Bucket的状态
        bucket_stat = self.bucket.get_bucket_stat()
        print('storage: ' + str(bucket_stat.storage_size_in_bytes))
        print('object count: ' + str(bucket_stat.object_count))
        print('multi part upload count: ' + str(bucket_stat.multi_part_upload_count))

    def get_all(self):
        '''
        如果需要获取全部的时候有指定数量,需要重新添加参数, 目前功能是全部获取
        :param nums: 最多展示的文件的数量
        '''
        files_list = set()
        for i, object_info in enumerate(oss2.ObjectIterator(self.bucket)):
            files_list.add(object_info.key)
            # if i + 1 >= nums:
            #     break
        for i in files_list:
            info = self.bucket.get_object_meta(i)
            self.tb.add_row([i, self.formatSize(info.content_length), info.etag, datetime.fromtimestamp(info.last_modified)])
        print(self.tb)

    def get_one(self, filename):
        '''
        :param filename: 仓库文件名
        '''
        try:
            info = self.bucket.get_object_meta(filename)
            self.tb.add_row([filename, self.formatSize(info.content_length), info.etag, datetime.fromtimestamp(info.last_modified)])
            print(self.tb)
        except oss2.exceptions.NoSuchKey:
            print("不存在此文件！")

    def upload(self, remote_file, local_file):
        '''
        :param remote_file: 仓库文件名
        :param local_file: 本地文件名
        '''
        try:
            self.bucket.get_object_meta(remote_file)
        except oss2.exceptions.NoSuchKey:
            oss2.resumable_upload(self.bucket, remote_file, local_file, multipart_threshold=200*1024,
                                  part_size=100*1024, num_threads=3,progress_callback=self.percentage)
        else:
            option = input("您要上传的文件仓库中已存在! 请选择：Y:覆盖 N:改名 ")
            if option.lower() == 'y':
                oss2.resumable_upload(self.bucket, remote_file, local_file, multipart_threshold=200 * 1024,
                                      part_size=100 * 1024, num_threads=3, progress_callback=self.percentage)
            elif option.lower() == 'n':
                new_remote_file_name = input("请输入更改之后的名字：")
                oss2.resumable_upload(self.bucket, new_remote_file_name, local_file, multipart_threshold=200 * 1024,
                                      part_size=100 * 1024, num_threads=3, progress_callback=self.percentage)
            else:
                print("输入有误，请重新操作！")

    def delete(self, filename):
        '''
        :param filename: 仓库文件名
        '''
        try:
            result = self.bucket.get_object_meta(filename)
            if result:
                self.bucket.delete_object(filename)
                print("删除成功")
        except oss2.exceptions.NoSuchKey:
            print("要删除的文件不存在！")

    def download(self, remote_file, local_file):
        '''
        :param remote_file: 仓库文件名
        :param local_file: 本地文件名
        :return:
        '''
        try:
            oss2.resumable_download(self.bucket, remote_file, local_file, multiget_threshold=200*1024,
                                    part_size=100*1024, num_threads=3, progress_callback=self.percentage)
        except oss2.exceptions.NotFound:
            print("下载的文件不存在！")

super_manager = OssOwnerManage()

def add_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--operation")
    parser.add_argument("-rf", "--remote_filename")
    parser.add_argument("-lf", "--local_filename")
    parser.add_argument("-f", "--filename")
    args = parser.parse_args()
    return args


def main():
    args = add_argument()
    operation = args.operation
    remote_filename = args.remote_filename
    local_filename = args.local_filename
    filename = args.filename

    if not operation:
        print("参数不完整")

    if operation == "all":
        super_manager.get_all()

    if operation == "get":
        if not filename:
            print("-f 参数不存在")
        else:
            super_manager.get_one(filename)

    if operation in {"upload", "download"}:
        if not remote_filename or not local_filename:
            print("-rf, -lf 参数不完整")
        else:
            if operation == "upload":
                super_manager.upload(remote_filename, local_filename)
            else:
                super_manager.download(remote_filename, local_filename)

    if operation == "delete":
        if not filename:
            print("-f 参数不存在")
        else:
            super_manager.delete(filename)


if __name__ == '__main__':
    main()



