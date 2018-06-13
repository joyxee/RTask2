# coding=UTF-8

import redis
from . import sysinfo

class Register(object):
    """上线时在服务器注册节点，离线时在服务器删除节点信息"""

    def __init__(self, config):
        self.taskname = config.TASK_NAME
        self.taskdescription = config.TASK_DESCRIPTION
        self.macid = sysinfo.get_macid()
        self.ips = sysinfo.get_ips()
        self.hostname = sysinfo.get_hostname()
        self.platform = sysinfo.get_platform()
        self.pool = redis.ConnectionPool(host=config.NODE_REDIS_HOST,
                                         port=config.NODE_REDIS_PORT,
                                         db=config.NODE_REDIS_DB,
                                         password=config.NODE_REDIS_PWD,
                                         encoding='utf-8',
                                         decode_responses=True)
        self.client = redis.StrictRedis(connection_pool=self.pool)

    def register_node(self):
        node_data = {'macid': self.macid,
                     'ips': self.ips,
                     'hostname': self.hostname,
                     'platform': self.platform,
                     'taskname': self.taskname,
                     'taskdescription': self.taskdescription}
        self.client.hset('nodes', self.macid, node_data)

    def unregister_node(self):
        self.client.hdel('nodes', self.macid)
