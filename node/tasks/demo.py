# coding=UTF-8


def main(task_id, task_data):
    """
    任务执行主体。服务器分发任务给节点，节点通过此方法执行任务。

    参数：
        task_id 任务唯一标识
        task_data 任务相关数据

    返回：
        result_data 任务执行后得到的数据
        auto_add_tasks 自动扩展增加的任务列表，[{task_id:'xxx', task_data:{}}, ]
    """
    return {"result_data":None, "auto_add_tasks":None}


def save(result_data):
    """
    保存任务执行后得到的相关数据。

    参数:
        result_data 执行main方法后返回的result_data
    """
    pass
