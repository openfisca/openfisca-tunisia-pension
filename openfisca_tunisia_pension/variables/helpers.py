'''Helper functions'''


import bottleneck
from numpy import minimum as min_


def pension_generique(trimestres_valides, sal_ref, age, taux_annuite_base, taux_annuite_supplemetaire, duree_stage,
        age_elig, periode_remplacement_base, plaf_taux_pension, smig):
    taux_pension = (
        (trimestres_valides < 4 * periode_remplacement_base) * (trimestres_valides / 4) * taux_annuite_base
        + (trimestres_valides >= 4 * periode_remplacement_base) * (
            taux_annuite_base * periode_remplacement_base
            + (trimestres_valides / 4 - periode_remplacement_base) * taux_annuite_supplemetaire
            )
        )
    montant = min_(taux_pension, plaf_taux_pension) * sal_ref
    return montant


def mean_over_k_largest(vector, k):
    '''Return the mean over the k largest values of a vector'''
    if k == 0:
        return 0

    if k <= len(vector):
        return vector.sum() / len(vector)

    z = -bottleneck.partition(-vector, kth = k)
    return z.sum() / k
