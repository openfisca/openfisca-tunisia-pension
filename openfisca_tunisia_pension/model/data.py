# -*- coding: utf-8 -*-


from openfisca_tunisia_pension.model.base import *


# raic -> raci

# Socio-economic data
# Donnée d'entrée de la simulation à fournir à partir d'une enquète ou
# à générer avec un générateur de cas type


# class idfoy(Variable):
#     column = IntCol()
#     entity = Individu
#     label = u"Identifiant du foyer"


# class idmen(Variable):
#     column = IntCol()
#     entity = Individu
#     label = u"Identifiant du ménage"


# class quifoy(Variable):
#     column = EnumCol(QUIMEN, )
#     entity = Individu
#     label = u"Rôle dans le foyer"


# class quimen(Variable):
#     column = EnumCol(QUIMEN, )
#     entity = Individu
#     label = u"Rôle dans le ménage"


class date_naissance(Variable):
    value_type = date
    default_value = date(1970, 1, 1)
    entity = Individu
    label = u"Date de naissance"
    definition_period = ETERNITY


class salaire(Variable):
    value_type = float
    entity = Individu
    label = u"Salaires"
    definition_period = YEAR


class age(Variable):
    value_type = int
    entity = Individu
    label = u"Âge"
    definition_period = YEAR


class trimestres_valides(Variable):
    value_type = int
    entity = Individu
    label = u"Nombre de trimestres validés"
    definition_period = YEAR


class TypesRegimeSecuriteSociale(Enum):
    __order__ = 'rsna rsa rsaa rtns rtte re rtfr raci salarie_cnrps pensionne_cnrps'
    # Needed to preserve the enum order in Python 2

    rsna = u"Régime des Salariés Non Agricoles"
    rsa = u"Régime des Salariés Agricoles"
    rsaa = u"Régime des Salariés Agricoles Amélioré"
    rtns = u"Régime des Travailleurs Non Salariés (secteurs agricole et non agricole)"
    rtte = u"Régime des Travailleurs Tunisiens à l'Etranger"
    re = u"Régime des Etudiants, diplômés de l'enseignement supérieur et stagiaires"
    rtfr = u"Régime des Travailleurs à Faibles Revenus (gens de maisons, travailleurs de chantiers, et artisans travaillant à la pièce)"
    raci = u"Régime des Artistes, Créateurs et Intellectuels"
    salarie_cnrps = u"Régime des salariés affilés à la Caisse Nationale de Retraite et de Prévoyance Sociale"
    pensionne_cnrps = u"Régime des salariés des pensionnés de la Caisse Nationale de Retraite et de Prévoyance Sociale"
    # references :
    # http://www.social.gov.tn/index.php?id=49&L=0
    # http://www.paie-tunisie.com/412/fr/83/reglementations/regimes-de-securite-sociale.aspx



class regime_securite_sociale(Variable):
    value_type = Enum
    possible_values = TypesRegimeSecuriteSociale
    default_value = TypesRegimeSecuriteSociale.rsna
    entity = Individu
    label = u"Régime de sécurité sociale du retraité"
    definition_period = ETERNITY
