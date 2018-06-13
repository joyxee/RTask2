# coding=UTF-8

# 服务端(监控端)配置文件

# 是否开启自动添加任务功能，如一个任务执行完之后可以自动解析出更多的任务
AUTO_ADD_TASKS = True

# 是否开启任务去重功能
TASK_DISTINCT = True

# 存放节点信息的Redis数据库，应由服务端统一提供一个Redis数据库给所有节点连接
NODE_REDIS_HOST = '192.168.0.171'
NODE_REDIS_PORT = 6380
NODE_REDIS_DB = 0
NODE_REDIS_PWD = ''

# 去重方式，redis集合(set)去重或者bloomfilter算法(bloom)去重
DISTINCT_METHOD = 'set'
# 若使用redis集合(set)去重，需要配置Redis数据库，应由服务端统一提供Redis数据库给所有节点连接
DISTINCT_SET_REDIS_TYPE = 'single'
DISTINCT_SET_REDIS_HOST = '192.168.0.171'
DISTINCT_SET_REDIS_PORT = 6381
DISTINCT_SET_REDIS_DB = 0
DISTINCT_SET_REDIS_PWD = ''
# 如使用Redis集群去重，请配置Redis集群节点
DISTINCT_SET_REDIS_NODES = [{"host": "127.0.0.1", "port": "6382"},
                            {"host": "127.0.0.1", "port": "6383"},
                            {"host": "127.0.0.1", "port": "6384"},
                            {"host": "127.0.0.1", "port": "6385"}]
# 若使用BloomFilter算法去重需要预先知道要去重的数量和错误率
DISTINCT_BLOOM_CAPACITY = 100000000
DISTINCT_BLOOM_ERROR_RATE = 0.00000001

# 任务分发服务器信息，使用gearman分布式任务分发框架，由服务端提供
GEARMAN_HOST = '192.168.0.171'
GEARMAN_PORT = '4730'

# RPC远程调用，认证和端口配置
RPC_PWD = 'rpc'
RPC_PORT = 5555