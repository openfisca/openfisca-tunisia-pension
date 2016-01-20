# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
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

import os


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


def init_country(qt = False):
    """Add country-specific content to OpenFisca-Core package."""
    from openfisca_core.taxbenefitsystems import XmlBasedTaxBenefitSystem

    from . import decompositions, entities, scenarios

#    from .model import datatrees
    from .model import data  # Load input variables into entities. # noqa
    from .model import model  # Load output variables into entities. # noqa

    class TaxBenefitSystem(XmlBasedTaxBenefitSystem):
        """Tunisian tax benefit system"""
        # AGGREGATES_DEFAULT_VARS = AGGREGATES_DEFAULT_VARS
        check_consistency = None  # staticmethod(utils.check_consistency)
#        columns_name_tree_by_entity = datatrees.columns_name_tree_by_entity
        CURRENCY = u"DT"

        DECOMP_DIR = os.path.dirname(os.path.abspath(decompositions.__file__))
        DEFAULT_DECOMP_FILE = decompositions.DEFAULT_DECOMP_FILE
        entity_class_by_key_plural = dict(
            (entity_class.key_plural, entity_class)
            for entity_class in entities.entity_class_by_symbol.itervalues()
            )
        legislation_xml_file_path = os.path.join(COUNTRY_DIR, 'param', 'param.xml')

        Scenario = scenarios.Scenario

    return TaxBenefitSystem
