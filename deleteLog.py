import os
import time
import operator  # 用于list排序
import schedule  # 用于轻量级定时任务


def timestamp_to_time(timestamp):
    '''时间戳转换为时间'''
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def _traversal(source_path):
    '''文件夹的遍历
    source_path 需要遍历的文件夹路径

    返回一个文件夹内所有文件的list
    以文件名为主、创建日记为次进行排序

    文件路径， 文件名， 文件类型， 创建日期
    '''
    return_list = []
    for dirpath, dirnames, filenames in os.walk(source_path):
        for item in filenames:
            find_file_path = os.path.join(dirpath, item)  # 获取文件路径
            filename, filetype = os.path.splitext(item)  # 分析文件名和文件类型
            tiemstamp = os.path.getmtime(find_file_path)  # 获得文件创建的时间戳
            fileCreateTime = timestamp_to_time(tiemstamp)  # 获取文件创建时间

            tempTuple = (find_file_path, filename, filetype,
                         fileCreateTime, tiemstamp)  # 拼接起来放入元组中
            return_list.append(tempTuple)  # 将文件数据的元组放入list中，等待后续处理

    return return_list


def main(path):
    '''定期删除日志'''
    print("执行时间：" + timestamp_to_time(time.time()))

    tempList = _traversal(path)

    # 输出测试，用于观察所有数据
    tempList.sort(key=operator.itemgetter(1, 3))  # 以文件名为主、创建日记为次进行排序
    for item in tempList:
        print(item[:3])

    tempList.sort(key=operator.itemgetter(3), reverse=True)  # 按时间进行升序排序

    # 输出测试，用于观察数据
    # for item in tempList:
    #   print(item[3])  # 观察时间排序
    # print(tempList[0][3])  # 观察最新的时间

    # 时间戳计算 3天 -> 3 * 24 * 60 * 60 = 259200
    for item in tempList:
        if int(item[4]) < (int(tempList[0][4])-259200):
            print("删除：" + item[0])
            os.remove(item[0])

    print("任务执行一次结束")
    # input()

def test(text_str):
    print("test：" + timestamp_to_time(time.time()) + "--" + text_str)

if __name__ == '__main__':
    print("定时任务开启：" + timestamp_to_time(time.time()))

    schedule.every().day.at("9:00").do(main, "./logs/")  # 定时每天9点开始
    schedule.every().hour.do(test,"测试,进程还活着")  # 每小时进行测试
    
    # main("./logs/")

    while True:
        schedule.run_pending()
        time.sleep(10)  # 10秒检测一次任务