# E = target table into which we will merge tables A and B
# TableASchema = IdA,Album,Genres,Label,Time,TrackName,Price,Artist,Released
# TableBSchema = IdB,Album,Genres,Label,Time,TrackName,Price,Artist,Released
# TableESchema = IdE, IdA, IdB, Album,Genres,Label,Time,TrackName,Price,Artist,Released

# Approach is to go through the golden data, look for rows with M = 1
# For every tuple that matches, compare the value of each attribute in TableA and TableB and resolve conflict incase it arises.

import csv
from datetime import datetime

# Read in Golden data
# First row from file SampledData.csv: 0,1,s_927, Taylor Swift, Welcome To New York,27-Oct-14, 3:32,Taylor Swift,Welcome To New York,27-Oct-14,3:32,1
f = open('SampledData.csv', 'r')
reader = csv.reader(f)
GoldenData = []
for line in reader:
    line[0] = int(line[0].strip())
    line[1] = int(line[1].strip())
    line[2] = line[2].strip()
    line[3] = line[3].strip()
    line[4] = line[4].strip()
    line[7] = line[7].strip()
    line[8] = line[8].strip()
    line[11] = int(line[11].strip())

    # 5
    line[5] = datetime.strptime(line[5].strip(), '%d-%b-%y')
    # 6
    line[6] = datetime.strptime(line[6].strip(), '%M:%S').time()
    # 9
    line[9] = datetime.strptime(line[9].strip(), '%d-%b-%y')
    # 10
    line[10] = datetime.strptime(line[10].strip(), '%M:%S').time()
    GoldenData.append(line)
f.close()

# Read Table A
# TableASchema =['Id', 'Album', 'Genres',	'Label', 'Time',	'TrackName',	'Price',	'Artist',	'Released']
# First row: 1,1989,"Pop, Music, Rock","2014 Big Machine Records, LLC.", 3:32, Welcome To New York,$1.29 , Taylor Swift,27-Oct-14

f = open('assets/tablea2_utf8.csv', 'r')
reader = csv.reader(f)
TableA = []
TableAMap = {}
linNo = 0
for line in reader:
    if linNo == 0:
        linNo += 1
        continue
    if not line:
        continue

    line[0] = int(line[0])
    line[1] = line[1].strip()
    line[2] = line[2].strip()
    line[3] = line[3].strip()
    try:
        line[4] = datetime.strptime(line[4].strip(), '%M:%S').time()
    except ValueError:
        continue
    line[5] = line[5].strip()
    line[6] = line[6].strip()

    line[7] = line[7].strip()
    try:
        line[8] = datetime.strptime(line[8].strip(), '%d-%b-%y')
    except ValueError:
        continue
    TableA.append(line)
    TableAMap[line[0]] = linNo - 1
    linNo += 1
f.close()

# Read Table B
# TableBSchema = Id,Album,Genres,Label,Time,TrackName,Price,Artist,Released
# First row: s_1,The Truth About Love [Explicit],Pop,RCA Records Label,3:37,Are We All We Are [Explicit],$1.29 ,P!nk,18-Sep-12
f = open('assets/tableB_utf8.csv', 'r')
reader = csv.reader(f)
TableB = []
TableBMap = {}
linNo = 0
for line in reader:
    if linNo == 0:
        linNo += 1
        continue

    line[0] = line[0].strip()
    line[1] = line[1].strip()
    line[2] = line[2].strip()
    line[3] = line[3].strip()
    try:
        line[4] = datetime.strptime(line[4].strip(), '%M:%S').time()
    except ValueError:
        # print ValueError
        continue
    line[5] = line[5].strip()
    line[6] = line[6].strip()
    line[7] = line[7].strip()
    line[8] = line[8].strip()
    try:
        line[9] = datetime.strptime(line[9].strip(), '%d-%b-%y')
    except ValueError:
        continue
    TableB.append(line)
    TableBMap[line[0]] = linNo - 1
    linNo += 1
f.close()

# Read Table D
# TableBSchema = Id,Album,Genres,Label,Time,TrackName,Price,Artist,Released
f = open('assets/tableD.csv', 'r')
reader = csv.reader(f)
TableD = []
TableDMap = {}
linNo = 0
for line in reader:
    if linNo == 0:
        linNo += 1
        continue

    line[0] = line[0].strip()
    line[1] = line[1].strip()
    line[2] = line[2].strip()
    line[3] = line[3].strip()
    # try:
    line[4] = datetime.strptime(line[4].strip(), '%M:%S').time()
    # except ValueError:
    #     # print ValueError
    #     continue
    line[5] = line[5].strip()
    line[6] = line[6].strip()
    line[7] = line[7].strip()
    line[8] = line[8].strip()
    # try:
    line[9] = datetime.strptime(line[9].strip(), '%d-%b-%y')
    # except ValueError:
    #     continue
    TableD.append(line)
    TableDMap[line[0]] = linNo - 1
    linNo += 1
f.close()

# Go through GT and look for tuples where Matching flag=1
MatchingData = []
for data in GoldenData:
    if data[-1] == 1:
        MatchingData.append(data)

# Schema of MatchingData = [GenId, IdA, IdB, ArtistA, TrackNameA, ReleasedA, TimeA, ArtistB, TrackNameB, ReleasedB, TimeB, M]
# First row: [0, 1, 's_927', 'Taylor Swift', 'Welcome To New York', datetime.datetime(2014, 10, 27, 0, 0),
# datetime.time(0, 3, 32), 'Taylor Swift', 'Welcome To New York', datetime.datetime(2014, 10, 27, 0, 0), datetime.time(0, 3, 32), 1]


TableE = []
Erow0 = ['IdE', 'IdA', 'IdB', 'Album', 'Genres', 'Label', 'Time', 'TrackName', 'Price', 'Artist', 'Released', 'Rating', 'IdD', 'Type']
TableE.append(Erow0)

for ind in range(len(MatchingData)):
    Erow = Erow0[:]
    Erow[0] = ind + 1
    Erow[1] = MatchingData[ind][1]
    Erow[2] = MatchingData[ind][2]

    IdA = MatchingData[ind][1]
    IdB = MatchingData[ind][2]

    # Compare album from 2 orginal tables
    if TableA[TableAMap[IdA]][1] == TableB[TableBMap[IdB]][1]:
        Erow[3] = TableA[TableAMap[IdA]][1]
    else:
        print str(ind + 1) + ' Conflict in attribute "Album"=> || Value in A: ' + TableA[TableAMap[IdA]][
            1] + '||  Value in B:' + TableB[TableBMap[IdB]][
                  1] + ' || Picking longer name into E and ValA if length is same.'
        print ''
        if len(TableA[TableAMap[IdA]][1]) > len(TableB[TableBMap[IdB]][1]):
            Erow[3] = TableA[TableAMap[IdA]][1]
        elif len(TableA[TableAMap[IdA]][1]) < len(TableB[TableBMap[IdB]][1]):
            Erow[3] = TableB[TableBMap[IdB]][1]
        else:
            Erow[3] = TableA[TableAMap[IdA]][1]

    # Compare genres from 2 original tables
    if TableA[TableAMap[IdA]][2] == TableB[TableBMap[IdB]][2]:
        Erow[4] = TableA[TableAMap[IdA]][2]
    else:
        print str(ind + 1) + ' Conflict in attribute "Genres"=>|| Value in A: ' + TableA[TableAMap[IdA]][
            2] + ' || Value in B:' + TableB[TableBMap[IdB]][
                  2] + ' || Picking longer name into E and ValA if length is same.'
        print ''
        if len(TableA[TableAMap[IdA]][2]) > len(TableB[TableBMap[IdB]][2]):
            Erow[4] = TableA[TableAMap[IdA]][2]
        elif len(TableA[TableAMap[IdA]][2]) < len(TableB[TableBMap[IdB]][2]):
            Erow[4] = TableB[TableBMap[IdB]][2]
        else:
            Erow[4] = TableA[TableAMap[IdA]][2]

    # Compare labels from the two original tables
    if TableA[TableAMap[IdA]][3] == TableB[TableBMap[IdB]][3]:
        Erow[5] = TableA[TableAMap[IdA]][3]
    else:
        print str(ind + 1) + ' Conflict in attribute "Label"=>|| Value in A: ' + TableA[TableAMap[IdA]][
            3] + ' || Value in B:' + TableB[TableBMap[IdB]][
                  3] + ' || Picking longer name into E and ValA if length is same.'
        print ''
        if len(TableA[TableAMap[IdA]][3]) > len(TableB[TableBMap[IdB]][3]):
            Erow[5] = TableA[TableAMap[IdA]][3]
        elif len(TableA[TableAMap[IdA]][3]) < len(TableB[TableBMap[IdB]][3]):
            Erow[5] = TableB[TableBMap[IdB]][3]
        else:
            Erow[5] = TableA[TableAMap[IdA]][3]

    # Time can be compared from MatchingData
    if MatchingData[ind][6] == MatchingData[ind][10]:
        Erow[6] = MatchingData[ind][6]
    else:
        print str(ind + 1) + ' Conflict in attribute "Time"=>|| Value in A: ' + str(
            MatchingData[ind][6]) + ' || Value in B:' + str(
            MatchingData[ind][10]) + ' || Picking the larger time duration into E'
        print ''
        Erow[6] = max(MatchingData[ind][6], MatchingData[ind][10])

    # TrackName can be compared from MatchingData
    if MatchingData[ind][4] == MatchingData[ind][8]:
        Erow[7] = MatchingData[ind][4]
    else:
        print str(ind + 1) + ' Conflict in attribute "TrackName"=>|| Value in A: ' + MatchingData[ind][
            4] + ' || Value in B:' + MatchingData[ind][8] + ' || Picking longer name into E and ValA if length is same.'
        print ''
        if len(MatchingData[ind][4]) > len(MatchingData[ind][8]):
            Erow[7] = MatchingData[ind][4]
        elif len(MatchingData[ind][4]) < len(MatchingData[ind][8]):
            Erow[7] = MatchingData[ind][8]
        else:
            Erow[7] = MatchingData[ind][4]

    # Compare Price from the two original tables
    if TableA[TableAMap[IdA]][-3] == TableB[TableBMap[IdB]][-3]:
        Erow[8] = TableA[TableAMap[IdA]][-3]
    else:
        print str(ind + 1) + ' Conflict in attribute "Price"=> || Value in A: ' + TableA[TableAMap[IdA]][
            -3] + '  || Value in B:' + TableB[TableBMap[IdB]][-3] + ' || Picking ValA into TableE.'
        print ''
        Erow[8] = TableA[TableAMap[IdA]][-3]

    # Compare Artist from MatchingData
    if MatchingData[ind][3] == MatchingData[ind][7]:
        Erow[9] = MatchingData[ind][3]
    else:
        print str(ind + 1) + ' Conflict in attribute "Artist"=> || Value in A: ' + MatchingData[ind][
            3] + ' ||  Value in B:' + MatchingData[ind][
                  7] + ' || Picking longer name into E and ValA if length is same.'
        print ''
        if len(MatchingData[ind][3]) > len(MatchingData[ind][7]):
            Erow[9] = MatchingData[ind][3]
        elif len(MatchingData[ind][3]) < len(MatchingData[ind][7]):
            Erow[9] = MatchingData[ind][7]
        else:
            Erow[9] = MatchingData[ind][3]

    # Released can be compared from MatchingData
    if MatchingData[ind][5] == MatchingData[ind][9]:
        Erow[10] = MatchingData[ind][5]
    else:
        print str(ind + 1) + ' Conflict in attribute "Released"=> || Value in A: ' + str(
            MatchingData[ind][5]) + ' || Value in B:' + str(
            MatchingData[ind][9]) + ' || Picking earlier of the two dates into E'
        print ''
        Erow[10] = min(MatchingData[ind][5], MatchingData[ind][9])

    # Add rating from Table B
    Erow[11] = TableB[TableBMap[IdB]][5]

    Erow[12] = ''

    # Add explicit/clean label to each tuple
    if '[explicit]' in Erow[3].lower() or '[explicit]' in Erow[7].lower():
        Erow[13] = 'Explicit'
    else:
        Erow[13] = 'Clean'

    TableE.append(Erow)

print len(TableD)
offset = len(MatchingData)
for ind in range(len(TableD)):
    Erow = Erow0[:]
    index = ind
    Erow[0] = index + 1 + offset
    Erow[1] = ''
    Erow[2] = ''

    # Compare album from 2 orginal tables
    Erow[3] = TableD[index][1]

    # Compare genres from 2 original tables
    Erow[4] = TableD[index][2]

    # Compare labels from the two original tables
    Erow[5] = TableD[index][3]

    # Time can be compared from MatchingData
    Erow[6] = TableD[index][4]

    # TrackName can be compared from MatchingData
    Erow[7] = TableD[index][6]

    # Compare Price from the two original tables
    Erow[8] = TableD[index][7]

    # Compare Artist from MatchingData
    Erow[9] = TableD[index][8]

    # Released can be compared from MatchingData
    Erow[10] = TableD[index][9]

    # Add rating from Table B
    Erow[11] = TableD[index][5]

    # Add ID from table D
    Erow[12] = TableD[index][0]

    # Add explicit/clean label to each tuple
    if '[explicit]' in Erow[3].lower() or '[explicit]' in Erow[7].lower():
        Erow[13] = 'explicit'
    else:
        Erow[13] = 'clean'

    TableE.append(Erow)

f = open('TableE.csv', 'wb')
wr = csv.writer(f)
for item in TableE:
    wr.writerow(item)
f.close()
