from openfisca_core.entities import build_entity


Individu = build_entity(
    key = 'individu',
    plural = 'individus',
    label = 'Individ',
    is_person = True
    )

FoyerFiscal = build_entity(
    key = 'foyer_fiscal',
    plural = 'foyers_fiscaux',
    label = 'Déclaration d’impôts',
    roles = [
        {
            'key': 'declarant',
            'plural': 'declarants',
            'label': 'Déclarants',
            'subroles': ['declarant_principal', 'conjoint']
            },
        {
            'key': 'personne_a_charge',
            'plural': 'personnes_a_charge',
            'label': 'Personnes à charge'
            },
        ]
    )

Menage = build_entity(
    key = 'menage',
    plural = 'menages',
    label = 'Logement principal',
    roles = [
        {
            'key': 'personne_de_reference',
            'label': 'Personne de référence',
            'max': 1
            },
        {
            'key': 'conjoint',
            'label': 'Conjoint',
            'max': 1
            },
        {
            'key': 'enfant',
            'plural': 'enfants',
            'label': 'Enfants',
            'max': 2
            },
        {
            'key': 'autre',
            'plural': 'autres',
            'label': 'Autres'
            }
        ]
    )

entities = [Individu, FoyerFiscal, Menage]
