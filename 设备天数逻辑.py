# import time
# import os
# from datetime import datetime, timedelta
#
# def get_last_4_months():
#     """
#     由于useractionlog2是按月分区，最近90天的记录需要从最近四个月的日志里提取
#     这个函数返回最近四个月的月份列表
#     """
#     month_list = []
#     for i in range(4):
#         month = int(time.strftime("%m", time.localtime()))
#         last_month = (month-i+12)%12
#         year = int(time.strftime("%Y", time.localtime()))
#         year = str(year if month>=last_month else year-1)
#         if last_month < 10:
#             last_month = '0'+str(last_month)
#         month_list.append(year+"_"+last_month)
#     return str(tuple(month_list))
#
# def get_start_end_time():
#     """
#     返回最近90天的起始时间点的整型值，由于useractionlog2中时间单位是ms，所以这里返回的时间值也转换为ms
#     partition为要插入的表的分区
#     """
#     now = datetime.now()
#     temp = (now-timedelta(days=90)).strftime("%Y-%m-%d 00:00:00")
#     start_time = (datetime.strptime(temp, "%Y-%m-%d %H:%M:%S")).timestamp()
#
#     temp = now.strftime("%Y-%m-%d 00:00:00")
#     end_time = (datetime.strptime(temp, "%Y-%m-%d %H:%M:%S")).timestamp()
#     partition = (now-timedelta(days=1)).strftime("%Y%m%d")
#     return 1000*int(start_time), 1000*int(end_time), partition
#
# def main():
#     last_4_months = get_last_4_months()
#     start_time, end_time, partition = get_start_end_time()
#
#     """
#     sql的查询逻辑：
#     1.先从useractionlog2提取到最近90天用户的行为日志，并将时间转换为日
#     2.统计每个uid在device_id上登录的天数
#     """
#     sql_template = \
#     '''
#     insert overwrite table device_data partition(dt='v_partition')
#     SELECT deviceid AS device_id,
#             uid,
#             count(distinct date_day) AS dev_uid_days_in_90
#     FROM
#         (SELECT DISTINCT deviceid,
#             uid,
#             date_sub(from_unixtime(cast(round(adjusttime/1000) AS bigint)),
#             10) AS date_day
#         FROM useractionlog2
#         WHERE month IN v_last_4_months
#                 AND adjusttime >= v_start_time
#                 AND adjusttime < v_end_time
#                 AND length(deviceid)>0) AS t
#     GROUP BY  deviceid, uid
#     '''
#     value_replace_dic = {"v_last_4_months": last_4_months, "v_start_time": str(start_time), "v_end_time": str(end_time), "v_partition": partition}
#     for x,y in value_replace_dic.items():
#         sql_template = sql_template.replace(x,y)
#     os.system('hive -e "%s"' % sql_template)
#     return 0


import os
import datetime


class CalDeviceData(object):
    sql_template = \
        '''
        insert overwrite table device_data partition(dt='v_partition')
        SELECT deviceid AS device_id,
                uid,
                count(distinct date_day) AS dev_uid_days_in_90
        FROM 
            (SELECT DISTINCT deviceid,
                uid,
                date_sub(from_unixtime(cast(round(adjusttime/1000) AS bigint)),
                10) AS date_day
            FROM useractionlog2
            WHERE month IN v_last_4_months
                    AND adjusttime >= v_start_time
                    AND adjusttime < v_end_time
                    AND length(deviceid)>0) AS t
        GROUP BY  deviceid, uid 
        '''

    def __init__(self, partition=datetime.datetime.today()+datetime.timedelta(days=-1)):
        #self.date_preset: datetime.date
        self.partition = partition

    #def get_month_list(self):
        #month_list = []
        #for i in range(4):
            # datetime.datetime.strptime(self.date_preset, "%Y-%m-%d") + datetime.timedelta(month)
            # month = datetime.datetime.strptime(, "%Y_%m")
            # month_list.append(month)
        #return month_list

    def get_start_end_time(self):
        return

    def set_partition(self, partition: str):
        """
        :param partition: 格式为"%Y%m%d"的日期字符串
        :return: None
        """
        self.partition = datetime.datetime.strptime(partition, "%Y%m%d")

    def do_calculate(self):
        return


def main():
    test = CalDeviceData()
    #test.set_partition()
    print(test.partition)
    return


if __name__ == "__main__":
    main()
