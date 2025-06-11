#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Life cycle assessment of a given flavored food system.
# Copyright (C) 2025-, Sarang Bhagwat <sarangb2@illinois.edu>
# 
# This module is under the MIT open-source license. See 
# https://github.com/sarangbhagwat/flavored_food_lca/blob/main/LICENSE
# for license details.

from flavored_food_simple_lca_only.utils import load_scenario,\
    food_lca, food_production_sys, load_eval_save, full_eval

f = food_production_sys.flowsheet
u, s = f.unit, f.stream

#%%
full_eval()
