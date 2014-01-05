# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
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


import collections

from openfisca_core.columns import IntCol, EnumCol, BoolCol, AgesCol
from openfisca_core.utils import Enum


QUIFOY = Enum(['vous', 'conj', 'enf1','enf2','enf3','enf4','enf5','enf6','enf7','enf8','enf9'])
QUIMEN = Enum(['pref', 'cref', 'enf1','enf2','enf3','enf4','enf5','enf6','enf7','enf8','enf9'])
REG = Enum(['rsna', 'rsa', 'rsaa', 'rtns', 'rtte', 're', 'rtfr', 'raic', 'cnrps_sal', 'cnrps_pen'])


# raic -> raci

# Socio-economic data
# Donnée d'entrée de la simulation à fournir à partir d'une enquète ou
# à générer avec un générateur de cas type
column_by_name = collections.OrderedDict((
    ('noi', IntCol()),
    ('idmen', IntCol()),
    ('idfoy', IntCol()),

    ('quimen', EnumCol(QUIMEN)),
    ('quifoy', EnumCol(QUIFOY)),

    ('statmarit', BoolCol()),
    ('loyer', IntCol()),

    ('sal0', IntCol()),
    ('sal1', IntCol()),
    ('sal2', IntCol()),
    ('sal3', IntCol()),
    ('sal4', IntCol()),
    ('sal5', IntCol()),
    ('sal6', IntCol()),
    ('sal7', IntCol()),
    ('sal8', IntCol()),
    ('sal9', IntCol()),
    ('sal10', IntCol()),

    ('age', AgesCol(default = 65)),
    ('nb_trim_val', IntCol()),
    ('regime', EnumCol(REG)),
    ))

for name, column in column_by_name.iteritems():
    if column.label is None:
        column.label = name
    assert column.name is None
    column.name = name
