  # -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 09:51:19 2019

@author: Anna
"""
import numpy as np
import math     
import upload as ul
import resistances as rs

data_dict = ul.dict_upload("C:/Users/anuri/Documents/InputData/Dictionary.csv")

# CLRTAP == MAPPING CRITICAL LEVELS FOR VEGETATION Revised Chapter 3 of the Manual on Methodologies and Criteria for Modelling and Mapping Critical Loads and Levels and Air Pollution Effects, Risks and Trends.
### FPHEN SIMPLE
#def fphen(day):
#    '''Fphen is a phenology function'''
#    if day>= data_dict["Astart_FD"] and day < data_dict["Aend_FD"]:
#        return 1
#    else:
#        return 0
    
 
def fphen(day):
    """ fphen is a phenology function. Method based on a fixed time interval. 
    From CLRTAP (2017), chap 3, pg 19-20"""
    if day >= data_dict["Astart_FD"] and day < data_dict["Astart_FD"] + data_dict["fphen_1FD"]:
        temp = (1-data_dict["fphen_a"])*((day -data_dict["Astart_FD"]) / data_dict["fphen_1FD"]) + data_dict["fphen_a"]    
    elif day >= (data_dict["Astart_FD"] + data_dict["fphen_1FD"]) and day <= data_dict["Aend_FD"] + data_dict["fphen_4FD"]:
        temp = 1
    elif day > data_dict["Aend_FD"] + data_dict["fphen_4FD"] and day <= data_dict["Aend_FD"]:
        temp = (1-data_dict["fphen_e"])*((data_dict["Aend_FD"] - day) / data_dict["fphen_4FD"]) + data_dict["fphen_e"]
    else:
        temp = 0
    return temp
    

def fleaf_light(R):
    """ fleaf_light is a function which describes leaf stomata respond to light
      From CLRTAP (2017), chap 3, pg 20"""    
    # PPFD = R/0.486263
    return(1 - math.e**(-data_dict["light_a"] * (R/0.486263)))

    
def SVP(T_C): 
    """SVP saturated water pressure. Different approaches. 
    temp = 0.611 kPa * math.e ** (17.502 * T[°C]/(T[°C] + 240.97[°C])) # From Campbell and Norman 2000 (CLRTAP 2017)
    temp = 0.61078 *math.e**(17.27*T[°C]/(T[°C]+237.3))) # Tetens formula in [Pa] https://en.wikipedia.org/wiki/Vapour_pressure_of_water
    temp = 610.7*(10**(7.5*T/(T+237.3))) # [Pa]
    T_C denotes air temperature [°C]""" 
    temp = 0.611 * math.e ** (17.502 * T_C/(T_C + 240.97))
    return temp 

def VPD(RHper, SVP):
    """Vapour pressure deficit. 
    CLRTAP 2017 [kPa]. 
    """
    return(100 - RHper)/100*SVP/1000 # [kPa] 

def fVPD(VPD):
    """fVPD Function of leaf stomata respond to air humidity.
    CLRTAP (2017) chap 3, pg 22"""
    temp = ((1 - data_dict["fmin"])*(data_dict["VPDmin"] - VPD)/(data_dict["VPDmin"] - data_dict["VPDmax"]) + data_dict["fmin"])
    temp = rs.apply_max(temp)
    temp = rs.apply_min(temp)
    return temp  

def ftemp(T_C):
    """ ftemp Function of leaf stomata respond to air temperature [°C]
    CLRTAP (2017) chap 3, pg 21
    T_C denotes air temperature [°C]"""
    bt = (data_dict["Tmax"] - data_dict["Topt"]) / (data_dict["Topt"] - data_dict["Tmin"])
    if (T_C > data_dict["Tmin"]) and (T_C < data_dict["Tmax"]):
        temp = ((T_C - data_dict["Tmin"]) / (data_dict["Topt"] - data_dict["Tmin"]))*((data_dict["Tmax"]- T_C) / (data_dict["Tmax"] - data_dict["Topt"]))**bt
        temp = rs.apply_max(temp)
        return temp
    else:
        return data_dict["fmin"]
 

def cO3_nmolm3(cO3_ppb, P_kPa, T_C):
    """Conversion function for ozone concentration from ppb to nmol*m-3  
    CLRTAP (2017) chap 3, pg 25
    P_kPa denotes air pressure [kPa], T_C denotes air temperature [°C]"""
    cO3_nmolm3 = cO3_ppb * P_kPa * 1000 / (8.31447 * (T_C + 273.15))
    return cO3_nmolm3