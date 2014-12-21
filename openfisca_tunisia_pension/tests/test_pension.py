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


import datetime


from openfisca_core.tools import assert_near
from . import base


def test_rsna():
#    test_list = [ {"year": 2011,
#                   "sal_mensuel": 1000,
#                   "nb_trim_val": 50,
#                   "age": 60,
#                   "pension": 5400 },

    year = 2011
    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        parent1 = dict(
            age = 60,  # birth = datetime.date(year - 60, 1, 1),
            nb_trim_val = 50,
            salaire = dict(
                [("{}".format(yr + 1), 1000) for yr in range(2014 - 40, 2014)]
                ),
            ),
        ).new_simulation(debug = True)
    assert_near(simulation.calculate('pension_rsna'), 5400, 1)



if __name__ == '__main__':

    test_rsna()

#    nose.core.runmodule(argv=[__file__, '-v', '-i test_*.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
