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
dtErr = 0
rfErr = 0
svmErr = 0
gnbErr =0
lrErr = 0 

for i in range(len(Ifeat)):
	X = Ifeat[0:i] + Ifeat[i+1:]
	Y = Ilabel[0:i] + Ilabel[i+1:]
	#DT
	dt = tree.DecisionTreeClassifier()
	dt = dt.fit(X, Y)
	dtPred = dt.predict([Ifeat[i]])
	dtErr += (Ilabel[i] != dtPred)
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != dtPred).sum()))


	#RF	
	rf = ensemble.RandomForestClassifier()
	rf = rf.fit(X, Y)
	rfPred = rf.predict([Ifeat[i]])
	rfErr += (Ilabel[i] != rfPred)
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != rfPred).sum()))

	#SVM
	s1 = svm.SVC()
	svmFit = s1.fit(X,Y)
	svmPred = s1.predict([Ifeat[i]])
	svmErr += (Ilabel[i] != svmPred)
	#print svmPred
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != svmPred).sum()))

	#NB
	gnb = naive_bayes.GaussianNB()
	gnb = gnb.fit(X,Y)
	gnbPred = gnb.predict([Ifeat[i]])
	gnbErr += (Ilabel[i] != gnbPred)
	#print gnbPred
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != gnbPred).sum()))

	#LR
	lr = linear_model.LogisticRegression()
	lr = lr.fit(X,Y)
	lrPred = gnb.predict([Ifeat[i]])
	lrErr += (Ilabel[i] != lrPred)
	#print lrPred

#print dtErr, type(dtErr)
dtRate = float(dtErr)/len(Ifeat) 
rfRate = float(rfErr)/len(Ifeat)
svmRate = float(svmErr)/len(Ifeat)
gnbRate = float(gnbErr)/len(Ifeat)
lrRate = float(lrErr)/len(Ifeat)	

print "dtRate: " + str(dtRate) + " rfRate: " + str(rfRate) + " svmRate: " + str(svmRate) + " gnbRate: " + str(gnbRate) + " lrRate: " + str(lrRate)

