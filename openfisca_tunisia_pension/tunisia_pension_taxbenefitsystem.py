import glob
import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from openfisca_tunisia_pension import entities

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
EXTENSIONS_PATH = os.path.join(COUNTRY_DIR, 'extensions')
EXTENSIONS_DIRECTORIES = glob.glob(os.path.join(EXTENSIONS_PATH, '*/'))


class TunisiaPensionTaxBenefitSystem(TaxBenefitSystem):
    '''Tunisian pensions tax benefit system'''
    CURRENCY = 'DT'

    def __init__(self):
        super(TunisiaPensionTaxBenefitSystem, self).__init__(entities.entities)

        # We add to our tax and benefit system all the variables
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'variables'))

        # We add to our tax and benefit system all the legislation parameters defined in the  parameters files
        parameters_path = os.path.join(COUNTRY_DIR, 'parameters')
        self.load_parameters(parameters_path)
