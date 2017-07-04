# -*- coding: utf-8 -*-

from openfisca_core import periods
from openfisca_core.tools import assert_near
from . import base


def test_rsna():
    year = 2011
    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        period = periods.period(year),
        parent1 = dict(
            age = 60,
            trimestres_valides = 50,
            salaire = dict(
                [("{}".format(yr + 1), 12 * 1000) for yr in range(2014 - 40, 2014)]
                ),
            ),
        ).new_simulation(debug = True)

    assert_near(simulation.calculate_add('salaire_reference_rsna', period = year), 12000, .001)
    assert_near(simulation.calculate_add('pension_rsna', period = year), 5400, 1)


if __name__ == '__main__':
    test_rsna()
