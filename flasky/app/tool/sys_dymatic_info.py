#! /usr/bin/env python
#encoding: utf-8

from __future__ import print_function
from sql import *
from datetime import datetime

#Time Setting
Time = 10


Receive_0 = 0.0
Send_0 = 0.0
write_size_0 = 0
read_size_0 = 0

Session = sessionmaker(bind=engine)
session = Session()

i=1
while 1:
    i+=1

    #内存信息
    from collections import OrderedDict

    Total_memory = 0
    Free_memory = 0
    Usingrate_0 = 0.0
    def meminfo():
        meminfo = OrderedDict()

        with open('/proc/meminfo') as f:
            for line in f:
                meminfo[line.split(':')[0]] = line.split(':')[1].strip()
        return meminfo

    if __name__ == '__main__':

        meminfo = meminfo()
        Tmemory=meminfo['MemTotal']
        Tmemory=Tmemory[:-3]
        Fmemory = meminfo['MemFree']
        Fmemory = Fmemory[:-3]
        Usingrate_0 = float((float(Tmemory) - int(Fmemory)) / int(Tmemory))*100
        Total_memory = int(Tmemory)
        Free_memory = int(Fmemory)
        Usingrate_0 = float(Usingrate_0)


    #网络信息
    from collections import namedtuple
    Receive = 0.0
    Send = 0.0
    def netdevs():
        with open('/proc/net/dev') as f:
            net_dump = f.readlines()

        device_data = {}
        data = namedtuple('data', ['rx', 'tx'])
        for line in net_dump[2:]:
            line = line.split(':')
            if line[0].strip() != 'lo':
                device_data[line[0].strip()] = data(float(line[1].split()[0]) / (1024.0 * 1024.0),
                                                    float(line[1].split()[8]) / (1024.0 * 1024.0))

        return device_data

    if __name__ == '__main__':

        netdevs = netdevs()
        ii=0
        for dev in netdevs.keys():
            if ii == 0 :
                Receive = float(netdevs[dev].rx)
                Send = float(netdevs[dev].tx)
            ii+=1

    #进程信息
    import os
    Process_cnt = 0
    def process_list():

        pids = []
        for subdir in os.listdir('/proc'):
            if subdir.isdigit():
                pids.append(subdir)

        return pids


    if __name__=='__main__':

        pids = process_list()
        Process_cnt = int(format(len(pids)))

    ##硬盘内存cpu使用率
    import os, time

    last_worktime = 0
    last_idletime = 0

    def get_cpu():
        global last_worktime, last_idletime
        f = open("/proc/stat", "r")
        line = ""
        while not "cpu " in line:
            line = f.readline()
        f.close()
        spl = line.split(" ")
        worktime = int(spl[2]) + int(spl[3]) + int(spl[4])
        idletime = int(spl[5])
        dworktime = (worktime - last_worktime)
        didletime = (idletime - last_idletime)
        rate = float(dworktime) / (didletime + dworktime)
        last_worktime = worktime
        last_idletime = idletime
        if (last_worktime == 0): return 0
        return rate


    statvfs = os.statvfs('/')
    total_disk_space = statvfs.f_frsize * statvfs.f_blocks
    free_disk_space = statvfs.f_frsize * statvfs.f_bfree
    disk_usage = (total_disk_space - free_disk_space) * 100.0 / total_disk_space
    disk_usage = float(disk_usage)
    disk_tip = "硬盘空间使用率（最大100%）："+str(disk_usage)+"%"
    Total_memory_1 = float(total_disk_space/1000000000.0)
    Free_memory_1 = float(free_disk_space / 1000000000.0)
    Usingrate_1 = float(disk_usage)


    cpu_usage = float(get_cpu()*100)
    cpu_tip = "CPU使用率（最大100%）："+str(cpu_usage)+"%"
    Usingrate_2 = float(cpu_usage)


    from collections import namedtuple

    Disk = namedtuple('Disk',
                      'major_number minor_number device_name read_count read_merged_count read_sections time_spent_reading write_count write_merged_count write_sections time_spent_write io_requests time_spent_doing_io weighted_time_spent_doing_do')


    def get_disk_info(device):
        with open('/proc/diskstats') as f:
            for line in f:
                if line.split()[2] == device:
                    return Disk(*line.split())
        raise RuntimeError('device ({0}) not found!'.format(device))


    write_cnt = 0
    write_size = 0
    write_time = 0
    read_cnt = 0
    read_size = 0
    read_time = 0
    def main():
        disk_info = get_disk_info('sda')
        global write_cnt
        write_cnt = int(format(disk_info.write_count))
        global write_size
        write_size = int(format(int(disk_info.write_sections) * 512))
        global write_time
        write_time = int(format(disk_info.time_spent_write))
        global read_cnt
        read_cnt = int(format(disk_info.read_count))
        global read_size
        read_size = int(format(int(disk_info.read_sections) * 512))
        global read_time
        read_time = int(format(disk_info.time_spent_reading))

    if __name__ == '__main__':
        main()

    import time

    #print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


    #print('总硬盘容量: %f G' % (Total_memory_1))
    #print('空闲硬盘容量: %f G' % (Free_memory_1))
    #print('硬盘使用率: %f %%' % (Usingrate_1))
    #print('网络接受流量: %f MiB' % (Receive))
    #print('网络发送流量: %f MiB' % (Send))


    #print('空闲内存: %d kB' %(Free_memory))
    #print('内存利用率: %f %%' % (Usingrate_0))
    #print('网络接受流量速度: %f M/s' % ((Receive - Receive_0) / Time))
    #print('网络发送流量速度: %f M/s' % ((Send - Send_0) / Time))
    #print('进程总数: %d ' % (Process_cnt))
    #print('cpu利用率: %f %%' % (Usingrate_2))
    #print('磁盘写速度: %f B/s' % ((write_size - write_size_0) * 1.0 / Time))
    #print('磁盘读速度: %f B/s' % ((read_size - read_size_0) * 1.0 / Time))


    newrecord = Sysinfo()
    newrecord.timestamp = date
    newrecord.mem_free = Free_memory
    newrecord.mem_used = Usingrate_0
    newrecord.net_reci = (Receive - Receive_0) / Time
    newrecord.net_send = (Send - Send_0) / Time
    newrecord.process = Process_cnt
    newrecord.cpu_used = Usingrate_2
    newrecord.disk_writ = (write_size - write_size_0) * 1.0 / Time
    newrecord.disk_read = (read_size - read_size_0) * 1.0 / Time

    session.add(newrecord)
    session.commit()


    Receive_0 = Receive
    Send_0 = Send
    write_size_0  =write_size
    read_size_0 = read_size

    time.sleep(Time)