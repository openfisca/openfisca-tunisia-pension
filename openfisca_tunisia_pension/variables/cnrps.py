"""Abstract regimes definition."""
import numpy as np
from openfisca_core.model_api import *
from openfisca_core.errors.variable_not_found_error import VariableNotFoundError
from openfisca_tunisia_pension.entities import Individu
'Régime de la Caisse nationale de retraite et de prévoyance sociale (CNRPS).'
from openfisca_core.model_api import *
from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.regimes.regime import AbstractRegimeEnAnnuites
from numpy import apply_along_axis, vstack
from openfisca_tunisia_pension.tools import make_mean_over_consecutive_largest

class cnrps_cotisation(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'cotisation retraite employeur'

    def formula(individu, period, parameters):
        NotImplementedError

class cnrps_duree_assurance(Variable):
    value_type = int
    entity = Individu
    definition_period = YEAR
    label = "Durée d'assurance (trimestres validés)"

class cnrps_duree_assurance_annuelle(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = "Durée d'assurance (en trimestres validés l'année considérée)"

class cnrps_eligible(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu est éligible à une pension CNRPS"
    definition_period = YEAR

    def formula(individu, period, parameters):
        duree_assurance = individu('cnrps_duree_assurance', period=period)
        salaire_de_reference = individu('cnrps_salaire_de_reference', period=period)
        age = individu('age', period=period)
        cnrps = parameters(period).retraite.cnrps
        duree_de_service_minimale_accomplie = duree_assurance > 4 * cnrps.duree_de_service_minimale
        critere_age_verifie = age >= cnrps.age_legal.civil.cadre_commun
        return duree_de_service_minimale_accomplie * critere_age_verifie * (salaire_de_reference > 0)

class cnrps_liquidation_date(Variable):
    value_type = date
    entity = Individu
    definition_period = ETERNITY
    label = 'Date de liquidation'
    default_value = date(2250, 12, 31)

class cnrps_majoration_pension(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH
    label = 'Majoration de pension'

    def formula(individu, period, parameters):
        NotImplementedError

class cnrps_pension(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension'

    def formula(individu, period):
        pension_brute = individu('cnrps_pension_brute', period)
        eligible = individu('cnrps_eligible', period)
        try:
            pension_minimale = individu('cnrps_pension_minimale', period)
        except VariableNotFoundError:
            pension_minimale = 0
        try:
            pension_maximale = individu('cnrps_pension_maximale', period)
        except (VariableNotFoundError, NotImplementedError):
            return max_(pension_brute, pension_minimale)
        return eligible * min_(pension_maximale, max_(pension_brute, pension_minimale))

class cnrps_pension_brute(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension brute'

    def formula(individu, period, parameters):
        taux_de_liquidation = individu('cnrps_taux_de_liquidation', period)
        salaire_de_reference = individu('cnrps_salaire_de_reference', period)
        return (taux_de_liquidation * salaire_de_reference,)

class cnrps_pension_maximale(Variable):
    value_type = float
    default_value = np.inf
    entity = Individu
    definition_period = YEAR
    label = 'Pension maximale'

    def formula(individu, period, parameters):
        NotImplementedError

class cnrps_pension_minimale(Variable):
    value_type = float
    default_value = 0
    entity = Individu
    definition_period = YEAR
    label = 'Pension minimale'

    def formula(individu, period, parameters):
        cnrps = parameters(period).retraite.cnrps
        pension_minimale = cnrps.pension_minimale
        duree_de_service_minimale = cnrps.duree_de_service_minimale
        smig_annuel = 12 * parameters(period).marche_travail.smig_40h_mensuel
        duree_assurance = individu('cnrps_duree_assurance', period)
        return apply_thresholds(duree_assurance / 4, [pension_minimale.duree_service_allocation_vieillesse, duree_de_service_minimale], [0, pension_minimale.allocation_vieillesse * smig_annuel, pension_minimale.minimum_garanti * smig_annuel])

class cnrps_pension_servie(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension servie'

    def formula(individu, period, parameters):
        annee_de_liquidation = individu('cnrps_liquidation_date', period).astype('datetime64[Y]').astype(int) + 1970
        if all(annee_de_liquidation > period.start.year):
            return individu.empty_array()
        last_year = period.last_year
        pension_au_31_decembre_annee_precedente = individu('cnrps_pension_au_31_decembre', last_year)
        revalorisation = parameters(period).cnrps.revalarisation_pension_servie
        pension = individu('cnrps_pension_au_31_decembre', period)
        return revalorise(pension_au_31_decembre_annee_precedente, pension, annee_de_liquidation, revalorisation, period)

class cnrps_salaire_de_base(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Salaire de base (salaire brut)'
    set_input = set_input_divide_by_period

class cnrps_salaire_de_reference(Variable):
    value_type = float
    entity = Individu
    label = 'Salaires de référence du régime de la CNRPS'
    definition_period = YEAR

    def formula(individu, period):
        """3 dernières rémunérations ou les 2 plus élevées sur demande."""
        n = 40
        k = 2
        mean_over_largest = make_mean_over_consecutive_largest(k)
        moyenne_2_salaires_plus_eleves = apply_along_axis(mean_over_largest, axis=0, arr=vstack([individu('cnrps_salaire_de_base', period=year) for year in range(period.start.year, period.start.year - n, -1)]))
        p = 3
        moyenne_3_derniers_salaires = sum((individu('cnrps_salaire_de_base', period=year) for year in range(period.start.year, period.start.year - p, -1))) / p
        salaire_refererence = where(individu('cnrps_salaire_de_reference_calcule_sur_demande', period), moyenne_2_salaires_plus_eleves, moyenne_3_derniers_salaires)
        return salaire_refererence

class cnrps_salaire_de_reference_calcule_sur_demande(Variable):
    value_type = bool
    entity = Individu
    label = "Le salaire de référence du régime de la CNRPS est calculé à la demande de l'agent sur ses meilleures années"
    definition_period = ETERNITY

class cnrps_taux_de_liquidation(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Taux de liquidation de la pension'

    def formula(individu, period, parameters):
        bareme_annuite = parameters(period).retraite.cnrps.bareme_annuite
        duree_assurance = individu('cnrps_duree_assurance', period)
        taux_annuite = bareme_annuite.calc(duree_assurance)
        return taux_annuite