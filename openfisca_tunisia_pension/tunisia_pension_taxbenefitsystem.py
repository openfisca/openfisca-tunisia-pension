# -*- coding: utf-8 -*-

import glob
import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from . import entities, scenarios

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
EXTENSIONS_PATH = os.path.join(COUNTRY_DIR, 'extensions')
EXTENSIONS_DIRECTORIES = glob.glob(os.path.join(EXTENSIONS_PATH, '*/'))


class TunisiaPensionTaxBenefitSystem(TaxBenefitSystem):
    """Tunisian pensions tax benefit system"""
    CURRENCY = u"DT"

    def __init__(self):
        TaxBenefitSystem.__init__(self, entities.entities)
        self.Scenario = scenarios.Scenario

        legislation_xml_file_path = os.path.join(COUNTRY_DIR, 'param', 'param.xml')
        self.add_legislation_params(legislation_xml_file_path)

        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'model'))
        for extension_dir in EXTENSIONS_DIRECTORIES:
            self.load_extension(extension_dir)
