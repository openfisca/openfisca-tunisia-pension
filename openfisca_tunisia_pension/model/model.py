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

from openfisca_core.columns import Prestation

from . import pension


prestation_by_name = collections.OrderedDict((
    ############################################################
    # Pensions
    ############################################################

    ('sal_ref_rsna', Prestation(pension._sal_ref_rsna, entity = "ind", label = u"Salaire de référence")),
    ('pension_rsna', Prestation(pension._pension_rsna, entity = "ind", label = u"Pension de retraite")),

    ('sal_ref_rsa', Prestation(pension._sal_ref_rsa, entity = "ind", label = u"Salaire de référence")),
    ('pension_rsa', Prestation(pension._pension_rsa, entity = "ind", label = u"Pension de retraite")),
    ))

for name, prestation in prestation_by_name.iteritems():
    if prestation.label is None:
        prestation.label = name
    assert prestation.name is None
    prestation.name = name
