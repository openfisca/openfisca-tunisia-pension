"""Abstract regimes definition."""
from openfisca_core.model_api import *
from openfisca_tunisia_pension.entities import Individu
'Régime de la Caisse nationale de retraite et de prévoyance sociale (CNRPS).'
from openfisca_core.model_api import *
from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.regimes.regime import AbstractRegimeEnAnnuites
from numpy import apply_along_axis, logical_not as not_, maximum as max_, vstack
from openfisca_tunisia_pension.variables.helpers import pension_generique
from openfisca_tunisia_pension.tools import make_mean_over_largest

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

class cnrps_liquidation_date(Variable):
    value_type = date
    entity = Individu
    definition_period = ETERNITY
    label = 'Date de liquidation'
    default_value = date(2250, 12, 31)

class cnrps_majoration_duree_assurance(Variable):
    value_type = float
    entity = Individu
    definition_period = ETERNITY
    label = "Majoration de durée d'assurance"

    def formula(individu, period):
        return individu('cnrps_majoration_duree_assurance_enfant', period) + individu('cnrps_majoration_duree_assurance_autre', period)

class cnrps_majoration_duree_assurance_autre(Variable):
    value_type = float
    entity = Individu
    definition_period = ETERNITY
    label = "Majoration de durée d'assurance autre que celle attribuée au motif des enfants"

class cnrps_majoration_pension(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Majoration de pension'

class cnrps_majoration_pension_au_31_decembre(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Majoration de pension au 31 décembre'

    def formula(individu, period, parameters):
        annee_de_liquidation = individu('cnrps_liquidation_date', period).astype('datetime64[Y]').astype(int) + 1970
        if all(annee_de_liquidation > period.start.year):
            return individu.empty_array()
        last_year = period.last_year
        majoration_pension_au_31_decembre_annee_precedente = individu('cnrps_majoration_pension_au_31_decembre', last_year)
        revalorisation = parameters(period).cnrps.revalorisation_pension_au_31_decembre
        majoration_pension = individu('cnrps_majoration_pension', period)
        return revalorise(majoration_pension_au_31_decembre_annee_precedente, majoration_pension, annee_de_liquidation, revalorisation, period)

class cnrps_pension(Variable):
    value_type = float
    entity = Individu
    label = 'Pension des affiliés au régime des salariés non agricoles'
    definition_period = YEAR

    def formula(individu, period, parameters):
        duree_assurance = individu('cnrps_duree_assurance', period=period)
        salaire_reference = individu('cnrps_salaire_reference', period=period)
        age = individu('age', period=period)
        cnrps = parameters(period).retraite.cnrps
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
        pension_minimale = stage * pension_min_sup + not_(stage) * pension_min_inf
        montant = pension_generique(duree_assurance, salaire_reference, taux_annuite_base, taux_annuite_supplementaire, duree_stage, age_eligible, periode_remplacement_base, plaf_taux_pension)
        eligibilite_age = age > age_eligible
        eligibilite = stage * eligibilite_age * (salaire_reference > 0)
        montant_pension_percu = max_(montant, pension_minimale * smig)
        return eligibilite * montant_pension_percu

class cnrps_pension_au_31_decembre(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension'

    def formula(individu, period):
        pension_brute_au_31_decembre = individu('cnrps_pension_brute_au_31_decembre', period)
        majoration_pension_au_31_decembre = individu('cnrps_majoration_pension_au_31_decembre', period)
        return pension_brute_au_31_decembre + majoration_pension_au_31_decembre

class cnrps_pension_brute(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension brute'

    def formula(individu, period, parameters):
        NotImplementedError

class cnrps_pension_brute_au_31_decembre(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension brute au 31 décembre'

    def formula(individu, period, parameters):
        annee_de_liquidation = individu('cnrps_liquidation_date', period).astype('datetime64[Y]').astype(int) + 1970
        if all(period.start.year < annee_de_liquidation):
            return individu.empty_array()
        last_year = period.last_year
        pension_brute_au_31_decembre_annee_precedente = individu('cnrps_pension_brute_au_31_decembre', last_year)
        revalorisation = parameters(period).cnrps.revalorisation_pension_au_31_decembre
        pension_brute = individu('cnrps_pension_brute', period)
        return revalorise(pension_brute_au_31_decembre_annee_precedente, pension_brute, annee_de_liquidation, revalorisation, period)

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
    definition_period = ETERNITY
    label = 'Salaire de référence'

class cnrps_salaire_reference(Variable):
    value_type = float
    entity = Individu
    label = 'Salaires de référence du régime de la CNRPS'
    definition_period = YEAR

    def formula(individu, period):
        """3 dernières rémunérations ou les 2 plus élevées sur demande."""
        n = 40
        k = 2
        mean_over_largest = make_mean_over_largest(k)
        moyenne_2_salaires_plus_eleves = apply_along_axis(mean_over_largest, axis=0, arr=vstack([individu('cnrps_salaire_de_base', period=year) for year in range(period.start.year, period.start.year - n, -1)]))
        p = 3
        moyenne_3_derniers_salaires = sum((individu('cnrps_salaire_de_base', period=year) for year in range(period.start.year, period.start.year - p, -1))) / p
        salaire_refererence = max_(moyenne_3_derniers_salaires, moyenne_2_salaires_plus_eleves)
        return salaire_refererence

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