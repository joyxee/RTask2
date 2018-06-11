# coding=UTF-8

# 节点配置文件

# 任务名，应与tasks目录下需要执行的任务模块名保持一致
TASK_NAME = 'demo'

# 具体描述本节点所执行的任务
TASK_DESCRIPTION = '这是一个Demo，接受任务后不执行任何动作。'

# 是否开启任务去重功能
TASK_DISTINCT = True

# 是否开启自动扩展功能，如执行一个任务之后会解析出更多的任务
AUTO_ADD_TASKS = True

# 最大错误次数
MAX_ERROR_NUMS = 10

# 超过最大错误次数休眠时间(秒)
EXCEED_ERRORS_SLEEP = 30*60

# Huey Redis 数据库，用于节点开启多线程异步执行任务，可以在每个节点独立配一个Redis
HUEY_REDIS_HOST = '127.0.0.1'
HUEY_REDIS_PORT = 6379
HUEY_REDIS_DB = 0
HUEY_REDIS_PWD = ''

# 存放节点信息的Redis数据库，应由服务端统一提供一个Redis数据库给所有节点连接
NODE_REDIS_HOST = '127.0.0.1'
NODE_REDIS_PORT = 6379
NODE_REDIS_DB = 0
NODE_REDIS_PWD = ''

# 去重方式，redis集合(set)去重或者bloomfilter算法(bloom)去重
DISTINCT_METHOD = 'set'
# 若使用redis集合(set)去重，需要配置Redis数据库，应由服务端统一提供Redis数据库给所有节点连接
DISTINCT_SET_REDIS_TYPE = 'single'
DISTINCT_SET_REDIS_HOST = '127.0.0.1'
DISTINCT_SET_REDIS_PORT = 6379
DISTINCT_SET_REDIS_DB = 0
DISTINCT_SET_REDIS_PWD = ''
# 任务去重如使用Redis集群，请配置Redis集群节点
DISTINCT_SET_REDIS_NODES = [{"host": "127.0.0.1", "port": "7000"},
                        {"host": "127.0.0.1", "port": "7001"},
                        {"host": "127.0.0.1", "port": "7002"},
                        {"host": "127.0.0.1", "port": "7003"}]
# 若使用BloomFilter算法去重需要预先知道要去重的数量和错误率
DISTINCT_BLOOM_CAPACITY = 100000000
DISTINCT_BLOOM_ERROR_RATE = 0.00000001
