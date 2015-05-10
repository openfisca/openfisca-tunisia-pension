# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from .base import * #  noqua


# raic -> raci

# Socio-economic data
# Donnée d'entrée de la simulation à fournir à partir d'une enquète ou
# à générer avec un générateur de cas type



reference_input_variable(
    column = IntCol(is_permanent = True),
    entity_class = Individus,
    label = u"Identifiant du foyer",
    name = 'idfoy',
    )

reference_input_variable(
    column = IntCol(is_permanent = True),
    entity_class = Individus,
    label = u"Identifiant du ménage",
    name = 'idmen',
    )


reference_input_variable(
    column = EnumCol(QUIMEN, is_permanent = True),
    entity_class = Individus,
    label = u"Rôle dans le foyer",
    name = 'quifoy',
    )

reference_input_variable(
    column = EnumCol(QUIMEN, is_permanent = True),
    entity_class = Individus,
    label = u"Rôle dans le ménage",
    name = 'quimen',
    )


reference_input_variable(
    column = DateCol(is_permanent = True),
    entity_class = Individus,
    label = u"Date de naissance",
    name = 'birth',
    )



reference_input_variable(
    column = EnumCol(
        enum = Enum(
            [
                u"Inconnue",
                u"Collège",
                u"Lycée"
                ],
            ),
        default = 0
        ),
    entity_class = Individus,
    label = u"Scolarité de l'enfant : collège, lycée...",
    name = "scolarite",
    )


reference_input_variable(
    column = IntCol(),
    entity_class = Individus,
    label = u"Salaires",
    name = 'salaire',
    )

reference_input_variable(
    column = AgeCol(),
    entity_class = Individus,
    label = u"Âge",
    name = 'age',
    )

reference_input_variable(
    column = IntCol(),
    entity_class = Individus,
    label = u"Nombre de trimestres validés",
    name = 'nb_trim_val',
    )

reference_input_variable(
    column = EnumCol(REG),
    entity_class = Individus,
    label = u"Régime de retraite",
    name = 'regime',
    )
