# (General) Imports
import pandas as pd
import numpy as np
import json
import time
import matplotlib.pyplot as plt
from collections import Counter

# Imports for loading scout results
from EMF_Scout_Functions import get_json
from EMF_Scout_Functions import walk
from EMF_Scout_Functions import loop_through_emms_emissions
from EMF_Scout_Functions import loop_through_emms_energy
from EMF_Scout_Functions import concat_and_filter_years

# ================== 1) LOAD SCOUT RESULTS
tic = time.time()
print("Start LOAD SCOUT RESULTS")

emm_regions = ['TRE', 'FRCC', 'MISW', 'MISC', 'MISE', 'MISS', 'ISNE', 'NYCW', 'NYUP', 'PJME',
               'PJMW', 'PJMC', 'PJMD', 'SRCA', 'SRSE', 'SRCE', 'SPPS', 'SPPC', 'SPPN', 'SRSG',
               'CANO', 'CASO', 'NWPP', 'RMRG', 'BASN']

# ecm_results_2
global list_keys
list_keys = []
path = 'Results_Files_3/ecm_results_2.json'
json_dict = get_json(path)
walk(json_dict,list_keys)
list_keys = [i for n, i in enumerate(list_keys) if i not in list_keys[:n]]
list_final_dataframes = []
list_final_dataframes = loop_through_emms_emissions(emm_regions, list_final_dataframes)
list_final_dataframes = loop_through_emms_energy(emm_regions, list_final_dataframes)
ecm_results_2 = concat_and_filter_years(list_final_dataframes)
ecm_results_2.to_csv('ecm_results_2.csv')

# ecm_results_3-1
#global list_keys
list_keys = []
path = 'Results_Files_3/ecm_results_3-1.json'
json_dict = get_json(path)
walk(json_dict,list_keys)
list_keys = [i for n, i in enumerate(list_keys) if i not in list_keys[:n]]
list_final_dataframes = []
list_final_dataframes = loop_through_emms_emissions(emm_regions, list_final_dataframes)
list_final_dataframes = loop_through_emms_energy(emm_regions, list_final_dataframes)
ecm_results_3_1 = concat_and_filter_years(list_final_dataframes)
ecm_results_3_1.to_csv('ecm_results_3-1.csv')

# ecm_results_1-1
#global list_keys
list_keys = []
path = 'Results_Files_3/ecm_results_1-1.json'
json_dict = get_json(path)
walk(json_dict,list_keys)
list_keys = [i for n, i in enumerate(list_keys) if i not in list_keys[:n]]
list_final_dataframes = []
list_final_dataframes = loop_through_emms_emissions(emm_regions, list_final_dataframes)
list_final_dataframes = loop_through_emms_energy(emm_regions, list_final_dataframes)
ecm_results_1_1 = concat_and_filter_years(list_final_dataframes)
ecm_results_1_1.to_csv('ecm_results_1-1.csv')

print("LOAD SCOUT RESULTS: Completed in " + str(time.time() - tic) + " seconds.")



# ================== 2) LOAD BASELINE
tic = time.time()
print("Start LOAD BASELINE")

com_bldg = ['assembly', 'education', 'food sales', 'food service',
            'health care', 'lodging', 'large office', 'small office', 'mercantile/service', 'warehouse', 'other', 'unspecified']
res_bldg = ['single family home', 'multi family home', 'mobile home']

global list_keys_baseline
list_keys_baseline = []
path = 'mseg_res_com_emm_NEW.json'
json_dict_baseline = get_json(path)
walk_baseline(json_dict_baseline,list_keys_baseline)
list_final_dataframes = []
list_keys_baseline = [i for n, i in enumerate(list_keys_baseline) if i not in list_keys_baseline[:n]]
list_final_dataframes = get_data_baseline(emm_regions,list_final_dataframes, com_bldg, res_bldg)
final_df = pd.concat(list_final_dataframes, axis=1)
final_df = final_df.transpose()
final_df = final_df[['2025', '2030','2035', '2040', '2045', '2050']]
conv_coefficients = get_conversion_coeffs(emm_regions)
final_df = convert_energy_to_co2(emm_regions, conv_coefficients)
final_df.to_csv('mseg_res_com_emm+emissions.csv')
final_df.loc['SUM'] = final_df.sum()/1.055

df = pd.read_csv('mseg_res_com_emm+emissions.csv')
df.index = df['Unnamed: 0']
df_filter = df[df['Unnamed: 1']=='Final Energy|Buildings|Commercial|Other|Gas']
df_filter = df_filter.drop(['Unnamed: 1', 'Unnamed: 0'], axis=1)
df_filter.loc['SUM'] = df_filter.sum()/1.055


# Combine Baseline and Scout Results
ecm_results_2_final = final_df.sort_index(ascending=True).subtract(ecm_results_2.sort_index(ascending=True))
ecm_results_3_1_final = final_df.sort_index(ascending=True).subtract(ecm_results_3_1.sort_index(ascending=True))
ecm_results_1_1_final = final_df.sort_index(ascending=True).subtract(ecm_results_1_1.sort_index(ascending=True))
#
ecm_results_2_final.to_csv('ecm_results_2_final.csv')
ecm_results_3_1_final.to_csv('ecm_results_3_1_final.csv')
ecm_results_1_1_final.to_csv('ecm_results_1_1_final.csv')

print("Completed LOAD BASELINE in " + str(time.time() - tic) + " seconds.")



# ================== 3) PLOT OUT EVERYTHING
tic = time.time()
print("Start PLOT OUT EVERYTHING")

emms = ['CASO', 'ISNE', 'SRSE']
for emm in emms:
    for i in range(0,len(ecm_results_1_1_final.sort_index(ascending=True).index)):
        if emm in ecm_results_1_1_final.sort_index(ascending=True).index[i]:
            df = pd.DataFrame(columns = ['2025', '2030', '2035', '2040', '2045', '2050'])
            df.loc['1-1'] = ecm_results_1_1_final.sort_index(ascending=True).iloc[i]
            df.loc['2'] = ecm_results_2_final.sort_index(ascending=True).iloc[i]
            df.loc['3-1'] = ecm_results_3_1_final.sort_index(ascending=True).iloc[i]
            df.loc['Baseline'] = final_df.sort_index(ascending=True).iloc[i]
            df = df.transpose()
    #         print(df)
            df.plot(kind='line', title = ecm_results_1_1_final.sort_index(ascending=True).index[i])
    #         plt.show()
            plt.savefig('test_aggregate/' + ecm_results_1_1_final.sort_index(ascending=True).index[i] + '.pdf')
            plt.clf()


print("Completed PLOT OUT EVERYTHING in " + str(time.time() - tic) + " seconds.")


# ================== 4) AREAS AND PRICES
tic = time.time()
print("Start AREAS AND PRICES")
res_com = 'residential'
price_elec_res = get_prices_electricity(emm_regions, res_com)
price_gas_res = get_prices_gas_oil(emm_regions, res_com, 'gas')
price_oil_res = get_prices_gas_oil(emm_regions, res_com, 'oil')
res_com = 'commercial'
price_elec_com = get_prices_electricity(emm_regions, res_com)
price_gas_com = get_prices_gas_oil(emm_regions, res_com, 'gas')
price_oil_com = get_prices_gas_oil(emm_regions, res_com, 'oil')
#
prices = pd.concat([price_elec_res, price_elec_com,price_gas_res, price_gas_com, price_oil_res, price_oil_com ], axis=0)

areas_df = get_areas(emm_regions)

prices_areas = pd.concat([prices, areas_df], axis=0)
prices_areas.to_csv('price_areas.csv')


print("Finished AREAS AND PRICES in " + str(time.time() - tic) + " seconds.")
