# coding=UTF-8

import os
import shlex
import importlib
import subprocess
import config
from datetime import datetime
from python3_gearman import GearmanWorker


class WorkerFactory(object):
    """一个worker表示一个线程，Worker类用于控制启动线程，停止线程"""
    task = importlib.import_module('tasks.' + config.TASK_NAME)

    def __init__(self):
        self.subprocesses = []

    def create_worker(self, worker_nums=1):
        cmd = shlex.split('python3 worker.py')
        for _ in range(worker_nums):
            subp = subprocess.Popen(cmd,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            self.subprocesses.append(subp)
        return self.subprocesses

    def destroy_all_workers(self):
        for subp in self.subprocesses:
            subp.kill()
        self.subprocesses = []

    def destroy_worker_by_index(self, index):
        subp = self.subprocesses[index:index+1]
        if subp:
            subp[0].kill()
            del self.subprocesses[index]


if __name__ == '__main__':
    try:
        gm_worker = GearmanWorker(
            [config.GEARMAN_HOST + ':' + config.GEARMAN_PORT])
        gm_worker.register_task(config.TASK_NAME, WorkerFactory.task.main)
        gm_worker.work()
    except Exception as e:
        time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('./logs/worker.err', 'a', encoding='UTF-8') as f:
            f.write('##############################\n')
            f.write('ErrorTime : ' + time_str + '\n')
            f.write('ErrorData : ' + str(e) + '\n')
            f.write('##############################\n')
    finally:
        gm_worker.shutdown()
