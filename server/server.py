# coding=UTF-8

from flask import Flask, render_template, request, redirect
from controller import NodeController


app = Flask(__name__)


##############################################节点管理##############################################
nodec = NodeController()
print(nodec.node_list())