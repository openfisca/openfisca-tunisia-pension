import math
from openfisca_core.model_api import *
from openfisca_tunisia_pension.entities import Individu

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
