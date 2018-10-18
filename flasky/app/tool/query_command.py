import subprocess
import json
from config import dir_path


def query_command():
    #answer = os.system('sudo /home/centos/kdd99_feature_extractor/build/src/kdd99extractor -l')
    #answer.readlines()
    #dir_path = '/home/centos/kdd99_feature_extractor/build/src/kdd99extractor'
    lines = subprocess.Popen('sudo ' + dir_path + ' -l',shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

    #print type(answer)
    interface_list=[]

    for line in lines.stdout.readlines():
        if line == "\n":
            break
        line = line.replace("\n","")
        line = line.replace(". ","\t")
        #line = line.replace(" ", "")
        list = line.split('\t')
        for idx,item in enumerate(list):
            #print type(item)
            list[idx] = item.rstrip()
            #item='das'
        item_dict = {}
        item_dict['id'] = int(list[0])
        item_dict['info'] = list[1]
        item_dict['name'] = list[2]
        interface_list.append(item_dict)
        #print list
    json_list = json.dumps(interface_list)
    #print json_list
    return json_list

# query_command()