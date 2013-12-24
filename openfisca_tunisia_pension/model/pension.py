# -*- coding:utf-8 -*-
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

"""
openFisca, Logiciel libre de simulation du système socio-fiscal français
Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

This file is part of openFisca.

    openFisca is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    openFisca is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with openFisca.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import division
from numpy import ( maximum as max_, minimum as min_, logical_xor as xor_, logical_and as and_, 
                     logical_not as not_, round) 


###############################################################################
## Pensions
###############################################################################

def generic_pension(nb_trim_val, sal_ref, age, 
                    taux_ann_base,taux_ann_sup, duree_stage, age_elig,
                    periode_remp_base, plaf_taux_pension, smig):

    stage = nb_trim_val > 4*duree_stage
    elig_age = age > age_elig
    elig = stage*elig_age*(sal_ref>0) 
    taux_pension = ( (nb_trim_val < 4*periode_remp_base)*(nb_trim_val/4*taux_ann_base) +
                       (nb_trim_val >= 4*periode_remp_base)*( taux_ann_base*periode_remp_base + (nb_trim_val/4 - periode_remp_base)*taux_ann_sup )) 
    
    montant = min_(taux_pension, plaf_taux_pension)*sal_ref
    return montant

def _sal_ref_rsna(sal0, sal1, sal2, sal3, sal4, sal5, sal6, sal7, sal8, sal9, sal10):
    """  
    Salaire de référence 
    """
    # TODO: gérer le nombre d'année
    # TODO: plafonner les salaires à 6 fois le smig de l'année d'encaissement
    
    sal_ref_rsna = (sal0 + sal1 + sal2 + sal3 + sal4 + sal5 + sal6 + sal7 + sal8 + sal9 + sal10)/10
    return sal_ref_rsna
    
def _sal_ref_rsa(sal0, sal1, sal2, _P):
    """  
    Salaire de référence
    """
    # TODO: gérer le nombre d'année
    # TODO: plafonner les salaires à 2 fois le smag de l'année d'encaissement
    
    base_declaration_rsa = 180
    base_liquidation_rsa = 300
    sal_ref_rsa = ((sal0 + sal1 + sal2)/3)*base_liquidation_rsa/base_declaration_rsa 
    
    return sal_ref_rsa 

def _pension(nb_trim_val, sal_ref, regime, age, _P):
    """
    Pension
    """
    taux_ann_base = _P.pension.rsna.taux_ann_base
    taux_ann_sup  = _P.pension.rsna.taux_ann_sup 
    duree_stage = _P.pension.rsna.stage_derog
    age_elig = _P.pension.rsna.age_dep_anticip
    periode_remp_base = _P.pension.rsna.periode_remp_base
    plaf_pension = _P.pension.rsna.plaf_taux_pension
    smig = _P.param_gen.smig_48h
    stage = nb_trim_val > 4*duree_stage 
    pension_min = (stage)*_P.pension.rsna.pension_min.sup + not_(stage)*_P.pension.rsna.pension_min.inf  

    elig_age = age > age_elig
    elig = stage*elig_age*(sal_ref>0) 
    taux_pension = ( (nb_trim_val < 4*periode_remp_base)*(nb_trim_val/4*taux_ann_base) +
                       (nb_trim_val >= 4*periode_remp_base)*( taux_ann_base*periode_remp_base + (nb_trim_val/4 - periode_remp_base)*taux_ann_sup )) 
    
    montant = min_(taux_pension, plaf_pension)*sal_ref
    
    
    montant_percu = max_(montant, pension_min*smig)
    pension = elig*montant_percu
    
    
    return pension


def _pension_rsna(nb_trim_val, sal_ref_rsna, regime, age, _P):
    """
    Pension du régime des salariés non-agricoles
    """
    taux_ann_base = _P.pension.rsna.taux_ann_base
    taux_ann_sup  = _P.pension.rsna.taux_ann_sup 
    duree_stage = _P.pension.rsna.stage_derog
    age_elig = _P.pension.rsna.age_dep_anticip
    periode_remp_base = _P.pension.rsna.periode_remp_base
    plaf_taux_pension = _P.pension.rsna.plaf_taux_pension
    smig = _P.param_gen.smig_48h
    stage = nb_trim_val > 4*duree_stage 
    pension_min = (stage)*_P.pension.rsna.pension_min.sup + not_(stage)*_P.pension.rsna.pension_min.inf  
    sal_ref = sal_ref_rsna

    montant = generic_pension(nb_trim_val, sal_ref, age, 
                    taux_ann_base,taux_ann_sup, duree_stage, age_elig,
                    periode_remp_base, plaf_taux_pension, smig)

    elig_age = age > age_elig
    elig = stage*elig_age*(sal_ref>0) 
    montant_percu = max_(montant, pension_min*smig)
    pension = elig*montant_percu    
    return pension


def _pension_rsa(nb_trim_val, sal_ref_rsa, regime, age, _P):
    """
    Pension du régime des salariés agricoles
    """
    taux_ann_base = _P.pension.rsa.taux_ann_base
    taux_ann_sup  = _P.pension.rsa.taux_ann_sup 
    duree_stage = _P.pension.rsa.stage_requis
    age_elig = _P.pension.rsa.age_legal
    periode_remp_base = _P.pension.rsa.periode_remp_base
    plaf_taux_pension = _P.pension.rsa.plaf_taux_pension
    smag = _P.param_gen.smag*25
    stage = nb_trim_val > 4*duree_stage 
    pension_min =_P.pension.rsa.pension_min  
    sal_ref = sal_ref_rsa

    montant = generic_pension(nb_trim_val, sal_ref, age, 
                    taux_ann_base,taux_ann_sup, duree_stage, age_elig,
                    periode_remp_base, plaf_taux_pension, smag)

    elig_age = age > age_elig
    elig = stage*elig_age*(sal_ref>0) 
    montant_percu = max_(montant, pension_min*smag)
    pension = elig*montant_percu    
    return pension