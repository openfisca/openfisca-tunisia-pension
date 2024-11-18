'''Régime des salariés non agricoles.'''


from openfisca_core.model_api import *


from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.regimes.regime import AbstractRegimeEnAnnuites
# from openfisca_tunisia_pension.tools import add_vectorial_timedelta, year_


from numpy import (
    apply_along_axis,
    logical_not as not_,
    maximum as max_,
    vstack,
    )


from openfisca_tunisia_pension.tools import make_mean_over_largest
from openfisca_tunisia_pension.variables.helpers import pension_generique


class RegimeRSNA(AbstractRegimeEnAnnuites):
    name = 'Régime des salariés non agricoles'
    variable_prefix = 'rsna'
    parameters_prefix = 'rsna'

    class salaire_reference(Variable):
        value_type = float
        entity = Individu
        label = 'Salaires de référence du régime des salariés non agricoles'
        definition_period = YEAR

        def formula(individu, period):
            # TODO: gérer le nombre d'année n
            # TODO: plafonner les salaires à 6 fois le smig de l'année d'encaissement
            k = 10
            mean_over_largest = make_mean_over_largest(k = k)
            n = 40
            salaire_refererence = apply_along_axis(
                mean_over_largest,
                axis = 0,
                arr = vstack([
                    individu('regime_name_salaire_de_base', period = year)
                    for year in range(period.start.year, period.start.year - n, -1)
                    ]),
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

            rsna = parameters(period).retraite.regime_name
            taux_annuite_base = rsna.taux_annuite_base
            taux_annuite_supplementaire = rsna.taux_annuite_supplementaire
            duree_stage = rsna.stage_derog
            age_eligible = rsna.age_dep_anticip
            periode_remplacement_base = rsna.periode_remplacement_base
            plaf_taux_pension = rsna.plaf_taux_pension
            smig = parameters(period).marche_travail.smig_48h

            pension_min_sup = rsna.pension_minimale.sup
            pension_min_inf = rsna.pension_minimale.inf

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