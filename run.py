# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd 
import functions as fn
import LAI
import flux
import resistances as rs

import upload as ul

# f1(f2(c,d),b)

data = pd.read_excel('C:/Users/anuri/Documents/DO3SE_PYTHON/SkuskyParametrov/2015outputSP.xlsx')

data_dict = ul.dict_upload("C:/Users/anuri/Documents/InputData/Dictionary.csv")

# nepriestupny rok
year = np.arange(1,366)
year = pd.Series(year)

fphen = year.apply(fn.fphen)
fphen = fphen.repeat(repeats = 24)
fphen.index = range(8760)

fleaf_light = data["R (Wh/m^2)"].apply(fn.fleaf_light) 
# Keďže empiricky sme videli, že počas väčšiny dní vynulovali prvú nenulovú hodnotu fleaf_light daného dňa, 
#preto vytvárame pole 'zoznam', kde indexy týchto prvých nenulových hodnôt zapíšeme
zoznam = []
for i in range(1, 8760):
    if fleaf_light[i] != 0 and fleaf_light[i - 1] == 0:
        zoznam.append(i)
        
# Vymazať vždy prvú hodnotu zo zoskupenia nenulových hodnôt...
#for i in range(len(zoznam)):
 #   fleaf_light[zoznam[i]] = 0
# ale nie su vymazane prve hodnoty dna...

VPD = fn.VPD(data["_RH%"], fn.SVP(data["Ts_C (C)"])) #### APLIKUJ NAJPRV RH_per, potom Teplotu
fVPD = VPD.apply(fn.fVPD)


ftemp = data["Ts_C (C)"].apply(fn.ftemp)

gext = 1/ data_dict["rext"]

gstol = rs.gstol(fphen, fleaf_light, fVPD, ftemp)


#vu_star = np.vectorize(rs.u_star)
#Rinc = rs.Rinc(LAI.SAI,vu_star(data["uh_zR (m/s)"]))

vu_starF = np.vectorize(rs.u_star)
vu_star = vu_starF(data["uh_zR (m/s)"])
Rinc = rs.Rinc(LAI.SAI,vu_star)

#vrstol = np.vectorize(rs.rstol)
#vrstol = pd.Series(vrstol(gstol))

vrstol = np.vectorize(rs.rstol)
vrstol = pd.Series(vrstol(gstol))

Rsur = rs.Rsur(LAI.LAI, vrstol , Rinc)
#problem, teraz je LAI array, preto Raur nevie ktore z LAI pouzit...
#teraz rieš ine...
cO3_nmolm3 = fn.cO3_nmolm3(data["O3_zR (ppb)"], data["P (kPa)"], data["Ts_C (C)"])

Fst_l = flux.Fstl(cO3_nmolm3, Rsur, rs.Rb(vu_star), gstol)


POD0, POD1 = 0, 0
for i in range(1,8760):
    POD0 = Fst_l[i]*0.0036 + POD0
    if Fst_l[i] > 1:
        POD1 = 0.0036*(Fst_l[i]-1)+POD1

print("POD0 = ", POD0)
print("POD1 = ", POD1)
            #print("Fst_l = ", Fst_l)