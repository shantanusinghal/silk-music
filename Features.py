import py_stringmatching as ps
import csv
from datetime import datetime, date
from sklearn import tree, ensemble, svm, naive_bayes, linear_model #.RandomForestClassifier
import time

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

dtTP = 0
dtFP = 0
dtFN = 0

rfTP = 0
rfFP = 0
rfFN = 0
 
svmTP = 0
svmFP = 0
svmFN = 0

gnbTP = 0
gnbFP = 0
gnbFN = 0 

lrTP = 0
lrFP = 0
lrFN = 0 


for i in range(len(Ifeat)):
	X = Ifeat[0:i] + Ifeat[i+1:]
	Y = Ilabel[0:i] + Ilabel[i+1:]
	#DT
	dt = tree.DecisionTreeClassifier()
	dt = dt.fit(X, Y)
	dtPred = dt.predict([Ifeat[i]])
	dtErr += (Ilabel[i] != dtPred)
	if dtPred == 1 and Ilabel[i] == 1:
		dtTP += 1
	if dtPred ==1 and Ilabel[i] == 0:
		dtFP += 1
	if dtPred == 0 and Ilabel[i] ==1:
		dtFN += 1
		
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != dtPred).sum()))


	#RF	
	rf = ensemble.RandomForestClassifier()
	rf = rf.fit(X, Y)
	rfPred = rf.predict([Ifeat[i]])
	rfErr += (Ilabel[i] != rfPred)
	if rfPred == 1 and Ilabel[i] == 1:
		rfTP += 1
	if rfPred ==1 and Ilabel[i] == 0:
		rfFP += 1
	if rfPred == 0 and Ilabel[i] ==1:
		rfFN += 1
		
	
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != rfPred).sum()))

	#SVM
	s1 = svm.SVC()
	svmFit = s1.fit(X,Y)
	svmPred = s1.predict([Ifeat[i]])
	svmErr += (Ilabel[i] != svmPred)
	if svmPred == 1 and Ilabel[i] == 1:
		svmTP += 1
	if svmPred ==1 and Ilabel[i] == 0:
		svmFP += 1
	if svmPred == 0 and Ilabel[i] ==1:
		svmFN += 1
		
	
	
	#print svmPred
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != svmPred).sum()))

	#NB
	gnb = naive_bayes.GaussianNB()
	gnb = gnb.fit(X,Y)
	gnbPred = gnb.predict([Ifeat[i]])
	gnbErr += (Ilabel[i] != gnbPred)
	if gnbPred == 1 and Ilabel[i] == 1:
		gnbTP += 1
	if gnbPred ==1 and Ilabel[i] == 0:
		gnbFP += 1
	if gnbPred == 0 and Ilabel[i] ==1:
		gnbFN += 1
	
	#print gnbPred
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != gnbPred).sum()))

	#LR
	lr = linear_model.LogisticRegression()
	lr = lr.fit(X,Y)
	lrPred = gnb.predict([Ifeat[i]])
	lrErr += (Ilabel[i] != lrPred)
	if lrPred == 1 and Ilabel[i] == 1:
		lrTP += 1
	if lrPred ==1 and Ilabel[i] == 0:
		lrFP += 1
	if lrPred == 0 and Ilabel[i] ==1:
		lrFN += 1
	#print lrPred

# The precision is the ratio tp / (tp + fp)
# The recall is the ratio tp / (tp + fn) 
		
dtPrecision = (dtTP*1.0)/(dtTP+dtFP)
dtRecall = (dtTP*1.0)/(dtTP+dtFN)
#print dtTP, dtFP, dtFN
#print dtPrecision, dtRecall
dtF1 = (2.0*dtPrecision*dtRecall)/(dtPrecision + dtRecall)

rfPrecision = (rfTP*1.0)/(rfTP+rfFP)
rfRecall = (rfTP*1.0)/(rfTP+rfFN)
rfF1 = (2.0*rfPrecision*rfRecall)/(rfPrecision + rfRecall)

svmPrecision = (svmTP*1.0)/(svmTP+svmFP)
svmRecall = (svmTP*1.0)/(svmTP+svmFN)
svmF1 = (2.0*svmPrecision*svmRecall)/(svmPrecision + svmRecall)

gnbPrecision = (gnbTP*1.0)/(gnbTP+ gnbFP)
gnbRecall = (gnbTP*1.0)/(gnbTP+ gnbFN)
gnbF1 = (2.0*gnbPrecision*gnbRecall)/(gnbPrecision + gnbRecall)

lrPrecision = (lrTP*1.0)/(lrTP+ lrFP)
lrRecall = (lrTP*1.0)/(lrTP + lrFN)
lrF1 = (2.0*lrPrecision*lrRecall)/(lrPrecision + lrRecall)
	
#print dtErr, type(dtErr)
# dtRate = float(dtErr)/len(Ifeat) 
# rfRate = float(rfErr)/len(Ifeat)
# svmRate = float(svmErr)/len(Ifeat)
# gnbRate = float(gnbErr)/len(Ifeat)
# lrRate = float(lrErr)/len(Ifeat)	

#print "dtRate: " + str(dtRate) + " rfRate: " + str(rfRate) + " svmRate: " + str(svmRate) + " gnbRate: " + str(gnbRate) + " lrRate: " + str(lrRate)

print "dtF1: " + str(dtF1) + " rfF1: " + str(rfF1) + " svmF1: " + str(svmF1) + " gnbF1: " + str(gnbF1) + " lrF1: " + str(lrF1)
print "dtPrecision: " + str(dtPrecision) + " rfPrecision: " + str(rfPrecision) + " svmPrecision: " + str(svmPrecision) + " gnbPrecision: " + str(gnbPrecision) + " lrPrecision: " + str(lrPrecision)
print "dtRecall: " + str(dtRecall) + " rfRecall: " + str(rfRecall) + " svmRecall: " + str(svmRecall) + " gnbRecall: " + str(gnbRecall) + " lrRecall: " + str(lrRecall)


# Result obtained:
# dtF1: 0.886956521739 rfF1: 0.902654867257 svmF1: 0.894736842105 gnbF1: 0.894736842105 lrF1: 0.894736842105
# dtPrecision: 0.894736842105 rfPrecision: 0.927272727273 svmPrecision: 0.910714285714 gnbPrecision: 0.910714285714 lrPrecision: 0.910714285714
# dtRecall: 0.879310344828 rfRecall: 0.879310344828 svmRecall: 0.879310344828 gnbRecall: 0.879310344828 lrRecall: 0.879310344828

# After step2, best matcher = RF = X


 
#Debug
Ufeat = Ifeat[0:len(Ifeat)/2]
ULabel = Ilabel[0:len(Ifeat)/2]
Vfeat = Ifeat[len(Ifeat)/2:]
Vlabel = Ilabel[len(Ifeat)/2:]

rfDebug = ensemble.RandomForestClassifier()
rfDebug = rf.fit(Ufeat, ULabel)
rfPredDebug = rf.predict(Vfeat)

#print rfPredDebug, len(rfPredDebug), len(Vlabel)

#Print False Positive and False Negative
for i in range(len(Vlabel)):
	if Vlabel[i] == 0 and rfPredDebug[i] == 1:
		print 'Debugging RF -> False Positive: ', sampledList[len(Ufeat)+i],  rfPredDebug[i]
		print Vfeat[i]

	if Vlabel[i] == 1 and rfPredDebug[i] == 0:
		print 'Debugging RF -> False Negative: ', sampledList[len(Ufeat)+i], rfPredDebug[i]
		print Vfeat[i]
	

# Debug issues identified:
# Fix 1:  Fix similarity score of time to be such that sim = 1- (diff/max)
# Fix 2:  Change similarity measure of date so that it is similar to the new similarity defined for time (above)
 
# dtF1: 0.894736842105 rfF1: 0.894736842105 svmF1: 0.894736842105 gnbF1: 0.894736842105 lrF1: 0.894736842105
# dtPrecision: 0.910714285714 rfPrecision: 0.910714285714 svmPrecision: 0.910714285714 gnbPrecision: 0.910714285714 lrPrecision: 0.910714285714
# dtRecall: 0.879310344828 rfRecall: 0.879310344828 svmRecall: 0.879310344828 gnbRecall: 0.879310344828 lrRecall: 0.879310344828
# Debugging RF -> False Positive:  [239, '1005', 's_1408', ' Eminem', ' Intro', '1-Jan-05', datetime.time(0, 0, 33), 'Armin van Buuren', 'Into', '19-Aug-16', datetime.time(0, 3, 24), 0] 1
# [0.44047619047619047, 0.8888888888888888, 0.5694444444444444, 0.8382352941176471]
# Debugging RF -> False Positive:  [251, '1054', 's_1428', ' Eminem', ' Untitled', '18-Jun-10', datetime.time(0, 3, 14), 'Burial', 'Untitled', '1-Jul-14', datetime.time(0, 0, 46), 0] 1
# [0.4365079365079365, 0.9629629629629629, 0.8055555555555555, 0.7628865979381443]
# Debugging RF -> False Positive:  [426, '2030', 's_2481', ' Beyonce', ' Intro (Live)', '26-Nov-10', datetime.time(0, 1, 11), 'Tye Tribbett & G.A.', 'Victory (Live)', '23-May-06', datetime.time(0, 4, 9), 0] 1
# [0.4868421052631579, 0.7945054945054945, 0.6296296296296297, 0.714859437751004]
# Debugging RF -> False Positive:  [427, '2053', 's_2468', ' Beyonce', ' Halo (Live)', '26-Nov-10', datetime.time(0, 6, 31), 'Tye Tribbett & G.A.', 'Intro (Live)', '23-May-06', datetime.time(0, 2, 3), 0] 1
# [0.4868421052631579, 0.736111111111111, 0.6296296296296297, 0.6854219948849105]	


# Step 4

###### REPEAT RUN 1 #########################
#############################################
#Step 2 repeat 
#############################################

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
	f4 = 1.0 - f4
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

dtTP = 0
dtFP = 0
dtFN = 0

rfTP = 0
rfFP = 0
rfFN = 0
 
svmTP = 0
svmFP = 0
svmFN = 0

gnbTP = 0
gnbFP = 0
gnbFN = 0 

lrTP = 0
lrFP = 0
lrFN = 0 


for i in range(len(Ifeat)):
	X = Ifeat[0:i] + Ifeat[i+1:]
	Y = Ilabel[0:i] + Ilabel[i+1:]
	#DT
	dt = tree.DecisionTreeClassifier()
	dt = dt.fit(X, Y)
	dtPred = dt.predict([Ifeat[i]])
	dtErr += (Ilabel[i] != dtPred)
	if dtPred == 1 and Ilabel[i] == 1:
		dtTP += 1
	if dtPred ==1 and Ilabel[i] == 0:
		dtFP += 1
	if dtPred == 0 and Ilabel[i] ==1:
		dtFN += 1
		
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != dtPred).sum()))


	#RF	
	rf = ensemble.RandomForestClassifier()
	rf = rf.fit(X, Y)
	rfPred = rf.predict([Ifeat[i]])
	rfErr += (Ilabel[i] != rfPred)
	if rfPred == 1 and Ilabel[i] == 1:
		rfTP += 1
	if rfPred ==1 and Ilabel[i] == 0:
		rfFP += 1
	if rfPred == 0 and Ilabel[i] ==1:
		rfFN += 1
		
	
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != rfPred).sum()))

	#SVM
	s1 = svm.SVC()
	svmFit = s1.fit(X,Y)
	svmPred = s1.predict([Ifeat[i]])
	svmErr += (Ilabel[i] != svmPred)
	if svmPred == 1 and Ilabel[i] == 1:
		svmTP += 1
	if svmPred ==1 and Ilabel[i] == 0:
		svmFP += 1
	if svmPred == 0 and Ilabel[i] ==1:
		svmFN += 1
		
	
	
	#print svmPred
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != svmPred).sum()))

	#NB
	gnb = naive_bayes.GaussianNB()
	gnb = gnb.fit(X,Y)
	gnbPred = gnb.predict([Ifeat[i]])
	gnbErr += (Ilabel[i] != gnbPred)
	if gnbPred == 1 and Ilabel[i] == 1:
		gnbTP += 1
	if gnbPred ==1 and Ilabel[i] == 0:
		gnbFP += 1
	if gnbPred == 0 and Ilabel[i] ==1:
		gnbFN += 1
	
	#print gnbPred
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != gnbPred).sum()))

	#LR
	lr = linear_model.LogisticRegression()
	lr = lr.fit(X,Y)
	lrPred = gnb.predict([Ifeat[i]])
	lrErr += (Ilabel[i] != lrPred)
	if lrPred == 1 and Ilabel[i] == 1:
		lrTP += 1
	if lrPred ==1 and Ilabel[i] == 0:
		lrFP += 1
	if lrPred == 0 and Ilabel[i] ==1:
		lrFN += 1
	#print lrPred

# The precision is the ratio tp / (tp + fp)
# The recall is the ratio tp / (tp + fn) 
		
dtPrecision = (dtTP*1.0)/(dtTP+dtFP)
dtRecall = (dtTP*1.0)/(dtTP+dtFN)
#print dtTP, dtFP, dtFN
#print dtPrecision, dtRecall
dtF1 = (2.0*dtPrecision*dtRecall)/(dtPrecision + dtRecall)

rfPrecision = (rfTP*1.0)/(rfTP+rfFP)
rfRecall = (rfTP*1.0)/(rfTP+rfFN)
rfF1 = (2.0*rfPrecision*rfRecall)/(rfPrecision + rfRecall)

svmPrecision = (svmTP*1.0)/(svmTP+svmFP)
svmRecall = (svmTP*1.0)/(svmTP+svmFN)
svmF1 = (2.0*svmPrecision*svmRecall)/(svmPrecision + svmRecall)

gnbPrecision = (gnbTP*1.0)/(gnbTP+ gnbFP)
gnbRecall = (gnbTP*1.0)/(gnbTP+ gnbFN)
gnbF1 = (2.0*gnbPrecision*gnbRecall)/(gnbPrecision + gnbRecall)

lrPrecision = (lrTP*1.0)/(lrTP+ lrFP)
lrRecall = (lrTP*1.0)/(lrTP + lrFN)
lrF1 = (2.0*lrPrecision*lrRecall)/(lrPrecision + lrRecall)
	
#print dtErr, type(dtErr)
# dtRate = float(dtErr)/len(Ifeat) 
# rfRate = float(rfErr)/len(Ifeat)
# svmRate = float(svmErr)/len(Ifeat)
# gnbRate = float(gnbErr)/len(Ifeat)
# lrRate = float(lrErr)/len(Ifeat)	

#print "dtRate: " + str(dtRate) + " rfRate: " + str(rfRate) + " svmRate: " + str(svmRate) + " gnbRate: " + str(gnbRate) + " lrRate: " + str(lrRate)


print 'RESULT AFTER DEBUGGING'
print "dtF1: " + str(dtF1) + " rfF1: " + str(rfF1) + " svmF1: " + str(svmF1) + " gnbF1: " + str(gnbF1) + " lrF1: " + str(lrF1)
print "dtPrecision: " + str(dtPrecision) + " rfPrecision: " + str(rfPrecision) + " svmPrecision: " + str(svmPrecision) + " gnbPrecision: " + str(gnbPrecision) + " lrPrecision: " + str(lrPrecision)
print "dtRecall: " + str(dtRecall) + " rfRecall: " + str(rfRecall) + " svmRecall: " + str(svmRecall) + " gnbRecall: " + str(gnbRecall) + " lrRecall: " + str(lrRecall)


#Debug AGAIN
Ufeat = Ifeat[0:len(Ifeat)/2]
ULabel = Ilabel[0:len(Ifeat)/2]
Vfeat = Ifeat[len(Ifeat)/2:]
Vlabel = Ilabel[len(Ifeat)/2:]

rfDebug = ensemble.RandomForestClassifier()
rfDebug = rf.fit(Ufeat, ULabel)
rfPredDebug = rf.predict(Vfeat)

#print rfPredDebug, len(rfPredDebug), len(Vlabel)


print 'DEBUGGING THE NEW MODEL'
#Print False Positive and False Negative
for i in range(len(Vlabel)):
	if Vlabel[i] == 0 and rfPredDebug[i] == 1:
		print 'Debugging RF -> False Positive: ', sampledList[len(Ufeat)+i],  rfPredDebug[i]
		print Vfeat[i]

	if Vlabel[i] == 1 and rfPredDebug[i] == 0:
		print 'Debugging RF -> False Negative: ', sampledList[len(Ufeat)+i], rfPredDebug[i]
		print Vfeat[i]

		
		
# execfile('Features.py')
# 00:04:55 0:01:00
# dtF1: 0.879310344828 rfF1: 0.894736842105 svmF1: 0.894736842105 gnbF1: 0.894736842105 lrF1: 0.894736842105
# dtPrecision: 0.879310344828 rfPrecision: 0.910714285714 svmPrecision: 0.910714285714 gnbPrecision: 0.910714285714 lrPrecision: 0.910714285714
# dtRecall: 0.879310344828 rfRecall: 0.879310344828 svmRecall: 0.879310344828 gnbRecall: 0.879310344828 lrRecall: 0.879310344828
# Debugging RF -> False Positive:  [239, '1005', 's_1408', ' Eminem', ' Intro', '1-Jan-05', datetime.time(0, 0, 33), 'Armin van Buuren', 'Into', '19-Aug-16', datetime.time(0, 3, 24), 0] 1
# [0.44047619047619047, 0.8888888888888888, 0.5694444444444444, 0.8382352941176471]
# Debugging RF -> False Positive:  [251, '1054', 's_1428', ' Eminem', ' Untitled', '18-Jun-10', datetime.time(0, 3, 14), 'Burial', 'Untitled', '1-Jul-14', datetime.time(0, 0, 46), 0] 1
# [0.4365079365079365, 0.9629629629629629, 0.8055555555555555, 0.7628865979381443]
# Debugging RF -> False Positive:  [426, '2030', 's_2481', ' Beyonce', ' Intro (Live)', '26-Nov-10', datetime.time(0, 1, 11), 'Tye Tribbett & G.A.', 'Victory (Live)', '23-May-06', datetime.time(0, 4, 9), 0] 1
# [0.4868421052631579, 0.7945054945054945, 0.6296296296296297, 0.714859437751004]
# Debugging RF -> False Positive:  [427, '2053', 's_2468', ' Beyonce', ' Halo (Live)', '26-Nov-10', datetime.time(0, 6, 31), 'Tye Tribbett & G.A.', 'Intro (Live)', '23-May-06', datetime.time(0, 2, 3), 0] 1
# [0.4868421052631579, 0.736111111111111, 0.6296296296296297, 0.6854219948849105]
# RESULT AFTER DEBUGGING
# dtF1: 0.879310344828 rfF1: 0.910714285714 svmF1: 0.894736842105 gnbF1: 0.894736842105 lrF1: 0.894736842105
# dtPrecision: 0.879310344828 rfPrecision: 0.944444444444 svmPrecision: 0.910714285714 gnbPrecision: 0.910714285714 lrPrecision: 0.910714285714
# dtRecall: 0.879310344828 rfRecall: 0.879310344828 svmRecall: 0.879310344828 gnbRecall: 0.879310344828 lrRecall: 0.879310344828
# DEBUGGING THE NEW MODEL
# Debugging RF -> False Positive:  [239, '1005', 's_1408', ' Eminem', ' Intro', '1-Jan-05', datetime.time(0, 0, 33), 'Armin van Buuren', 'Into', '19-Aug-16', datetime.time(0, 3, 24), 0] 1
# [0.44047619047619047, 0.8888888888888888, 0.5694444444444444, 0.16176470588235292]
# Debugging RF -> False Positive:  [251, '1054', 's_1428', ' Eminem', ' Untitled', '18-Jun-10', datetime.time(0, 3, 14), 'Burial', 'Untitled', '1-Jul-14', datetime.time(0, 0, 46), 0] 1
# [0.4365079365079365, 0.9629629629629629, 0.8055555555555555, 0.23711340206185572]
# Debugging RF -> False Positive:  [260, '1114', 's_519', ' Eminem', ' Yellow Brick Road', '12-Nov-04', datetime.time(0, 5, 46), 'Elton John', 'Goodbye Yellow Brick Road', '12-Nov-02', datetime.time(0, 3, 16), 0] 1
# [0.49523809523809526, 0.7770370370370371, 0.9259259259259259, 0.5664739884393064]		

###### REPEAT RUN 2 #########################
#############################################
#Step 2 repeat 
#############################################

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
	#f3 = jaro1.get_raw_score(item[5],item[9])#Released Date - 5,9 - Jaro
	
	#print item[5], item[6]
	date1 = datetime.strptime(item[5],'%d-%b-%y')
	date2 = datetime.strptime(item[9],'%d-%b-%y')
	#print date1, date2, '-------------------------------------------'
	timeObj4 = datetime.strptime('00:00:00', '%H:%M:%S').time()
	
	dif = datetime.combine(max(date1, date2), timeObj4) - datetime.combine( min(date1, date2), timeObj4)
	norm = datetime.combine(date.today(), timeObj4)- datetime.combine(min(date1, date2), timeObj4)
	
	f3 = 1.0*(norm.days-dif.days)/norm.days
	# print 1.0*(norm.days-dif.days)/norm.days
	
	timeObj3 = datetime.strptime('00:00', '%M:%S').time()
	
	#print timeObj3 #, item 
	f4 = (datetime.combine(date.today(), max(item[6],item[10])) - datetime.combine(date.today(), min(item[6],item[10]))).total_seconds()#Time -6,10 - diff/max	
	f4de =(datetime.combine(date.today(), max(item[6],item[10])) - datetime.combine(date.today(), timeObj3)).total_seconds()
	f4/= f4de
	f4 = 1.0 - f4
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

dtTP = 0
dtFP = 0
dtFN = 0

rfTP = 0
rfFP = 0
rfFN = 0
 
svmTP = 0
svmFP = 0
svmFN = 0

gnbTP = 0
gnbFP = 0
gnbFN = 0 

lrTP = 0
lrFP = 0
lrFN = 0 


for i in range(len(Ifeat)):
	X = Ifeat[0:i] + Ifeat[i+1:]
	Y = Ilabel[0:i] + Ilabel[i+1:]
	#DT
	dt = tree.DecisionTreeClassifier()
	dt = dt.fit(X, Y)
	dtPred = dt.predict([Ifeat[i]])
	dtErr += (Ilabel[i] != dtPred)
	if dtPred == 1 and Ilabel[i] == 1:
		dtTP += 1
	if dtPred ==1 and Ilabel[i] == 0:
		dtFP += 1
	if dtPred == 0 and Ilabel[i] ==1:
		dtFN += 1
		
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != dtPred).sum()))


	#RF	
	rf = ensemble.RandomForestClassifier()
	rf = rf.fit(X, Y)
	rfPred = rf.predict([Ifeat[i]])
	rfErr += (Ilabel[i] != rfPred)
	if rfPred == 1 and Ilabel[i] == 1:
		rfTP += 1
	if rfPred ==1 and Ilabel[i] == 0:
		rfFP += 1
	if rfPred == 0 and Ilabel[i] ==1:
		rfFN += 1
		
	
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != rfPred).sum()))

	#SVM
	s1 = svm.SVC()
	svmFit = s1.fit(X,Y)
	svmPred = s1.predict([Ifeat[i]])
	svmErr += (Ilabel[i] != svmPred)
	if svmPred == 1 and Ilabel[i] == 1:
		svmTP += 1
	if svmPred ==1 and Ilabel[i] == 0:
		svmFP += 1
	if svmPred == 0 and Ilabel[i] ==1:
		svmFN += 1
		
	
	
	#print svmPred
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != svmPred).sum()))

	#NB
	gnb = naive_bayes.GaussianNB()
	gnb = gnb.fit(X,Y)
	gnbPred = gnb.predict([Ifeat[i]])
	gnbErr += (Ilabel[i] != gnbPred)
	if gnbPred == 1 and Ilabel[i] == 1:
		gnbTP += 1
	if gnbPred ==1 and Ilabel[i] == 0:
		gnbFP += 1
	if gnbPred == 0 and Ilabel[i] ==1:
		gnbFN += 1
	
	#print gnbPred
	#print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != gnbPred).sum()))

	#LR
	lr = linear_model.LogisticRegression()
	lr = lr.fit(X,Y)
	lrPred = gnb.predict([Ifeat[i]])
	lrErr += (Ilabel[i] != lrPred)
	if lrPred == 1 and Ilabel[i] == 1:
		lrTP += 1
	if lrPred ==1 and Ilabel[i] == 0:
		lrFP += 1
	if lrPred == 0 and Ilabel[i] ==1:
		lrFN += 1
	#print lrPred

# The precision is the ratio tp / (tp + fp)
# The recall is the ratio tp / (tp + fn) 
		
dtPrecision = (dtTP*1.0)/(dtTP+dtFP)
dtRecall = (dtTP*1.0)/(dtTP+dtFN)
#print dtTP, dtFP, dtFN
#print dtPrecision, dtRecall
dtF1 = (2.0*dtPrecision*dtRecall)/(dtPrecision + dtRecall)

rfPrecision = (rfTP*1.0)/(rfTP+rfFP)
rfRecall = (rfTP*1.0)/(rfTP+rfFN)
rfF1 = (2.0*rfPrecision*rfRecall)/(rfPrecision + rfRecall)

svmPrecision = (svmTP*1.0)/(svmTP+svmFP)
svmRecall = (svmTP*1.0)/(svmTP+svmFN)
svmF1 = (2.0*svmPrecision*svmRecall)/(svmPrecision + svmRecall)

gnbPrecision = (gnbTP*1.0)/(gnbTP+ gnbFP)
gnbRecall = (gnbTP*1.0)/(gnbTP+ gnbFN)
gnbF1 = (2.0*gnbPrecision*gnbRecall)/(gnbPrecision + gnbRecall)

lrPrecision = (lrTP*1.0)/(lrTP+ lrFP)
lrRecall = (lrTP*1.0)/(lrTP + lrFN)
lrF1 = (2.0*lrPrecision*lrRecall)/(lrPrecision + lrRecall)
	
#print dtErr, type(dtErr)
# dtRate = float(dtErr)/len(Ifeat) 
# rfRate = float(rfErr)/len(Ifeat)
# svmRate = float(svmErr)/len(Ifeat)
# gnbRate = float(gnbErr)/len(Ifeat)
# lrRate = float(lrErr)/len(Ifeat)	

#print "dtRate: " + str(dtRate) + " rfRate: " + str(rfRate) + " svmRate: " + str(svmRate) + " gnbRate: " + str(gnbRate) + " lrRate: " + str(lrRate)


print 'RESULT AFTER DEBUGGING'
print "dtF1: " + str(dtF1) + " rfF1: " + str(rfF1) + " svmF1: " + str(svmF1) + " gnbF1: " + str(gnbF1) + " lrF1: " + str(lrF1)
print "dtPrecision: " + str(dtPrecision) + " rfPrecision: " + str(rfPrecision) + " svmPrecision: " + str(svmPrecision) + " gnbPrecision: " + str(gnbPrecision) + " lrPrecision: " + str(lrPrecision)
print "dtRecall: " + str(dtRecall) + " rfRecall: " + str(rfRecall) + " svmRecall: " + str(svmRecall) + " gnbRecall: " + str(gnbRecall) + " lrRecall: " + str(lrRecall)


#Debug AGAIN
Ufeat = Ifeat[0:len(Ifeat)/2]
ULabel = Ilabel[0:len(Ifeat)/2]
Vfeat = Ifeat[len(Ifeat)/2:]
Vlabel = Ilabel[len(Ifeat)/2:]

rfDebug = ensemble.RandomForestClassifier()
rfDebug = rf.fit(Ufeat, ULabel)
rfPredDebug = rf.predict(Vfeat)

#print rfPredDebug, len(rfPredDebug), len(Vlabel)


print 'DEBUGGING THE NEW MODEL'
#Print False Positive and False Negative
for i in range(len(Vlabel)):
	if Vlabel[i] == 0 and rfPredDebug[i] == 1:
		print 'Debugging RF -> False Positive: ', sampledList[len(Ufeat)+i],  rfPredDebug[i]
		print Vfeat[i]

	if Vlabel[i] == 1 and rfPredDebug[i] == 0:
		print 'Debugging RF -> False Negative: ', sampledList[len(Ufeat)+i], rfPredDebug[i]
		print Vfeat[i]
		

# execfile('Features.py')
# 00:04:55 0:01:00
# dtF1: 0.879310344828 rfF1: 0.902654867257 svmF1: 0.894736842105 gnbF1: 0.894736842105 lrF1: 0.894736842105
# dtPrecision: 0.879310344828 rfPrecision: 0.927272727273 svmPrecision: 0.910714285714 gnbPrecision: 0.910714285714 lrPrecision: 0.910714285714
# dtRecall: 0.879310344828 rfRecall: 0.879310344828 svmRecall: 0.879310344828 gnbRecall: 0.879310344828 lrRecall: 0.879310344828
# Debugging RF -> False Positive:  [251, '1054', 's_1428', ' Eminem', ' Untitled', '18-Jun-10', datetime.time(0, 3, 14), 'Burial', 'Untitled', '1-Jul-14', datetime.time(0, 0, 46), 0] 1
# [0.4365079365079365, 0.9629629629629629, 0.8055555555555555, 0.7628865979381443]
# RESULT AFTER DEBUGGING
# dtF1: 0.879310344828 rfF1: 0.902654867257 svmF1: 0.894736842105 gnbF1: 0.894736842105 lrF1: 0.894736842105
# dtPrecision: 0.879310344828 rfPrecision: 0.927272727273 svmPrecision: 0.910714285714 gnbPrecision: 0.910714285714 lrPrecision: 0.910714285714
# dtRecall: 0.879310344828 rfRecall: 0.879310344828 svmRecall: 0.879310344828 gnbRecall: 0.879310344828 lrRecall: 0.879310344828
# DEBUGGING THE NEW MODEL
# Debugging RF -> False Positive:  [251, '1054', 's_1428', ' Eminem', ' Untitled', '18-Jun-10', datetime.time(0, 3, 14), 'Burial', 'Untitled', '1-Jul-14', datetime.time(0, 0, 46), 0] 1
# [0.4365079365079365, 0.9629629629629629, 0.8055555555555555, 0.23711340206185572]
# Debugging RF -> False Positive:  [426, '2030', 's_2481', ' Beyonce', ' Intro (Live)', '26-Nov-10', datetime.time(0, 1, 11), 'Tye Tribbett & G.A.', 'Victory (Live)', '23-May-06', datetime.time(0, 4, 9), 0] 1
# [0.4868421052631579, 0.7945054945054945, 0.6296296296296297, 0.285140562248996]
# Debugging RF -> False Positive:  [427, '2053', 's_2468', ' Beyonce', ' Halo (Live)', '26-Nov-10', datetime.time(0, 6, 31), 'Tye Tribbett & G.A.', 'Intro (Live)', '23-May-06', datetime.time(0, 2, 3), 0] 1
# [0.4868421052631579, 0.736111111111111, 0.6296296296296297, 0.3145780051150895]
# RESULT AFTER DEBUGGING
# dtF1: 0.902654867257 rfF1: 0.910714285714 svmF1: 0.894736842105 gnbF1: 0.894736842105 lrF1: 0.894736842105
# dtPrecision: 0.927272727273 rfPrecision: 0.944444444444 svmPrecision: 0.910714285714 gnbPrecision: 0.910714285714 lrPrecision: 0.910714285714
# dtRecall: 0.879310344828 rfRecall: 0.879310344828 svmRecall: 0.879310344828 gnbRecall: 0.879310344828 lrRecall: 0.879310344828
# DEBUGGING THE NEW MODEL
# Debugging RF -> False Positive:  [239, '1005', 's_1408', ' Eminem', ' Intro', '1-Jan-05', datetime.time(0, 0, 33), 'Armin van Buuren', 'Into', '19-Aug-16', datetime.time(0, 3, 24), 0] 1
# [0.44047619047619047, 0.8888888888888888, 0.02389705882352941, 0.16176470588235292]
# Debugging RF -> False Positive:  [251, '1054', 's_1428', ' Eminem', ' Untitled', '18-Jun-10', datetime.time(0, 3, 14), 'Burial', 'Untitled', '1-Jul-14', datetime.time(0, 0, 46), 0] 1
# [0.4365079365079365, 0.9629629629629629, 0.3748939779474131, 0.23711340206185572]
# Debugging RF -> False Positive:  [426, '2030', 's_2481', ' Beyonce', ' Intro (Live)', '26-Nov-10', datetime.time(0, 1, 11), 'Tye Tribbett & G.A.', 'Victory (Live)', '23-May-06', datetime.time(0, 4, 9), 0] 1
# [0.4868421052631579, 0.7945054945054945, 0.5713914174252276, 0.285140562248996]
# Debugging RF -> False Positive:  [427, '2053', 's_2468', ' Beyonce', ' Halo (Live)', '26-Nov-10', datetime.time(0, 6, 31), 'Tye Tribbett & G.A.', 'Intro (Live)', '23-May-06', datetime.time(0, 2, 3), 0] 1
# [0.4868421052631579, 0.736111111111111, 0.5713914174252276, 0.3145780051150895]
# Debugging RF -> False Positive:  [448, '2392', 's_1074', ' Maroon 5', " Can't Stop", '22-May-07', datetime.time(0, 2, 32), 'OneRepublic', "Can't Stop", '14-Apr-14', datetime.time(0, 4, 9), 0] 1
# [0, 0.9696969696969697, 0.27635736857224935, 0.6104417670682731]
	



# STEP 5

rfFinal = ensemble.RandomForestClassifier()
rfFinal = rf.fit(Ifeat, Ilabel)

for i in range(len(Jfeat)):
	rfPredFinal = rf.predict([Jfeat[i]])
	if rfPredFinal == 1 and Jlabel[i] == 1:
		rfTP += 1
	if rfPredFinal ==1 and Jlabel[i] == 0:
		rfFP += 1
	if rfPredFinal == 0 and Jlabel[i] ==1:
		rfFN += 1
rfPrecision = (rfTP*1.0)/(rfTP+rfFP)
rfRecall = (rfTP*1.0)/(rfTP+rfFN)
rfF1 = (2.0*rfPrecision*rfRecall)/(rfPrecision + rfRecall)

print "FINAL RESULT on J: "
print "rfPrecision" +' ' + str(rfPrecision) + ' ' + "rfRecall" +' ' + str(rfRecall) +' '+ "rfF1" +' ' + str(rfF1)
	#Code for Precision, Recall, F1 without CV


















################ DISCARDING THIS RUN	
# ###### REPEAT RUN 3 #########################
# #############################################
# #Step 2 repeat 
# #############################################

# #Converting every row to feature vector
# featList = []
# label = []
# for item in sampledList:
	# #print item
	# fi = []
	
	# #ws_tok = WhitespaceTokenizer()
	# #artistSet1 = ws_tok.tokenize(item[3])
	# #artistSet2 = ws_tok.tokenize(item[7])
	# #lev = ps.SmithWaterman()
	# item[3] = item[3].strip()
	# item[7] = item[7].strip()
	# if len(item[3])==len(item[7]):
		# hd = ps.HammingDistance()
		# f1 = hd.get_raw_score(item[3], item[7])
		# f1 /= len(item[3])
		# f1 = 1 - f1 
	# else:
		# if len(item[3]) < len(item[7]):
			# item[3] += ' '*(len(item[7])-len(item[3]))
		# else:
			# item[7] += ' '*(len(item[3])-len(item[7]))
		# hd = ps.HammingDistance()
		# f1 = hd.get_raw_score(item[3], item[7])
		# f1 /= len(item[3])
		# f1 = 1 - f1 	
		
	# # f1 = lev.get_raw_score(item[3],item[7])#Artist- 3,7 - Jaro
	
	# #jaro2 = ps.Jaro()
	# #f2 = jaro1.get_raw_score(item[4],item[8])#Trackname -4,8 - Jaro
	# item[4] = item[4].strip()
	# item[8] = item[8].strip()
	# if len(item[4])==len(item[8]):
		# hd = ps.HammingDistance()
		# f2 = hd.get_raw_score(item[4], item[8])
		# f2 /= len(item[4])
		# f2 = 1 - f2 
	# else:
		# if len(item[4]) < len(item[8]):
			# item[4] += ' '*(len(item[8])-len(item[4]))
		# else:
			# item[8] += ' '*(len(item[4])-len(item[8]))
		# hd = ps.HammingDistance()
		# f2 = hd.get_raw_score(item[4], item[8])
		# f2 /= len(item[4])
		# f2 = 1 - f2 	
	
	
	
	
	# jaro3 = ps.Jaro()
	# #f3 = jaro1.get_raw_score(item[5],item[9])#Released Date - 5,9 - Jaro
	
	# #print item[5], item[6]
	# date1 = datetime.strptime(item[5],'%d-%b-%y')
	# date2 = datetime.strptime(item[9],'%d-%b-%y')
	# #print date1, date2, '-------------------------------------------'
	# timeObj4 = datetime.strptime('00:00:00', '%H:%M:%S').time()
	
	# dif = datetime.combine(max(date1, date2), timeObj4) - datetime.combine( min(date1, date2), timeObj4)
	# norm = datetime.combine(date.today(), timeObj4)- datetime.combine( min(date1, date2), timeObj4)
	
	# f3 = 1.0*(norm.days-dif.days)/norm.days
	# # print 1.0*(norm.days-dif.days)/norm.days
	
	# timeObj3 = datetime.strptime('00:00', '%M:%S').time()
	
	# #print timeObj3 #, item 
	# f4 = (datetime.combine(date.today(), max(item[6],item[10])) - datetime.combine(date.today(), min(item[6],item[10]))).total_seconds()#Time -6,10 - diff/max	
	# f4de =(datetime.combine(date.today(), max(item[6],item[10])) - datetime.combine(date.today(), timeObj3)).total_seconds()
	# f4/= f4de
	# f4 = 1.0 - f4
	# #print f4 
	# #sampledList[item]
	
	# fi.append(f1)
	# fi.append(f2)
	# fi.append(f3)
	# fi.append(f4)
	# label.append(item[-1])
	# featList.append(fi)
	
	
# #print featList
# #print label	

# #H = featList
# Ifeat = featList[0:300]
# #U = Ifeat[0:150]
# #V = Ifeat[150:-1]
# Jfeat = featList[300:-1]
# Ilabel = label[0:300]
# #Ulabel = Ilabel[0:150]
# #Vlabel = Ilabel[150:-1]
# Jlabel = label[300:-1]

# #print Ifeat
# #print len(Ilabel)
# dtErr = 0
# rfErr = 0
# svmErr = 0
# gnbErr =0
# lrErr = 0 

# dtTP = 0
# dtFP = 0
# dtFN = 0

# rfTP = 0
# rfFP = 0
# rfFN = 0
 
# svmTP = 0
# svmFP = 0
# svmFN = 0

# gnbTP = 0
# gnbFP = 0
# gnbFN = 0 

# lrTP = 0
# lrFP = 0
# lrFN = 0 


# for i in range(len(Ifeat)):
	# X = Ifeat[0:i] + Ifeat[i+1:]
	# Y = Ilabel[0:i] + Ilabel[i+1:]
	# #DT
	# dt = tree.DecisionTreeClassifier()
	# dt = dt.fit(X, Y)
	# dtPred = dt.predict([Ifeat[i]])
	# dtErr += (Ilabel[i] != dtPred)
	# if dtPred == 1 and Ilabel[i] == 1:
		# dtTP += 1
	# if dtPred ==1 and Ilabel[i] == 0:
		# dtFP += 1
	# if dtPred == 0 and Ilabel[i] ==1:
		# dtFN += 1
		
	# #print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != dtPred).sum()))


	# #RF	
	# rf = ensemble.RandomForestClassifier()
	# rf = rf.fit(X, Y)
	# rfPred = rf.predict([Ifeat[i]])
	# rfErr += (Ilabel[i] != rfPred)
	# if rfPred == 1 and Ilabel[i] == 1:
		# rfTP += 1
	# if rfPred ==1 and Ilabel[i] == 0:
		# rfFP += 1
	# if rfPred == 0 and Ilabel[i] ==1:
		# rfFN += 1
		
	
	# #print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != rfPred).sum()))

	# #SVM
	# s1 = svm.SVC()
	# svmFit = s1.fit(X,Y)
	# svmPred = s1.predict([Ifeat[i]])
	# svmErr += (Ilabel[i] != svmPred)
	# if svmPred == 1 and Ilabel[i] == 1:
		# svmTP += 1
	# if svmPred ==1 and Ilabel[i] == 0:
		# svmFP += 1
	# if svmPred == 0 and Ilabel[i] ==1:
		# svmFN += 1
		
	
	
	# #print svmPred
	# #print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != svmPred).sum()))

	# #NB
	# gnb = naive_bayes.GaussianNB()
	# gnb = gnb.fit(X,Y)
	# gnbPred = gnb.predict([Ifeat[i]])
	# gnbErr += (Ilabel[i] != gnbPred)
	# if gnbPred == 1 and Ilabel[i] == 1:
		# gnbTP += 1
	# if gnbPred ==1 and Ilabel[i] == 0:
		# gnbFP += 1
	# if gnbPred == 0 and Ilabel[i] ==1:
		# gnbFN += 1
	
	# #print gnbPred
	# #print("Number of mislabeled points out of a total %d points : %d" % (len(V),(Vlabel != gnbPred).sum()))

	# #LR
	# lr = linear_model.LogisticRegression()
	# lr = lr.fit(X,Y)
	# lrPred = gnb.predict([Ifeat[i]])
	# lrErr += (Ilabel[i] != lrPred)
	# if lrPred == 1 and Ilabel[i] == 1:
		# lrTP += 1
	# if lrPred ==1 and Ilabel[i] == 0:
		# lrFP += 1
	# if lrPred == 0 and Ilabel[i] ==1:
		# lrFN += 1
	# #print lrPred

# # The precision is the ratio tp / (tp + fp)
# # The recall is the ratio tp / (tp + fn) 
		
# dtPrecision = (dtTP*1.0)/(dtTP+dtFP)
# dtRecall = (dtTP*1.0)/(dtTP+dtFN)
# #print dtTP, dtFP, dtFN
# #print dtPrecision, dtRecall
# dtF1 = (2.0*dtPrecision*dtRecall)/(dtPrecision + dtRecall)

# rfPrecision = (rfTP*1.0)/(rfTP+rfFP)
# rfRecall = (rfTP*1.0)/(rfTP+rfFN)
# rfF1 = (2.0*rfPrecision*rfRecall)/(rfPrecision + rfRecall)

# svmPrecision = (svmTP*1.0)/(svmTP+svmFP)
# svmRecall = (svmTP*1.0)/(svmTP+svmFN)
# svmF1 = (2.0*svmPrecision*svmRecall)/(svmPrecision + svmRecall)

# gnbPrecision = (gnbTP*1.0)/(gnbTP+ gnbFP)
# gnbRecall = (gnbTP*1.0)/(gnbTP+ gnbFN)
# gnbF1 = (2.0*gnbPrecision*gnbRecall)/(gnbPrecision + gnbRecall)

# lrPrecision = (lrTP*1.0)/(lrTP+ lrFP)
# lrRecall = (lrTP*1.0)/(lrTP + lrFN)
# lrF1 = (2.0*lrPrecision*lrRecall)/(lrPrecision + lrRecall)
	
# #print dtErr, type(dtErr)
# # dtRate = float(dtErr)/len(Ifeat) 
# # rfRate = float(rfErr)/len(Ifeat)
# # svmRate = float(svmErr)/len(Ifeat)
# # gnbRate = float(gnbErr)/len(Ifeat)
# # lrRate = float(lrErr)/len(Ifeat)	

# #print "dtRate: " + str(dtRate) + " rfRate: " + str(rfRate) + " svmRate: " + str(svmRate) + " gnbRate: " + str(gnbRate) + " lrRate: " + str(lrRate)


# print 'RESULT AFTER DEBUGGING'
# print "dtF1: " + str(dtF1) + " rfF1: " + str(rfF1) + " svmF1: " + str(svmF1) + " gnbF1: " + str(gnbF1) + " lrF1: " + str(lrF1)
# print "dtPrecision: " + str(dtPrecision) + " rfPrecision: " + str(rfPrecision) + " svmPrecision: " + str(svmPrecision) + " gnbPrecision: " + str(gnbPrecision) + " lrPrecision: " + str(lrPrecision)
# print "dtRecall: " + str(dtRecall) + " rfRecall: " + str(rfRecall) + " svmRecall: " + str(svmRecall) + " gnbRecall: " + str(gnbRecall) + " lrRecall: " + str(lrRecall)


# #Debug AGAIN
# Ufeat = Ifeat[0:len(Ifeat)/2]
# ULabel = Ilabel[0:len(Ifeat)/2]
# Vfeat = Ifeat[len(Ifeat)/2:]
# Vlabel = Ilabel[len(Ifeat)/2:]

# rfDebug = ensemble.RandomForestClassifier()
# rfDebug = rf.fit(Ufeat, ULabel)
# rfPredDebug = rf.predict(Vfeat)

# #print rfPredDebug, len(rfPredDebug), len(Vlabel)


# print 'RUN 3: DEBUGGING THE NEW MODEL'
# #Print False Positive and False Negative
# for i in range(len(Vlabel)):
	# if Vlabel[i] == 0 and rfPredDebug[i] == 1:
		# print 'Debugging RF -> False Positive: ', sampledList[len(Ufeat)+i],  rfPredDebug[i]
		# print Vfeat[i]

	# if Vlabel[i] == 1 and rfPredDebug[i] == 0:
		# print 'Debugging RF -> False Negative: ', sampledList[len(Ufeat)+i], rfPredDebug[i]
		# print Vfeat[i]
		
