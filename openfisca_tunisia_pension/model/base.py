# -*- coding: utf-8 -*-


from datetime import date

from openfisca_core.columns import (AgeCol, DateCol, EnumCol, FloatCol, IntCol)
from openfisca_core.enumerations import Enum
from openfisca_core.variables import Variable

from openfisca_tunisia_pension.entities import FoyerFiscal, Individu, Menage


__all__ = [
    'AgeCol',
    'date',
    'DateCol',
    'Enum',
    'EnumCol',
    'FloatCol',
    'FoyerFiscal',
    'IntCol',
    'Individu',
    'Menage',
    'QUIFOY',
    'QUIMEN',
    'REG',
    'Variable',
    ]

QUIFOY = Enum(['vous', 'conj', 'enf1', 'enf2', 'enf3', 'enf4', 'enf5', 'enf6', 'enf7', 'enf8', 'enf9'])
QUIMEN = Enum(['pref', 'cref', 'enf1', 'enf2', 'enf3', 'enf4', 'enf5', 'enf6', 'enf7', 'enf8', 'enf9'])
REG = Enum(['rsna', 'rsa', 'rsaa', 'rtns', 'rtte', 're', 'rtfr', 'raic', 'cnrps_sal', 'cnrps_pen'])
