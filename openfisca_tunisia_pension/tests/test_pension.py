# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013 OpenFisca Team
# https://github.com/openfisca/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# The model variables are created by each country-specific package (cf function init_country())
# Note: The variables below are not inited (to None) here, to ensure that execution will fail when they are used before
# OpenFisca country-specific package is properly inited.# -*- coding:utf-8 -*-
# Created on 14 mai 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)


#import nose
import openfisca_tunisia_pension
openfisca_tunisia_pension.init_country()
from openfisca_core.simulations import ScenarioSimulation


def test_rsna():
    year = 2011 
    test_list = [ {"year": 2011,
                   "sal_mensuel": 1000,
                   "nb_trim_val": 50,
                   "age": 60,
                   "pension": 5400 },
                ]
    for dico in test_list:
        simulation = ScenarioSimulation()
        year = dico.pop("year")
        simulation.set_config(year = year, nmen = 1)
        simulation.set_param()
        test_case = simulation.scenario
        pension = dico.pop("pension")
        for key, val in dico.iteritems():
            if key in ["sal_mensuel"]:
                for i in range(10):
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
#             simulation.set_config(year = year, nmen = 1)
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

