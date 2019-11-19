# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 17:11:42 2019

@author: Hanka
"""


import numpy as np
import pandas as pd 
import functions as fn
import LAI
import flux
import resistances as rs
import upload as ul

data = pd.read_excel('C:/Users/anuri/Documents/DO3SE_PYTHON/SkuskyParametrov/2015outputSP.xlsx')

data_dict = ul.dict_upload("C:/Users/anuri/Documents/InputData/Dictionary.csv")

# neoriestupny rok
year = np.arange(1,366)
year = pd.Series(year)

fphen = year.apply(fn.fphen)
fphen = fphen.repeat(repeats = 24)
fphen.index = range(8760)
fphen
# FPHEN
dif_fphen = fphen - data["f_phen"]
print("FPHEN")
print("min = ", min(dif_fphen))
print("max = ", max(dif_fphen))

fleaf_light = data["R (Wh/m^2)"].apply(fn.fleaf_light) 
# Keďže empiricky sme videli, že počas väčšiny dní vynulovali prvú nenulovú hodnotu fleaf_light daného dňa, 
#preto vytvárame pole 'zoznam', kde indexy týchto prvých nenulových hodnôt zapíšeme
zoznam = []
for i in range(1, 8760):
    if fleaf_light[i] != 0 and fleaf_light[i - 1] == 0:
        zoznam.append(i)
        
# Vymazať vždy prvú hodnotu zo zoskupenia nenulových hodnôt...
for i in range(len(zoznam)):
    fleaf_light[zoznam[i]] = 0
# ale nie su vymazane prve hodnoty dna...

dif_fleaf_light = fleaf_light - data["f_light"]
print("fleaf_light")
print("min = ", min(dif_fleaf_light))
print("max = ", max(dif_fleaf_light))

dif_fleaf_light = fphen - data["leaf_f_light"]
print("fleaf_light")
print("min = ", min(dif_fleaf_light))
print("max = ", max(dif_fleaf_light))

VPD = fn.VPD(data["_RH%"], fn.SVP(data["Ts_C (C)"])) #### APLIKUJ NAJPRV RH_per, potom Teplotu
print("VPD")
dif_VPD = VPD - data["VPD (kPa)"]
print("min = ", min(dif_VPD))
print("max = ", max(dif_VPD))

fVPD = VPD.apply(fn.fVPD)
print("fVPD")
dif_fVPD = fVPD - data["f_VPD"]
print("min = ", min(dif_fVPD))
print("max = ", max(dif_fVPD))

ftemp = data["Ts_C (C)"].apply(fn.ftemp)
print("ftemp")
dif_ftemp = ftemp - data["f_temp"]
print("min = ", min(dif_ftemp))
print("max = ", max(dif_ftemp))

print("LAI")
dif_LAI = LAI.LAI - data["LAI"]
print("min = ", min(dif_LAI))
print("max = ", max(dif_LAI))

print("u_star")
vu_starF = np.vectorize(rs.u_star)
vu_star = vu_starF(data["uh_zR (m/s)"])
dif_u_star = vu_star - data["u* (m/s)"]
print("min = ", min(dif_u_star))
print("max = ", max(dif_u_star))

print("Rinc")
dif_Rinc = rs.Rinc(LAI.SAI,vu_star) - data["Rinc (s/m)"]
print("min = ", min(dif_Rinc))
print("max = ", max(dif_Rinc))

print("Rb")
dif_Rb = rs.Rb(vu_star) - data["Rb (s/m)"]
print("min = ", min(dif_Rb))
print("max = ", max(dif_Rb))

vrstol = np.vectorize(rs.rstol)
aaa = pd.Series(vrstol(gstol))
print("Rsur")
dif_Rsur = rs.Rsur(LAI.LAI, aaa , Rinc) - data["Rsur (s/m)"]
print("min = ", min(dif_Rsur))
print("max = ", max(dif_Rsur))


gstol = rs.gstol(fphen, fleaf_light, fVPD, ftemp)
print("gstol")
dif_gstol = gstol - data["Gsto_l (mmol/m^2/s)"]
print("min = ", min(dif_gstol))
print("max = ", max(dif_gstol))


print("cO3_nmolm3")
cO3_nmolm3 = fn.cO3_nmolm3(data["O3_zR (ppb)"], data["P (kPa)"], data["Ts_C (C)"])
dif_cO3_nmol = cO3_nmolm3 - data["O3 (nmol/m^3)"]
print("min = ", min(dif_cO3_nmol))
print("max = ", max(dif_cO3_nmol))

print("cO3_nmolm3")
cO3_nmolm3 = fn.cO3_nmolm3(data["O3_zR (ppb)"], data["P (kPa)"], data["Ts_C (C)"])
dif_cO3_nmol = cO3_nmolm3 - data["O3 (nmol/m^3)"]
print("min = ", min(dif_cO3_nmol))
print("max = ", max(dif_cO3_nmol))
