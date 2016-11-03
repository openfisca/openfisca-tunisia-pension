# -*- coding: utf-8 -*-


from openfisca_tunisia_pension.model.base import *  #  noqua


# raic -> raci

# Socio-economic data
# Donnée d'entrée de la simulation à fournir à partir d'une enquète ou
# à générer avec un générateur de cas type


class idfoy(Variable):
    column = IntCol(is_permanent = True)
    entity_class = Individus
    label = u"Identifiant du foyer"


class idmen(Variable):
    column = IntCol(is_permanent = True)
    entity_class = Individus
    label = u"Identifiant du ménage"


class quifoy(Variable):
    column = EnumCol(QUIMEN, is_permanent = True)
    entity_class = Individus
    label = u"Rôle dans le foyer"


class quimen(Variable):
    column = EnumCol(QUIMEN, is_permanent = True)
    entity_class = Individus
    label = u"Rôle dans le ménage"


class birth(Variable):
    column = DateCol(is_permanent = True)
    entity_class = Individus
    label = u"Date de naissance"


class scolarite(Variable):
    column = EnumCol(
        enum = Enum(
            [
                u"Inconnue",
                u"Collège",
                u"Lycée"
                ],
            ),
        default = 0
        )
    entity_class = Individus
    label = u"Scolarité de l'enfant : collège, lycée..."


class salaire(Variable):
    column = IntCol()
    entity_class = Individus
    label = u"Salaires"


class age(Variable):
    column = AgeCol()
    entity_class = Individus
    label = u"Âge"


class nb_trim_val(Variable):
    column = IntCol()
    entity_class = Individus
    label = u"Nombre de trimestres validés"


class regime(Variable):
    column = EnumCol(REG)
    entity_class = Individus
    label = u"Régime de retraite"
