
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 09:31:08 2019

@author: Hanka
"""
import pandas as pd

# DATA UPLOADING
#def data_upload(adres):
#    aa = pd.read_excel(adres)    

# DICTIONARY UPLOADING
def dict_upload(adres):
    temp = pd.read_csv(adres, delimiter=";", decimal = ",", header = [0])
    #dataset = pd.read_csv("C:/Users/anuri/Documents/InputData/Dictionary.csv", delimiter=";", decimal = ",", header = [0])
# decimal = "," # v povodnom dokumente oznacujeme desatinnu ciarku ciarkou, robilo to šarapatu
    # teraz uz nebude treba menit string na float, lebo uz cisla rozpozna ako cisla
    dataDict = temp.loc[:,["Name","Value"]]
#dataDict = dataset.loc[:,['Name','Value']]
#dataDict.loc[2,'Value']
    dic = dataDict.set_index('Name')['Value'].to_dict()
    for key,val in dic.items():
        exec(key + '=val')
    return dic
    


#def dictionary(data_dict):
#    dataDict = data_dict.loc[:,["Name","Value"]]
#dataDict = dataset.loc[:,['Name','Value']]
#dataDict.loc[2,'Value']
#    dic = dataDict.set_index('Name')['Value'].to_dict()
#    for key,val in dic.items():
#        exec(key + '=val')
#    return dic 
    