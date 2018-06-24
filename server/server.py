# coding=UTF-8

import config
from flask import Flask, render_template, request, redirect
from controller import NodeController, RedisController, TaskController


app = Flask(__name__)
redis_controller = RedisController()
node_controller = NodeController(redis_controller.node_client)
task_controller = TaskController()


##################任务队列###########################
@app.route('/', methods=['GET'])
@app.route('/tasks/', methods=['GET'])
def task_lists():
    node_list = node_controller.node_list()
    executable_tasks = list()
    for n in node_list:
        executable_tasks.append(n['taskname'])
    task_list = task_controller.task_list()
    return render_template('tasks.html', task_list=task_list, executable_tasks=executable_tasks)


@app.route('/tasks/add/', methods=['POST'])
def add_task():
    taskname = request.form['name']
    tasknum = request.form['num']
    for _ in range(int(tasknum)):
        task_controller.add_task(taskname)
    return tasknum


##################节点管理###########################
@app.route('/nodes/', methods=['GET'])
def node_lists():
    node_list = node_controller.node_list()
    node_nums = len(node_list)
    return render_template('nodes.html',
                           node_list=node_list,
                           node_nums=node_nums)


@app.route('/nodeinfo/<macid>/', methods=['GET'])
def node_info(macid):
    base_info = node_controller.node_search(macid)
    if base_info:
        extra_info = node_controller.node_system_info(macid)
        return render_template('nodeinfo.html',
                               base_info=base_info,
                               cpu_info=extra_info['cpu_info'],
                               memory_info=extra_info['memory_info'],
                               disk_info=extra_info['disk_info'],
                               network_info=extra_info['network_info'])
    else:
        return redirect('/nodes/')


@app.route('/nodestopall/<macid>/', methods=['POST'])
def node_stop_all(macid):
    node_controller.node_stop_all_workers(macid)
    return redirect('/nodes/')


@app.route('/nodedelete/<macid>/', methods=['POST'])
def node_delete(macid):
    node_controller.node_remove(macid)
    return redirect('/nodes/')


##################进程管理###########################
@app.route('/workers/', methods=['GET'])
def worker_lists():
    node_list = node_controller.node_list()
    worker_nums = 0
    for node in node_list:
        worker_nums += node['workers']
    return render_template('workers.html',
                           node_list=node_list,
                           worker_nums=worker_nums)


@app.route('/workercontrol/<macid>/<controltype>/', methods=['POST'])
def worker_control(macid, controltype):
    if controltype == 'add':
        node_controller.node_start_worker(macid)
    elif controltype == 'reduce':
        node_controller.node_stop_worker(macid)
    return redirect('workers')


##################Redis 状态###########################
@app.route('/redis/', methods=['GET'])
def redis_lists():
    redis_lists = list()
    node_redis_info = redis_controller.node_redis_info()
    brief_node_redis_info = {'desc': 'Redis 节点信息数据库',
                             'name': 'node',
                             'type': '单机',
                             'ip_port': config.NODE_REDIS_HOST + ' : ' + str(config.NODE_REDIS_PORT),
                             'dbsize': node_redis_info['dbsize'],
                             'clients': node_redis_info['connected_clients'],
                             'used_memory': node_redis_info['used_memory_human']}
    redis_lists.append(brief_node_redis_info)

    if config.TASK_DISTINCT:
        distinct_redis_info = redis_controller.distinct_redis_info()
        brief_distinct_redis_info = {
            'desc': 'Redis 数据去重数据库', 'name': 'distinct'}
        if config.DISTINCT_SET_REDIS_TYPE == 'single':
            brief_distinct_redis_info['type'] = '单机'
            brief_distinct_redis_info['ip_port'] = config.DISTINCT_SET_REDIS_HOST + \
                ' : ' + str(config.DISTINCT_SET_REDIS_PORT)
            brief_distinct_redis_info['dbsize'] = distinct_redis_info['dbsize']
            brief_distinct_redis_info['clients'] = distinct_redis_info['connected_clients']
            brief_distinct_redis_info['used_memory'] = distinct_redis_info['used_memory_human']
        else:
            brief_distinct_redis_info['type'] = '集群'
            brief_distinct_redis_info['ip_port'] = [
                node['host'] + ' : ' + node['port'] for node in config.DISTINCT_SET_REDIS_NODES]
            brief_distinct_redis_info['dbsize'] = [
                k + ' : ' + str(v) for k, v in redis_controller.distinct_client.items()]
            brief_distinct_redis_info['clients'] = [
                k + ' : ' + str(v['connected_clients']) for k, v in distinct_redis_info.items()]
            brief_distinct_redis_info['used_memory'] = [
                k + ' : ' + v['used_memory_human'] for k, v in distinct_redis_info.items()]
        redis_lists.append(brief_distinct_redis_info)

    return render_template('redis.html', redis_lists=redis_lists)


@app.route('/redissave/<name>/<savetype>', methods=['POST'])
def redis_save(name, savetype):
    if name == 'distinct' and config.TASK_DISTINCT:
        if savetype == 'save':
            redis_controller.distinct_redis_save(is_bgsave=False)
        elif savetype == 'bgsave':
            redis_controller.distinct_redis_save(is_bgsave=True)
    elif name == 'node':
        redis_controller.node_redis_save()

    return redirect('/redis/')


if __name__ == '__main__':
    if redis_controller.redis_checked:
        app.run(host='0.0.0.0', port=8888, debug=True)
    else:
        print('Redis数据库连接失败!请检查Redis连接配置是否正确或者正常运行')
