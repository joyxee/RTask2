# coding=UTF-8

import re
import redis
import zerorpc
import config
from contextlib import contextmanager


@contextmanager
def connect_rpc_node(rpc_ip_port):
    rpc_node = zerorpc.Client(timeout=3, heartbeat=3)
    rpc_node.connect(rpc_ip_port)
    try:
        yield rpc_node
    except Exception as e:
        pass
    finally:
        rpc_node.close()


class NodeController(object):
    """节点管理类"""

    def __init__(self, client):
        self.client = client

    def _rpcip_check(self, ip):
        try:
            rpc = zerorpc.Client(timeout=3, heartbeat=3)
            rpc.connect(
                "tcp://{ip}:{port}".format(ip=ip, port=config.RPC_PORT))
            ping = rpc.ping()
            rpc.close()
            return ping
        except Exception as e:
            return False

    def _node_worker_count(self, rpcip):
        result = None
        with connect_rpc_node(rpcip) as rpc:
            result = rpc.worker_count(config.RPC_PASSWORD)
        return result

    def node_list(self):
        nodes_str = self.client.hgetall('nodes')
        nodes = list()
        for _, v in nodes_str.items():
            data = eval(v)
            dst_ip = None
            ips = data['ips']
            for ip in ips:
                if re.match('\d+\.\d+\.\d+\.\d+', ip) and self._rpcip_check(ip):
                    dst_ip = ip
                    break
            data['rpcip'] = "tcp://{ip}:{port}".format(
                ip=dst_ip, port=config.RPC_PORT)
            data['workers'] = self._node_worker_count(data['rpcip'])
            nodes.append(data)
        return nodes

    def node_search(self, macid):
        node = self.client.hget('nodes', macid)
        node = eval(node)
        dst_ip = None
        ips = node['ips']
        for ip in ips:
            if self._rpcip_check(ip):
                dst_ip = ip
                break
        node['rpcip'] = "tcp://{ip}:{port}".format(
            ip=dst_ip, port=config.RPC_PORT)
        node['workers'] = self._node_worker_count(node['rpcip'])
        return node

    def node_start_worker(self, macid, worker_nums=1):
        node = self.node_search(macid)
        with connect_rpc_node(node['rpcip']) as rpc:
            rpc.start_worker(config.RPC_PASSWORD, worker_nums)

    def node_stop_worker(self, macid, worker_index=0):
        node = self.node_search(macid)
        with connect_rpc_node(node['rpcip']) as rpc:
            rpc.stop_worker(config.RPC_PASSWORD, worker_index)

    def node_stop_all_workers(self, macid):
        node = self.node_search(macid)
        with connect_rpc_node(node['rpcip']) as rpc:
            rpc.stop_all_workers(config.RPC_PASSWORD)

    def node_system_info(self, macid):
        node = self.node_search(macid)
        info = None
        with connect_rpc_node(node['rpcip']) as rpc:
            info = rpc.system_info(config.RPC_PASSWORD)
        return info

    def node_remove(self, macid):
        to_remove_node = self.node_search(macid)
        self.client.hdel('nodes', macid)
        with connect_rpc_node(to_remove_node['rpcip']) as rpc:
            rpc.stop_all_workers(config.RPC_PASSWORD)
            rpc.shutdown(config.RPC_PASSWORD)


class TaskController(object):
    """任务管理类，通过gearman提交任务，查看任务数量等"""

    def __init__(self, arg):
        super(TaskController, self).__init__()
        self.arg = arg


class RedisController(object):
    """Redis管理类，查看Redis数据库相关信息"""

    def __init__(self):
        node_redis_pool = redis.ConnectionPool(host=config.NODE_REDIS_HOST,
                                               port=config.NODE_REDIS_PORT,
                                               db=config.NODE_REDIS_DB,
                                               password=config.NODE_REDIS_PWD,
                                               encoding='utf-8',
                                               decode_responses=True)
        self.node_client = redis.StrictRedis(connection_pool=node_redis_pool)
        if config.TASK_DISTINCT:
            if config.DISTINCT_SET_REDIS_TYPE == 'single':
                distinct_redis_pool = redis.ConnectionPool(host=config.DISTINCT_SET_REDIS_HOST,
                                                           port=config.DISTINCT_SET_REDIS_PORT,
                                                           db=config.DISTINCT_SET_REDIS_DB,
                                                           password=config.DISTINCT_SET_REDIS_PWD,
                                                           encoding='utf-8',
                                                           decode_responses=True)
                self.distinct_client = redis.StrictRedis(
                    connection_pool=distinct_redis_pool)
            else:
                self.distinct_client = rediscluster.StrictRedisCluster(startup_nodes=config.DISTINCT_SET_REDIS_NODES,
                                                                       decode_responses=True,
                                                                       socket_timeout=3,
                                                                       socket_connect_timeout=3)
        try:
            self.node_client.ping()
            if config.TASK_DISTINCT:
                self.distinct_client.ping()
        except Exception as e:
            self.redis_checked = False
        else:
            self.redis_checked = True

    def node_redis_info(self):
        info = self.node_client.info()
        info['dbsize'] = self.node_client.dbsize()
        return info

    def distinct_redis_info(self):
        info = self.distinct_client.info()
        if config.DISTINCT_SET_REDIS_TYPE == 'single':
            info['dbsize'] = self.distinct_client.dbsize()
        return info

    def node_redis_save(self):
        return self.node_client.save()

    def distinct_redis_save(self, is_bgsave=False):
        if is_bgsave:
            return self.distinct_client.bgsave()
        else:
            return self.distinct_client.save()