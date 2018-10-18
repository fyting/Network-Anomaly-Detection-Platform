import subprocess,time
import os
from config import dir_path,flow_file_location, kill_file_location,abs_path

def FlowMonitorStart(interfaceid):
    #kill process if exsist

    abspath = abs_path
    #print abspath
    ans = subprocess.Popen("cat " + abspath + "save_pid.txt",
                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #print ans.stdout.readlines()[0]
    pid = ans.stdout.readlines()[0]

    ans = subprocess.Popen("kill -9 " + pid,
                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #print "kill -9 'cat " + abspath + "save_pid.txt' "
    #print ans.stdout.readlines()

    ans = subprocess.Popen("rm " + abspath + "save_pid.txt",
                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


    ans = subprocess.Popen("cat " + abspath + "save_pid2.txt",
                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #print ans.stdout.readlines()[0]
    pid = ans.stdout.readlines()[0]

    ans = subprocess.Popen("kill -9 " + pid,
                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #print "kill -9 'cat " + abspath + "save_pid.txt' "
    #print ans.stdout.readlines()

    ans = subprocess.Popen("rm " + abspath + "save_pid2.txt",
                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


    #print "rm " + abspath + "save_pid.txt"
    #print ans.stdout.readlines()


    #print ans.stdout.readlines()




    ans = subprocess.Popen(' sudo ' + kill_file_location,
                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #print ans.stdout.readlines()
    #empty flow file
    ans = subprocess.Popen(' ""> ' + flow_file_location,
                        shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    #print ans.stdout.readlines()
    #Start
    time.sleep(1)
    subprocess.Popen('nohup sudo ' + dir_path + ' -i ' + str(interfaceid) + ' -e >>' + flow_file_location + ' &',
                     shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

    print 'nohup sudo ' + dir_path + ' -i ' + str(interfaceid) + ' -e >>' + flow_file_location + ' &'
    #Start Catch

    #abspath = '/home/centos/netflow/'
    subprocess.Popen(
        'nohup python ' + abspath + 'catch_data.py 1>' + abspath + 'catch.log & echo $! > ' + abspath + 'save_pid.txt',
        shell=True)

    subprocess.Popen(
        'nohup python ' + abspath + 'sys_dymatic_info.py 1>' + abspath + 'sysinfo.log & echo $! > ' + abspath + 'save_pid2.txt',
        shell=True)


    print 'nohup python ' + abspath + 'sys_dymatic_info.py 1>' + abspath + 'sysinfo.log & echo $! > ' + abspath + 'save_pid2.txt'
    #print ans.stdout.readlines()

if __name__ == '__main__':
    FlowMonitorStart(6)