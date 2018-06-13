# coding=UTF-8

import redis
import zerorpc
import config
from contextlib import contextmanager


@contextmanager
def connect_rpc_node(rpcip):
    rpc_node = zerorpc.Client(timeout=3, heartbeat=3)
    rpc_node.connect(
        "tcp://{ip}:{port}".format(ip=rpcip, port=config.RPC_PORT))
    try:
        yield rpc_node
    except Exception as e:
        pass
    finally:
        rpc_node.close()


class NodeController(object):
    """节点管理类"""

    def __init__(self):
        self.pool = redis.ConnectionPool(host=config.NODE_REDIS_HOST,
                                         port=config.NODE_REDIS_PORT,
                                         db=config.NODE_REDIS_DB,
                                         password=config.NODE_REDIS_PWD,
                                         encoding='utf-8',
                                         decode_responses=True)
        self.client = redis.StrictRedis(connection_pool=self.pool)

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
            rpcip = None
            ips = data['ips']
            for ip in ips:
                if self._rpcip_check(ip):
                    rpcip = ip
                    break
            data['rpcip'] = "tcp://{ip}:{port}".format(
                ip=rpcip, port=config.RPC_PORT)
            data['workers'] = self._node_worker_count(rpcip)
            nodes.append(data)
        return nodes

    def node_search(self, macid):
        node = self.client.hget('nodes', macid)
        node = eval(node)
        rpcip = None
        ips = node['ips']
        for ip in ips:
            if self._rpcip_check(ip):
                rpcip = ip
                break
        node['rpcip'] = "tcp://{ip}:{port}".format(
            ip=rpcip, port=config.RPC_PORT)
        node['workers'] = self._node_worker_count(rpcip)
        return node

    def node_start_worker(self, macid, worker_nums=1):
        node = self.node_search(macid)
        with connect_rpc_node(node['rpcip']) as rpc:
            rpc.start_worker(config.RPC_PASSWORD, worker_nums)

    def node_stop_worker(self, macid, worker_index=0):
        node = self.node_search(macid)
        with connect_rpc_node(node['rpcip']) as rpc:
            rpc.stop_worker(config.RPC_PASSWORD, worker_nums)

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
        with connect_rpc_node(to_remove_node['rpcip']) as rpc:
            rpc.stop_all_workers(config.RPC_PASSWORD)
            rpc.shutdown(config.RPC_PASSWORD)
        self.client.hdel('nodes', macid)


class TaskController(object):
    """任务管理类，通过gearman提交任务，查看任务数量等"""

    def __init__(self, arg):
        super(TaskController, self).__init__()
        self.arg = arg
