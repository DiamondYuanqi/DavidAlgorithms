
import numpy as np
import pandas as pd
import random
import csv
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from graphviz import Digraph
#计算熵
def calcEntropy(dataSet):
    mD = len(dataSet)
    dataLabelList = [x[-1] for x in dataSet]
    dataLabelSet = set(dataLabelList)
    ent = 0
    for label in dataLabelSet:
        mDv = dataLabelList.count(label)
        prop = float(mDv) / mD
        ent = ent - prop * np.math.log(prop, 2)

    return ent

# # 拆分数据集
# # index - 要拆分的特征的下标
# # feature - 要拆分的特征
# # 返回值 - dataSet中index所在特征为feature，且去掉index一列的集合
def splitDataSet(dataSet, index, feature):
    splitedDataSet = []
    mD = len(dataSet)
    for data in dataSet:
        if(data[index] == feature):
            sliceTmp = data[:index]
            sliceTmp.extend(data[index + 1:])
            splitedDataSet.append(sliceTmp)
    return splitedDataSet

#根据信息增益 - 选择最好的特征
# 返回值 - 最好的特征的下标
def chooseBestFeature(dataSet):
    entD = calcEntropy(dataSet)
    mD = len(dataSet)
    featureNumber = len(dataSet[0]) - 1
    maxGain = -100
    maxIndex = -1
    for i in range(featureNumber):
        entDCopy = entD
        featureI = [x[i] for x in dataSet]
        featureSet = set(featureI)
        for feature in featureSet:
            splitedDataSet = splitDataSet(dataSet, i, feature)  # 拆分数据集
            mDv = len(splitedDataSet)
            entDCopy = entDCopy - float(mDv) / mD * calcEntropy(splitedDataSet)
        if(maxIndex == -1):
            maxGain = entDCopy
            maxIndex = i
        elif(maxGain < entDCopy):
            maxGain = entDCopy
            maxIndex = i

    return maxIndex

# 寻找最多的，作为标签
def mainLabel(labelList):
    labelRec = labelList[0]
    maxLabelCount = -1
    labelSet = set(labelList)
    for label in labelSet:
        if(labelList.count(label) > maxLabelCount):
            maxLabelCount = labelList.count(label)
            labelRec = label
    return labelRec

#生成决策树
# featureNamesSet 是featureNames取值的集合
# labelListParent 是父节点的标签列表
def createDecisionTree(dataSet, featureNames):
    labelList = [x[-1] for x in dataSet]
    if(len(dataSet[0]) == 1): #没有可划分的属性了
        return mainLabel(labelList)  #选出最多的label作为该数据集的标签
    elif(labelList.count(labelList[0]) == len(labelList)): # 全部都属于同一个Label
        return labelList[0]

    bestFeatureIndex = chooseBestFeature(dataSet)
    bestFeatureName = featureNames.pop(bestFeatureIndex)
    myTree = {bestFeatureName: {}}
    featureList = [x[bestFeatureIndex] for x in dataSet]
    featureSet = set(featureList)
    for feature in featureSet:
        featureNamesNext = featureNames[:]
        splitedDataSet = splitDataSet(dataSet, bestFeatureIndex, feature)
        myTree[bestFeatureName][feature] = createDecisionTree(splitedDataSet, featureNamesNext)
    return myTree

def createFullDecisionTree(dataSet, featureNames, featureNamesSet, labelListParent):
    labelList = [x[-1] for x in dataSet]
    if(len(dataSet) == 0):
        return mainLabel(labelListParent)
    elif(len(dataSet[0]) == 1): #没有可划分的属性了
        return mainLabel(labelList)  #选出最多的label作为该数据集的标签
    elif(labelList.count(labelList[0]) == len(labelList)): # 全部都属于同一个Label
        return labelList[0]

    bestFeatureIndex = chooseBestFeature(dataSet)
    #print('index',bestFeatureIndex)
    bestFeatureName = featureNames.pop(bestFeatureIndex)
    myTree = {bestFeatureName: {}}
    featureList = featureNamesSet.pop(bestFeatureIndex)
    #print('ss',featureList)
    featureSet = set(featureList)
    #print('featureSet',featureSet)
    for feature in featureSet:
        featureNamesNext = featureNames[:]
        #print('featureNamesNext',featureNamesNext)
        featureNamesSetNext = featureNamesSet[:][:]
        #print('featureNamesSetNext',featureNamesSetNext)
        splitedDataSet = splitDataSet(dataSet, bestFeatureIndex, feature)
        myTree[bestFeatureName][feature] = createFullDecisionTree(splitedDataSet, featureNamesNext, featureNamesSetNext, labelList)
    return myTree


def readWatermelonDataSet():

    ifile = open(r'/Users/yuanqi8099/Downloads/data/data3.txt',encoding='UTF-8')
    #print(ifile)
    featureName = ifile.readline()  #表头
    featureName = featureName.rstrip("\n")
    #print(featureName)
    featureNames = (featureName.split(' ')[0]).split('\t')
    #print(featureNames)
    lines = ifile.readlines()
    dataSet = []
    for line in lines:
        tmp = line.split('\n')[0]
        #print('tmp',tmp)
        tmp = tmp.split('\t')
        dataSet.append(tmp)
    random.shuffle(dataSet)
    dlen = int(len(dataSet) * 2 / 3)
    testDlen = len(dataSet) - dlen
    D = dataSet[0:dlen]
    #print('d',D)
    testD = dataSet[dlen:len(dataSet)]



    labelList = [x[-1] for x in D]
    #print('labelList',labelList)
    #获取featureNamesSet
    featureNamesSet = []
    for i in range(len(D[0]) - 1):
        col = [x[i] for x in D]
        colSet = set(col)
        featureNamesSet.append(list(colSet))
    #print('saa',featureNamesSet)

    return D, featureNames, featureNamesSet,labelList,testD

def tree_predict(tree, data):
  #print(data)
  feature = list(tree.keys())[0]#取树第一个结点的键（特征）
  #print(feature)
  label = data[feature]#该特征下所有属性
  next_tree = tree[feature][label]#下一个结点树
  if type(next_tree) == str:#如果是个字符串
    return next_tree
  else:
    return tree_predict(next_tree, data)

class TreeViewer:
    def __init__(self):
        self.id_iter = map(str, range(0xffff))
        self.g = Digraph('G', filename='decisionTree.gv4')

    def create_node(self, label, shape=None):
        id = next(self.id_iter)
        self.g.node(name=id, label=label, shape=shape, fontname="Microsoft YaHei")
        return id

    def build(self, key, node, from_id):
        for k in node.keys():
            v = node[k]
            if type(v) is dict:
                first_attr = list(v.keys())[0]
                id = self.create_node(first_attr+"？", shape='box')
                self.g.edge(from_id, id, k, fontsize = '12', fontname="Microsoft YaHei")
                self.build(first_attr, v[first_attr], id)
            else:
                id = self.create_node(v)
                self.g.edge(from_id, id, k, fontsize = '12', fontname="Microsoft YaHei")

    def show(self, root):
        first_attr = list(root.keys())[0]
        id = self.create_node(first_attr+"？", shape='box')
        self.build(first_attr, root[first_attr], id)
        self.g.view()

def main():
    #读取数据
    pingjun=0.0
    for i in range(1,11):
        dataSet, featureNames, featureNamesSet,labelList,testD = readWatermelonDataSet()
       # print('daas',dataSet)
        tree=createFullDecisionTree(dataSet, featureNames,featureNamesSet,labelList)
        tree2=createDecisionTree(dataSet, featureNames)
        #print('tree2',tree2)
       # print(tree)
        train= pd.DataFrame(dataSet, columns=['y1','y2','y3','y4','class'])
        print('train',train)
        test=pd.DataFrame(testD, columns=['y1','y2','y3','y4','class'])
        print('test', test)
        feature = list(train.columns[:])
        print('feat',feature)

        y_predict = test.apply(lambda x: tree_predict(tree, x), axis=1)
        label_list = test.iloc[:, -1]
        score = accuracy_score(label_list, y_predict)
        pingjun+=score
        print('第'+repr(i)+'次补全分支准确率为：' + repr(score * 100) + '%')
    print("平均准确率为："+repr(pingjun*10)+'%')
    viewer = TreeViewer()
    viewer.show(tree)

if __name__ == "__main__":
    main()




