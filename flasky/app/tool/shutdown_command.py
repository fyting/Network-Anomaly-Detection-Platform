import subprocess,time
import os
from config import dir_path,flow_file_location, kill_file_location,abs_path

def FlowMonitorShutdown():
    #kill process if exsist

    abspath = abs_path
    #print abspath
    ans = subprocess.Popen("cat " + abspath + "save_pid.txt",
                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #print ans.stdout.readlines()[0]
    pid = ans.stdout.readlines()[0]

    ans = subprocess.Popen("kill -9 " + pid,
                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print "kill -9 'cat " + abspath + "save_pid.txt' "
    #print ans.stdout.readlines()

    ans = subprocess.Popen("rm " + abspath + "save_pid.txt",
                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #print "rm " + abspath + "save_pid.txt"
    #print ans.stdout.readlines()


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



    #print ans.stdout.readlines()




    ans = subprocess.Popen(' sudo ' + kill_file_location,
                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #print ans.stdout.readlines()
    #empty flow file
    ans = subprocess.Popen(' ""> ' + flow_file_location,
                        shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    #print ans.stdout.readlines()
    #Start

if __name__ == '__main__':
    FlowMonitorShutdown()