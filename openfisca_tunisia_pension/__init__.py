"""OpenFisca Tunisia Pension tax-benefit system."""

# Standard Library
import logging
import os

# Third Party
from openfisca_core.parameters import ParameterNode
from openfisca_core.taxbenefitsystems import TaxBenefitSystem

# First Party
from openfisca_tunisia_pension import entities
from openfisca_tunisia_pension.scripts_ast import script_ast

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))

# Sous-arbres de paramètres dont openfisca-tunisia est propriétaire, et que ce paquet
# lit chez lui plutôt que d'en garder une copie.
#
# POURQUOI. Les deux paquets ont longtemps porté chacun leur `marche_travail`, et les
# copies ont divergé sans que rien ne le signale : le SMIG s'était arrêté ici au
# 1er mai 2019 avec 36 références, quand celui d'openfisca-tunisia courait jusqu'au
# 1er janvier 2025 avec 110. Comme les pensions minimales sont indexées sur le SMIG,
# elles étaient inengendrables pour 2020-2026 — une valeur périmée, pas une valeur
# manquante, donc silencieuse.
#
# La règle qui en découle : un sous-arbre a un propriétaire et un seul. `retraite/`
# appartient à ce paquet, `marche_travail/` à openfisca-tunisia. Le test
# `tests/test_parametres_partages.py` échoue si un chemin réapparaît des deux côtés.
SOUS_ARBRES_PARTAGES = ("marche_travail",)

logging.getLogger("numba.core.ssa").disabled = True
logging.getLogger("numba.core.byteflow").disabled = True
logging.getLogger("numba.core.interpreter").disabled = True

# Convert regimes classes to OpenFisca variables.
script_ast.main(verbose=False)


class TunisiaPensionTaxBenefitSystem(TaxBenefitSystem):
    """Tunisian pensions tax benefit system"""

    CURRENCY = "DT"

    def __init__(self):
        super(TunisiaPensionTaxBenefitSystem, self).__init__(entities.entities)

        # We add to our tax and benefit system all the variables
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, "variables"))

        # We add to our tax and benefit system all the legislation parameters defined in the  parameters files
        parameters_path = os.path.join(COUNTRY_DIR, "parameters")
        self.load_parameters(parameters_path)

        self.greffer_parametres_partages()

    def greffer_parametres_partages(self) -> None:
        """Greffe les sous-arbres de paramètres dont openfisca-tunisia est propriétaire.

        `load_parameters` ne sait construire un arbre que depuis un seul répertoire :
        on greffe donc les sous-arbres partagés après coup, chacun lu à sa source.
        """
        import openfisca_tunisia

        racine = os.path.join(
            os.path.dirname(os.path.abspath(openfisca_tunisia.__file__)),
            "parameters",
        )
        for nom in SOUS_ARBRES_PARTAGES:
            chemin = os.path.join(racine, nom)
            if not os.path.isdir(chemin):
                msg = (
                    f"Le sous-arbre partagé « {nom} » est introuvable dans "
                    f"openfisca-tunisia ({chemin}). Les deux paquets ont-ils dérivé ?"
                )
                raise FileNotFoundError(msg)
            self.parameters.add_child(nom, ParameterNode(nom, directory_path=chemin))


CountryTaxBenefitSystem = TunisiaPensionTaxBenefitSystem
