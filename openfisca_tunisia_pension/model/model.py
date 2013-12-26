# -*- coding:utf-8 -*-Boll
# Copyright © 2012 Clément Schaff, Mahdi Ben Jelloul

"""
OpenFiscaTn, Logiciel libre de simulation du système socio-fiscal tunisien
Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

This file is part of openFisca.

    openFisca is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    openFisca is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with openFisca.  If not, see <http://www.gnu.org/licenses/>.
"""


from datetime import date

from openfisca_core.columns import Prestation, BoolPresta
from openfisca_core.descriptions import ModelDescription

from . import pension


class OutputDescription(ModelDescription):
    """
    Model description
    """

    ############################################################
    # Pensions
    ############################################################
    
    sal_ref_rsna = Prestation(pension._sal_ref_rsna, entity="ind", label=u"Salaire de référence")
    pension_rsna = Prestation(pension._pension_rsna, entity="ind", label=u"Pension de retraite")
    
    sal_ref_rsa = Prestation(pension._sal_ref_rsa, entity="ind", label=u"Salaire de référence")
    pension_rsa = Prestation(pension._pension_rsa, entity="ind", label=u"Pension de retraite")
