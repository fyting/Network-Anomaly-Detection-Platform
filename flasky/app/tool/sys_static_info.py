#! /usr/bin/env python
#encoding: utf-8
from collections import OrderedDict
import os, time
#from __future__ import print_function

def meminfoF():
    ''' Return the information in /proc/meminfo
    as a dictionary '''
    meminfo = OrderedDict()

    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo

def call_sys_static():
    ##cpu处理器信息
    list = []

    with open('/proc/cpuinfo') as f:
        for line in f:
            # Ignore the blank line separating the information between
            # details about two processing units
            if line.strip():
                if line.rstrip('\n').startswith('model name'):
                    model_name = line.rstrip('\n').split(':')[1]
                    list.append(model_name)

    #内存信息

    Total_memory = 0



        # print(meminfo())

    meminfo = meminfoF()
    Tmemory = meminfo['MemTotal']
    Tmemory = Tmemory[:-3]
    Total_memory = int(Tmemory)


    statvfs = os.statvfs('/')
    total_disk_space = statvfs.f_frsize * statvfs.f_blocks
    free_disk_space = statvfs.f_frsize * statvfs.f_bfree
    disk_usage = (total_disk_space - free_disk_space) * 100.0 / total_disk_space
    disk_usage = float(disk_usage)
    Total_memory_1 = float(total_disk_space/1000000000.0)
    Free_memory_1 = float(free_disk_space / 1000000000.0)
    Usingrate_1 = float(disk_usage)

    #print(list)
    #print('总内存: %d kB' % (Total_memory))
    #print('总硬盘容量: %f G' % (Total_memory_1))
    #print('空闲硬盘容量: %f G' % (Free_memory_1))
    #print('硬盘使用率: %f %%' % (Usingrate_1))

    dict_static = {}
    dict_static['CPU_List'] = list
    dict_static['Total_Memory'] = Total_memory
    dict_static['Total_Disc'] = Total_memory_1
    dict_static['Free_Disc'] = Free_memory_1
    dict_static['Disc_rate'] = Usingrate_1

    return dict_static


if __name__ == '__main__':
    call_sys_static()