import functools
from numpy import (
    apply_along_axis,
    maximum as max_,
    vstack,
    )

from openfisca_core import periods
from openfisca_core.model_api import *
from openfisca_tunisia_pension.entities import Individu


class salaire_reference_rsa(Variable):
    value_type = float
    entity = Individu
    label = 'Salaires de référence du régime des salariés agricoles'
    definition_period = YEAR

    def formula(individu, period):
        # TODO: gérer le nombre d'année
        # TODO: plafonner les salaires à 2 fois le smag de l'année d'encaissement
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


class pension_rsa(Variable):
    value_type = float
    entity = Individu
    label = 'Salaires de référence du régime des salariés agricoles'
    definition_period = YEAR

    def formula(individu, period, parameters):
        rsa = parameters.retraite.rsa(period)
        taux_annuite_base = rsa.taux_annuite_base
        taux_annuite_supplemetaire = rsa.taux_annuite_supplemetaire
        duree_stage = rsa.stage_requis
        age_elig = rsa.age_legal
        periode_remplacement_base = rsa.periode_remplacement_base
        plaf_taux_pension = rsa.plaf_taux_pension
        smag = parameters(period).marche_travail.smag * 25
        duree_stage_validee = trimestres_valides > 4 * duree_stage
        pension_min = rsa.pension_min
        salaire_reference = individu('salaire_reference_rsa', period)

        montant = pension_generique(trimestres_valides, sal_ref, age, taux_annuite_base, taux_annuite_supplemetaire,
            duree_stage, age_elig, periode_remplacement_base, plaf_taux_pension, smag)

        elig_age = age > age_elig
        elig = duree_stage_validee * elig_age * (salaire_reference > 0)
        montant_percu = max_(montant, pension_min * smag)
        pension = elig * montant_percu
        return pension
