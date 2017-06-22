# -*- coding: utf-8 -*-

import datetime


from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem


# Exceptionally for this test do not import TaxBenefitSystem from tests.base.
tax_benefit_system = TunisiaPensionTaxBenefitSystem()


def check_legislation_xml_file(year):
    compact_legislation = tax_benefit_system.get_legislation(year)

    assert compact_legislation is not None


def test_legislation_xml_file():
    for year in range(2006, datetime.date.today().year + 1):
        yield check_legislation_xml_file, year
