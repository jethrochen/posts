昨天在服务器上跑了个脚本，然后希望没天定时执行，于是加进了crontab，然而crontab并没有成功执行。  
究其原因，是因为crontab和终端bash所用的环境变量不是同一个，导致脚本中调用的命令crontab找不到。  
解决方案：在crontab中加入相应的环境配置
```bash
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/home/ubuntu/data/hive-2.1/bin:/home/ubuntu/data/hadoop-2.6.4/bin:/home/ubuntu/data/hadoop-2.6.4/sbin:/home/ubuntu/data/hbase-1.2.5/bin
```