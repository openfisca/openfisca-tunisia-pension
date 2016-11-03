# -*- coding: utf-8 -*-

from tunisia_pension_taxbenefitsystem import TunisiaPensionTaxBenefitSystem

CountryTaxBenefitSystem = TunisiaPensionTaxBenefitSystem


import os


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


def init_country(qt = False):
    """Add country-specific content to OpenFisca-Core package."""
    from openfisca_core.taxbenefitsystems import LegacyTaxBenefitSystem

    from . import decompositions, entities, scenarios

#    from .model import datatrees
    from .model import data  # Load input variables into entities. # noqa
    from .model import model  # Load output variables into entities. # noqa

    class TaxBenefitSystem(LegacyTaxBenefitSystem):
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
