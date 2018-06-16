forked from [HatBoy/RTask](https://github.com/HatBoy/RTask)

改动：  
1. 使用gearman作为分布式任务分发框架（原版使用Python+redis实现的任务队列）；  
2. 去掉了huey，原版使用huey是为了开启多进程，比如在节点A启动x个消费者，然后节点A产生x个任务，刚好让每个消费者执行一个任务，而这个任务是while True类型的，即每个消费者一直执行最初分配的任务，如果此时节点A在产生1个任务，就会没有消费者去执行这个任务，当然原版代码的逻辑不会让这种情况发生，这里例子只是为了说明huey并没有起到任务队列的作用，即使改动代码逻辑使huey起到任务队列的作用，也与gearman重复了，此处使用了gearman，因此huey去掉了，而直接采用subprocess在节点开启多进程，与原版效果一致，但代码逻辑更简洁明了；  
3. 严格区分开节点(node,原版是server)和监控端(server,原版是monitor)；  
4. 节点间可以执行不同的任务了，节点向服务器报告本节点所能执行的任务，服务端根据所有节点报告的任务类型分类提交任务队列。即假如有A、B两个节点，他们执行的任务是test_A,有C、D、E三个节点，他们执行的任务是test_B，服务端就可以分别提交x个test_A和y个test_B任务，gearman根据任务类型分发任务给对应的节点。  
5. 优化、精简代码