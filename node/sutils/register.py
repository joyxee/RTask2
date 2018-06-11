# coding=UTF-8

from . import sysinfo
from ..config import *


class Register(Object):
    """上线时在服务器注册节点，离线时在服务器删除节点信息"""

    def __init__(self):
        self.pool = redis.ConnectionPool(host=NODE_REDIS_HOST,
                                         port=NODE_REDIS_POST,
                                         db=NODE_REDIS_DB,
                                         password=NODE_REDIS_PWD,
                                         encoding='utf-8',
                                         decode_responses=True)
        self.client = redis.StrictRedis(connection_pool=self.pool)
        self.macid = sysinfo.get_macid()
        self.ips = sysinfo.get_ips()
        self.hostname = sysinfo.get_hostname()
        self.platform = sysinfo.get_platform()

    def register_node(self):
        node_data = {'macid': self.macid,
                     'tasks': list(),
                     'ips': self.ips,
                     'hostname': self.hostname,
                     'platform': self.platform,
                     'taskname': TASK_NAME,
                     'taskdescription': TASK_DESCRIPTION}
        self.client.hset('task_nodes', self.macid, host_data)

    def unregister_node(self):
        self.client.hdel('task_nodes', self.macid)
