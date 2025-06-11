#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# LCA: a lightweight life cycle assessment module that may be used with 
# biorefinery models in Bioindustrial-Park.
# Copyright (C) 2020-, Sarang Bhagwat <sarangb2@illinois.edu>
# 
# This module is under the UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flavored_food_simple_lca_only.utils import load_scenario,\
    food_lca, food_production_sys, load_eval_save, full_eval

f = food_production_sys.flowsheet
u, s = f.unit, f.stream

#%%
full_eval()
