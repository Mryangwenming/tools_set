# tools_set
记录Python的一些技巧及方法.

用Python通过网络快速共享文件.
  - 进入到要共享文件的目录下,运行下面的命令
  - python -m http.server
  - 后面可以加-b 参数指定地址及端口号

列表辗平.
  - 通过itertools包中的itertools.chain.from_iterable 快速辗平一个列表.
  - list = [[1, 2], [3, 4], [5, 6]]
  - list(itertools.chain.from_iterable(a_list)) ----> [1, 2, 3, 4, 5, 6]
  - list(itertools.chain(*a_list)) ----> [1, 2, 3, 4, 5, 6] 

添加脚本的执行参数的话,可以click模块, 它为命令行工具的开发封装了大量方法，使开发者只需要专注于功能实现.
