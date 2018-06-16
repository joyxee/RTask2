# coding=UTF-8

from flask import Flask, render_template, request, redirect
from controller import NodeController


app = Flask(__name__)
node_controller = NodeController()

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
