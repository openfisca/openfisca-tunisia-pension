'''Régime de la Caisse nationale de retraite et de prévoyance sociale (CNRPS).'''


from openfisca_core.model_api import *


from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.regimes.regime import AbstractRegimeEnAnnuites


from numpy import (
    apply_along_axis,
    logical_not as not_,
    maximum as max_,
    vstack,
    )

from openfisca_tunisia_pension.variables.helpers import pension_generique
from openfisca_tunisia_pension.tools import make_mean_over_largest


class RegimeCNRPS(AbstractRegimeEnAnnuites):
    name = 'Régime des salariés non agricoles'
    variable_prefix = 'cnrps'
    parameters_prefix = 'cnrps'

    class salaire_reference(Variable):
        value_type = float
        entity = Individu
        label = 'Salaires de référence du régime de la CNRPS'
        definition_period = YEAR

        def formula(individu, period):
            '''3 dernières rémunérations ou les 2 plus élevées sur demande.'''
            n = 40
            k = 2
            mean_over_largest = make_mean_over_largest(k)
            moyenne_2_salaires_plus_eleves = apply_along_axis(
                mean_over_largest,
                axis = 0,
                arr = vstack([individu('regime_name_salaire_de_base', period = year) for year in range(period.start.year, period.start.year - n, -1)]),
                )
            p = 3
            moyenne_3_derniers_salaires = sum(
                individu('regime_name_salaire_de_base', period = year)
                for year in range(period.start.year, period.start.year - p, -1)
                ) / p

            salaire_refererence = max_(
                moyenne_3_derniers_salaires,
                moyenne_2_salaires_plus_eleves
                )
            return salaire_refererence

    class pension(Variable):
        value_type = float
        entity = Individu
        label = 'Pension des affiliés au régime des salariés non agricoles'
        definition_period = YEAR

        def formula(individu, period, parameters):
            duree_assurance = individu('regime_name_duree_assurance', period = period)
            salaire_reference = individu('regime_name_salaire_reference', period = period)
            age = individu('age', period = period)

            cnrps = parameters(period).retraite.regime_name
            taux_annuite_base = cnrps.taux_annuite_base
            taux_annuite_supplementaire = cnrps.taux_annuite_supplementaire
            duree_stage = cnrps.stage_derog
            age_eligible = cnrps.age_dep_anticip
            periode_remplacement_base = cnrps.periode_remplacement_base
            plaf_taux_pension = cnrps.plaf_taux_pension
            smig = parameters(period).marche_travail.smig_48h

            pension_min_sup = cnrps.pension_minimale.sup
            pension_min_inf = cnrps.pension_minimale.inf

            stage = duree_assurance > 4 * duree_stage
            pension_minimale = (
                stage * pension_min_sup + not_(stage) * pension_min_inf
                )
            montant = pension_generique(
                duree_assurance,
                salaire_reference,
                taux_annuite_base,
                taux_annuite_supplementaire,
                duree_stage,
                age_eligible,
                periode_remplacement_base,
                plaf_taux_pension,
                )
            # eligibilite
            eligibilite_age = age > age_eligible
            eligibilite = stage * eligibilite_age * (salaire_reference > 0)
            # plafonnement
            montant_pension_percu = max_(montant, pension_minimale * smig)
            return eligibilite * montant_pension_percu
