import py_stringmatching as ps
import csv
from datetime import datetime, date
from sklearn import tree, ensemble, svm, naive_bayes, linear_model
from sklearn.metrics import precision_recall_fscore_support

# Reading every row of csv into a list
f = open('SampledData.csv', 'rb')
csvRead = csv.reader(f, delimiter=',')
sampledList = []
for row in csvRead:
    row[0] = int(row[0])
    row[-1] = int(row[-1])
    timeObj1=datetime.strptime(row[6].strip(), '%M:%S').time()
    row[6] = timeObj1
    timeObj1=datetime.strptime(row[10].strip(), '%M:%S').time()
    row[10] = timeObj1
    # iteration #2: trim whitespaces from artist and track labels
    row[3] = row[3].strip()
    row[4] = row[4].strip()
    row[7] = row[7].strip()
    row[8] = row[8].strip()
    sampledList.append(row)
f.close()

# Converting every row in to a feature vector
featList = []
label = []
ws = ps.WhitespaceTokenizer()
for item in sampledList:
    fi = []

    jaro1 = ps.Jaro()

    # iteration #3:
    # pull the feature value to zero if none of the token pairs from either artist strings have a high
    # enough similarity score
    f1 = 0
    for t1 in ws.tokenize(item[3]):
        if max([jaro1.get_raw_score(t1, t2) for t2 in ws.tokenize(item[7])]) > .75:
            f1 = jaro1.get_raw_score(item[3], item[7])
            break

    # iteration #3:
    # if the artist doesn't match scale down the track similarity by a factor of 3
    # and if the track score isn't high enough pull it down to 0
    jaro2 = ps.Jaro()
    f2 = jaro1.get_raw_score(item[4], item[8])
    if f1 == 0:
        f2 /= 3
    elif f2 < 0.6:
        f2 = 0

    # convert to datetime object
    date1 = datetime.strptime(item[5],'%d-%b-%y')
    date2 = datetime.strptime(item[9],'%d-%b-%y')
    timeObj4 = datetime.strptime('00:00:00', '%H:%M:%S').time()
    # take the difference of the weights
    dif = datetime.combine(max(date1, date2), timeObj4) - datetime.combine( min(date1, date2), timeObj4)
    norm = datetime.combine(date.today(), timeObj4)- datetime.combine( min(date1, date2), timeObj4)
    # normalize the feature value
    f3 = 1.0*(norm.days-dif.days)/norm.days

    # convert to datetime object
    timeObj3 = datetime.strptime('00:00', '%M:%S').time()
    # take the difference of the track time lengths
    f4 = (datetime.combine(date.today(), max(item[6],item[10])) - datetime.combine(date.today(), min(item[6],item[10]))).total_seconds()#Time -6,10 - diff/max
    f4de =(datetime.combine(date.today(), max(item[6],item[10])) - datetime.combine(date.today(), timeObj3)).total_seconds()
    # normalize the feature value
    f4 /= f4de
    f4 = 1.0 - f4

    # add the feature values to the feature vector
    fi.append(f1)
    fi.append(f2)
    fi.append(f3)
    fi.append(f4)
    label.append(item[-1])
    featList.append(fi)


# split the data-set in to development set (I) and evaluation sets (J)
Ifeat = featList[0:300]
Jfeat = featList[300:-1]
Ilabel = label[0:300]
Jlabel = label[300:-1]

# initialize data structures for cross validation
dtTrue = []
rfTrue = []
svmTrue = []
gnbTrue = []
lrTrue = []

# STEP 2: perform leave-one-out-cross-validation
for i in range(len(Ifeat)):
    X = Ifeat[0:i] + Ifeat[i+1:]
    Y = Ilabel[0:i] + Ilabel[i+1:]

    # decision trees
    dt = tree.DecisionTreeClassifier()
    dt = dt.fit(X, Y)
    dtPred = dt.predict([Ifeat[i]])
    dtTrue.append(dtPred)

    # random forest
    rf = ensemble.RandomForestClassifier()
    rf = rf.fit(X, Y)
    rfPred = rf.predict([Ifeat[i]])
    rfTrue.append(rfPred)

    # support vector machine
    s1 = svm.SVC()
    svmFit = s1.fit(X,Y)
    svmPred = s1.predict([Ifeat[i]])
    svmTrue.append(svmPred)

    # gaussian naive bayes
    gnb = naive_bayes.GaussianNB()
    gnb = gnb.fit(X,Y)
    gnbPred = gnb.predict([Ifeat[i]])
    gnbTrue.append(gnbPred)

    # logistic regression
    lr = linear_model.LogisticRegression()
    lr = lr.fit(X,Y)
    lrPred = gnb.predict([Ifeat[i]])
    lrTrue.append(lrPred)

# report the scores for all the classifiers
print "decision tree"
print precision_recall_fscore_support(Ilabel, dtTrue)
print "random forest"
print precision_recall_fscore_support(Ilabel, rfTrue)
print "svm"
print precision_recall_fscore_support(Ilabel, svmTrue)
print "gnb"
print precision_recall_fscore_support(Ilabel, gnbTrue)
print "lr"
print precision_recall_fscore_support(Ilabel, lrTrue)

# STEP 3: debug random forest classifier

# split the development set into two halves U and V
Ufeat = Ifeat[0:len(Ifeat)/2]
ULabel = Ilabel[0:len(Ifeat)/2]
Vfeat = Ifeat[len(Ifeat)/2:]
Vlabel = Ilabel[len(Ifeat)/2:]
vFeatTrue = []

# train the classifier on U and evaluate on V
rfDebug = ensemble.RandomForestClassifier()
rfDebug = rfDebug.fit(Ufeat, ULabel)
rfPredDebug = rfDebug.predict(Vfeat)

# output the false positives and false negatives in the predictions made by the classifier on V
print 'DEBUGGING THE NEW MODEL'
for i in range(len(Vlabel)):

    vFeatTrue.append(rfPredDebug[i])

    if Vlabel[i] == 0 and rfPredDebug[i] == 1:
        print 'Debugging RF -> False Positive: ', sampledList[len(Ufeat) + i],  rfPredDebug[i]
        print Vfeat[i]
        print rfDebug.decision_path([Vfeat[i]])

    if Vlabel[i] == 1 and rfPredDebug[i] == 0:
        print 'Debugging RF -> False Negative: ', sampledList[len(Ufeat) + i], rfPredDebug[i]
        print Vfeat[i]
        print rfDebug.decision_path([Vfeat[i]])

# output the precision, recall and F1 score of the classifier during debugging
print 'predictions on V-features'
print vFeatTrue
print 'precision, recall and f1 on V-features'
print precision_recall_fscore_support(Vlabel, vFeatTrue)

# STEP 4: report the precision, recall and F1 score for all the classifiers on J

# decision tree trained on I and evaluated on J
dtFinal = tree.DecisionTreeClassifier()
dtFinal = dtFinal.fit(Ifeat, Ilabel)
dtFinalTrue = []
for i in range(len(Jfeat)):
    dtPredFinal = dtFinal.predict([Jfeat[i]])
    dtFinalTrue.append(dtPredFinal)
print "Decision Tree evaluated on J:"
print precision_recall_fscore_support(Jlabel, dtFinalTrue)

# random forest (best classifier) trained on I and evaluated on J
rfFinal = ensemble.RandomForestClassifier()
rfFinal = rfFinal.fit(Ifeat, Ilabel)
rfFinalTrue = []
for i in range(len(Jfeat)):
    rfPredFinal = rf.predict([Jfeat[i]])
    rfFinalTrue.append(rfPredFinal)
print "Random Forest evaluated on J:"
print precision_recall_fscore_support(Jlabel, rfFinalTrue)

# support vector machine trained on I and evaluated on J
svmFinal = svm.SVC()
svmFinal = svmFinal.fit(Ifeat, Ilabel)
svmFinalTrue = []
for i in range(len(Jfeat)):
    svmPredFinal = svmFinal.predict([Jfeat[i]])
    svmFinalTrue.append(svmPredFinal)
print "Support Vector Machine evaluated on J:"
print precision_recall_fscore_support(Jlabel, svmFinalTrue)

# gaussian naive bayes trained on I and evaluated on J
gnbFinal = naive_bayes.GaussianNB()
gnbFinal = gnbFinal.fit(Ifeat, Ilabel)
gnbFinalTrue = []
for i in range(len(Jfeat)):
    gnbPredFinal = gnbFinal.predict([Jfeat[i]])
    gnbFinalTrue.append(gnbPredFinal)
print "Gaussian Naive Bayes evaluated on J:"
print precision_recall_fscore_support(Jlabel, gnbFinalTrue)

# logistic regression trained on I and evaluated on J
lrFinal = linear_model.LogisticRegression()
lrFinal = lrFinal.fit(Ifeat, Ilabel)
lrFinalTrue = []
for i in range(len(Jfeat)):
    lrPredFinal = lrFinal.predict([Jfeat[i]])
    lrFinalTrue.append(lrPredFinal)
print "Logistic Regression evaluated on J:"
print precision_recall_fscore_support(Jlabel, lrFinalTrue)
