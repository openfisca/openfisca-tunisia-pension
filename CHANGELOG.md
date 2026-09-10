# Changelog

### 5.1.1 - [#22](https://github.com/openfisca/openfisca-tunisia-pension/pull/22)

* Amélioration technique.
* Périodes concernées : aucune.
* Zones impactées : aucune.
* Détails :
  - Élargit les bornes de dépendance à `openfisca-core >=43.0.0, <45.0.0` et `numpy >=1.24.3, <3`, et rafraîchit `uv.lock`, qui restait sur core 43.5.0.
  - **Les deux bornes devaient bouger ensemble.** Élargir la seule borne d'`openfisca-core` ne suffit pas : sur Python 3.13, core 44 exige `numpy >=2.1.0`, que le plafond `numpy <2` interdisait. Le résolveur retombait alors silencieusement sur core 43, y compris en résolution `maximal` — de sorte que la CI validait une compatibilité avec core 44 qu'elle ne testait pas.
  - Le verrou est rafraîchi **par mise à jour ciblée** (`uv lock --upgrade-package openfisca-core --upgrade-package numpy`) et non globale : trois paquets sur cent dix-huit bougent. Une mise à jour globale emportait aussi `ruff` de 0.15.5 à 0.16.6, dont les règles nouvelles font échouer le lint sur les variables engendrées par `script_ast` — une remontée d'outil n'a pas sa place dans un correctif de dépendance.
  - Compatibilité vérifiée localement, dépendances effectivement installées : `openfisca-core 44.7.1`, `numpy 2.4.6`, `ruff` inchangé, lint propre et les 53 tests passent.
  - Ce changement ne modifie aucun calcul. Il lève le seul obstacle technique à ce que ce paquet dépende d'`openfisca-tunisia`, dont les bornes sont `openfisca-core >=44, <45` — préalable à la fin de la duplication des paramètres partagés entre les deux dépôts, au premier rang desquels le SMIG, arrêté ici au 1er mai 2019 et courant jusqu'au 1er janvier 2025 dans l'autre.

<!-- -->

# 5.1.0

* Amélioration technique.
* Périodes concernées : toutes.
* Détails :
  - Alignement CI et outillage sur openfisca-tunisia : Ubuntu 24.04, Python 3.10–3.12, uv (sync, cache), Node.js 24
  - Lint : passage à ruff uniquement (remplacement de flake8), per-file-ignores pour les variables générées (script_ast)
  - Makefile : même structure que openfisca-tunisia (format-style, check-style, uv run)
  - Tests YAML : clé `individu` remplacée par `input` (API openfisca_core) ; tests taux_de_liquidation en 1986 avec attendus ajustés ; correction salaire_de_reference attendu
  - CI : suppression du job test-api ; dépendance tomli pour get_minimal_version (Python 3.10)
  - Documentation des règles ruff dans pyproject.toml

# 5.0.0 [#15](https://github.com/openfisca/openfisca-tunisia-pension/pull/15)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `variables/regimes/cnrps`.
* Détails :
  - Introduit le régime de la CNRPS


# 4.0.0 [#14](https://github.com/openfisca/openfisca-tunisia-pension/pull/14)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `variables/regimes`.
* Détails :
  - Sépare les régimes dans différents répertoires

# 3.0.0 [#13](https://github.com/openfisca/openfisca-tunisia-pension/pull/13)

* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : `parameters/pension`, `parameters/retraite`.
* Détails :
  - Renomme `parameters/pension` en  `parameters/retraite`

### 2.0.1 [#11](https://github.com/openfisca/openfisca-tunisia-pension/pull/11)

* Amélioration technique.
* Détails :
  - Utilise variables au lieu de model.
  - Utilise github actions et pyproject.toml.

### 2.0.0

* Migrate to openfisca-core v24 syntax
* Update `regime_securite_social` variable periodicity
* Details:
    * Move parameters from xml format to yaml files tree

### 1.0.0
* Renomme `nb_trim_val` en `duree_assurance`
* Utilisation de noms longs pour différent paramètres

## 0.9.2
* Migrate old-syntax formula

## 0.9.1
* Fix legislation tests

## 0.9.0
* Migrate to openfisca-core 14.0.1 syntax
* Use bottleneck.partition instead of deprecated bottleneck.partsort

## 0.8.0
* Migrate to openfisca-core 12.0.3 syntax
