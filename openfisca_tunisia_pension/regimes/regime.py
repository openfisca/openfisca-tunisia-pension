'''Abstract regimes definition.'''


from openfisca_core.model_api import *
# from openfisca_core.errors.variable_not_found_error import VariableNotFoundError

# Import the Entities specifically defined for this tax and benefit system
from openfisca_tunisia_pension.entities import Individu


class AbstractRegime(object):
    name = None
    variable_prefix = None
    parameters = None

    class cotisation(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = 'cotisation retraite employeur'

        def formula(individu, period, parameters):
            NotImplementedError

    class duree_assurance(Variable):
        value_type = int
        entity = Individu
        definition_period = YEAR
        label = "Durée d'assurance (trimestres validés)"

        # def formula(individu, period, parameters):
        #     duree_assurance_validee = individu("regime_name_duree_assurance_validee", period)
        #     annee_de_liquidation = individu('regime_name_liquidation_date', period).astype('datetime64[Y]').astype(int) + 1970
        #     majoration_duree_assurance = individu('regime_name_majoration_duree_assurance', period)
        #     return where(
        #         annee_de_liquidation == period.start.year,
        #         round_(duree_assurance_validee + majoration_duree_assurance),  # On arrondi l'année de la liquidation
        #         duree_assurance_validee
        #         )

    class liquidation_date(Variable):
        value_type = date
        entity = Individu
        definition_period = ETERNITY
        label = 'Date de liquidation'
        default_value = date(2250, 12, 31)

    class majoration_pension(Variable):
        value_type = int
        entity = Individu
        definition_period = MONTH
        label = 'Majoration de pension'

        def formula(individu, period, parameters):
            NotImplementedError

    class pension(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = 'Pension'

        def formula(individu, period, parameters):
            NotImplementedError

    class pension_brute(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = 'Pension brute'

        def formula(individu, period, parameters):
            NotImplementedError

    class pension_servie(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = 'Pension servie'

        def formula(individu, period, parameters):
            NotImplementedError


class AbstractRegimeEnAnnuites(AbstractRegime):
    name = 'Régime en annuités'
    variable_prefix = 'regime_en_annuites'
    parameters = 'regime_en_annuites'

    class duree_assurance_annuelle(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = "Durée d'assurance (en trimestres validés l'année considérée)"

    class majoration_duree_assurance(Variable):
        value_type = float
        entity = Individu
        definition_period = ETERNITY
        label = "Majoration de durée d'assurance"

        def formula(individu, period):
            return (
                individu('regime_name_majoration_duree_assurance_enfant', period)
                + individu('regime_name_majoration_duree_assurance_autre', period)
                )

    class majoration_duree_assurance_autre(Variable):
        value_type = float
        entity = Individu
        definition_period = ETERNITY
        label = "Majoration de durée d'assurance autre que celle attribuée au motif des enfants"

    class majoration_pension(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = 'Majoration de pension'

    class majoration_pension_au_31_decembre(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = 'Majoration de pension au 31 décembre'

        def formula(individu, period, parameters):
            annee_de_liquidation = individu('regime_name_liquidation_date', period).astype('datetime64[Y]').astype(int) + 1970
            # Raccouci pour arrêter les calculs dans le passé quand toutes les liquidations ont lieu dans le futur
            if all(annee_de_liquidation > period.start.year):
                return individu.empty_array()
            last_year = period.last_year
            majoration_pension_au_31_decembre_annee_precedente = individu('regime_name_majoration_pension_au_31_decembre', last_year)
            revalorisation = parameters(period).regime_name.revalorisation_pension_au_31_decembre
            majoration_pension = individu('regime_name_majoration_pension', period)
            return revalorise(
                majoration_pension_au_31_decembre_annee_precedente,
                majoration_pension,
                annee_de_liquidation,
                revalorisation,
                period,
                )

    class pension(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = 'Pension'

        def formula(individu, period):
            pension_brute = individu('regime_name_pension_brute', period)
            majoration_pension = individu('regime_name_majoration_pension', period)
            return pension_brute + majoration_pension

    class pension_au_31_decembre(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = 'Pension'

        def formula(individu, period):
            pension_brute_au_31_decembre = individu('regime_name_pension_brute_au_31_decembre', period)
            majoration_pension_au_31_decembre = individu('regime_name_majoration_pension_au_31_decembre', period)
            return pension_brute_au_31_decembre + majoration_pension_au_31_decembre

    class pension_brute(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = 'Pension brute'

        def formula(individu, period, parameters):
            taux_de_liquidation = individu('regime_name_taux_de_liquidation', period)
            salaire_de_reference = individu('regime_name_salaire_de_reference', period)
            pension_minimale = individu('regime_name_pension_minimale', period)
            pension_maximale = individu('regime_name_pension_maximale', period)
            return min_(
                pension_maximale,
                max_(
                    taux_de_liquidation * salaire_de_reference,
                    pension_minimale
                    )
                )

    class pension_brute_au_31_decembre(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = 'Pension brute au 31 décembre'

        def formula(individu, period, parameters):
            annee_de_liquidation = individu('regime_name_liquidation_date', period).astype('datetime64[Y]').astype(int) + 1970
            # Raccouci pour arrêter les calculs dans le passé quand toutes les liquidations ont lieu dans le futur
            if all(period.start.year < annee_de_liquidation):
                return individu.empty_array()
            last_year = period.last_year
            pension_brute_au_31_decembre_annee_precedente = individu('regime_name_pension_brute_au_31_decembre', last_year)
            revalorisation = parameters(period).regime_name.revalorisation_pension_au_31_decembre
            pension_brute = individu('regime_name_pension_brute', period)
            return revalorise(
                pension_brute_au_31_decembre_annee_precedente,
                pension_brute,
                annee_de_liquidation,
                revalorisation,
                period,
                )

    class pension_maximale(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = 'Pension maximale'

        def formula(individu, period, parameters):
            NotImplementedError

    class pension_minimale(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = 'Pension minimale'

        def formula(individu, period, parameters):
            NotImplementedError

    class pension_servie(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = 'Pension servie'

        def formula(individu, period, parameters):
            annee_de_liquidation = individu('regime_name_liquidation_date', period).astype('datetime64[Y]').astype(int) + 1970
            # Raccouci pour arrêter les calculs dans le passé quand toutes les liquidations ont lieu dans le futur
            if all(annee_de_liquidation > period.start.year):
                return individu.empty_array()
            last_year = period.last_year
            pension_au_31_decembre_annee_precedente = individu('regime_name_pension_au_31_decembre', last_year)
            revalorisation = parameters(period).regime_name.revalarisation_pension_servie
            pension = individu('regime_name_pension_au_31_decembre', period)
            return revalorise(
                pension_au_31_decembre_annee_precedente,
                pension,
                annee_de_liquidation,
                revalorisation,
                period,
                )

    class salaire_de_base(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = 'Salaire de base (salaire brut)'
        set_input = set_input_divide_by_period

    class salaire_de_reference(Variable):
        value_type = float
        entity = Individu
        definition_period = ETERNITY
        label = 'Salaire de référence'

    class taux_de_liquidation(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = 'Taux de liquidation de la pension'

        def formula(individu, period, parameters):
            bareme_annuite = parameters(period).retraite.regime_name.bareme_annuite
            duree_assurance = individu('regime_name_duree_assurance', period)
            taux_annuite = bareme_annuite.calc(duree_assurance)
            return taux_annuite


# def revalorise(variable_31_decembre_annee_precedente, variable_originale, annee_de_liquidation, revalorisation, period):
#     return select(
#         [
#             annee_de_liquidation > period.start.year,
#             annee_de_liquidation == period.start.year,
#             annee_de_liquidation < period.start.year,
#             ],
#         [
#             0,
#             variable_originale,
#             variable_31_decembre_annee_precedente * revalorisation
#             ]
#         )
