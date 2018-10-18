# -*- coding: utf-8 -*-

from openfisca_core.tools import assert_near
from openfisca_tunisia import TunisiaTaxBenefitSystem

# Extend tunisia tax_benefit_system
tax_benefit_system = TunisiaTaxBenefitSystem()
tax_benefit_system.load_extension("openfisca_tunisia_pension")


__all__ = [
    'assert_near',
    'tax_benefit_system',
    ]
