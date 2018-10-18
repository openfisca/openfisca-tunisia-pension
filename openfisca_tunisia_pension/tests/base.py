from openfisca_tunisia import TunisiaTaxBenefitSystem

# Extend tunisia tax_benefit_system
tax_benefit_system = TunisiaTaxBenefitSystem()
tax_benefit_system.load_extension("openfisca_tunisia_pension")


__all__ = [
    'tax_benefit_system',
    ]
