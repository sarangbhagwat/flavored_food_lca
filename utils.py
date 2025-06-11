#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Bioindustrial-Park: BioSTEAM's Premier Biorefinery Models and Results
# Copyright (C) 2025-, Sarang Bhagwat <sarangb2@illinois.edu>
# 
# This module is under the UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.


import biosteam as bst
import thermosteam as tmo
from flavored_food_simple_lca_only.chemicals_data import chems
from flavored_food_simple_lca_only.process_settings import CFs
from flavored_food_simple_lca_only.lca import FoodLCA
import pandas as pd
import contourplots as cp

HeatUtility = hu = bst.HeatUtility
PowerUtility = pu = bst.PowerUtility
PowerUtility = bst.PowerUtility

_kg_per_short_ton = 907.185

#%% set thermo
tmo.settings.set_thermo(chems)

#%%
materials = {}
heat_utilities = {}
power_utility = {}
wastes = {}

M101 = bst.Mixer('M101', ins=('acetate', 'CSL', 'other_input_materials'), 
                outs='output_wastes',)
# hu = HeatUtility(heat_transfer_efficiency=1., unit=M101)
@M101.add_specification(run=False)
def M101_spec():
    pass

def M101_design():
    sn = M101.sn
    M101.heat_utilities = [i.copy() for i in heat_utilities[sn]]
    M101.power_utility = power_utility[sn].copy()
    
M101._design = M101_design

BT701 = bst.BoilerTurbogenerator('BT701', satisfy_system_electricity_demand=False)
# natural_gas = tmo.Stream('natural_gas', CH4 = 1.)
# BT701.ins[0] = natural_gas

CT801 = bst.CoolingTower('CT801')
CWP802 = bst.ChilledWaterPackage('CWP802')

#%%
food_production_sys = system = sys =\
    bst.System.from_units('food_production_sys', 
                           units=[M101,
                                  BT701,
                                  CT801,
                                  CWP802,])

#%% Base case 

materials['base case'] = materials_base_case = tmo.Stream('materials_base_case')
wastes['base case'] = wastes_base_case = tmo.Stream('wastes_base_case')

## flows in kg/h per ton MP/h
materials_base_case.imass['CSL'] = 2838.70 * 0.90
materials_base_case.imass['FermMicrobe'] = 102.49 * 0.75
materials_base_case.imass['MgCl2'] = 12.39
materials_base_case.imass['NaOH'] = 1086.22 * 0.02
materials_base_case.imass['SodiumAcetate'] = 2868.44
materials_base_case.imass['ZincSulfate'] = 0.27

wastes_base_case.imass['CO2'] = 1507.982666

### heat utility demands in kJ/h per ton MP/h
heat_utilities['base case'] = heat_utilities_base_case = []

# low-pressure steam
hu_lps = hu()
hu_lps(18096606.67, 70 + 273.15, 80 + 273.15)
heat_utilities_base_case.append(hu_lps)

# # medium-pressure steam
# hu_mps = hu()
# hu_mps(11404553.96, 130 + 273.15, 140 + 273.15)
# heat_utilities_base_case.append(hu_mps)

# cooling water
hu_cooling_water = hu()
hu_cooling_water(-13997170.21, 70 + 273.15, 60 + 273.15)
heat_utilities_base_case.append(hu_cooling_water)

# chilled water
hu_chilled_water = hu()
hu_chilled_water(-43134364.18, 30 + 273.15, 20 + 273.15)
heat_utilities_base_case.append(hu_chilled_water)
###

pu_power_consumption = pu()
pu_power_consumption(16041.12)
power_utility['base case'] = pu_power_consumption

#%% Improved case 

## flows in kg/h per ton MP/h
materials['improved case'] = materials_improved_case = tmo.Stream('materials_improved_case')
wastes['improved case'] = wastes_improved_case = tmo.Stream('wastes_improved_case')

materials_improved_case.imass['CSL'] = 1883.97 * 0.90
materials_improved_case.imass['FermMicrobe'] = 61.81 * 0.75
materials_improved_case.imass['MgCl2'] = 8.22
materials_improved_case.imass['NaOH'] = 767.93 * 0.02
materials_improved_case.imass['SodiumAcetate'] = 2956.82
materials_improved_case.imass['ZincSulfate'] = 0.18

wastes_improved_case.imass['CO2'] = 1554.444856

### heat utility demands in kJ/h per ton MP/h
heat_utilities['improved case'] = heat_utilities_improved_case = []

# low-pressure steam
hu_lps = hu()
hu_lps(11404553.96, 70 + 273.15, 80 + 273.15)
heat_utilities_improved_case.append(hu_lps)

# # medium-pressure steam
# hu_mps = hu()
# hu_mps(11404553.96, 130 + 273.15, 140 + 273.15)
# heat_utilities_improved_case.append(hu_mps)

# cooling water
hu_cooling_water = hu()
hu_cooling_water(-8395871.664, 70 + 273.15, 60 + 273.15)
heat_utilities_improved_case.append(hu_cooling_water)

# chilled water
hu_chilled_water = hu()
hu_chilled_water(-11404553.96, 30 + 273.15, 20 + 273.15)
heat_utilities_improved_case.append(hu_chilled_water)
###

pu_power_consumption = pu()
pu_power_consumption(9630.68)
power_utility['improved case'] = pu_power_consumption

#%% Solar power case 

## flows in kg/h per ton MP/h
materials['improved + solar power case'] = materials['improved case'].copy()
wastes['improved + solar power case'] = wastes['improved case'].copy()
heat_utilities['improved + solar power case'] = heat_utilities['improved case'].copy()
power_utility['improved + solar power case'] = power_utility['improved case'].copy()

#%% LCA

feedstock = M101.ins[0]
CSL_fresh = M101.ins[1]
MP = tmo.Stream('MP')
MP.imass['FermMicrobe'] = _kg_per_short_ton

food_lca = FoodLCA(system=food_production_sys, 
                 CFs=CFs, 
                 feedstock=feedstock,
                 feedstock_ID='SodiumAcetate',
                 main_product=MP, 
                 main_product_chemical_IDs=['FermMicrobe',], 
                 by_products=[], 
                 cooling_tower=CT801, 
                 chilled_water_processing_units=[CWP802], 
                 boiler=BT701, 
                 has_turbogenerator=False,
                 add_EOL_GWP=False,
                 input_biogenic_carbon_streams=[CSL_fresh],
                 )

#%% function for loading scenarios
def load_scenario(scenario_name):
    sn = scenario_name
    input_materials = M101.ins[2]
    input_materials.copy_like(materials[sn])
    
    M101.sn = sn
    
    M101.ins[0].imass['SodiumAcetate'] = materials[sn].imass['SodiumAcetate']
    input_materials.imass['SodiumAcetate'] = 0.
    
    M101.ins[1].imass['CSL'] = materials[sn].imass['CSL']
    input_materials.imass['CSL'] = 0.
    
    M101.outs[0].copy_like(wastes[sn])
    
    # M101.simulate()
    # BT701.simulate()
    food_production_sys.simulate()
    
    # Set Electricity CFs according to scenario
    if sn in ['base case', 'improved case']:
        CFs['GWP_100']['Electricity'] = CFs['GWP_100']['Electricity_US_Mix']
        CFs['FEC']['Electricity'] = CFs['FEC']['Electricity_US_Mix']
    elif sn in ['improved + solar power case']:
        CFs['GWP_100']['Electricity'] = CFs['GWP_100']['Electricity_PV_Battery']
        CFs['FEC']['Electricity'] = CFs['FEC']['Electricity_PV_Battery']
    else:
        raise ValueError(f'"{sn}" is not an implemented scenario.\n')
        
#%%
def replace_keys(dict_object):
    d = dict_object
    key_map = {'H2SO4': 'sulfuric acid',
     'NaOH': 'sodium hydroxide',
     'CalciumDihydroxide': 'calcium hydroxide',
     'CH4': 'natural gas',
     'CO2': 'carbon dioxide',
     'CSL': 'corn steep liquor',
     'FermMicrobe': 'yeast inoculum',
     'ZincSulfate': 'zinc sulfate'}
    
    for k in list(d.keys()):
        v = d[k]
        k_new = key_map[k]
        d[k_new] = v
        del[d[k]]
    
    return dict_object

#%% function to plot stacked bars for indicator values for both cases

def plot_stacked_bars(base_case_breakdown, 
                      improved_case_breakdown,
                      improved_plus_solar_power_case_breakdown,
                      filename,
                      colors,
                      y_label = r"$\bfCarbon$" + " " + r"$\bfIntensity$",
                      y_units = '%',
                      y_ticks = [0, 5, 10, 15, 20],
                      remove_zero_val_items=True,
                      add_percent_symbols_to_y_ticks=False,
                      ):
    base_case_breakdown = {k:v[0] for k,v in base_case_breakdown.items()
                           if not v[0]==0 or not remove_zero_val_items}
    improved_case_breakdown = {k:v[0] for k,v in improved_case_breakdown.items()
                           if not v[0]==0 or not remove_zero_val_items}
    improved_plus_solar_power_case_breakdown = {k:v[0] for k,v in improved_plus_solar_power_case_breakdown.items()
                           if not v[0]==0 or not remove_zero_val_items}
    
    combined_breakdown = {'base case': base_case_breakdown,
                          'improved case': improved_case_breakdown,
                          'improved + solar power case': improved_plus_solar_power_case_breakdown}
    
    df_combined_breakdown = pd.DataFrame.from_dict(combined_breakdown)
    cp.stacked_bar_plot(dataframe=df_combined_breakdown, 
                     y_ticks = y_ticks,
                     y_label = y_label, 
                     y_units = y_units, 
                     colors=colors,
                     hatch_patterns=('\\', '//', '|', 'x',),
                     filename=filename,
                     n_minor_ticks=4,
                     fig_height=5.5*1.1777*0.94*1.0975,
                     fig_width=7,
                     add_percent_symbols_to_y_ticks=add_percent_symbols_to_y_ticks,
                     # show_totals=True,
                     # totals=totals,
                     # sig_figs_for_totals=3,
                     # totals_label_text=r"$\bfsum:$",
                     # units_list=[i.units for i in unit_groups[0].metrics],
                     )

#%% function for loading and evaluating a single scenario and saving raw results
def load_eval_save(scenario_name):
    load_scenario(scenario_name)
    
    # GWP_100
    dict_GWP_breakdown = food_lca.material_GWP_breakdown
    replace_keys(dict_GWP_breakdown)
    dict_GWP_breakdown['sodium acetate'] = food_lca.feedstock_GWP
    dict_GWP_breakdown['electricity'] = food_lca.net_electricity_GWP
    dict_GWP_breakdown['direct non-biogenic emissions'] = food_lca.direct_non_biogenic_emissions_GWP

    dict_GWP_breakdown = {k:[v] for k,v in dict_GWP_breakdown.items()}
    df = pd.DataFrame.from_dict(dict_GWP_breakdown)
    df.to_excel(f'{scenario_name}_GWP.xlsx'.replace(' ', '_'))
    
    # FEC
    dict_FEC_breakdown = food_lca.material_FEC_breakdown
    replace_keys(dict_FEC_breakdown)
    dict_FEC_breakdown['sodium acetate'] = food_lca.feedstock_FEC
    dict_FEC_breakdown['electricity'] = food_lca.net_electricity_FEC
    
    dict_FEC_breakdown = {k:[v] for k,v in dict_FEC_breakdown.items()}
    df = pd.DataFrame.from_dict(dict_FEC_breakdown)
    df.to_excel(f'{scenario_name}_FEC.xlsx'.replace(' ', '_'))
    
    return [dict_GWP_breakdown, dict_FEC_breakdown]

#%% function for full eval and saving figures

def full_eval(scenario_names=['base case', 'improved case', 'improved + solar power case']):
    results = {i:{} for i in scenario_names}
    for i in scenario_names:
        results[i]['GWP_100'], results[i]['FEC'] = load_eval_save(i)
    
    # GWP_100
    plot_stacked_bars(results[scenario_names[0]]['GWP_100'], 
                      results[scenario_names[1]]['GWP_100'],
                      results[scenario_names[2]]['GWP_100'], 
                      filename='GWP_full_results.png',
                      y_label = r"$\mathrm{\bfCarbon}$" + " " + r"$\mathrm{\bfIntensity}$",
                      y_units = r"$\mathrm{kg}$"+" "+ r"$\mathrm{CO}_{2}\mathrm{-eq.}\cdot\mathrm{kg}^{-1}$",
                      y_ticks = [0, 5, 10, 15, 20],
                      colors=['#607429', '#8FAE3E',  '#E1F8C0',],)
    
    # FEC
    plot_stacked_bars(results[scenario_names[0]]['FEC'], 
                      results[scenario_names[1]]['FEC'], 
                      results[scenario_names[2]]['FEC'], 
                      filename='FEC_full_results.png',
                      y_label = r"$\mathrm{\bfFossil}$" + " " + r"$\mathrm{\bfEnergy}$"+ " " + r"$\mathrm{\bfConsumption}$",
                      y_units = r"$\mathrm{MJ}\cdot\mathrm{kg}^{-1}$",
                      y_ticks = [0, 100, 200, 300],
                      colors=['#A100A1', '#FF80FF', '#FEC1FE',],)
