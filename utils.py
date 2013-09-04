# -*- coding:utf-8 -*-
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

"""
openFisca, Logiciel libre de simulation de système socio-fiscal
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
from src import __version__ as VERSION
import pickle
from datetime import datetime
from src.lib.utils import of_import
import numpy as np
from numpy import logical_not as not_
from src.lib.columns import EnumCol, IntCol, BoolCol, AgesCol, FloatCol, DateCol, Prestation, BoolPresta, IntPresta, EnumPresta

from src.countries.tunisia_pension import ENTITIES_INDEX

class Scenario(object):
    def __init__(self):
        super(Scenario, self).__init__()
        self.year = None
        self.indiv = {}
        # indiv est un dict de dict. La clé est le noi de l'individu
        # Exemple :
        # 0: {'quifoy': 'vous', 'noi': 0, 'quifam': 'parent 1', 'noipref': 0, 'noidec': 0, 
        #     'birth': datetime.date(1980, 1, 1), 'quimen': 'pref', 'noichef': 0}
        self.declar = {}
        
        # menage est un dict de dict la clé est la pref
        self.menage = {}

        # on ajoute un individu, déclarant et chef de famille
        self.addIndiv(0, datetime(1955,1,1).date(), 'vous', 'chef')
    
        self.nmen = None
        self.xaxis = None
        self.maxrev = None
        self.same_rev_couple = None
        self.year = None
    
    def copy(self):
        from copy import deepcopy
        return deepcopy(self)

    
    def check_consistency(self):
        '''
        Vérifie que le ménage entré est valide
        '''
        for noi, vals in self.indiv.iteritems():
            age = self.year - vals['birth'].year
            if age < 0:
                return u"L'année de naissance doit être antérieure à celle de la simulation (voir Fichier->Paramètres pour régler la date de la simulation"
            if vals['quifoy'] in ('vous', 'conj'):
                if age < 18: return u'Le déclarant et son éventuel conjoint doivent avoir plus de 18 ans'  # TODO
            else:
                if age > 25 and (vals['inv']==0): return u'Les personnes à charges doivent avoir moins de 25 ans si elles ne sont pas invalides'
#            if vals['quifoy'] == 'conj' and not vals['quifam'] == 'part':
#                return u"Un conjoint sur la déclaration d'impôt doit être le partenaire dans la famille"
        return ''
    
    def modify(self, noi, newQuifoy = None, newFoyer = None):
        oldFoyer, oldQuifoy = self.indiv[noi]['noidec'], self.indiv[noi]['quifoy']
        if newQuifoy == None: newQuifoy = oldQuifoy
        if newFoyer == None: newFoyer = oldFoyer
        if oldQuifoy == 'vous':
            toAssign = self.getIndiv(oldFoyer, 'noidec')
            del self.declar[oldFoyer]
            self._assignPerson(noi, quifoy = newQuifoy, foyer = newFoyer)
            for person in toAssign:
                oldPos = self.indiv[person]['quifoy']
                if oldPos == "vous": continue
                else: self.modify(person, newQuifoy = oldPos, newFoyer = 0)
        else:
            self._assignPerson(noi, quifoy = newQuifoy, foyer = newFoyer)
        self.genNbEnf()

    
    def hasConj(self, noidec):
        '''
        Renvoie True s'il y a un conjoint dans la déclaration 'noidec', sinon False
        '''
        for vals in self.indiv.itervalues():
            if (vals['noidec'] == noidec) and (vals['quifoy']=='conj'):
                return True
        return False
                
    def _assignVous(self, noi):
        ''' 
        Ajoute la personne numéro 'noi' et crée son foyer
        '''
        self.indiv[noi]['quifoy'] = 'vous'
        self.indiv[noi]['noidec'] = noi
        self.declar.update({noi:{}})

    def _assignConj(self, noi, noidec):
        ''' 
        Ajoute la personne numéro 'noi' à la déclaration numéro 'noidec' en tant 
        que 'conj' si declar n'a pas de conj. Sinon, cherche le premier foyer sans
        conjoint. Sinon, crée un nouveau foyer en tant que vous.
        '''
        decnum = noidec
        if (noidec not in self.declar) or self.hasConj(noidec):
            for k in self.declar:
                if not self.hasConj(k):
                    decnum = k
        if not self.hasConj(decnum):
            self.indiv[noi]['quifoy'] = 'conj'
            self.indiv[noi]['noidec'] = decnum
        else:
            self._assignVous(noi)

    def _assignPac(self, noi, noidec):
        ''' 
        Ajoute la personne numéro 'noi' à la déclaration numéro 'noidec' en tant 
        que 'pac'.
        '''
        self.indiv[noi]['quifoy'] = 'pac0'
        self.indiv[noi]['noidec'] = noidec

    
    def _assignPerson(self, noi, quifoy = None, foyer = None, quifam = None, famille = None):
        if quifoy is not None:
            if   quifoy     == 'vous': self._assignVous(noi)
            elif quifoy     == 'conj': self._assignConj(noi, foyer)
            elif quifoy[:3] == 'pac' : self._assignPac(noi, foyer)
        
        self.genNbEnf()

    def rmvIndiv(self, noi):
        oldFoyer, oldQuifoy = self.indiv[noi]['noidec'], self.indiv[noi]['quifoy']
        oldFamille, oldQuifam = self.indiv[noi]['noichef'], self.indiv[noi]['quifam']
        if oldQuifoy == 'vous':
            toAssign = self.getIndiv(oldFoyer, 'noidec')
            for person in toAssign:
                if self.indiv[person]['quifoy']     == 'conj': self._assignPerson(person, quifoy = 'conj', foyer = 0)
                if self.indiv[person]['quifoy'][:3] == 'pac' : self._assignPerson(person, quifoy = 'pac' , foyer = 0)
            del self.declar[noi]
        if oldQuifam == 'chef':
            toAssign = self.getIndiv(oldFamille, 'noichef')
            for person in toAssign:
                if self.indiv[person]['quifam']     == 'part': self._assignPerson(person, quifam = 'part', famille = 0)
                if self.indiv[person]['quifam'][:3] == 'enf' : self._assignPerson(person, quifam = 'enf' , famille = 0)
            del self.famille[noi]
        del self.indiv[noi]
        self.genNbEnf()

    def getIndiv(self, noi, champ = 'noidec'):
        for person, vals in self.indiv.iteritems():
            if vals[champ] == noi:
                yield person

    def addIndiv(self, noi, birth, quifoy, quifam):
        self.indiv.update({noi:{'birth':birth,
                                'quifoy': 'none',
                                'quifam': 'none',
                                'noidec':  0,
                                'noichef': 0,
                                'noipref': 0}})

        self._assignPerson(noi, quifoy = quifoy, foyer = 0, quifam = quifam, famille = 0)
        self.updateMen()

    def nbIndiv(self):
        return len(self.indiv)
            
    def genNbEnf(self):
        for noi, vals in self.indiv.iteritems():
            if vals.has_key('statmarit'):
                statmarit = vals['statmarit']
            else: statmarit = 2
            if self.hasConj(noi) and (noi == vals['noidec']) and not statmarit in (1,5):
                statmarit = 1
            elif not self.hasConj(noi) and (noi == vals['noidec']) and not statmarit in (2,3,4):
                statmarit = 2
            # si c'est un conjoint, même statmarit que 'vous'
            if vals['quifoy'] == 'conj':
                statmarit = self.indiv[vals['noidec']]['statmarit']
            vals.update({'statmarit':statmarit})
                
        for noidec, vals in self.declar.iteritems():
            vals.update(self.NbEnfFoy(noidec))

    def NbEnfFoy(self, noidec):
        out = {}
        n = 0
        for vals in self.indiv.itervalues():
            if (vals['noidec']==noidec) and (vals['quifoy'][:3]=='pac'):
                n += 1
                if (self.year - vals['birth'].year >= 18) and vals['inv'] == 0: out['nbJ'] += 1
                vals['quifoy'] = 'pac%d' % n
        return out
        pass

    def updateMen(self):
        '''
        Il faut virer cela
        '''
        people = self.indiv
        for noi in xrange(self.nbIndiv()):
            if   noi == 0: quimen = 'pref'
            elif noi == 1: quimen = 'cref'
            else:  quimen = 'enf%d' % (noi-1)
            people[noi].update({'quimen': quimen,
                                'noipref': 0})

    def __repr__(self):
        outstr = "INDIV" + '\n'
        for key, val in self.indiv.iteritems():
            outstr += str(key) + str(val) + '\n'
        outstr += "DECLAR" + '\n'
        for key, val in self.declar.iteritems():
            outstr += str(key) + str(val) + '\n'
        outstr += "MENAGE" + '\n'
        for key, val in self.menage.iteritems():
            outstr += str(key) + str(val) + '\n'
        return outstr

    def saveFile(self, fileName):
        outputFile = open(fileName, 'wb')
        pickle.dump({'version': VERSION, 'indiv': self.indiv, 'declar': self.declar, 'menage': self.menage}, outputFile)
        outputFile.close()
    
    def openFile(self, fileName):
        inputFile = open(fileName, 'rb')
        S = pickle.load(inputFile)
        inputFile.close()
        self.indiv = S['indiv']
        self.declar = S['declar']
        self.menage = S['menage']


    def populate_datatable(self, datatable):
        '''
        Popualte a datatable from a given scenario
        '''
        from pandas import DataFrame, concat
        import numpy as np
        scenario = self
        
        if self.nmen is None:
            raise Exception('france.scenario: self.nmen should be not None')
        
        nmen = self.nmen 
        same_rev_couple = self.same_rev_couple
        datatable.NMEN = nmen
        datatable._nrows = datatable.NMEN*len(scenario.indiv)
        datesim = datatable.datesim
        datatable.table = DataFrame()
    
        idmen = np.arange(60001, 60001 + nmen)
        
        for noi, dct in scenario.indiv.iteritems():
            birth = dct['birth']
            age = datesim.year- birth.year
            agem = 12*(datesim.year- birth.year) + datesim.month - birth.month
            noidec = dct['noidec']
            quifoy = datatable.description.get_col('quifoy').enum[dct['quifoy']]
            
            
            quimen = datatable.description.get_col('quimen').enum[dct['quimen']]
            dct = {'noi': noi*np.ones(nmen),
                   'age': age*np.ones(nmen),
                   'agem': agem*np.ones(nmen),
                   'quimen': quimen*np.ones(nmen),
                   'quifoy': quifoy*np.ones(nmen),
                   'idmen': idmen,
                   'idfoy': idmen*100 + noidec}
                
            datatable.table = concat([datatable.table, DataFrame(dct)], ignore_index = True)
    
        datatable.gen_index(ENTITIES_INDEX)
    
        for name in datatable.col_names:
            if not name in datatable.table:
                datatable.table[name] = datatable.description.get_col(name)._default
            
        entity = 'men'
        nb = datatable.index[entity]['nb']
        for noi, dct in scenario.indiv.iteritems():
            for var, val in dct.iteritems():
                if var in ('birth', 'noipref', 'noidec', 'noichef', 'quifoy', 'quimen', 'quifam'): 
                    continue
                if not datatable.index[entity] is None:
                    datatable.set_value(var, np.ones(nb)*val, entity, noi)
            del var, val
            
        entity = 'foy'
        nb = datatable.index[entity]['nb']
        for noi, dct in scenario.declar.iteritems():
            for var, val in dct.iteritems():
                if not datatable.index[entity][noi] is None:
                    datatable.set_value(var, np.ones(nb)*val, entity, noi)
    
        index = datatable.index['men']
        nb = index['nb']
        for noi, dct in scenario.menage.iteritems():
            for var, val in dct.iteritems():
                if not index[noi] is None:
                    datatable.set_value(var, np.ones(nb)*val, entity, noi)
            del var, val
    

        if nmen>1:
            if self.maxrev is None:
                raise Exception('tunisia_pension.utils.Scenario: self.maxrev should not be None')
            maxrev = self.maxrev      
            datatable.MAXREV = maxrev
            
            if self.xaxis is None:
                raise Exception('tunisia_pension.utils.Scenario: self.xaxis should not be None')
            
            xaxis = self.xaxis    
            axes = build_axes('tunisia_pension')
            var = None
            
            for axe in axes:
                if axe.name == xaxis:
                    datatable.XAXIS = axe.col_name
                    var = axe.col_name
                    
            if var is None:
                datatable.XAXIS = xaxis 
                var = xaxis
                        
            vls = np.linspace(0, maxrev, nmen)
            if same_rev_couple is True:
                entity = 'men'
                datatable.set_value(var, 0.5*vls, entity, opt = 0)
                datatable.set_value(var, 0.5*vls, entity, opt = 1)
            else:
                datatable.set_value(var, vls, entity, opt = 0)
                
            datatable._isPopulated = True
        


country = "tunisia_pension"
XAXIS_PROPERTIES =  of_import('','XAXIS_PROPERTIES', country)


class Xaxis(object):
    def __init__(self, col_name = None, country = None):
        super(Xaxis, self).__init__()
        
        self.col_name = col_name
        if self.col_name is not None:
            self.set(col_name)
            self.set_label(country)
        else:
            self.typ_tot = None
            self.typ_tot_default = None
                 
    def set_label(self, country):
        from src.lib.utils import of_import
        from src.lib.datatable import Description
        InputDescription = of_import('model.data', 'InputDescription', country)
        description = Description(InputDescription().columns)
        label2var, var2label, var2enum = description.builds_dicts()
        print self.col_name
        self.label = var2label[self.col_name]
        

    def set(self, col_name, name = None, typ_tot = None, typt_tot_default = None):
        """
        Set Xaxis attributes
        """
        self.name = XAXIS_PROPERTIES[col_name]['name']
        self.typ_tot = XAXIS_PROPERTIES[col_name]['typ_tot']
        self.typ_tot_default = XAXIS_PROPERTIES[col_name]['typ_tot_default'] 
        



def build_axes(country):
    # TODO: should be in __init__.py of tunisia
    from src.lib.utils import of_import
    Xaxis = of_import('utils','Xaxis', country)
    axes = []
    for col_name in XAXIS_PROPERTIES:
        axe = Xaxis(col_name, country)
        axes.append(axe)
    del axe
    return axes


REV_TYPE = {'superbrut' : ['salsuperbrut'],
             'brut': ['salbrut'],
             'imposable'      : ['sal']}        

