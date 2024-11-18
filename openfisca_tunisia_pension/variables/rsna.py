"""Abstract regimes definition."""
from openfisca_core.model_api import *
from openfisca_tunisia_pension.entities import Individu
'Régime des salariés non agricoles.'
from openfisca_core.model_api import *
from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.regimes.regime import AbstractRegimeEnAnnuites
from numpy import apply_along_axis, logical_not as not_, maximum as max_, vstack
from openfisca_tunisia_pension.tools import make_mean_over_largest
from openfisca_tunisia_pension.variables.helpers import pension_generique

class rsna_cotisation(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'cotisation retraite employeur'

    def formula(individu, period, parameters):
        NotImplementedError

class rsna_duree_assurance(Variable):
    value_type = int
    entity = Individu
    definition_period = YEAR
    label = "Durée d'assurance (trimestres validés)"

class rsna_duree_assurance_annuelle(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = "Durée d'assurance (en trimestres validés l'année considérée)"

class rsna_liquidation_date(Variable):
    value_type = date
    entity = Individu
    definition_period = ETERNITY
    label = 'Date de liquidation'
    default_value = date(2250, 12, 31)

class rsna_majoration_duree_assurance(Variable):
    value_type = float
    entity = Individu
    definition_period = ETERNITY
    label = "Majoration de durée d'assurance"

    def formula(individu, period):
        return individu('rsna_majoration_duree_assurance_enfant', period) + individu('rsna_majoration_duree_assurance_autre', period)

class rsna_majoration_duree_assurance_autre(Variable):
    value_type = float
    entity = Individu
    definition_period = ETERNITY
    label = "Majoration de durée d'assurance autre que celle attribuée au motif des enfants"

class rsna_majoration_pension(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Majoration de pension'

class rsna_majoration_pension_au_31_decembre(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Majoration de pension au 31 décembre'

    def formula(individu, period, parameters):
        annee_de_liquidation = individu('rsna_liquidation_date', period).astype('datetime64[Y]').astype(int) + 1970
        if all(annee_de_liquidation > period.start.year):
            return individu.empty_array()
        last_year = period.last_year
        majoration_pension_au_31_decembre_annee_precedente = individu('rsna_majoration_pension_au_31_decembre', last_year)
        revalorisation = parameters(period).rsna.revalorisation_pension_au_31_decembre
        majoration_pension = individu('rsna_majoration_pension', period)
        return revalorise(majoration_pension_au_31_decembre_annee_precedente, majoration_pension, annee_de_liquidation, revalorisation, period)

class rsna_pension(Variable):
    value_type = float
    entity = Individu
    label = 'Pension des affiliés au régime des salariés non agricoles'
    definition_period = YEAR

    def formula(individu, period, parameters):
        duree_assurance = individu('rsna_duree_assurance', period=period)
        salaire_reference = individu('rsna_salaire_reference', period=period)
        age = individu('age', period=period)
        rsna = parameters(period).retraite.rsna
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
        pension_minimale = stage * pension_min_sup + not_(stage) * pension_min_inf
        montant = pension_generique(duree_assurance, salaire_reference, taux_annuite_base, taux_annuite_supplementaire, duree_stage, age_eligible, periode_remplacement_base, plaf_taux_pension)
        eligibilite_age = age > age_eligible
        eligibilite = stage * eligibilite_age * (salaire_reference > 0)
        montant_pension_percu = max_(montant, pension_minimale * smig)
        return eligibilite * montant_pension_percu

class rsna_pension_au_31_decembre(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension'

    def formula(individu, period):
        pension_brute_au_31_decembre = individu('rsna_pension_brute_au_31_decembre', period)
        majoration_pension_au_31_decembre = individu('rsna_majoration_pension_au_31_decembre', period)
        return pension_brute_au_31_decembre + majoration_pension_au_31_decembre

class rsna_pension_brute(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension brute'

    def formula(individu, period, parameters):
        NotImplementedError

class rsna_pension_brute_au_31_decembre(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension brute au 31 décembre'

    def formula(individu, period, parameters):
        annee_de_liquidation = individu('rsna_liquidation_date', period).astype('datetime64[Y]').astype(int) + 1970
        if all(period.start.year < annee_de_liquidation):
            return individu.empty_array()
        last_year = period.last_year
        pension_brute_au_31_decembre_annee_precedente = individu('rsna_pension_brute_au_31_decembre', last_year)
        revalorisation = parameters(period).rsna.revalorisation_pension_au_31_decembre
        pension_brute = individu('rsna_pension_brute', period)
        return revalorise(pension_brute_au_31_decembre_annee_precedente, pension_brute, annee_de_liquidation, revalorisation, period)

class rsna_pension_servie(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension servie'

    def formula(individu, period, parameters):
        annee_de_liquidation = individu('rsna_liquidation_date', period).astype('datetime64[Y]').astype(int) + 1970
        if all(annee_de_liquidation > period.start.year):
            return individu.empty_array()
        last_year = period.last_year
        pension_au_31_decembre_annee_precedente = individu('rsna_pension_au_31_decembre', last_year)
        revalorisation = parameters(period).rsna.revalarisation_pension_servie
        pension = individu('rsna_pension_au_31_decembre', period)
        return revalorise(pension_au_31_decembre_annee_precedente, pension, annee_de_liquidation, revalorisation, period)

class rsna_salaire_de_base(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Salaire de base (salaire brut)'
    set_input = set_input_divide_by_period

class rsna_salaire_de_reference(Variable):
    value_type = float
    entity = Individu
    definition_period = ETERNITY
    label = 'Salaire de référence'

class rsna_salaire_reference(Variable):
    value_type = float
    entity = Individu
    label = 'Salaires de référence du régime des salariés non agricoles'
    definition_period = YEAR

    def formula(individu, period):
        k = 10
        mean_over_largest = make_mean_over_largest(k=k)
        n = 40
        salaire_refererence = apply_along_axis(mean_over_largest, axis=0, arr=vstack([individu('rsna_salaire_de_base', period=year) for year in range(period.start.year, period.start.year - n, -1)]))
        return salaire_refererence

class rsna_taux_de_liquidation(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Taux de liquidation de la pension'

    def formula(individu, period, parameters):
        bareme_annuite = parameters(period).retraite.rsna.bareme_annuite
        duree_assurance = individu('rsna_duree_assurance', period)
        taux_annuite = bareme_annuite.calc(duree_assurance)
        return taux_annuite