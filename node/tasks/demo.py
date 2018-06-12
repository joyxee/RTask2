# coding=UTF-8

import time

def main(gearman_worker, gearman_job):
    """
    任务执行主体。服务器分发任务给节点，节点通过此方法执行任务。

    参数：
        gearman_worker : gearman的一个worker实例
        gearman_job : gearman分发的任务信息

    返回（最后返回的字典需要转换为字符串）：
        result_data 任务执行后得到的数据
        auto_add_tasks 自动扩展增加的任务列表，[data1, data2, ...] 列表
        的每个data应与gearman_job中的data格式一致
    """
    worker_addr = str(gearman_worker)
    with open('./logs/demo-worker_{0}.log'.format(worker_addr[-10:-2]), 'a', encoding='UTF-8') as f:
        f.write('worker : ' + str(gearman_worker) + '\n')
        f.write('data : ' + str(gearman_job.data) + '\n')
    time.sleep(5)
    return str({"result_data": None, "auto_add_tasks": None})
