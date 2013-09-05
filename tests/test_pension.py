# -*- coding:utf-8 -*-
# Created on 14 mai 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)

import nose
from src.lib.simulation import ScenarioSimulation
from datetime import datetime


def test_rsna():
    
    
    year = 2011
    country = "tunisia_pension"
    
    
    test_list = [ {"year" : 2011, "sal_mensuel": 1000, "nb_trim_val": 50, "age": 60, "pension": 5400 },
                 ]

    for dico in test_list:
        simulation = ScenarioSimulation()
        year = dico.pop("year")
        simulation.set_config(year = year, country = country, nmen = 1)
        simulation.set_param()
        test_case = simulation.scenario
        pension = dico.pop("pension")
        for key, val in dico.iteritems():
            if key in ["sal_mensuel"]:
                for i in range(10): 
                    print "sal" + str(i)
                    test_case.indiv[0].update({"sal" + str(i): val*12})
            else:
                test_case.indiv[0].update({key: val})

        df = simulation.get_results_dataframe(index_by_code=True)
        if not abs(df.loc["pension_rsna"][0] - pension) < 1:
            print year
            print "OpenFisca :", abs(df.loc["pension_rsna"][0])
            print "Real value :", pension
        
        assert abs(df.loc["pension_rsna"][0] - pension) < 1 

    
# 
# 
# def test_rsna():
#     """
#     test  
#     """
#     country = 'tunisia_pension'
#     dico = { 
#             "sal0": [
#             {"year" : 2011, "amount": 20000, "pension_rsna": -1181 },
#             ]
#             }
# 
#     
#     for revenu, test_list in dico.iteritems():        
#         for item in test_list: 
#             year = item["year"]
#             amount = item["amount"]
#             pension_rsna = item["pension_rsna"]
#             simulation = ScenarioSimulation()
#             simulation.set_config(year = year, country = country, nmen = 1)
#             simulation.set_param()
#             test_case = simulation.scenario
#             
#             test_case.indiv[0].update({"nb_trim_val": 50})
#             test_case.indiv[0].update({revenu: amount})
#             
#             df = simulation.get_results_dataframe(index_by_code=True)
#             print df
#             if not abs(df.loc["pension_rsna"][0] - pension_rsna) < 1:
#                 print year
#                 print revenu
#                 print amount
#                 print "OpenFisca :", abs(df.loc["pension_rsna"][0])
#                 print "Real value :", pension_rsna
#             
#             assert abs(df.loc["pension_rsna"][0] - pension_rsna) < 1 


if __name__ == '__main__':
   

    test_rsna()
    
#    nose.core.runmodule(argv=[__file__, '-v', '-i test_*.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)

