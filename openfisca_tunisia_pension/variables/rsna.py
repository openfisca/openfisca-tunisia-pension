import functools
from numpy import (
    apply_along_axis,
    logical_not as not_,
    maximum as max_,
    minimum as min_,
    vstack,
    )

from openfisca_core import periods
from openfisca_core.model_api import *
from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.variables.helpers import mean_over_k_largest, pension_generique


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
        smig = parameters(period).marche_travail.smig_48h

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
