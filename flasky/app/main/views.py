from flask import render_template, redirect, request, url_for, flash, Response

import json
from sqlalchemy import and_
from . import main
from datetime import datetime, timedelta, time
from ..models import User,Config,Sysinfo,Netflow
from ..tool.query_command import query_command
from ..tool.execute_command import FlowMonitorStart
from ..tool.shutdown_command import FlowMonitorShutdown
from ..tool.sys_static_info import call_sys_static

from .. import db

@main.route('/')
def index():
    return redirect(url_for('main.dashboard'))


@main.route('/dashboard')
def dashboard():
    flash('Welcome!')
    return render_template('dashboard.html')


@main.route('/system/overview')
def sysoverview():
    info_dict = call_sys_static()
    cpu_cores = len(info_dict['CPU_List'])
    Total_memory = info_dict['Total_Memory']
    Total_disk = info_dict['Total_Disc']
    memory_size = str (round(Total_memory*1.0 /1024 /1024,1))
    disk_size = str (int(Total_disk))
    cpu_rate = round(info_dict['CPU_Rate'],1)
    mem_rate = round(info_dict['Memory_Rate'],1)
    disk_rate = round(info_dict['Disk_Rate'], 1)

    return render_template('SystemOverview.html',info_dict=info_dict,cpu_cores=cpu_cores,memory_size=memory_size,
                           disk_size=disk_size,cpu_rate=cpu_rate,mem_rate=mem_rate,disk_rate=disk_rate)


@main.route('/system/CPU')
def syscpu():
    return render_template('SystemCPU.html')

@main.route('/system/CPUgraph_line/<int:token>')
def cpugraph_line(token):
    delta_time = 600
    if token == 2:
        delta_time = 3600
    if token == 3:
        delta_time = 3600*24

    agoTime = datetime.now() - timedelta(seconds=delta_time)

    info_list = Sysinfo.query.filter(Sysinfo.timestamp>=agoTime).all()
    data = []
    for item in info_list:
        dict_tmp = {}
        dict_tmp['name'] = item.timestamp.strftime("%H:%M:%S")
        dict_tmp['value'] = item.cpu_used
        data.append(dict_tmp)

    content = json.dumps(data)
    #resp = Response_headers(content)
    return Response(content)

@main.route('/system/CPUgraph_pie')
def cpugraph_pie():

    data = []
    info_dict = call_sys_static()

    dict_tmp = {}
    dict_tmp['name'] = 'Used'
    dict_tmp['value'] = round(info_dict['CPU_Rate'],2)
    data.append(dict_tmp)

    dict_tmp = {}
    dict_tmp['name'] = 'Free'
    dict_tmp['value'] = 100 - round(info_dict['CPU_Rate'], 2)
    data.append(dict_tmp)

    content = json.dumps(data)
    #resp = Response_headers(content)
    return Response(content)



@main.route('/system/Memory')
def sysmemory():
    return render_template('SystemMemory.html')


@main.route('/system/Disk')
def sysdisk():
    return render_template('SystemDisk.html')


@main.route('/system/Network')
def sysnetwork():
    return render_template('SystemNetwork.html')


@main.route('/detector/overview')
def detoverview():
    return render_template('DetectorOverview.html')


@main.route('/detector/source')
def detsource():
    return render_template('DetectorSource.html')


@main.route('/detector/connection')
def detconnection():
    return render_template('DetectorConnection.html')


@main.route('/detector/flow')
def detflow():
    return render_template('DetectorFlow.html')


@main.route('/setting')
def setting():
    json_list = query_command()
    json_list = json.loads(json_list)
    UseId = Config.query.filter_by(key='NowUseInterface').first()
    if UseId != None:
        UseId = int (UseId.value)
    #print UseId
    start = Config.query.filter_by(key='IsStart').first()
    #print start
    warninginfo = request.args.get("warninginfo")
    successinfo = request.args.get("successinfo")
    return render_template('Setting.html',start=start,json_list=json_list,UseId=UseId,warning_message=warninginfo,success_message=successinfo)


@main.route('/change_interface/<token>')
def change_interface(token):
    NUI = Config.query.filter_by(key='NowUseInterface').first()
    if NUI == None:
        NUI = Config()
        NUI.key='NowUseInterface'
    NUI.value = token
    db.session.add(NUI)
    db.session.commit()
    warninginfo = ' Monitor will only start after manual restart!'
    return redirect(url_for('main.setting',warninginfo=warninginfo))


@main.route('/monitor_start')
def monitor_start():
    successinfo = ' Monitor has been started!'
    warninginfo = ' ERROR!'
    NUI = Config.query.filter_by(key='NowUseInterface').first()
    if NUI != None:
        value = int (NUI.value)
        FlowMonitorStart(value)

        start = Config.query.filter_by(key='IsStart').first()
        if start == None:
            start = Config()
            start.key='IsStart'
            start.value='S'
            db.session.add(start)
            db.session.commit()

        return redirect(url_for('main.setting', successinfo=successinfo))
    return redirect(url_for('main.setting', warninginfo=warninginfo))


@main.route('/monitor_restart')
def monitor_restart():
    successinfo = ' Monitor has been restarted!'
    warninginfo = ' ERROR!'
    NUI = Config.query.filter_by(key='NowUseInterface').first()
    if NUI != None:
        value = int(NUI.value)
        FlowMonitorStart(value)

        start = Config.query.filter_by(key='IsStart').first()
        if start == None:
            start = Config()
            start.key='IsStart'
            start.value='R'
            db.session.add(start)
            db.session.commit()

        return redirect(url_for('main.setting', successinfo=successinfo))
    return redirect(url_for('main.setting', warninginfo=warninginfo))


@main.route('/monitor_shutdown')
def monitor_shutdown():
    successinfo = ' Monitor has been shutdown!'
    FlowMonitorShutdown()

    start = Config.query.filter_by(key='IsStart').first()
    if start != None:
        db.session.delete(start)
        db.session.commit()

    return redirect(url_for('main.setting', successinfo=successinfo))

@main.route('/drop_data')
def drop_data():
    FlowMonitorShutdown()
    NetflowList = Netflow.query.all()
    SysinfoList = Sysinfo.query.all()
    for item in NetflowList:
        db.session.delete(item)
    for item in SysinfoList:
        db.session.delete(item)
    db.session.commit()
    successinfo = ' Data has been cleaned!'
    return redirect(url_for('main.setting', successinfo=successinfo))