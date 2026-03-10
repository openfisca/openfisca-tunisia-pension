import math
from openfisca_tunisia_pension.entities import Individu
from openfisca_core.model_api import (
    Variable,
    MONTH,
    where,
    min_,
    set_input_dispatch_by_period,
)



class age_deces(Variable):
    value_type = int
    entity = Individu
    default_value = -1 # Not deceased
    definition_period = MONTH
    label = "Age au décès"
    set_input = set_input_dispatch_by_period

class deces_par_accident(Variable):
    value_type = bool
    entity = Individu
    default_value = False
    definition_period = MONTH
    label = "Décès suite à un accident (circulation, travail)"
    set_input = set_input_dispatch_by_period

class cnrps_duree_services_effectifs(Variable):
    value_type = int
    entity = Individu
    default_value = 0
    definition_period = MONTH
    label = "Durée des services effectifs (années complètes)"
    set_input = set_input_dispatch_by_period

class cnrps_remuneration_annuelle_deces(Variable):
    value_type = float
    entity = Individu
    default_value = 0.0
    definition_period = MONTH
    label = "Rémunération annuelle de base au moment du décès"
    set_input = set_input_dispatch_by_period

class cnrps_pension_reference_deces(Variable):
    value_type = float
    entity = Individu
    default_value = 0.0
    definition_period = MONTH
    label = "Montant de la pension dont l'agent bénéficiait ou aurait bénéficié"
    set_input = set_input_dispatch_by_period

class nombre_orphelins_eligibles(Variable):
    value_type = int
    entity = Individu
    default_value = 0
    definition_period = MONTH
    label = "Nombre d'enfants eligibles à la Pension Temporaire d'Orphelin (PTO)"
    set_input = set_input_dispatch_by_period

class conjoint_survivant_eligible(Variable):
    value_type = bool
    entity = Individu
    default_value = False
    definition_period = MONTH
    label = "Présence d'un conjoint survivant éligible à la pension de réversion"
    set_input = set_input_dispatch_by_period


class cnrps_capital_deces(Variable):
    value_type = float
    entity = Individu
    label = "Montant du Capital-Décès servi aux ayants droit"
    definition_period = MONTH

    def formula(individu, period, parameters):
        age_deces = individu('age_deces', period)
        is_accident = individu('deces_par_accident', period)
        r_annuelle = individu('cnrps_remuneration_annuelle_deces', period)
        duree_services = individu('cnrps_duree_services_effectifs', period)
        nb_enfants = individu('nombre_enfants_charge', period)

        # Returns 0 if not deceased
        is_deceased = age_deces >= 0

        # CD = R + MA + ME
        # MA: Majoration ancienneté -> R/12 per year of service (max 18)
        duree_retenue = min_(duree_services, 18)
        MA = (r_annuelle / 12) * duree_retenue

        CD1 = r_annuelle + MA

        # ME: Majoration enfants -> 10% per child
        ME = CD1 * 0.10 * nb_enfants

        CD_base = CD1 + ME

        # Accidents in activity double the capital (assuming age < 60 means activity/accident applicability for the multiplier)
        # Note: The manual indicates retirees deceased by accident don't get the 200% rate.
        multiplier_accident = where(is_accident * (age_deces < 60), 2.0, 1.0)

        CD_actif = CD_base * multiplier_accident

        # For retirees, the capital is reduced based on age
        # < 70 -> 50%
        # 70-75 -> 40%
        # 75-80 -> 30%
        # 80-85 -> 20%
        # > 85 -> 10%
        # Assuming age >= 60 implies retiree for this specific calculation if not accident

        taux_retraite = where(
            age_deces >= 85, 0.10,
            where(
                age_deces >= 80, 0.20,
                where(
                    age_deces >= 75, 0.30,
                    where(
                        age_deces >= 70, 0.40,
                        where(
                            age_deces >= 60, 0.50,
                            1.0 # default for active agents < 60
                        )
                    )
                )
            )
        )

        CD_final = CD_actif * taux_retraite

        # Ensure it's not below SMIG (simplified to constant for this model based on parameters later, using 0 check for now as placeholder for smig check if needed)

        return CD_final * is_deceased


class cnrps_pension_de_reversion(Variable):
    value_type = float
    entity = Individu
    label = "Pension de réversion servie au conjoint survivant"
    definition_period = MONTH

    def formula(individu, period, parameters):
        pension_ref = individu('cnrps_pension_reference_deces', period)
        eligible = individu('conjoint_survivant_eligible', period)
        nb_orphelins = individu('nombre_orphelins_eligibles', period)
        is_deceased = individu('age_deces', period) >= 0

        # Base is 75%
        taux_reversion = 0.75

        # Reduction based on number of orphans
        taux_reversion = where(
            nb_orphelins >= 5, 0.50,
            where(
                nb_orphelins == 4, 0.60, # 75% - 5% (3rd) - 10% (4th)
                where(
                    nb_orphelins == 3, 0.70, # 75% - 5%
                    0.75
                )
            )
        )

        return pension_ref * taux_reversion * eligible * is_deceased

class cnrps_pension_orphelins_totale(Variable):
    value_type = float
    entity = Individu
    label = "Montant total des pensions temporaires d'orphelins (PTO) servi"
    definition_period = MONTH

    def formula(individu, period, parameters):
        pension_ref = individu('cnrps_pension_reference_deces', period)
        conjoint_eligible = individu('conjoint_survivant_eligible', period)
        nb_orphelins = individu('nombre_orphelins_eligibles', period)
        is_deceased = individu('age_deces', period) >= 0

        # Base logic: 10% per orphan
        taux_orphelins = nb_orphelins * 0.10

        # Caps depending on the presence of a spouse
        taux_orphelins = where(
            conjoint_eligible,
            where(
                nb_orphelins >= 5, 0.50, # Global cap is 100%, spouse gets 50%, rest 50%
                where(
                    nb_orphelins == 4, 0.40,
                    where(
                        nb_orphelins == 3, 0.30,
                        taux_orphelins
                    )
                )
            ),
            # If no eligible spouse, they get their portions. (Wait: manual says "If non attribution to conjoint, distributed to orphans")
            # Generally, the maximum for orphans WITHOUT spouse isn't explicitly capped at 50%, they might share 100% of the pension.
            # "En cas de non-attribution de la pension du conjoint... répartie à parts égales entre les orphelins"
            # So rate = 10% * N + 75% (or the conjoint's theoretical part). Max 100%.
            min_(1.0, nb_orphelins * 0.10 + 0.75) * (nb_orphelins > 0)
        )

        return pension_ref * taux_orphelins * is_deceased
