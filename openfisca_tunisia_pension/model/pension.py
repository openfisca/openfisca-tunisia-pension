# -*- coding:utf-8 -*-


from __future__ import division

import bottleneck
import functools
from numpy import (
    apply_along_axis,
    logical_not as not_,
    maximum as max_,
    minimum as min_,
    vstack,
    )

from openfisca_core import periods
from openfisca_tunisia_pension.model.base import *  # noqa


class salaire_reference_rsa(Variable):
    column = FloatCol()
    entity = Individu
    label = u"Salaires de référence du régime des salariés agricoles"
    definition_period = YEAR

    def function(self, simulation, period):
        # TODO: gérer le nombre d'année
        # TODO: plafonner les salaires à 2 fois le smag de l'année d'encaissement
        # period = period.start.offset('first-of', 'month').period('year')
        base_declaration_rsa = 180
        base_liquidation_rsa = 300

        n = 3
        mean_over_largest = functools.partial(mean_over_k_largest, k = n)
        salaire = apply_along_axis(
            mean_over_largest,
            axis = 0,
            arr = vstack([
                simulation.calculate('salaire', period = periods.period("year", year))
                for year in range(period.start.year, period.start.year - n, -1)
                ]),
            )
        salaire_refererence = salaire * base_liquidation_rsa / base_declaration_rsa
        return period, salaire_refererence


class salaire_reference_rsna(Variable):
    column = FloatCol()
    entity = Individu
    label = u"Salaires de référence du régime des salariés non agricoles"
    definition_period = YEAR

    def function(individu, period):

        # TODO: gérer le nombre d'année n
        # TODO: plafonner les salaires à 6 fois le smig de l'année d'encaissement
        n = 10
        mean_over_largest = functools.partial(mean_over_k_largest, k = n)
        salaire_refererence = apply_along_axis(
            mean_over_largest,
            axis = 0,
            arr = vstack([
                individu('salaire', period = year)
                for year in range(period.start.year, period.start.year - n, -1)
                ]),
            )
        return salaire_refererence


class pension_rsna(Variable):
    column = FloatCol()
    entity = Individu
    label = u"Pension des affiliés au régime des salariés non agricoles"
    definition_period = YEAR

    def function(individu, period, legislation):
        nb_trim_val = individu('nb_trim_val', period = period)
        salaire_reference = individu('salaire_reference_rsna', period = period)
        # regime = simulation.calculate('regime', period = period)
        age = individu('age', period = period)

        taux_ann_base = legislation(period.start).pension.rsna.taux_ann_base
        taux_ann_sup = legislation(period.start).pension.rsna.taux_ann_sup
        duree_stage = legislation(period.start).pension.rsna.stage_derog
        age_elig = legislation(period.start).pension.rsna.age_dep_anticip
        periode_remp_base = legislation(period.start).pension.rsna.periode_remp_base
        plaf_taux_pension = legislation(period.start).pension.rsna.plaf_taux_pension
        smig = legislation(period.start).param_gen.smig_48h

        pension_min_sup = legislation(period.start).pension.rsna.pension_min.sup
        pension_min_inf = legislation(period.start).pension.rsna.pension_min.inf

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
        return pension


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


def mean_over_k_largest(vector, k):
    '''Return the mean over the k largest values of a vector'''
    if k == 0:
        return 0

    z = -bottleneck.partsort(-vector, k)[:k]
    return z.sum() / k
