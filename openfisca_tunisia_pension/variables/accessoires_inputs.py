from openfisca_tunisia_pension.entities import Individu
from openfisca_core.model_api import (
    Variable,
    MONTH,
    set_input_dispatch_by_period,
)



class nombre_enfants_charge(Variable):
    value_type = int
    entity = Individu
    default_value = 0
    definition_period = MONTH
    label = "Nombre d'enfants à charge pour les indemnités familiales"
    set_input = set_input_dispatch_by_period

class mere_divorcee_garde_enfants(Variable):
    value_type = bool
    entity = Individu
    default_value = False
    definition_period = MONTH
    label = "Mère divorcée ayant obtenu la garde de ses enfants"
    set_input = set_input_dispatch_by_period

class conjoint_sans_revenu(Variable):
    value_type = bool
    entity = Individu
    default_value = False
    definition_period = MONTH
    label = "Conjoint sans aucun revenu (activité, retraite, ou invalidité)"
    set_input = set_input_dispatch_by_period
