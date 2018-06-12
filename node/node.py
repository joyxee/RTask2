# coding=UTF-8

import redis
import config
import zerorpc
from datetime import datetime
from sutils.register import Register
from worker import WorkerFactory
from sutils import sysinfo


def RPC_auth(func):
    def wrapper(*args, **kwargs):
        if len(args) < 2:
            result = 'Wrong arguments'
        elif args[1] != config.RPC_PWD:
            result = 'Wrong password'
        else:
            result = func(*args, **kwargs)
        return result
    return wrapper


class RPCNode(object):
    """可以让服务器端远程调用的节点类"""

    def __init__(self):
        self.worker_factory = WorkerFactory()

    def ping(self):
        return True

    @RPC_auth
    def start_worker(self, password=None, worker_nums=1):
        self.worker_factory.create_worker(worker_nums)
        return worker_nums

    @RPC_auth
    def stop_worker(self, password=None, worker_index=0):
        self.worker_factory.destroy_worker_by_index(worker_index)
        return worker_index

    @RPC_auth
    def stop_all_workers(self, password=None):
        self.worker_factory.destroy_all_workers()
        return True

    @RPC_auth
    def worker_count(self, password=None):
        return len(self.worker_factory.subprocesses)

    @RPC_auth
    def system_info(self, password=None):
        info_data = {
            'macid': sysinfo.get_macid(),
            'cpu_info': sysinfo.get_cpu(),
            'memory_info': sysinfo.get_memory(),
            'disk_info': sysinfo.get_disk(),
            'network_info': sysinfo.get_network()
        }
        return info_data

    @RPC_auth
    def shutdown(self, password=None):
        self.stop_all_workers()
        exit()


if __name__ == '__main__':
    try:
        register = Register(config)
        register.register_node()
        s = zerorpc.Server(RPCNode())
        s.bind("tcp://0.0.0.0:{0}".format(config.RPC_PORT))
        s.run()
    except Exception as e:
        time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('./logs/node.err', 'a', encoding='UTF-8') as f:
            f.write('##############################\n')
            f.write('ErrorTime : ' + time_str + '\n')
            f.write('ErrorData : ' + str(e) + '\n')
            f.write('##############################\n')
    finally:
        register.unregister_node()
