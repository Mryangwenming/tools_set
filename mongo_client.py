from pymongo import MongoClient


class MongoManager(object):
    """
    mongodb操作封装
    """
    def __init__(self, host='localhost', port=27017, db_name=None, collection_name=None):
        """
        初始化连接 + 认证
        :param host: ip
        :param port: 端口
        :param db_name: 数据库名称 可选
        :param collection_name: 集合名称 可选 需要先有数据库名称后 此数据才可使用
        :return:
        """
        self.host = host
        self.port = port
        self.client = MongoClient(host, 27017, username='app', password='app_topo',
                                  authMechanism='SCRAM-SHA-1', authSource='admin')
        if db_name:
            self.db = self.client.__getattr__(db_name)
        else:
            self.db = None
        if self.db and collection_name:
            self.collection = self.db.__getattr__(collection_name)
        else:
            self.collection = None

    def close(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.close()

    def select_db(self, db_name):
        """
        选择数据库
        :param db_name: 数据库名称
        :return:
        """
        self.db = self.client.__getattr__(db_name)

    def select_collection(self, collection_name):
        """
        选择集合
        :param collection_name: 集合名称
        :return:
        """
        if self.db:
            self.collection = self.db.__getattr__(collection_name)
        else:
            raise Exception('db not connection')

    def insert_document(self, data):
        """
        插入数据 多个和单个
        :param data:
        :return:
        """
        if self.collection:
            if isinstance(data, list):
                self.collection.insert_many(data)
            elif isinstance(data, dict):
                self.collection.insert_one(data)
            else:
                raise Exception('data type error')
        else:
            raise Exception('collection not connection')

    def drop_collection(self, collection_name):
        """
        删除集合
        :param collection_name 集合名称
        :return:
        """
        if self.db:
            self.db.get_collection(collection_name).drop()
        else:
            raise Exception('db not connection')

    def drop_db(self, db_name):
        self.client.drop_database(db_name)

    def find_document_many(self, filter_=None, show=None, collection_name=None,
                           db_name=None, return_type=1):
        """
        查询数据
        如果有集合连接 直接查询
        如果有数据库连接和集合名  可以查询
        如果有数据库名称和集合名称  可以查询

        分页 数量少的时候可以使用 limit skip
        数量多的时候建议使用 搜索_id 并且取比次_id大的指定数量 在创建集合时默认会把_id创建唯一索引
        db.node.find({'_id': {'$gt': ObjectId('5ed85a242ae5cf13b63b91aa')}}).limit(10)
        此处未使用分页

        :param filter_: 搜寻条件 {'_id': '123'}
        :param show: 显示字段 {'_id': 0, 'data': 1}
        :param collection_name: 集合名称 可选 在没有连接节点时需要传
        :param db_name: 数据库名称 可选 在没有连接数据库时需要传
        :param return_type: 返回形式 生成器还是列表 默认1 列表  0生成器
        :return:
        """
        if not filter_:
            filter_ = {}
        if not show:
            show = {}
        if self.collection:
            collection = self.collection
        elif self.db and collection_name:
            collection = self.select_collection(collection_name)
        else:
            if db_name and collection_name:
                collection = self.select_db(db_name).select_collection(collection_name)
            else:
                raise Exception('db not collection')

        data = collection.find(filter_, show)
        if return_type == 1:
            return [res for res in data]
        else:
            return data


if __name__ == '__main__':
    pass
    # 建议使用方式
    # with MongoManager(db_name='test2', collection_name='line') as mon:
    #     mon.insert_document({'data': 456})
    #     poi = mon.find_document_many({'data': 456}, {'_id': 0})
    #     print(poi)
    #     mon.drop_db('test2')

