import os
import subprocess
import shutil
import argparse


def get_py_file(root_path):
    for file in os.listdir(root_path):
        if file.startswith(".") or file.startswith("__"):
            pass
        else:
            node_path = os.path.join(root_path, file)
            if os.path.isdir(node_path):
                for i in get_py_file(node_path):
                    yield os.path.join(node_path, i)
            if os.path.isfile(node_path) and (node_path).endswith(".py"):
                yield node_path


def add_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--file_path")
    parser.add_argument("-f", "--filter_file")
    args = parser.parse_args()
    return args


def compile_file(file_path, filter_set):
    for file in get_py_file(file_path):
        file_name = os.path.split(file)[-1]
        abspath = os.path.split(file)[0]
        name = file_name.split(".")[0]

        if name in filter_set:
            pass
        else:
            cmd = "python -m nuitka --module --recurse-none --plugin-enable=pylint-warnings {} --output-dir={}".format(file, abspath)
            _, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            if err:
                print("Error compiling project: {}".format(err))
            try:
                shutil.rmtree(os.path.join(abspath, "{}.build".format(name)))
                os.remove(os.path.join(abspath, "{}.pyi".format(name)))
                os.remove(file)
            except Exception as e:
                print("Delete file is error: {}".format(e))

    print("Complete compilation!")


def main():
    args = add_argument()
    try:
        file_path = args.file_path
        filter_set = args.filter_file.split(",")
        compile_file(file_path, filter_set)
    except AttributeError:
        print("输入的参数不完整")


if __name__ == '__main__':
    main()









