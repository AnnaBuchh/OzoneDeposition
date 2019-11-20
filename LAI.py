# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 08:57:12 2019
  
@author: Hanka
"""

import numpy as np
import pandas as pd
import upload as ul

data_dict = ul.dict_upload("C:/Users/anuri/Documents/InputData/Dictionary.csv")

# Pre nepriestupný rok
r = np.arange(1,366,1)
SGS, EGS = int(data_dict["Astart_FD"]), int(data_dict["Aend_FD"])
LAIp_a, LAIp_b = int(data_dict["LAI_1"]), int(data_dict["LAI_2"])
LAI_a, LAI_b, LAI_c, LAI_d = data_dict["LAI_a"], data_dict["LAI_b"], data_dict["LAI_c"], data_dict["LAI_d"]

# LAI parameters LAI_a - LAI_2 set up according Simpson 2003         (NWSEDI DOKONALE!!..)
LAI = np.full(365,np.NaN)

LAI[:SGS - 1]=LAI_a
for i in range(LAIp_a + 1):
    LAI[SGS + i - 1] = ((LAI_b-LAI_a)*i/LAIp_a+LAI_a)
    #print('LAI = ', LAI[SGS+i])

for i in range(EGS - SGS - LAIp_a - LAIp_b + 1):
    LAI[SGS + LAIp_a + i - 1] = LAI_b +(LAI_c-LAI_b)*i/(EGS - SGS - LAIp_a - LAIp_b)
    #print('LAI = ', LAI[SGS + LAIp_a +i])

for i in range(LAIp_b + 1):
    LAI[EGS - LAIp_b + i - 1] = LAI_c +(LAI_d-LAI_c)*i/LAIp_b
    #print('LAI = ', LAI[EGS - LAIp_b +i])

LAId = LAI 
LAI[EGS:]=LAI_d

LAI = pd.Series(LAI)
LAI = LAI.repeat(repeats = 24)
LAI.index = range(8760)
# ZATIAL!!!
SAI = LAI + 1