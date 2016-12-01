import py_stringmatching as ps
import csv
from datetime import datetime, date
from sklearn import tree, ensemble, svm, naive_bayes, linear_model #.RandomForestClassifier


timeObj1=datetime.strptime('03:55', '%M:%S').time()
timeObj2 = datetime.strptime('04:55', '%M:%S').time()
print max(timeObj1,timeObj2), datetime.combine(date.today(), max(timeObj1,timeObj2)) - datetime.combine(date.today(), min(timeObj1,timeObj2))

#Reading every row of csv into a list
f = open('SampledData.csv','rb')
csvRead = csv.reader(f,delimiter=',')
sampledList = []
for row in csvRead:
	row[0] = int(row[0])
	row[-1] = int(row[-1])
	timeObj1=datetime.strptime(row[6].strip(), '%M:%S').time()
	row[6] = timeObj1
	timeObj1=datetime.strptime(row[10].strip(), '%M:%S').time()
	row[10] = timeObj1
	
	#l.append(line[:-1])
	sampledList.append(row)
	#print row
f.close()

#print row[6]
#print max(row[6],row[10])

#print sampledList

#Converting every row to feature vector
featList = []
label = []
for item in sampledList:
	#print item
	fi = []
	
	jaro1 = ps.Jaro()
	f1 = jaro1.get_raw_score(item[3],item[7])#Artist- 3,7 - Jaro
	
	jaro2 = ps.Jaro()
	f2 = jaro1.get_raw_score(item[4],item[8])#Trackname -4,8 - Jaro
	
	jaro3 = ps.Jaro()
	f3 = jaro1.get_raw_score(item[5],item[9])#Released Date - 5,9 - Jaro
	
	timeObj3 = datetime.strptime('00:00', '%M:%S').time()
	#print timeObj3 #, item 
	f4 = (datetime.combine(date.today(), max(item[6],item[10])) - datetime.combine(date.today(), min(item[6],item[10]))).total_seconds()#Time -6,10 - diff/max	
	f4de =(datetime.combine(date.today(), max(item[6],item[10])) - datetime.combine(date.today(), timeObj3)).total_seconds()
	f4/= f4de
	#print f4 
	#sampledList[item]
	
	fi.append(f1)
	fi.append(f2)
	fi.append(f3)
	fi.append(f4)
	label.append(item[-1])
	featList.append(fi)
	
	
#print featList
#print label	

#H = featList
Ifeat = featList[0:300]
#U = Ifeat[0:150]
#V = Ifeat[150:-1]
Jfeat = featList[300:-1]
Ilabel = label[0:300]
#Ulabel = Ilabel[0:150]
#Vlabel = Ilabel[150:-1]
Jlabel = label[300:-1]

#print Ifeat
#print len(Ilabel)
# dtErr = 0
# rfErr = 0
# svmErr = 0
# gnbErr =0
# lrErr = 0

dtTp = 0.0
dtFp = 0.0
dtFn = 0.0
rfTp = 0.0
rfFp = 0.0
rfFn = 0.0
svmTp = 0.0
svmFp = 0.0
svmFn = 0.0
gnbTp = 0.0
gnbFp = 0.0
gnbFn = 0.0
lrTp = 0.0
lrFp = 0.0
lrFn = 0.0



for i in range(len(Ifeat)):
	X = Ifeat[0:i] + Ifeat[i+1:]
	Y = Ilabel[0:i] + Ilabel[i+1:]
	#DT
	dt = tree.DecisionTreeClassifier()
	dt = dt.fit(X, Y)
	dtPred = dt.predict([Ifeat[i]])
	if dtPred == Ilabel[i]:
		dtTp += 1
	elif dtPred == 1:
		dtFp += 1
	else:
		dtFn += 1
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != dtPred).sum()))


	#RF	
	rf = ensemble.RandomForestClassifier()
	rf = rf.fit(X, Y)
	rfPred = rf.predict([Ifeat[i]])
	if rfPred == Ilabel[i]:
		rfTp += 1
	elif rfPred == 1:
		rfFp += 1
	else:
		rfFn += 1
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != rfPred).sum()))

	#SVM
	s1 = svm.SVC()
	svmFit = s1.fit(X,Y)
	svmPred = s1.predict([Ifeat[i]])
	if svmPred == Ilabel[i]:
		svmTp += 1
	elif svmPred == 1:
		svmFp += 1
	else:
		svmFn += 1
	#print svmPred
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != svmPred).sum()))

	#NB
	gnb = naive_bayes.GaussianNB()
	gnb = gnb.fit(X,Y)
	gnbPred = gnb.predict([Ifeat[i]])
	if gnbPred == Ilabel[i]:
		gnbTp += 1
	elif gnbPred == 1:
		gnbFp += 1
	else:
		gnbFn += 1
	#print gnbPred
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != gnbPred).sum()))

	#LR
	lr = linear_model.LogisticRegression()
	lr = lr.fit(X,Y)
	lrPred = gnb.predict([Ifeat[i]])
	if lrPred == Ilabel[i]:
		lrTp += 1
	elif lrPred == 1:
		lrFp += 1
	else:
		lrFn += 1
	#print lrPred

#print dtErr, type(dtErr)
# dtRate = float(dtErr)/len(Ifeat)
# rfRate = float(rfErr)/len(Ifeat)
# svmRate = float(svmErr)/len(Ifeat)
# gnbRate = float(gnbErr)/len(Ifeat)
# lrRate = float(lrErr)/len(Ifeat)

dtPrecision = dtTp / (dtTp + dtFp)
dtRecall = dtTp / (dtTp + dtFn)
dtF1Score = 2 * (dtPrecision * dtRecall) / (dtPrecision + dtRecall)

rfPrecision = rfTp / (rfTp + rfFp)
rfRecall = rfTp / (rfTp + rfFn)
rfF1Score = 2 * (rfPrecision * rfRecall) / (rfPrecision + rfRecall)

svmPrecision = svmTp / (svmTp + svmFp)
svmRecall = svmTp / (svmTp + svmFn)
svmF1Score = 2 * (svmPrecision * svmRecall) / (svmPrecision + svmRecall)

gnbPrecision = gnbTp / (gnbTp + gnbFp)
gnbRecall = gnbTp / (gnbTp + gnbFn)
gnbF1Score = 2 * (gnbPrecision * gnbRecall) / (gnbPrecision + gnbRecall)

lrPrecision = lrTp / (lrTp + lrFp)
lrRecall = lrTp / (lrTp + lrFn)
lrF1Score = 2 * (lrPrecision * lrRecall) / (lrPrecision + lrRecall)

print "dtPrecision: " + str(dtPrecision) + "dtRecall: " + str(dtRecall) + "dtF1: " + str(dtF1Score)
print "rfPrecision: " + str(rfPrecision) + "rfRecall: " + str(rfRecall) + " rfF1: " + str(rfF1Score)
print "svmPrecision: " + str(svmPrecision) + "svmRecall: " + str(svmRecall) + " svmF1: " + str(svmF1Score)
print "gnbPrecision: " + str(gnbPrecision) + "gnbRecall: " + str(gnbRecall) + " gnbF1: " + str(gnbF1Score)
print "lrPrecision: " + str(lrPrecision) + "lrRecall: " + str(lrRecall) + " lrF1: " + str(lrF1Score)

