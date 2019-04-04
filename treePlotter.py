 #-*- coding:utf-8 -*-
import matplotlib.pyplot as plt
#定义文本框跟箭头格式
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt,  xycoords='axes fraction',
             xytext=centerPt, textcoords='axes fraction',
             va="center", ha="center", bbox=nodeType, arrowprops=arrow_args )
    

def createPlot(): 
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    createPlot.ax1 = plt.subplot(111, frameon=False)  # no ticks
    # createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
    plotNode('a decision node',(0.5,0.1),(0.1,0.5),decisionNode)
    plotNode('a leaf node',(0.8,0.1),(0.3,0.8),leafNode)
    plt.show()
    
    
def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree)[0]#找到第一个节点
    secondDict = myTree[firstStr] #第二个节点
    for key in secondDict.keys(): #第二节点的字典的key 
        if type(secondDict[key]).__name__=='dict':  #判断第二节点是否为字典
            numLeafs += getNumLeafs(secondDict[key]) #第二节点是字典 ，递归调用getNum  
        else :numLeafs += 1 #第二节点不是字典，说明此节点是最后一个节点
    return numLeafs


def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree)[0]#找到第一个节点
    secondDict = myTree[firstStr] #第二个节点
    for key in secondDict.keys(): #第二节点的字典的key 
        if type(secondDict[key]).__name__=='dict':  #判断第二节点是否为字典
            thisDepth = 1 + getTreeDepth(secondDict[key]) #第二节点是字典 ，递归调用getNum  
        else :thisDepth = 1 #第二节点不是字典，说明此节点是最后一个节点
    if thisDepth > maxDepth: maxDepth =thisDepth
    return maxDepth


def retrieveTree(i):
    listOfTrees =[{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                  {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                  ]
    return listOfTrees[i]


def plotMidText(cntrPt, parentPt, txtString):#在父子节点间填充文本信息
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)


def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)  #叶子节点个数
    depth = getTreeDepth(myTree)  #树的高度
    firstStr =list(myTree)[0] 
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff) #按照叶子结点个数划分x轴
    plotMidText(cntrPt,parentPt,nodeTxt)
    plotNode(firstStr,cntrPt,parentPt,decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD  #plotTree.yOff  全局变量
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ =='dict':
            plotTree(secondDict[key],cntrPt,str(key))# 第二节点是字典，递归调用plotTree
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW #x方向计算结点坐标
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)#绘制子节点
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))#添加文本信息
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD #下次重新调用时恢复y


def createPlot(inTree): 
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)  # no ticks
    # createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5 / plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()