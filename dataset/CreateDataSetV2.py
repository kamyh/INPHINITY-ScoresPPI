# -*- coding: utf-8 -*-
"""
Created on Mon May  2 05:06:26 2016

@author: diogo
"""

import cPickle              # import module first
#import pylab as plt

import matplotlib as mpl
mpl.use('Agg')
#import matplotlib.pyplot as plt
import numpy as np
import csv
#from __future__ import division
import os.path


def createQtdScoreNoNormal():
    interIdPreced = vecId[0]
    vecResultFinal = []  
    vecResultsProv = []
    position = 0
    
    for idInter in vecId:
        if interIdPreced == idInter: 
            qtdScores = vecQtd[position]
            aux = 0
            while aux < qtdScores:
                vecResultsProv.append(vecScor[position])
                aux = aux +1
                
        else:
            vecIdsDS.append(interIdPreced)
            vecTypeClass.append(vecCla[position])
            
            
            interIdPreced = idInter
            print position
            vecResultFinal.append(vecResultsProv)
            vecResultsProv = []
            
            qtdScores = vecQtd[position]
            aux = 0
            while aux < qtdScores:
                vecResultsProv.append(vecScor[position])
                aux = aux +1
        position = position + 1
    return vecResultFinal


def createQtdScoreNormal(matValues):
    matNormalValues = []
    for interact in matValues:
        aux = len(interact)
        print "Nb Interaction: " + str(aux)
        vecNormalScore = []
        for valueInter in interact:
            auxScor = valueInter/aux
            vecNormalScore.append(auxScor)
        matNormalValues.append(vecNormalScore)
    return matNormalValues
            
def createVecSize(matValues):
    qtdInteractions = []
    for nmInteractions in matValues:
        qtdInteractions.append(len(nmInteractions))
    return qtdInteractions

def controlNumberInteractionsOnlyOne(vecListQtdInter, position):
    QtdInteractionInt = []   
    onlyZeros = 0
    for i in vecListQtdInter:
        QtdInteractionInt.append(int(i))
        if i == qtdInteractionsAll[position]:
            onlyZeros = 1
    if onlyZeros == 1 and typeConfig ==1:
        QtdInteractionInt = [0] * (len(vecListQtdInter)-3)
        QtdInteractionInt.insert(0,vecListQtdInter[0])
        QtdInteractionInt.insert(1,vecListQtdInter[1])
        QtdInteractionInt.insert(2,qtdInteractionsAll[position])
    return QtdInteractionInt
    

def writeFile(n, binsList, vecid, vecCla, pathFile, boolNormaliz):
    #binsList = bins.tolist()
    position = 0
    binsListR = [round(i,5) for i in binsList]
    
    if boolNormaliz == 1:
        binsListR = [format(i, '.8f') for i in binsListR]
    
    binsListR.insert(0, "ID_interaction")
    binsListR.insert(1, "Class_interactions")
    
    with open(pathFile, 'w') as outcsv:   
    #configure writer to write standard csv file
        writer = csv.writer(outcsv, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(binsListR)
        for idInteract, typeClass, listHisto in zip(vecid, vecCla,n ):
            listAux = listHisto.tolist()
            listAux.insert(0, typeClass)
            listAux.insert(0, idInteract)
        #Write item to outcsv
            #listAuxB = [int(i) for i in listAux]
            listAuxB = controlNumberInteractionsOnlyOne(listAux, position)
            writer.writerow(listAuxB)
            position = position +1

def creatVecNBins(matriceScores, Bins):
    matResultsBins = []
    matBinsNum = []
    for interaction in matriceScores:
        a, b = np.histogram(interaction, bins=Bins)
        matResultsBins.append(a)
        matBinsNum.append(b)
    return matResultsBins, matBinsNum

#CONFIGR USER#################################################################
def getUserConfigTypeDataSet():  
    aux = 1
    x = -1
    while (aux == 1):
        try:
            x = int(input("Use normal dataSet : (Yes = 1/ No = 0): "))
        except:
            print "Input not legal"
        if(x == 1 or x == 0 ):
            aux = 0
    return x

def getUserConfigBinds():  
    aux = 1
    x = -1
    while (aux == 1):
        try:
            x = int(input("Number of Bins (1) or Vector of Bins (2) :"))
        except:
            print "Input not legal"
        if(x == 1 or x == 2 ):
            aux = 0
    if(x == 1):
        aux = 1
        while(aux == 1):
            try:
                x = int(input("Number of Bins (1-90) :"))
            except:
                print "Input not legal"
            if(x>0 and x < 91):
                aux = 0
        return x, 1
    if(x == 2):
        aux = 1
        while(aux == 1):
            try:
                x = int(input("Quantity of Bins (1-90) :"))
            except:
                print "input not legal"
            if(x>0 and x < 91):
                aux = 0
        vecBins = []
        valueBin = -1
        while (aux < x):
            try:
                valueBin = int(input("Insert value : "))
            except:
                print "input not legal"
                valueBin = -1
            if (valueBin >= 0):
                vecBins.append(valueBin)
                aux= aux +1
        return vecBins, 2
        
def pathFilePickle():
    aux = 0
    while(aux == 0):
        filePath = raw_input("File path: ")
        result = os.path.isfile(filePath)
        if(result == True):
            return filePath
        else:
            print "File not exists"
            
def pathSaveFile():
    filePath = raw_input("Save file: ")
    return filePath
#END CONFIGR USER#############################################################

pathFile = pathFilePickle()

pathFileSave = pathSaveFile()

#chemain = '/home/diogo/Bureau/gradesdict.p'

#pathFileSave = '/home/diogo/Bureau/test.csv'



f = open(pathFile, 'r')   # 'r' for reading; can be omitted
vecId, vecCla, vecScor, vecQtd = cPickle.load(f)          # dump data to f
f.close()



vecId
vecIdsDS = []
vecTypeClass = []

vecQtdProteins = []


vecResultFinal = []
vecResultNormal = []

binsConfig, typeConfig = getUserConfigBinds()   

typeDataSet = getUserConfigTypeDataSet()

vecResultFinal = createQtdScoreNoNormal()

qtdInteractionsAll = createVecSize(vecResultFinal)

if (typeDataSet == 1):
    vecResultNormal = createQtdScoreNormal(vecResultFinal)




qtdScoresHisto = []
SepHisto = []

print binsConfig

if(typeDataSet == 1):
    qtdScoresHisto, SepHisto = creatVecNBins(vecResultNormal, binsConfig)
else:
    qtdScoresHisto, SepHisto = creatVecNBins(vecResultFinal, binsConfig)


len(vecResultFinal[0])



vecNumBins = len(qtdScoresHisto[0])
aux = 0
auxVec = []
while(aux < vecNumBins):
    auxVec.append(aux)
    aux = aux +1
writeFile(qtdScoresHisto, auxVec, vecIdsDS, vecTypeClass, pathFileSave, 0)  




#yyy, zzz = creatVecNBins(vecResultFinal, 2)
#if(auxVector == 1):    
#    writeFile(qtdScoresHisto, binsConfig, vecIdsDS, vecTypeClass, pathFile, 0)
#else:
#    vecNumBins = binsConfig
#    aux = 0
#    auxVec = []
#    while(aux < vecNumBins):
#        auxVec.append(aux)
#        aux = aux +1
#    writeFile(qtdScoresHisto, auxVec[:-1], vecIdsDS, vecTypeClass, pathFile, 0)    
    
#qq = [1,2,3,4,5,6,7,8,9,00]
#qq[:-1]
#np.set_printoptions(suppress=True)


