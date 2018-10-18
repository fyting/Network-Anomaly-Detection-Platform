#coding:utf-8
import time,os
from datetime import datetime
from sql import *
import scipy.io as scio
from numpy import *
from config import flow_file_location,abs_path

HttpRetType = ['REJ','RSTO','SF','S0']

dataCovariance = {}
dataAverage = {}
dataDecIndex = {}
dataE = {}


#Data should be at the same folder.

AverageStr = 'average_vector.mat'
CovarianceStr = 'covariance_matrix.mat'
DecIndexStr = 'dec_index.mat'
EStr = 'e.mat'

for flagtype in HttpRetType:
    FilePrefix = abs_path + 'matData/' + flagtype + '/' + flagtype + '_'

    dataCovariance[flagtype] = scio.loadmat(FilePrefix + CovarianceStr)['covariance_matrix']
    dataAverage[flagtype] = scio.loadmat(FilePrefix + AverageStr)['average_vector']
    dataDecIndex[flagtype] = scio.loadmat(FilePrefix + DecIndexStr)['dec_index']
    dataE[flagtype] = scio.loadmat(FilePrefix + EStr)['e']

    #print dataCovariance[flagtype]



FeatureUsed = [1,5,6,10,11,12,13,14,15,17,18,19,20,22,23,24,25,26,27,28]

Session = sessionmaker(bind=engine)
session = Session()


# location = session.query(Config).fliter_by(name = 'FlowFileLocation').first()
# if location == None:
#     location = '/home/centos/kdd99_feature_extractor/build/src/a.txt'
# else:
#     location = location.value

#This should be changed in practice use. Or get from database or config file.
#flow_file_location = '/home/centos/kdd99_feature_extractor/build/src/a.txt'


f = open(flow_file_location,'r')
countline = 0


print 'Work now starts. It is:',time.asctime( time.localtime(time.time()) )

while 1:
    line = f.readline()
    if line == None or line=='':
        print 'Finish work num:', -countline
        if countline < 0:
            countline = 0
        print 'No work to do. It is:',time.asctime( time.localtime(time.time()) )
        print 'Now sleeping ...'
        time.sleep(10)
    else:
        countline -= 1
        if countline > 0:# ignore first 150 connection(not exsist forward-relationship)
            continue

        #print line
        datalist = line.split(',')
        #print datalist.__len__()

        NewRecord = Netflow()
        NewRecord.f1 = float(datalist[0])
        NewRecord.f2 = datalist[1]
        NewRecord.f3 = datalist[2]
        NewRecord.f4 = datalist[3]
        NewRecord.f5 = float(datalist[4])
        NewRecord.f6 = float(datalist[5])
        NewRecord.f7 = float(datalist[6])
        NewRecord.f8 = float(datalist[7])
        NewRecord.f9 = float(datalist[8])

        NewRecord.f23 = float(datalist[9])
        NewRecord.f24 = float(datalist[10])
        NewRecord.f25 = float(datalist[11])
        NewRecord.f26 = float(datalist[12])
        NewRecord.f27 = float(datalist[13])
        NewRecord.f28 = float(datalist[14])
        NewRecord.f29 = float(datalist[15])
        NewRecord.f30 = float(datalist[16])
        NewRecord.f31 = float(datalist[17])

        NewRecord.f32 = float(datalist[18])
        NewRecord.f33 = float(datalist[19])
        NewRecord.f34 = float(datalist[20])
        NewRecord.f35 = float(datalist[21])
        NewRecord.f36 = float(datalist[22])
        NewRecord.f37 = float(datalist[23])
        NewRecord.f38 = float(datalist[24])
        NewRecord.f39 = float(datalist[25])
        NewRecord.f40 = float(datalist[26])
        NewRecord.f41 = float(datalist[27])

        NewRecord.fromIP = datalist[28]
        NewRecord.fromPort = int(datalist[29])
        NewRecord.toIP = datalist[30]
        NewRecord.toPort = int(datalist[31])

        NewRecord.timestamp = datalist[32]

        if datalist[2]=='http':
            #print datalist
            flagtype = datalist[3]
            if flagtype == 'SF' or flagtype == 'OTH' or flagtype == 'SH' or flagtype == 'RSTR':
                flagtype = 'SF'
            if flagtype == 'REJ':
                flagtype = 'REJ'
            if flagtype == 'RSTO' or flagtype == 'RSTOS0':
                flagtype = 'RSTO'
            if flagtype == 'S0' or flagtype == 'S1' or flagtype == 'S2' or flagtype == 'S3':
                flagtype = 'S0'

            datalist[23] = 0 #ERROR Happen in this Feature,force to fix

            X_former = []
            for i in FeatureUsed:
                if i<=6:
                    X_former.append(float(datalist[i-1]))
                elif i==19 or i==20:
                    X_former.append(math.log(256.0-float(datalist[i - 1])))
                else:
                    X_former.append(math.log(float(datalist[i-1])+1.0))

            #???
            #X_former[11] = 1
            #X_former[12] = 1

            #print X_former
            #input()
            dataDecList = dataDecIndex[flagtype][:,0].tolist()
            # print type(dataDecList)
            n_size = float (len(dataDecList))
            #print n_size

            X_dec = []
            for i in dataDecList:
                X_dec.append(X_former[i-1])

            #X_dec[15] = 0
            #X_dec[10] = 0
            #X_dec[3] = X_dec[4] = 17
            #X_dec[11] = 256 - 74
            #X_dec[12] = 256 - 209
            #X_dec[1] = 256
            #X_dec[2] = 1273

            #print X_dec
            #input()

            X_mat = mat(X_dec)
            #print X_mat
            #print 'A',dataAverage[flagtype]
            X_mat = X_mat - dataAverage[flagtype]
            #print 'E',X_mat
            #print X_mat
            Cov_mat = mat(dataCovariance[flagtype])
            #print Cov_mat

            exp_value = X_mat * Cov_mat.I * X_mat.T * -1/2
            #print exp_value[0,0]

            #print linalg.det(Cov_mat)
            px = math.exp(exp_value[0,0]) / math.pow(2 * math.pi, n_size / 2) / math.pow(linalg.det(Cov_mat),0.5)
            #print px,dataE[flagtype][0,0]
            if px > dataE[flagtype][0,0]:
                is_error = False
            else:
                is_error = True
            #print is_error,datalist[3]

            NewRecord.evalue = px
            NewRecord.error = is_error
        session.add(NewRecord)
        session.commit()
        #while 1:
        #    1


f.close()