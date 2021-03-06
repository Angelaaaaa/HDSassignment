# read file and make it pandas

import pandas as pd



practicesName = "T201804ADDR+BNFT.CSV"
presFile = "T201804PDPI+BNFT.CSV"
# presFile = "test.CSV"
# columnNamePrac = ['code','surgury','surgery','address','city','county','postcode']
patiFile = "gp-reg-pat-prac-all.csv"

def readToPandas(name,columnName):
    if(columnName==None):
        pandasInfo = pd.read_csv(name)
    else:
        pandasInfo = pd.read_csv(name,skiprows=1, names =columnName)
    return pandasInfo

# return london practice code as list
def getCityPractice(practiceInfo,city):
    practiceInfo['city'] = practiceInfo['city'].str.strip()
    practiceInfo['county'] = practiceInfo['county'].str.strip()
    cityPrac = practiceInfo.loc[(practiceInfo['city'] == city) | (practiceInfo['county'] == city)]
    cityPracList = cityPrac['code'].tolist()
    # print(len(cityPrac))
    return cityPracList


# get total patient number related to the practiselist
def getPatientNumber(practiceList,Q):
    pati = readToPandas(patiFile,None)
    patiNumDict = dict(zip(pati.CODE, pati.NUMBER_OF_PATIENTS))
    sum = 0
    errorList = []
    for paticode in practiceList:
        if(paticode in patiNumDict.keys()):
            sum = sum + patiNumDict[paticode]
        else:
            errorList.append(paticode)
    print('Q'+str(Q)+' 1).total num of patients: ' + str(sum))
    print('      doesnt exist practice: ' + str(errorList))

def getTotalPres(practiceList,Q):
    presColumn = [' SHA', 'PCT', 'PRACTICE', 'BNF CODE', 'BNF NAME', 'ITEMS  ', 'NIC', 'ACT_COST', 'QUANTITY', 'PERIOD',
                  'Null']
    presInfo = readToPandas(presFile,presColumn)
    presQuantity = presInfo[['PRACTICE', 'QUANTITY']]
    presQuantity = presQuantity.loc[presQuantity['PRACTICE'].isin(practiceList)][['PRACTICE','QUANTITY']]
    presQuantity = presQuantity[['PRACTICE', 'QUANTITY']]
    sum  = presQuantity['QUANTITY'].sum()
    print('Q'+str(Q)+' 2).total num of prescription : ' + str(sum))

def getTotalPresCost(practiceList,Q):
    presColumn = [' SHA', 'PCT', 'PRACTICE', 'BNF CODE', 'BNF NAME', 'ITEMS  ', 'NIC', 'ACT_COST', 'QUANTITY', 'PERIOD',
                  'Null']

    presInfo = readToPandas(presFile, presColumn)
    presCost = presInfo[['PRACTICE','QUANTITY', 'ACT_COST']]
    presCost = presCost.loc[presCost['PRACTICE'].isin(practiceList)][['PRACTICE', 'QUANTITY','ACT_COST']]
    presCost = presCost[['PRACTICE', 'QUANTITY','ACT_COST']]

    presCost['TOTAL_COST'] = presCost['QUANTITY']*presCost['ACT_COST']

    sum = presCost['TOTAL_COST'].sum()
    print('Q'+str(Q)+' 3).total cost of prescription : ' + str(sum))

def getFrequencyOfPres(practiceList,Q):
    presColumn = [' SHA', 'PCT', 'PRACTICE', 'BNF_CODE', 'BNF_NAME', 'ITEMS  ', 'NIC', 'ACT_COST', 'QUANTITY', 'PERIOD',
                  'Null']
    presInfo = readToPandas(presFile, presColumn)
    presFreq = presInfo[['PRACTICE','BNF_NAME','QUANTITY']]
    presFreqLn = presFreq.loc[presFreq['PRACTICE'].isin(practiceList)][['BNF_NAME','QUANTITY']]
    presFreqLn  = presFreqLn[['BNF_NAME','QUANTITY']]
    presFreqLn = presFreqLn.groupby('BNF_NAME').sum()
    presFreqLn = presFreqLn.sort_values('QUANTITY')


    print(presFreqLn.nlargest(10,'QUANTITY'))
    print(presFreqLn.nsmallest(10,'QUANTITY'))
    print('\n\n')

    # print(presFreqLn)

def getAllPresRelatedToChapter(chapNum):
    presColumn = [' SHA', 'PCT', 'PRACTICE', 'BNF_CODE', 'BNF_NAME', 'ITEMS  ', 'NIC', 'ACT_COST', 'QUANTITY', 'PERIOD',
                  'Null']
    presInfo = readToPandas(presFile, presColumn)
    presCode = presInfo[['BNF_CODE', 'QUANTITY','ACT_COST']]
    # find chapter related
    presCha = presCode.loc[lambda presCode: ((presCode.BNF_CODE > chapNum ) & (presCode.BNF_CODE < str(0)+str(int(chapNum)+1))), :]
    sum  = presCha['QUANTITY'].sum()
    print('Q3.total num of prescription related to chapter' + chapNum + ' is '+str(sum))

    presCha = presCha[['BNF_CODE', 'QUANTITY','ACT_COST']]
    presCha['TOTAL_COST'] = presCha['QUANTITY']*presCha['ACT_COST']

    totalcost = presCha['TOTAL_COST'].sum()
    print('Q3.total cost of prescription related to chapter' + chapNum + ' is '+str(totalcost))


#
# # Q1
# # get london practice names
# praclistLn = getCityPractice(readToPandas(practicesName,columnNamePrac),'LONDON')
#
# # 1).get total patient number
# getPatientNumber(praclistLn,1)
#
# # 2).get prescription data
# getTotalPres(praclistLn,1)
#
# # 3).get prescription total cost data
# getTotalPresCost(praclistLn,1)
#
# # 4).get prescription frequency
# getFrequencyOfPres(praclistLn,1)
#
#
# # Q2
# # get cambridge practice names
# praclistCA = getCityPractice(readToPandas(practicesName,columnNamePrac),'CAMBRIDGE')
#
# # 1).get total patient number
# getPatientNumber(praclistCA,2)
#
# # 2).get prescription data
# getTotalPres(praclistCA,2)
#
# # 3).get prescription total cost data
# getTotalPresCost(praclistCA,2)
#
# # 4).get prescription frequency
# getFrequencyOfPres(praclistCA,2)
#
# Q3
# 1).get quantity pres & get total cost related to chapter 2
# getAllPresRelatedToChapter('02')
#
# # 2).get quantity pres & get total cost related to chapter 4.2
# getAllPresRelatedToChapter('0402')

# Q4
# 1). total patients in practice and store in dictionary
# 2). total cost of a practice