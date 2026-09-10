# Audit sources retraite OpenFisca Tunisia Pension

Généré le 2026-09-10 par `scripts/generate_pension_source_audit.py`.

## Synthèse

- Fichiers paramètres retraite: 63
- Paramètres avec valeurs ou barèmes: 50
- Paramètres avec référence: 31 / 50
- Paramètres sans référence: 19 / 50
- Paramètres multi-dates: 6
- Textes JORT locaux: 1

## Couverture par régime

| Régime | Paramètres avec valeurs |
| --- | ---: |
| `cnrps` | 35 |
| `rsa` | 7 |
| `rsna` | 8 |

## Textes cités dans les références

| Texte | Occurrences paramètres | Statut |
| --- | ---: | --- |
| `1959-18` - Loi n° 59-18 du 5 février 1959, pensions civiles et militaires | 3 | JORT 1959/8, texte pivot |
| `1960-33` - Loi n° 60-33 du 14 décembre 1960, invalidité/vieillesse/survie secteur non agricole | 1 | JORT 1960/57, texte pivot |
| `1981-70` - Texte cité par les paramètres | 3 | JORT 1981/51 |
| `1985-1177` - Texte cité par les paramètres | 4 | JORT 1985/68 |
| `1985-1178` - Texte cité par les paramètres | 2 | JORT 1985/68 |
| `1985-12` - Loi n° 85-12 du 5 mars 1985, pensions civiles et militaires secteur public | 17 | JORT 1985/20, texte pivot |
| `1985-611` - Texte cité par les paramètres | 4 | à résoudre |
| `1988-71` - Texte cité par les paramètres | 1 | JORT 1988/45 |
| `1993-308` - Texte cité par les paramètres | 4 | JORT 1993/13 |
| `2007-43` - Loi n° 2007-43 du 25 juin 2007, pensions public/privé/régimes spéciaux | 2 | texte local, JORT 2007/51, texte pivot |
| `2019-37` - Loi n° 2019-37 du 30 avril 2019, relèvement âge retraite | 2 | JORT 2019/35, texte pivot |
| `2024-9` - Texte cité par les paramètres | 4 | JORT 2024/20 |

## Textes JORT locaux

| Fichier | Lois détectées | Articles détectés |
| --- | --- | --- |
| `tmp/JORTs/Loi-n°-2007-43-du-25-Juin-2007-Fr.txt` | `2007-43`; cite `1983-31`, `1985-12`, `1985-16`, `1988-16` | premier, 2, 30 (nouveau), 37 (nouveau), 46 (nouveau), 47 (nouveau), 3, 4, 5 |

## Paramètres sans référence

| Paramètre | Description | Dates |
| --- | --- | --- |
| `retraite.cnrps.age_legal.civil.enseignants_du_superieur` | Age de départ à la retraite pour certains enseignants du supérieur | 2019-04-01 |
| `retraite.cnrps.duree_de_service_minimale` | Durée de service minimale requise pour prétendre à une pension de retraite | 1974-01-01 |
| `retraite.cnrps.pension_minimale.allocation_vieillesse` | Allocation de vieillesse (en parts du Smig) | 1959-02-01 |
| `retraite.cnrps.pension_minimale.duree_service_allocation_vieillesse` | Durée de service minimale requise pour prétendre à une allocation de vieillesse | 1974-01-01 |
| `retraite.cnrps.pension_minimale.minimum_garanti` | Pension minimale garanti de la CNRPS | 1974-01-01 |
| `retraite.rsa.age_legal` | Age légal de de départ à la retraite | 1981-02-24 |
| `retraite.rsa.pension_min` | Pension minimale (en part de SMAG) | 1981-02-24 |
| `retraite.rsa.periode_remplacement_base` | Période de remplacement de base | 1981-02-24 |
| `retraite.rsa.plaf_taux_pension` | Plafonnement du taux de pension | 1981-02-24 |
| `retraite.rsa.stage_requis` | Durée normale du stage requis | 1981-02-24 |
| `retraite.rsa.taux_annuite_base` | Taux d'annuité de base | 1981-02-24 |
| `retraite.rsa.taux_annuite_supplementaire` | Taux d'annuité supplémentaire | 1981-02-24 |
| `retraite.rsna.age_dep_anticip` | Age minimum de départ à la retraite anticipée | 1974-01-01 |
| `retraite.rsna.age_legal` | Age légal de de départ à la retraite | 1974-01-01 |
| `retraite.rsna.pension_minimale.inf` | Inférieur à la durée du stage requis | 1974-01-01 |
| `retraite.rsna.pension_minimale.sup` | Supérieur à la durée du stage requis | 1974-01-01 |
| `retraite.rsna.plaf_taux_pension` | Plafonnement du taux de pension | 1974-01-01 |
| `retraite.rsna.stage_derog` | Durée du stage dérogatoire | 1974-01-01 |
| `retraite.rsna.stage_requis` | Durée normale du stage requis | 1974-01-01 |

## Paramètres multi-dates à relier finement

| Paramètre | Dates | Lois citées |
| --- | --- | --- |
| `retraite.cnrps.age_legal.civil.cadre_commun` | 1959-02-01, 2019-07-01, 2020-01-01 | `1959-18`, `1985-12`, `2019-37` |
| `retraite.cnrps.age_legal.civil.cadres_actifs` | 1959-02-01, 2019-07-01, 2020-01-01 | `1959-18`, `1985-12`, `2019-37` |
| `retraite.cnrps.bareme_annuite` | 1959-02-01, 1985-01-01 | `1959-18`, `1985-12` |
| `retraite.cnrps.depart_anticipe.meres_3_enfants.age_maximum_enfant` | 1985-03-05, 1988-06-27 | `1985-12`, `1988-71` |
| `retraite.cnrps.depart_anticipe.sur_demande.cadre_commun.age_minimum` | 1985-03-05, 2007-06-25 | `1985-12`, `2007-43` |
| `retraite.cnrps.depart_anticipe.sur_demande.cadre_commun.duree_minimum` | 1985-03-05, 2007-06-25 | `1985-12`, `2007-43` |

## Accès aux paramètres depuis les variables

| Fichier | Paramètres retraite accédés |
| --- | --- |
| `accessoires_formulas.py` | `retraite.cnrps.accessoires.indemnites_familiales` |
| `cnrps.py` | `retraite.cnrps`, `retraite.cnrps.bareme_annuite` |
| `rsa.py` | `retraite.rsa`, `retraite.rsa.bareme_annuite` |
| `rsna.py` | `retraite.rsna`, `retraite.rsna.bareme_annuite` |
| `survivants.py` | `retraite.cnrps.capital_deces`, `retraite.cnrps.survivants` |

## Recommandations

- Ajouter des références aux paramètres RSA et aux accessoires/pensions minimales avant toute correction de valeur.
- Promouvoir le texte `2007-43` depuis `tmp/JORTs` vers un emplacement de sources documenté si le dépôt doit conserver les textes pivots.
- Résoudre prioritairement les textes `1959-18`, `1960-33`, `1981-6`, `1985-12` et `2019-37` dans le cache JORT ou dans le corpus législatif externe.
- Traiter les paramètres multi-dates avec une référence par date d'effet, car les dates OpenFisca ne coïncident pas toujours avec la date de signature du texte.
