# -*- coding:utf-8 -*-
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

"""
openFisca, Logiciel libre de simulation du système socio-fiscal français
Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

This file is part of openFisca.

    openFisca is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    openFisca is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with openFisca.  If not, see <http://www.gnu.org/licenses/>.
"""


from __future__ import division


from numpy import maximum as max_, minimum as min_, logical_not as not_


from openfisca_core import periods
from .base import *  # noqa


@reference_formula
class salaire_reference_rsa(SimpleFormulaColumn):
    column = FloatCol()
    entity_class = Individus
    label = u"Salaires de référence du régime des salariés agricoles"

    def function(self, simulation, period):
        # TODO: gérer le nombre d'année
        # TODO: plafonner les salaires à 2 fois le smag de l'année d'encaissement
        period = period.start.offset('first-of', 'month').period('year')
        base_declaration_rsa = 180
        base_liquidation_rsa = 300

        salaire = 0

        for year in range(period.start.year, period.start.year - 3, -1):
            print year
            print simulation.calculate('salaire', period = periods.period("year", year))
            salaire += simulation.calculate('salaire', period = periods.period("year", year))

        salaire = (salaire / 3) * base_liquidation_rsa / base_declaration_rsa
        return period, sal_ref_rsa


@reference_formula
class salaire_reference_rsna(SimpleFormulaColumn):
    column = FloatCol()
    entity_class = Individus
    label = u"Salaires de référence du régime des salariés non agricoles"

    def function(self, simulation, period):

        # TODO: gérer le nombre d'année
        # TODO: plafonner les salaires à 6 fois le smig de l'année d'encaissement

        period = period.start.offset('first-of', 'month').period('year')

        salaire = 0
        for year in range(period.start.year, period.start.year - 10, -1):
            salaire += simulation.calculate('salaire', period = periods.period("year", year))
        return period, salaire


@reference_formula
class pension_rsna(SimpleFormulaColumn):
    column = FloatCol()
    entity_class = Individus
    label = u"Pension des affiliés au régime des salariés non agricoles"

    def function(self, simulation, period):

        nb_trim_val = simulation.calculate('nb_trim_val', period = period)
        salaire_reference = simulation.calculate('salaire_reference_rsna', period = period)
#        regime = simulation.calculate('regime', period = period)
        age = simulation.calculate('age', period = period)

        taux_ann_base = simulation.legislation_at(period.start).pension.rsna.taux_ann_base
        taux_ann_sup = simulation.legislation_at(period.start).pension.rsna.taux_ann_sup
        duree_stage = simulation.legislation_at(period.start).pension.rsna.stage_derog
        age_elig = simulation.legislation_at(period.start).pension.rsna.age_dep_anticip
        periode_remp_base = simulation.legislation_at(period.start).pension.rsna.periode_remp_base
        plaf_taux_pension = simulation.legislation_at(period.start).pension.rsna.plaf_taux_pension
        smig = simulation.legislation_at(period.start).param_gen.smig_48h

        pension_min_sup = simulation.legislation_at(period.start).pension.rsna.pension_min.sup
        pension_min_inf = simulation.legislation_at(period.start).pension.rsna.pension_min.inf

        stage = nb_trim_val > 4 * duree_stage
        pension_min = (
            stage * pension_min_sup +
            not_(stage) * pension_min_inf
            )
        montant = generic_pension(nb_trim_val, salaire_reference, age, taux_ann_base, taux_ann_sup, duree_stage,
                                  age_elig, periode_remp_base, plaf_taux_pension, smig)

        elig_age = age > age_elig
        elig = stage * elig_age * (salaire_reference > 0)
        montant_percu = max_(montant, pension_min * smig)
        pension = elig * montant_percu
        return period, pension


def _pension_rsa(nb_trim_val, sal_ref_rsa, regime, age, _P):
    """
    Pension du régime des salariés agricoles
    """
    taux_ann_base = _P.pension.rsa.taux_ann_base
    taux_ann_sup = _P.pension.rsa.taux_ann_sup
    duree_stage = _P.pension.rsa.stage_requis
    age_elig = _P.pension.rsa.age_legal
    periode_remp_base = _P.pension.rsa.periode_remp_base
    plaf_taux_pension = _P.pension.rsa.plaf_taux_pension
    smag = _P.param_gen.smag * 25
    stage = nb_trim_val > 4 * duree_stage
    pension_min = _P.pension.rsa.pension_min
    sal_ref = sal_ref_rsa

    montant = generic_pension(nb_trim_val, sal_ref, age, taux_ann_base, taux_ann_sup, duree_stage,
                              age_elig, periode_remp_base, plaf_taux_pension, smag)

    elig_age = age > age_elig
    elig = stage * elig_age * (sal_ref > 0)
    montant_percu = max_(montant, pension_min * smag)
    pension = elig * montant_percu
    return pension


# Helper function

def generic_pension(nb_trim_val, sal_ref, age,
                    taux_ann_base, taux_ann_sup, duree_stage, age_elig,
                    periode_remp_base, plaf_taux_pension, smig):
    # stage = nb_trim_val > 4*duree_stage
    # elig_age = age > age_elig
    # elig = stage*elig_age*(sal_ref>0)
    taux_pension = (
        (nb_trim_val < 4 * periode_remp_base) * (nb_trim_val / 4 * taux_ann_base) +
        (nb_trim_val >= 4 * periode_remp_base) * (
            taux_ann_base * periode_remp_base +
            (nb_trim_val / 4 - periode_remp_base) * taux_ann_sup
            )
        )
    montant = min_(taux_pension, plaf_taux_pension) * sal_ref
    return montant






#
#def _pension(nb_trim_val, sal_ref, regime, age, _P):
#    """
#    Pension
#    """
#    taux_ann_base = _P.pension.rsna.taux_ann_base
#    taux_ann_sup  = _P.pension.rsna.taux_ann_sup
#    duree_stage = _P.pension.rsna.stage_derog
#    age_elig = _P.pension.rsna.age_dep_anticip
#    periode_remp_base = _P.pension.rsna.periode_remp_base
#    plaf_pension = _P.pension.rsna.plaf_taux_pension
#    smig = _P.param_gen.smig_48h
#    stage = nb_trim_val > 4 * duree_stage
#    pension_min = (stage)*_P.pension.rsna.pension_min.sup + not_(stage)*_P.pension.rsna.pension_min.inf
#
#    elig_age = age > age_elig
#    elig = stage * elig_age * (sal_ref > 0)
#    taux_pension = ( (nb_trim_val < 4 * periode_remp_base)*(nb_trim_val / 4 * taux_ann_base) +
#                       (nb_trim_val >= 4*periode_remp_base)*( taux_ann_base*periode_remp_base + (nb_trim_val/4 - periode_remp_base)*taux_ann_sup ))
#
#    montant = min_(taux_pension, plaf_pension)*sal_ref
#
#    montant_percu = max_(montant, pension_min*smig)
#    pension = elig*montant_percu
#    return pension

