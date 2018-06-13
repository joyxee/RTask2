# coding=UTF-8

import redis
import zerorpc
import config


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
            rpc.connect("tcp://{ip}:{port}".format(ip=ip, port=config.RPC_PORT))
            ping = rpc.ping()
            rpc.close()
            return ping
        except Exception as e:
            return False

    def node_list(self):
        nodes_str = self.client.hgetall('nodes')
        nodes = list()
        for _,v in nodes_str.items():
            data = eval(v)
            rpcip = None
            ips = data['ips']
            for ip in ips:
                if self._rpcip_check(ip):
                    rpcip = ip
                    break
            data['rpcip'] = "tcp://{ip}:{port}".format(ip=rpcip, port=config.RPC_PORT)
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
        node['rpcip'] = "tcp://{ip}:{port}".format(ip=rpcip, port=RPC_PORT)
        return node
