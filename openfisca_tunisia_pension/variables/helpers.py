'''Helper functions'''


from numpy import minimum as min_


def pension_generique(duree_assurance, sal_ref, taux_annuite_base, taux_annuite_supplementaire, duree_stage,
        age_elig, periode_remplacement_base, plaf_taux_pension):
    taux_pension = (
        (duree_assurance < 4 * periode_remplacement_base) * (duree_assurance / 4) * taux_annuite_base
        + (duree_assurance >= 4 * periode_remplacement_base) * (
            taux_annuite_base * periode_remplacement_base
            + (duree_assurance / 4 - periode_remplacement_base) * taux_annuite_supplementaire
            )
        )
    montant = min_(taux_pension, plaf_taux_pension) * sal_ref
    return montant
