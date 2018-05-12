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
        self.partition = partition.replace(hour=0, minute=0, second=0, microsecond=0)

    def set_partition(self, partition: str):
        """
        设置要新建的分区
        :param partition: 格式为"%Y%m%d"的日期字符串
        :return: None
        """
        self.partition = datetime.datetime.strptime(partition, "%Y%m%d")

    def get_month_list(self):
        """
        由于原始数据按月分区，所以要获取最近90天的数据，必须在最近四个月的分区里查询
        :return: 返回包含最近四个月份的列表，比如['2018_05','2018_04','2018_03','2018_02']
        """
        month_list = []
        for i in range(4):
            year = self.partition.year
            month = self.partition.month
            if month-i <= 0:
                month = month - i + 12
                year = year - 1
            else:
                month = month - i
            if month < 10:
                month = '0' + str(month)
            month_list.append(str(year) + "_" + str(month))
        return month_list

    def get_start_end_time(self):
        end_time = self.partition + datetime.timedelta(days=1)
        start_time = end_time + datetime.timedelta(days=-90)
        return 1000*start_time.timestamp(), 1000*end_time.timestamp()

    def do_calculate(self):
        """
        把sql_template中变量替换后，调用系统命令执行
        :return:
        """
        last_4_month = str(tuple(self.get_month_list()))
        start_time, end_time = self.get_start_end_time()
        value_replace_dic = {
            "v_last_4_months": last_4_month,
            "v_start_time": str(start_time),
            "v_end_time": str(end_time),
            "v_partition": str(self.partition.strftime("%Y%m%d"))
        }
        sql = CalDeviceData.sql_template
        for x, y in value_replace_dic.items():
            sql = sql.replace(x, y)
        print(sql)
        os.system('hive -e "%s"' % sql)


def main():
    test = CalDeviceData()
    for i in range(20180501, 20180506):
        test.set_partition(str(i))
        test.do_calculate()
    return


if __name__ == "__main__":
    main()
