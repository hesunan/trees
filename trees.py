from math import log
import operator


def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet: #the the number of unique elements and their occurance
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2) #log base 2
    return shannonEnt


def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return dataSet, labels


def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]     #chop out axis used for splitting
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


def chooseBestFeatureTopSplit(dataSet):
    numFeatures = len(dataSet[0]) -1 #最后一列是标签  
    baseEntropy = calcShannonEnt(dataSet) #所有数据的信息熵
    bestInfoGainn = 0.0
    bestFeature = -1
    for i in range(numFeatures):#遍历不同的属性
        featList = [example[i] for example in dataSet] #取出每一列
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:#在第i个属性里，遍历第i个属性所有不同的属性值
            subDataSet = splitDataSet(dataSet,i,value) #划分数据 
            prob = len(subDataSet)/float(len(dataSet))  #len([[]]) 行数
            newEntropy += prob *calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestInfoGainn):
            bestInfoGainn = infoGain
            bestFeature = i
    return bestFeature


def majorityCnt(classList):
    classCount ={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1


def createTree(dataSet,labels):
    #mytree 是一个字典，key 是属性值，val 是类别或者是另一个字典，
    #如果val 是类标签，则该子节点就是叶子节点
    #如果val是另一个数据字典，则该节点是一个判断节点
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList): #类别完全相同，停止划分
        return classList[0]
    if len(dataSet[0])==1: #完全划分
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureTopSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet] # 某属性的所有取值
    uniqueVals = set(featValues)
    for value in uniqueVals :
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree


def classify(inputTree,featLabels,testVec):
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr) #将标签转化成索引
    for key in secondDict.keys():
        if testVec[featIndex] == key:  
            if type(secondDict[key]).__name__=='dict':
                classLabel = classify(secondDict[key],featLabels,testVec)
            else : classLabel = secondDict[key]#到达叶子节点，返回标签
    return classLabel


def storeTree(inputTree,filename):
    import pickle
    with open(filename,'wb') as f:
        pickle.dump(inputTree,f)
    
def grabTree(filename):
    import pickle
    with open(filename,'rb') as f:
        t = pickle.load(f)
    return t
