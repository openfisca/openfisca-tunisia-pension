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
    column = DateCol()
    entity = Individu
    label = u"Date de naissance"
    definition_period = ETERNITY


class salaire(Variable):
    column = IntCol()
    entity = Individu
    label = u"Salaires"
    definition_period = YEAR


class age(Variable):
    column = AgeCol()
    entity = Individu
    label = u"Âge"
    definition_period = YEAR


class nb_trim_val(Variable):
    column = IntCol()
    entity = Individu
    label = u"Nombre de trimestres validés"
    definition_period = YEAR


class regime(Variable):
    column = EnumCol(REG)
    entity = Individu
    label = u"Régime de retraite"
    definition_period = YEAR
