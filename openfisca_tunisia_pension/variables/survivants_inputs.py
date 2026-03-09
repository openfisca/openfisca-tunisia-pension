from openfisca_core.model_api import *
from openfisca_tunisia_pension.entities import Individu

class age_deces(Variable):
    value_type = int
    entity = Individu
    default_value = -1 # Not deceased
    definition_period = MONTH
    label = "Age au décès"
    set_input = set_input_dispatch_by_period

class deces_par_accident(Variable):
    value_type = bool
    entity = Individu
    default_value = False
    definition_period = MONTH
    label = "Décès suite à un accident (circulation, travail)"
    set_input = set_input_dispatch_by_period

class cnrps_duree_services_effectifs(Variable):
    value_type = int
    entity = Individu
    default_value = 0
    definition_period = MONTH
    label = "Durée des services effectifs (années complètes)"
    set_input = set_input_dispatch_by_period

class cnrps_remuneration_annuelle_deces(Variable):
    value_type = float
    entity = Individu
    default_value = 0.0
    definition_period = MONTH
    label = "Rémunération annuelle de base au moment du décès"
    set_input = set_input_dispatch_by_period

class cnrps_pension_reference_deces(Variable):
    value_type = float
    entity = Individu
    default_value = 0.0
    definition_period = MONTH
    label = "Montant de la pension dont l'agent bénéficiait ou aurait bénéficié"
    set_input = set_input_dispatch_by_period

class nombre_orphelins_eligibles(Variable):
    value_type = int
    entity = Individu
    default_value = 0
    definition_period = MONTH
    label = "Nombre d'enfants eligibles à la Pension Temporaire d'Orphelin (PTO)"
    set_input = set_input_dispatch_by_period

class conjoint_survivant_eligible(Variable):
    value_type = bool
    entity = Individu
    default_value = False
    definition_period = MONTH
    label = "Présence d'un conjoint survivant éligible à la pension de réversion"
    set_input = set_input_dispatch_by_period
