from openfisca_core.tools import assert_near

from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem


__all__ = [
    'assert_near',
    'tax_benefit_system',
    'TunisiaPensionTaxBenefitSystem',
    ]


tax_benefit_system = TunisiaPensionTaxBenefitSystem()
