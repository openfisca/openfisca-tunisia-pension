'''
Created on 2013/09/05

@author: mahdi.barouni
'''
from pandas import  HDFStore 
from pandas.io.stata import read_stata
import os


def test():
    year = 2010
    DATA_DIR = "D:/Dossier CRESS/Micro simulation"
    stata_filename = "pension2010.dta"
    filename = os.path.join(DATA_DIR,stata_filename)
    df = read_stata(filename)
    
    hdf5_filename = "survey.h5" 
    store = HDFStore(hdf5_filename)
    store['survey_'+ str(year)] = df
    
    print store


def test2():
    year = 2010
    hdf5_filename = "survey.h5" 
    store = HDFStore(hdf5_filename)
    df = store['survey_'+ str(year)]
    print df
    
    

if __name__ == '__main__':
    test2()