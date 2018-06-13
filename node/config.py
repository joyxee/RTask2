# coding=UTF-8

# 节点配置文件

# 任务名，应与tasks目录下需要执行的任务模块名保持一致
TASK_NAME = 'demo'

# 具体描述本节点所执行的任务
TASK_DESCRIPTION = '这是一个Demo，接受任务后打印任务id到Log文件。'

# 存放节点信息的Redis数据库，应由服务端统一提供一个Redis数据库给所有节点连接
NODE_REDIS_HOST = '192.168.0.171'
NODE_REDIS_PORT = 6380
NODE_REDIS_DB = 0
NODE_REDIS_PWD = ''

# 任务分发服务器信息，使用gearman分布式任务分发框架，由服务端提供
GEARMAN_HOST = '192.168.0.171'
GEARMAN_PORT = '4730'

# RPC远程调用，认证和端口配置
RPC_PASSWORD = 'rpc'
RPC_PORT = 5555
