#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Life cycle assessment of a given flavored food system.
# Copyright (C) 2025-, Sarang Bhagwat <sarangb2@illinois.edu>
# 
# This module is under the MIT open-source license. See 
# https://github.com/sarangbhagwat/flavored_food_lca/blob/main/LICENSE
# for license details.

import biosteam as bst
from flavored_food_simple_lca_only.chemicals_data import chems

HeatUtility = bst.HeatUtility
PowerUtility = bst.PowerUtility

#%% set utilities
_lps = bst.HeatUtility.get_heating_agent('low_pressure_steam')
_mps = bst.HeatUtility.get_heating_agent('medium_pressure_steam')
_hps = bst.HeatUtility.get_heating_agent('high_pressure_steam')

#-from Somesh-#
_lps.T = 121. + 273.15
_lps.P = 103710.2497

_mps.T = 52. + 273.15
_mps.P = 400837.7468
#--#

_cooling = bst.HeatUtility.get_cooling_agent('cooling_water')
_chilled = bst.HeatUtility.get_cooling_agent('chilled_water')
_chilled_brine = bst.HeatUtility.get_cooling_agent('chilled_brine')

#-from Somesh-#
_cooling.T = 28 + 273.15
_cooling.T_limit = _cooling.T + 9
#--#

#%% unused
# CH4 = chems.CH4
# CH4_MW, CH4_LHV = CH4.MW, CH4.LHV

# # as utility regeneration processes are not modeled in Singh group SuperPro model
# def get_ng_req(utilities, combustion_eff=0.8):
#     for u in utilities:
#         if isinstance(u, HeatUtility):
#             return CH4_MW * combustion_eff*u.duty/CH4_LHV
#         else:
#             raise TypeError('Argument "utilities" must be an iterable of HeatUtility objects.')
            
            
#%% set characterization factors
# GREET 2023 unless otherwise specified
CFs = {}
CFs['GWP_100'] = GWP_CFs = {
                # 'AmmoniumHydroxide': ,
                # 'CO2': ,
                'CSL': 1.6119,
                'MgCl2': 0., # ecoinvent 3.8, market for magnesium chloride, from titanium sponge production
                # 'N2': ,
                'NaOH': 2.0521,
                # 'O2': ,
                'SodiumAcetate': 1.2482,
                'FermMicrobe': 2.5612, # Yeast
                # 'Water': ,
                'ZincSulfate': 2.6309,
                'CH4': 0.3877, # NA NG from shale and conventional recovery
                
                'Electricity': 0.4181, # US Mix
                'Electricity_US_Mix': 0.4181, # US Mix
                'Electricity_PV_Battery': 0.046944 # Electricity from grid-connected PV plus battery system
                }

# GREET 2023 unless otherwise specified
CFs['FEC'] = FEC_CFs = {
                # 'AmmoniumHydroxide': ,
                # 'CO2': ,
                'CSL': 12.,
                'MgCl2': 0., # ecoinvent 3.8, market for magnesium chloride, from titanium sponge production
                # 'N2': ,
                'NaOH': 29.,
                # 'O2': ,
                'SodiumAcetate': 37.,
                'FermMicrobe': 39., # Yeast
                # 'Water': ,
                'ZincSulfate': 30.,
                'CH4': 51., # NA NG from shale and conventional recovery
                
                'Electricity': 5.441, # US Mix
                'Electricity_US_Mix': 5.441, # US Mix
                'Electricity_PV_Battery': 0.5465 # Electricity from grid-connected PV plus battery system
                }

