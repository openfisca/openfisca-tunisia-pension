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
    value_type = float
    entity = Individu
    label = 'Salaires de référence du régime des salariés agricoles'
    definition_period = YEAR

    def formula(individu, period):
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
                individu('salaire', period = periods.period('year', year))
                for year in range(period.start.year, period.start.year - n, -1)
                ]),
            )
        salaire_refererence = salaire * base_liquidation_rsa / base_declaration_rsa
        return salaire_refererence


class salaire_reference_rsna(Variable):
    value_type = float
    entity = Individu
    label = 'Salaires de référence du régime des salariés non agricoles'
    definition_period = YEAR

    def formula(individu, period):
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
    value_type = float
    entity = Individu
    label = 'Pension des affiliés au régime des salariés non agricoles'
    definition_period = YEAR

    def formula(individu, period, parameters):
        trimestres_valides = individu('trimestres_valides', period = period)
        salaire_reference = individu('salaire_reference_rsna', period = period)
        age = individu('age', period = period)

        taux_annuite_base = parameters(period).pension.rsna.taux_annuite_base
        taux_annuite_supplemetaire = parameters(period).pension.rsna.taux_annuite_supplemetaire
        duree_stage = parameters(period).pension.rsna.stage_derog
        age_eligible = parameters(period).pension.rsna.age_dep_anticip
        periode_remplacement_base = parameters(period).pension.rsna.periode_remplacement_base
        plaf_taux_pension = parameters(period).pension.rsna.plaf_taux_pension
        smig = parameters(period).param_gen.smig_48h

        pension_min_sup = parameters(period).pension.rsna.pension_minimale.sup
        pension_min_inf = parameters(period).pension.rsna.pension_minimale.inf

        stage = trimestres_valides > 4 * duree_stage
        pension_minimale = (
            stage * pension_min_sup + not_(stage) * pension_min_inf
            )
        montant = pension_generique(
            trimestres_valides,
            salaire_reference,
            age,
            taux_annuite_base,
            taux_annuite_supplemetaire,
            duree_stage,
            age_eligible,
            periode_remplacement_base,
            plaf_taux_pension,
            smig,
            )
        # eligibilite
        eligibilite_age = age > age_eligible
        eligibilite = stage * eligibilite_age * (salaire_reference > 0)
        # plafonnement
        montant_pension_percu = max_(montant, pension_minimale * smig)
        return eligibilite * montant_pension_percu


def _pension_rsa(trimestres_valides, sal_ref_rsa, regime, age, _P):
    '''
    Pension du régime des salariés agricoles
    '''
    taux_annuite_base = _P.pension.rsa.taux_annuite_base
    taux_annuite_supplemetaire = _P.pension.rsa.taux_annuite_supplemetaire
    duree_stage = _P.pension.rsa.stage_requis
    age_elig = _P.pension.rsa.age_legal
    periode_remplacement_base = _P.pension.rsa.periode_remplacement_base
    plaf_taux_pension = _P.pension.rsa.plaf_taux_pension
    smag = _P.param_gen.smag * 25
    stage = trimestres_valides > 4 * duree_stage
    pension_min = _P.pension.rsa.pension_min
    sal_ref = sal_ref_rsa

    montant = pension_generique(trimestres_valides, sal_ref, age, taux_annuite_base, taux_annuite_supplemetaire,
        duree_stage, age_elig, periode_remplacement_base, plaf_taux_pension, smag)

    elig_age = age > age_elig
    elig = stage * elig_age * (sal_ref > 0)
    montant_percu = max_(montant, pension_min * smag)
    pension = elig * montant_percu
    return pension


# Helper function

def pension_generique(trimestres_valides, sal_ref, age, taux_annuite_base, taux_annuite_supplemetaire, duree_stage,
        age_elig, periode_remplacement_base, plaf_taux_pension, smig):
    taux_pension = (
        (trimestres_valides < 4 * periode_remplacement_base) * (trimestres_valides / 4) * taux_annuite_base
        + (trimestres_valides >= 4 * periode_remplacement_base) * (
            taux_annuite_base * periode_remplacement_base
            + (trimestres_valides / 4 - periode_remplacement_base) * taux_annuite_supplemetaire
            )
        )
    montant = min_(taux_pension, plaf_taux_pension) * sal_ref
    return montant


def mean_over_k_largest(vector, k):
    '''Return the mean over the k largest values of a vector'''
    if k == 0:
        return 0

    if k <= len(vector):
        return vector.sum() / len(vector)

    z = -bottleneck.partition(-vector, kth = k)
    return z.sum() / k
