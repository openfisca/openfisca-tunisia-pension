'''OpenFisca Tunisia Pension tax-benefit system.'''


import logging
import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from openfisca_tunisia_pension import entities
from openfisca_tunisia_pension.scripts_ast import script_ast


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))

logging.getLogger('numba.core.ssa').disabled = True
logging.getLogger('numba.core.byteflow').disabled = True
logging.getLogger('numba.core.interpreter').disabled = True

# Convert regimes classes to OpenFisca variables.
script_ast.main(verbose = False)


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


CountryTaxBenefitSystem = TunisiaPensionTaxBenefitSystem
