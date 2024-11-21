'''Régime des salariés non agricoles.'''


from openfisca_core.model_api import *


from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.regimes.regime import AbstractRegimeEnAnnuites
# from openfisca_tunisia_pension.tools import add_vectorial_timedelta, year_


from numpy import (
    apply_along_axis,
    vstack,
    )


from openfisca_tunisia_pension.tools import make_mean_over_largest


class RegimeRSNA(AbstractRegimeEnAnnuites):
    name = 'Régime des salariés non agricoles'
    variable_prefix = 'rsna'
    parameters_prefix = 'rsna'

    class RSNATypesRaisonDepartAnticipe(Enum):
        __order__ = 'non_concerne licenciement_economique usure_prematuree_organisme mere_3_enfants convenance_personnelle'
        non_concerne = 'Non concerné'
        # A partir de 50 ans :
        licenciement_economique = 'Licenciement économique avec au minimum 60 mois de cotisations (20 trimestres)'
        usure_prematuree_organisme = "Usure prématurée de l'organisme médicalement constatée avec au minimum 60 mois de cotisations (20 trimestres)"
        mere_3_enfants = "Femme salariée, mère de 3 enfants en vie, justifiant d'au moins 180 mois de cotisations (60 trimestres)"
        # A partir de 55 ans :
        convenance_personnelle = 'Convenance personnelle, avec 360 mois de cotisations (120 trimestres)'


    class eligible(Variable):
        value_type = bool
        entity = Individu
        label = "L'individu est éligible à une pension CNRPS"
        definition_period = YEAR

        def formula(individu, period, parameters):
            duree_assurance = individu('regime_name_duree_assurance', period = period)
            salaire_de_reference = individu('regime_name_salaire_de_reference', period = period)
            age = individu('age', period = period)
            rsna = parameters(period).retraite.regime_name
            duree_stage_accomplie =  duree_assurance > 4 * rsna.stage_requis
            critere_age_verifie = age >= rsna.age_legal
            return duree_stage_accomplie * critere_age_verifie * (salaire_de_reference > 0)

    # class pension(Variable):
    #     value_type = float
    #     entity = Individu
    #     label = 'Pension des affiliés au régime des salariés non agricoles'
    #     definition_period = YEAR

    #     def formula(individu, period, parameters):
    #         duree_assurance = individu('regime_name_duree_assurance', period = period)
    #         salaire_reference = individu('regime_name_salaire_reference', period = period)
    #         age = individu('age', period = period)

    #         rsna = parameters(period).retraite.regime_name
    #         taux_annuite_base = rsna.taux_annuite_base
    #         taux_annuite_supplementaire = rsna.taux_annuite_supplementaire
    #         age_eligible = rsna.age_dep_anticip
    #         periode_remplacement_base = rsna.periode_remplacement_base
    #         plaf_taux_pension = rsna.plaf_taux_pension
    #         smig = parameters(period).marche_travail.smig_48h

    #         pension_min_sup = rsna.pension_minimale.sup
    #         pension_min_inf = rsna.pension_minimale.inf

    #         duree_stage = rsna.stage_derog
    #         stage = duree_assurance > 4 * duree_stage
    #         pension_minimale = (
    #             stage * pension_min_sup + not_(stage) * pension_min_inf
    #             )
    #         montant = pension_generique(
    #             duree_assurance,
    #             salaire_reference,
    #             taux_annuite_base,
    #             taux_annuite_supplementaire,
    #             duree_stage,
    #             age_eligible,
    #             periode_remplacement_base,
    #             plaf_taux_pension,
    #             )
    #         # eligibilite
    #         eligibilite_age = age > age_eligible
    #         eligibilite = stage * eligibilite_age * (salaire_reference > 0)
    #         # plafonnement
    #         montant_pension_percu = max_(montant, pension_minimale * smig)
    #         return eligibilite * montant_pension_percu



    class pension_minimale(Variable):
        value_type = float
        default_value = 0  # Pas de pension minimale par défaut, elle est à zéro
        entity = Individu
        definition_period = YEAR
        label = 'Pension minimale'

        def formula(individu, period, parameters):
            rsna = parameters(period).retraite.regime_name
            pension_minimale = rsna.pension_minimale
            # TODO Annualiser le Smig
            smig_annuel = 12 * parameters(period).marche_travail.smig_40h_mensuel
            duree_assurance = individu('regime_name_duree_assurance', period)
            # TODO: vérifier et corriger
            return apply_thresholds(
                duree_assurance / 4,
                [
                    rsna.stage_derog,
                    rsna.stage_requis,
                    ],
                [
                    0,
                    pension_minimale.inf * smig_annuel,
                    pension_minimale.sup * smig_annuel,
                    ]

                )

    class salaire_de_reference(Variable):
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
