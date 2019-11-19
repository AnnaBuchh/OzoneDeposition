# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 11:37:33 2019

@author: Hanka
"""

import numpy as np
import pandas as pd
import math
import functions as fn
import upload as ul

data_dict = ul.dict_upload("C:/Users/anuri/Documents/InputData/Dictionary.csv")
k = data_dict["k"]

def u_star(u):
    """Friction velocity 
    Simpson et al. 2012
    [m s-1] minimal value of u_* is 0.03732. For our parametrisation:"""
    if (u == 0):
        temp = k/(math.log(3, math.e)*10)
    else:
        temp = u * k / math.log(3, math.e)    
    #temp = temp.replace(0,k/(math.log(3, math.e)*10)) # lebo ak u = 0, tak u* = 0.03732.... a nie 0 ako nám vychádza podľa vzorca 
    return temp


def Rb(u_star):
    """Quasi-laminar resistance
    Simpson et al. 2012: EMEP MSC-W model: description, eq. 53, Simpson 2003
    Sc is Schmidt number, Pr is Prandtl number, Di is diffusivity of ozone (Massman 1998)"""
    temp = 2 / (k * u_star) *(data_dict["Sc"] *10**4/ (data_dict["Di"] * 0.72))** (2/3)
    # Ked bude v dictionary Pr= 0.72 a Di = 0.15. Dovtedy povodne.  
    #temp = 2 / (k * u_star) *(data_dict["Sc"] *10**4/ (data_dict["Di"] * 0.72))** (2/3)
    return temp

def Rinc(SAI, u_star):
    """In-canopy resistance
    Erisman et al. 1974
    [s m-1]""" #lit. je v Simpson 2012, str. 7846
    temp = 14 * SAI * 20 / u_star
    return temp

def apply_max(index):
    return max(data_dict["fmin"], index)

def apply_min(index):
    return min(1, index)

def gstol(fphen, fleaf_light, fVPD, ftemp):
    """Based od Jarvis 1976 - The interpretation of the variations in leaf water potential and stomatal conductance found in canopies in the field.
    and improved by Emberson 2000, Simpson et al. 2012, CLRTAP 2017 (chap 3, pg 17)
    gstol and gmax [mmol O3 m-2 PLA s-1]"""
    temp = data_dict["gmax"] * fphen * fleaf_light * (ftemp * fVPD).apply(apply_max)#  max(fmin, ftemp * fVDP)
    return temp

def rstol(gstol):
    """ Stomatal resistance is reciprocal stomatal conductance, unit conversion is by conversion factor 41000.
    Maximal value of stomatal resistance is 100000. 
    
    [s m-1]"""   
    if gstol == 0:
        temp = 100000
    else:
        temp = 41000 / gstol
    return temp

def Rsur(LAI, rstol,  Rinc):
    """Aurface resistance to ozone deposition , it comprises of resistance of plant canopy and undeelying soil.
    Emberson 2001 Modelling and mapping ozone deposition in Europe
    [s m-1]
    rext is the external resistance of the exterior plant parts, Rinc is the land-cover specific in-canooy aerodynamic resistance,
    Rsoil = Rgs is the soil resistance to destruction or absorption at the ground surface"""
    if LAI == data_dict["LAI_a"] or LAI == data_dict["LAI_d"]:
        SAI = LAI
    else:
        SAI = LAI + 1
    temp = 1 / (LAI / rstol + SAI/data_dict["rext"] + 1/(Rinc + data_dict["Rsoil"]))
    return temp