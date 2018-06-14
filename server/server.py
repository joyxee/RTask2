# coding=UTF-8

from flask import Flask, render_template, request, redirect
from controller import NodeController


app = Flask(__name__)


##############################################节点管理##############################################
@app.route('/nodes/', methods=['GET'])
def node_lists():
    node_controller = NodeController()
    node_list = node_controller.node_list()
    node_nums = len(node_list)
    return render_template('nodes.html', node_list=node_list, node_nums=node_nums)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)