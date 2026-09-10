# Changelog

### 5.3.1 - [#19](https://github.com/openfisca/openfisca-tunisia-pension/pull/19)

* Amélioration technique.
* Périodes concernées : aucune.
* Zones impactées : aucune — outillage seul.
* Détails :
  - Ajoute `scripts/generate_pension_source_audit.py`, qui dresse la carte de ce qui est sourcé et de ce qui ne l'est pas : couverture par régime, textes cités, paramètres sans référence, paramètres multi-dates, et rapprochement avec le corpus JORT local quand il est disponible. Sortie dans `reports/openfisca/pension_source_audit.md` et `parameters_candidates/retraite_source_candidates.yml`.
  - **Ce que l'audit établit aujourd'hui** : 50 paramètres portent une valeur ou un barème, **31 ont une référence et 19 n'en ont aucune**. Les sept paramètres du régime des salariés agricoles n'en ont pas une seule, et portent tous la même date conventionnelle du 24 février 1981.
  - Il isole aussi un texte impossible : le décret cité « n° 85-611 du 3 juin 1986 », dont le millésime et l'année ne peuvent pas être justes tous les deux. Le rapport le classe « à résoudre ».
  - **Correction au passage** : l'extraction des numéros de texte lisait aussi le champ `note`, dont les plages de pages — « pp. 1312-1315 » — ont exactement la forme d'un numéro de loi. Le rapport annonçait un « texte 1312-1315 » à résoudre. Elle ne lit plus que `title` et `href`.

<!-- -->

## 5.3.0 - [#21](https://github.com/openfisca/openfisca-tunisia-pension/pull/21)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 1985-03-05.
* Zones impactées : `parameters/retraite/cnrps/survivants`, `parameters/retraite/cnrps/capital_deces`, `variables/survivants.py`.
* Détails :
  - **Survivants — loi n° 85-12 du 5 mars 1985.** Les taux de réversion étaient des constantes écrites dans `variables/survivants.py`. Ils deviennent des paramètres datés et référencés : `taux_conjoint` (0,75 — article 43), `taux_orphelin` (0,10 — article 45), `plafond_cumul` (1,0 — article 45) et `taux_partage_5_orphelins` (0,50 — article 45).
  - **Capital-décès — décret n° 93-308 du 1er février 1993.** Même traitement : `majoration_par_enfant` (0,10), `multiplicateur_deces_accidentel` (2,0), `plafond_anciennete_mois` (18) et le barème `taux_retraite_selon_age`, dégressif de 100 % avant 60 ans à 10 % à partir de 85 ans (article 6).
  - Le remaniement **préserve les résultats** : les six tests de `test_survivants` et les trois de `test_capital_deces` passent à l'identique.
  - **Localisations JORT** ajoutées aux références qui n'en avaient pas — lois n° 59-18, 60-33, 85-12, 88-71, 2007-43 —, et **vingt-trois références converties de la chaîne libre à la forme structurée** `title` + `href` + `note`, avec l'URL du fascicule sur pist.tn. Une référence en texte libre ne se vérifie pas ; une URL, si.
  - Neuf références restent en texte libre, faute d'URL vérifiée : les indemnités du décret « n° 85-611 du 3 juin 1986 » — dont le millésime et l'année se contredisent —, la loi n° 81-70 des indemnités de revenu unique, et le décret n° 85-1178 des départs anticipés astreignants.

<!-- -->

## 5.2.0 - [#23](https://github.com/openfisca/openfisca-tunisia-pension/pull/23)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 2020-01-01.
* Zones impactées : `parameters/marche_travail`, pensions minimales de tous les régimes.
* Détails :
  - Ce paquet lit désormais les sous-arbres de paramètres dont `openfisca-tunisia` est propriétaire **chez lui**, greffés au chargement, au lieu d'en garder une copie. La copie locale de `marche_travail` est supprimée.
  - **Le SMIG était figé depuis 2019.** Les deux paquets portaient chacun leur `marche_travail`, et les copies avaient divergé sans que rien ne le signale : la série s'arrêtait ici au 1er mai 2019 avec 36 références, quand celle d'`openfisca-tunisia` court jusqu'au 1er janvier 2025 avec 110. Le SMIG 40 h lu passe de **343,892 dinars** gelés à **448,238** en 2025.
  - **Conséquence sur les calculs** : les pensions minimales — `minimum_garanti` et `allocation_vieillesse` du CNRPS, `inf` et `sup` du RSNA — sont indexées sur le SMIG. Elles étaient donc **fausses de 2020 à 2026**, d'une valeur périmée et non d'une valeur manquante : rien ne le signalait.
  - La règle qui en découle : un sous-arbre de paramètres a un propriétaire et un seul. `retraite/` appartient à ce paquet, `marche_travail/` à `openfisca-tunisia`, dont la PR #402 a retiré sa copie morte de `retraite/`. `tests/test_parametres_partages.py` interdit le retour de la duplication.
  - Trois éléments que seul l'autre paquet portait sont récoltés au passage : l'URL du fascicule du JORT sur les âges légaux du cadre commun et des cadres actifs — dont les références en texte libre deviennent structurées et gagnent leur page —, le paragraphe sur l'option de report des enseignants du supérieur introduite par la loi n° 2019-37, et `rsna/plaf_taux_pension.yaml`.
  - Le plancher d'`openfisca-core` monte à **44.0.3**, puisque c'est ce qu'`openfisca-tunisia` exige. Le patch compte : `.github/get_minimal_version.py` épingle le plancher **à l'exact** pour la matrice « minimal », et `44.0.0` n'a jamais été publiée — la série 44 commence à 44.0.3. Un plancher qui n'existe pas rend la résolution minimale insatisfiable.

<!-- -->

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
