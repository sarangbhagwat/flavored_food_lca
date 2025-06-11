#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Life cycle assessment of a given flavored food system.
# Copyright (C) 2025-, Sarang Bhagwat <sarangb2@illinois.edu>
# 
# This module is under the MIT open-source license. See 
# https://github.com/sarangbhagwat/flavored_food_lca/blob/main/LICENSE
# for license details.

import thermosteam as tmo
from thermosteam import functional as fn
from biorefineries import cane

cane_chems = cane.create_sugarcane_chemicals()

#%% conversion factors
_cal2joule = 4.184

#%% Create Chemical objects
chems = []

for i in cane_chems: chems.append(i)

def chemical_defined(ID, **kwargs):
    chem = tmo.Chemical.blank(ID, **kwargs)
    chems.append(chem)
    return chem

def chemical_database(ID, **kwargs):
    chem = tmo.Chemical(ID, **kwargs)
    chems.append(chem)
    return chem

Water = chemical_database('H2O')

Protein = chemical_defined('Protein', phase='l', 
                           formula='CH1.57O0.31N0.29S0.007', 
                           Hf=-17618*_cal2joule)

CSL = chemical_defined('CSL', phase='l', formula='CH2.8925O1.3275N0.0725S0.00175', 
                      Hf=Protein.Hf/4+Water.Hf/2+(-682502.448)/4)

FermMicrobe = chemical_defined('FermMicrobe', phase='l',
                      # formula='CH1.8O0.5N0.2', 
                      # formula='CH1.82O0.51N0.12',
                      formula='C8.34H7.36ON6.29',
                      Hf=-31169.39*_cal2joule)
AmmoniumHydroxide = chemical_database('AmmoniumHydroxide', phase='l', Hf=-336.719e3)
MgCl2 = chemical_database('MgCl2', phase='l')
NaOH = chemical_database('NaOH', phase='l')
SodiumAcetate = chemical_database('SodiumAcetate', phase='l')
ZincSulfate = chemical_database('ZincSulfate', phase='l')

CO2 = chemical_database('CO2')
CH4 = chemical_database('CH4')
N2 = chemical_database('N2')
O2 = chemical_database('O2')
SO2 = chemical_database('SO2')

HCl = chemical_database('HCl')
# Ash = chemical_database('Ash')

# =============================================================================
# Set assumptions/estimations for missing properties
# =============================================================================

# Set chemical heat capacity
# Cp of biomass (1.25 J/g/K) from Leow et al., Green Chemistry 2015, 17 (6), 3584–3599
for chemical in (CSL,):
    chemical.Cn.add_model(1.25*chemical.MW)

# Set chemical molar volume following assumptions in lipidcane biorefinery,
# assume densities for solulables and insolubles to be 1e5 and 1540 kg/m3, respectively
# !!! This has significant impacts on results, need to double-check accuracy
def set_rho(chemical, rho):       
    V = fn.rho_to_V(rho, chemical.MW)
    chemical.V.add_model(V, top_priority=True)

# for chemical in chems:
#     if chemical.ID in phase_change_chemicals: pass
#     elif chemical.ID in solubles: set_rho(chemical, 1e5)
#     elif chemical.ID in insolubles: set_rho(chemical, 1540)

# The Lakshmi Prasad model gives negative kappa values for some chemicals
for chemical in chems:
    if chemical.locked_state:
        try: chemical.kappa.move_up_model_priority('Lakshmi Prasad', -1)
        except: pass
 
# Default missing properties of chemicals to those of water,
for chemical in chems: chemical.default()

# set_rho(HMTHP, 1e5)
