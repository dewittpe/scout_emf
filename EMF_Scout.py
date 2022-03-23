
import pandas as pd
import numpy as np
import json
from collections import Counter
 


# ================== 1) LOAD SCOUT RESULTS

def get_json(json_name):
    with open(json_name, 'r') as f:
        file = json.load(f)
    return file

def walk(json_dict, list_keys, key_list=[]):
    
    # Explore the data structure from the current location
    for key, item in json_dict.items():
        # If there are additional levels in the dict, call the function
        # again to advance another level deeper into the data structure
        if isinstance(item, list):
            nothing = 1
        elif isinstance(item, dict):
            walk(item, list_keys, key_list + [key])
        else:
            if key == '2022':    #<---- this is just to select firt set of keys, not the same set for all the years
                list_keys.append(key_list)
                
def retrieve_values(list_args, json_dict):
    i = 0
    item = json_dict[list_args[i]]
    while (isinstance(item, dict)) and (i<len(list_args)-1):
        i += 1
        item = item[list_args[i]] 
    return item

def extract_sum(keywords, list_keys, name):
    list_selection = []
    list_keywords = []
    for list_ in list_keys:
        if all(item in list_ for item in keywords):
            if ('ventilation' in keywords):
                if 'demand' not in list_:
                    list_keywords.append(list_)
                    vals = retrieve_values(list_, json_dict)
                    df = pd.DataFrame.from_dict(vals, orient='index')
                    list_selection.append(df)
            else:
                list_keywords.append(list_)
                vals = retrieve_values(list_, json_dict)
                df = pd.DataFrame.from_dict(vals, orient='index')
                list_selection.append(df)
    if len(list_selection)>0:
        df_sum = pd.concat(list_selection, axis=1).sum(axis=1).to_frame(name)
    else:
        years = ['2022','2023','2024','2025','2026','2027','2028','2029','2030',
                '2031','2032','2033','2034','2035','2036','2037','2038','2039',
                '2040','2041','2042','2043','2044','2045','2046','2047','2048',
                '2049','2050']
        df_sum = pd.DataFrame(index=years)
        df_sum[name] = 0
    return df_sum

def get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor):
    string_1 = 'Markets and Savings (by Category)'
    string_2 = "Max adoption potential"
    list_dfs = []
    no_fueld_eus = ['Computers and Electronics', 'Refrigeration', 'Lighting', 'Other']
    for fuel in fuels:
        for eu in enduses:
            if eu in no_fueld_eus:
                for bt in buildings:
                    list_dfs.append(extract_sum([string_1, string_2, emm, string_emissions_or_energy, bt, eu], list_keys, name))
            else:
                for bt in buildings:
                    list_dfs.append(extract_sum([string_1, string_2, emm, string_emissions_or_energy, bt, eu, fuel], list_keys, name))
    return (pd.concat(list_dfs, axis=1).sum(axis=1)*emission_factor).to_frame(name)

def loop_through_emms_emissions(emm_regions, list_final_dataframes):
    
    com = ['Commercial (Existing)', 'Commercial (New)']
    res = ['Residential (Existing)', 'Residential (New)']

    emissions = 'Avoided CO\u2082 Emissions (MMTons)'
    
    direct_fuels = ['Natural Gas', 'Distillate/Other', 'Biomass', 'Propane']
    indirect_fuels = ['Electric']
    appliances = ['Cooking', 'Water Heating', 'Refrigeration']
    appliances_gas = ['Cooking', 'Water Heating']
    cooling = ['Cooling (Equip.)']
    heating = ['Heating (Equip.)']
    lighting = ['Lighting']
    other = ['Computers and Electronics', "Other"]
    
    string_emissions_or_energy = 'Avoided CO\u2082 Emissions (MMTons)'
    emission_factor = 1
    emission_title_piece = 'Emissions|CO2|Energy|Demand|Buildings|'
    
    
    for emm in emm_regions:
        
        print(emm)
        # COMMERCIAL
        buildings = com
        
        name = emm + '*' + emission_title_piece + 'Commercial|Appliances|Direct'
        fuels = direct_fuels
        enduses = appliances_gas
        df_co2_commercial_appliances_direct = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_commercial_appliances_direct)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Appliances|Indirect'
        fuels = indirect_fuels
        enduses = appliances
        df_co2_commercial_appliances_indirect = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_commercial_appliances_indirect)
        # 
        name = emm + '*' + emission_title_piece + 'Commercial|Cooling|Direct'
        fuels = direct_fuels
        enduses = cooling
        df_co2_commercial_cooling_direct = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_commercial_cooling_direct)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Cooling|Indirect'
        fuels = indirect_fuels
        enduses = cooling
        df_co2_commercial_cooling_indirect = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_commercial_cooling_indirect)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Heating|Direct'
        fuels = direct_fuels
        enduses = heating
        df_co2_commercial_heating_direct = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_commercial_heating_direct)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Heating|Indirect'
        fuels = indirect_fuels
        enduses = heating
        df_co2_commercial_heating_indirect = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_commercial_heating_indirect)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Other|Direct'
        fuels = direct_fuels
        enduses = ['none']
        df_co2_commercial_other_direct = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_commercial_other_direct)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Other|Indirect'
        fuels = indirect_fuels
        enduses = other
        df_co2_commercial_other_indirect = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_commercial_other_indirect)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Lighting|Indirect'
        fuels = indirect_fuels
        enduses = lighting
        df_co2_commercial_lighting_indirect = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_commercial_lighting_indirect)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Lighting'
        fuels = indirect_fuels
        enduses = lighting
        df_co2_commercial_lighting = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_commercial_lighting)


        # RESIDENTIAL
        buildings = res
        
        name = emm + '*' + emission_title_piece + 'Residential|Appliances|Direct'
        fuels = direct_fuels
        enduses = appliances_gas
        df_co2_residential_appliances_direct = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_residential_appliances_direct)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Appliances|Indirect'
        fuels = indirect_fuels
        enduses = appliances
        df_co2_residential_appliances_indirect = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_residential_appliances_indirect)
        # 
        name = emm + '*' + emission_title_piece + 'Residential|Cooling|Direct'
        fuels = direct_fuels
        enduses = cooling
        df_co2_residential_cooling_direct = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_residential_cooling_direct)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Cooling|Indirect'
        fuels = indirect_fuels
        enduses = cooling
        df_co2_residential_cooling_indirect = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_residential_cooling_indirect)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Heating|Direct'
        fuels = direct_fuels
        enduses = heating
        df_co2_residential_heating_direct = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_residential_heating_direct)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Heating|Indirect'
        fuels = indirect_fuels
        enduses = heating
        df_co2_residential_heating_indirect = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_residential_heating_indirect)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Other|Direct'
        fuels = direct_fuels
        enduses = ['none']
        df_co2_residential_other_direct = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_residential_other_direct)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Other|Indirect'
        fuels = indirect_fuels
        enduses = other
        df_co2_residential_other_indirect = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_residential_other_indirect)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Lighting|Indirect'
        fuels = indirect_fuels
        enduses = lighting
        df_co2_residential_lighting_indirect = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_residential_lighting_indirect)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Lighting'
        fuels = indirect_fuels
        enduses = lighting
        df_co2_residential_lighting = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_co2_residential_lighting)
    
        #Combinations
        #Commercial
        # Emissions|CO2|Energy|Demand|Buildings|Commercial|Appliances
        df_co2_commercial_appliances = pd.concat([df_co2_commercial_appliances_direct, 
                                                df_co2_commercial_appliances_indirect], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Commercial|Appliances')
        list_final_dataframes.append(df_co2_commercial_appliances)

        # Emissions|CO2|Energy|Demand|Buildings|Commercial|Heating
        df_co2_commercial_heating = pd.concat([df_co2_commercial_heating_direct,
                                            df_co2_commercial_heating_indirect], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Commercial|Heating')
        list_final_dataframes.append(df_co2_commercial_heating)

        # Emissions|CO2|Energy|Demand|Buildings|Commercial|Cooling
        df_co2_commercial_cooling = pd.concat([df_co2_commercial_cooling_direct, 
                                            df_co2_commercial_cooling_indirect], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Commercial|Cooling')
        list_final_dataframes.append(df_co2_commercial_cooling)

        # Emissions|CO2|Energy|Demand|Buildings|Commercial|Direct
        df_co2_commercial_direct = pd.concat([df_co2_commercial_appliances_direct,
                                            df_co2_commercial_cooling_direct,
                                            df_co2_commercial_heating_direct,
                                            df_co2_commercial_other_direct], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Commercial|Direct')
        list_final_dataframes.append(df_co2_commercial_direct)

        # Emissions|CO2|Energy|Demand|Buildings|Commercial|Indirect
        df_co2_commercial_indirect = pd.concat([df_co2_commercial_appliances_indirect,
                                            df_co2_commercial_cooling_indirect,
                                            df_co2_commercial_heating_indirect,
                                            df_co2_commercial_other_indirect,
                                            df_co2_commercial_lighting_indirect], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Commercial|Indirect')
        list_final_dataframes.append(df_co2_commercial_indirect)

        # Emissions|CO2|Energy|Demand|Buildings|Commercial
        df_co2_commercial = pd.concat([df_co2_commercial_indirect, 
                                      df_co2_commercial_direct], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Commercial')
        list_final_dataframes.append(df_co2_commercial)


        # Emissions|CO2|Energy|Demand|Buildings|Commercial|Other
        df_co2_commercial_other = pd.concat([df_co2_commercial_other_indirect, 
                                            df_co2_commercial_other_direct], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Commercial|Other')
        list_final_dataframes.append(df_co2_commercial_other)
        

        # Emissions|CO2|Energy|Demand|Buildings|Residential|Appliances
        df_co2_residential_appliances = pd.concat([df_co2_residential_appliances_direct, 
                                                df_co2_residential_appliances_indirect], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Residential|Appliances')
        list_final_dataframes.append(df_co2_residential_appliances)

        # Emissions|CO2|Energy|Demand|Buildings|Residential|Heating
        df_co2_residential_heating = pd.concat([df_co2_residential_heating_direct,
                                            df_co2_residential_heating_indirect], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Residential|Heating')
        list_final_dataframes.append(df_co2_residential_heating)

        # Emissions|CO2|Energy|Demand|Buildings|Residential|Cooling
        df_co2_residential_cooling = pd.concat([df_co2_residential_cooling_direct, 
                                            df_co2_residential_cooling_indirect], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Residential|Cooling')
        list_final_dataframes.append(df_co2_residential_cooling)

        # Emissions|CO2|Energy|Demand|Buildings|Residential|Direct
        df_co2_residential_direct = pd.concat([df_co2_residential_appliances_direct,
                                            df_co2_residential_cooling_direct,
                                            df_co2_residential_heating_direct,
                                            df_co2_residential_other_direct], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Residential|Direct')
        list_final_dataframes.append(df_co2_residential_direct)

        # Emissions|CO2|Energy|Demand|Buildings|Residential|Indirect
        df_co2_residential_indirect = pd.concat([df_co2_residential_appliances_indirect,
                                            df_co2_residential_cooling_indirect,
                                            df_co2_residential_heating_indirect,
                                            df_co2_residential_other_indirect,
                                            df_co2_residential_lighting_indirect], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Residential|Indirect')
        list_final_dataframes.append(df_co2_residential_indirect)

        # Emissions|CO2|Energy|Demand|Buildings|Residential
        df_co2_residential = pd.concat([df_co2_residential_direct, 
                                       df_co2_residential_indirect], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Residential')
        list_final_dataframes.append(df_co2_residential)


        # Emissions|CO2|Energy|Demand|Buildings|Residential|Other
        df_co2_residential_other = pd.concat([df_co2_residential_other_indirect, 
                                            df_co2_residential_other_direct], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Residential|Other')
        list_final_dataframes.append(df_co2_residential_other)

        
        # Emissions|CO2|Energy|Demand|Buildings|Direct
        df_co2_direct = pd.concat([df_co2_residential_direct, 
                                df_co2_commercial_direct], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Direct')
        list_final_dataframes.append(df_co2_direct)

        # Emissions|CO2|Energy|Demand|Buildings|Indirect
        df_co2_indirect = pd.concat([df_co2_residential_indirect,
                                    df_co2_commercial_indirect], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Indirect')
        list_final_dataframes.append(df_co2_indirect)
        
        #All
        # Emissions|CO2|Energy|Demand|Buildings
        df_co2 = pd.concat([df_co2_residential, 
                            df_co2_commercial], axis=1).sum(axis=1).to_frame(emm + '*Emissions|CO2|Energy|Demand|Buildings')
        list_final_dataframes.append(df_co2)

    return list_final_dataframes

def loop_through_emms_energy(emm_regions, list_final_dataframes):
    
    com = ['Commercial (Existing)', 'Commercial (New)']
    res = ['Residential (Existing)', 'Residential (New)']
    
    gas = ['Natural Gas', 'Propane']
    oil = ['Distillate/Other']
    bio = ['Biomass']
    elect = ['Electric']
    appliances = ['Cooking', 'Water Heating', 'Refrigeration']
    appliances_gas = ['Cooking', 'Water Heating']
    cooling = ['Cooling (Equip.)']
    heating = ['Heating (Equip.)']
    lighting = ['Lighting']
    other = ['Computers and Electronics', "Other"]
    
    string_emissions_or_energy = 'Energy Savings (MMBtu)'
    emission_factor = 1.05505585262e-9
    emission_title_piece = 'Final Energy|Buildings|'
    
    for emm in emm_regions:
        print(emm)
        
        # COMMERCIAL
        buildings = com
        
        name = emm + '*' + emission_title_piece + 'Commercial|Appliances|Gas'
        fuels = gas
        enduses = appliances_gas
        df_energy_commercial_appliances_gas = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_commercial_appliances_gas)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Appliances|Electricity'
        fuels = elect
        enduses = appliances
        df_energy_commercial_appliances_electricity = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_commercial_appliances_electricity)
        # 
        name = emm + '*' + emission_title_piece + 'Commercial|Cooling|Gas'
        fuels = gas
        enduses = cooling
        df_energy_commercial_cooling_gas = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        #         list_final_dataframes.append(df_energy_commercial_cooling_gas)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Cooling|Electricity'
        fuels = elect
        enduses = cooling
        df_energy_commercial_cooling_electricity = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_commercial_cooling_electricity)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Heating|Gas'
        fuels = gas
        enduses = heating
        df_energy_commercial_heating_gas = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_commercial_heating_gas)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Heating|Electricity'
        fuels = elect
        enduses = heating
        df_energy_commercial_heating_electricity = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_commercial_heating_electricity)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Other|Gas'
        fuels = gas
        enduses = ['none']
        df_energy_commercial_other_gas = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_commercial_other_gas)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Other|Electricity'
        fuels = elect
        enduses = other
        df_energy_commercial_other_electricity = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_commercial_other_electricity)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Lighting|Electricity'
        fuels = elect
        enduses = lighting
        df_energy_commercial_lighting_electricity = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_commercial_lighting_electricity)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Lighting'
        fuels = elect
        enduses = lighting
        df_energy_commercial_lighting = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        #         list_final_dataframes.append(df_energy_commercial_lighting)
        
        # RESIDENTIAL
        buildings = res
        
        name = emm + '*' + emission_title_piece + 'Residential|Appliances|Gas'
        fuels = gas
        enduses = appliances_gas
        df_energy_residential_appliances_gas = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_residential_appliances_gas)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Appliances|Electricity'
        fuels = elect
        enduses = appliances
        df_energy_residential_appliances_electricity = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_residential_appliances_electricity)
        # 
        name = emm + '*' + emission_title_piece + 'Residential|Cooling|Gas'
        fuels = gas
        enduses = cooling
        df_energy_residential_cooling_gas = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        #         list_final_dataframes.append(df_energy_residential_cooling_gas)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Cooling|Electricity'
        fuels = elect
        enduses = cooling
        df_energy_residential_cooling_electricity = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_residential_cooling_electricity)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Heating|Gas'
        fuels = gas
        enduses = heating
        df_energy_residential_heating_gas = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_residential_heating_gas)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Heating|Electricity'
        fuels = elect
        enduses = heating
        df_energy_residential_heating_electricity = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_residential_heating_electricity)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Other|Gas'
        fuels = gas
        enduses = ['none']
        df_energy_residential_other_gas = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_residential_other_gas)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Other|Electricity'
        fuels = elect
        enduses = other
        df_energy_residential_other_electricity = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_residential_other_electricity)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Lighting|Electricity'
        fuels = elect
        enduses = lighting
        df_energy_residential_lighting_electricity = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_residential_lighting_electricity)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Lighting'
        fuels = elect
        enduses = lighting
        df_energy_residential_lighting = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        #         list_final_dataframes.append(df_energy_residential_lighting)
        
        
        # 
        # OIL and BIOMASS
        #RESIDENTIAL      
        #
        name = emm + '*' + emission_title_piece + 'Residential|Heating|Biomass solids'
        fuels = bio
        enduses = heating
        df_energy_residential_heating_biomass = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_residential_heating_biomass)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Biomass solids'
        fuels = bio
        enduses = heating
        df_energy_residential_bio = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_residential_bio)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Heating|Oil'
        fuels = oil
        enduses = heating
        df_energy_residential_heating_oil = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_residential_heating_oil)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Appliances|Oil'
        fuels = oil
        enduses = appliances_gas
        df_energy_residential_appliances_oil = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_residential_appliances_oil)
        #
        name = emm + '*' + emission_title_piece + 'Residential|Other|Oil'
        fuels = oil
        enduses = ['none']
        df_energy_residential_other_oil = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_residential_other_oil)
        #

        
        # COMMERCIAL
        buildings = com
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Heating|Biomass solids'
        fuels = bio
        enduses = heating
        df_energy_commercial_heating_biomass = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        #         list_final_dataframes.append(df_energy_commercial_heating_biomass)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Biomass solids'
        fuels = bio
        enduses = heating
        df_energy_commercial_bio = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        #         list_final_dataframes.append(df_energy_commercial_bio)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Heating|Oil'
        fuels = oil
        enduses = heating
        df_energy_commercial_heating_oil = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_commercial_heating_oil)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Appliances|Oil'
        fuels = oil
        enduses = appliances_gas
        df_energy_commercial_appliances_oil = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_commercial_appliances_oil)
        #
        name = emm + '*' + emission_title_piece + 'Commercial|Other|Oil'
        fuels = oil
        enduses = ['none']
        df_energy_commercial_other_oil = get_specific_series(fuels, enduses, buildings, list_keys, emm, name, string_emissions_or_energy, emission_factor)
        list_final_dataframes.append(df_energy_commercial_other_oil)
        #

  
  
        
        # ELECTRICITY
        # Final Energy|Buildings|Commercial|Electricity
        df_energy_commercial_electricity = pd.concat([df_energy_commercial_appliances_electricity,
                                                df_energy_commercial_cooling_electricity,
                                                df_energy_commercial_heating_electricity,
                                                df_energy_commercial_lighting_electricity,
                                                df_energy_commercial_other_electricity], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Commercial|Electricity')
        list_final_dataframes.append(df_energy_commercial_electricity)
        # Final Energy|Buildings|Residential|Electricity
        df_energy_residential_electricity = pd.concat([df_energy_residential_appliances_electricity,
                                                df_energy_residential_cooling_electricity,
                                                df_energy_residential_heating_electricity,
                                                df_energy_residential_lighting_electricity,
                                                df_energy_residential_other_electricity], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Residential|Electricity')
        list_final_dataframes.append(df_energy_residential_electricity)
        
         
        # GAS
        # Final Energy|Buildings|Commercial|Gas
        df_energy_commercial_gas = pd.concat([df_energy_commercial_appliances_gas,
                                              df_energy_commercial_cooling_gas,
                                                df_energy_commercial_heating_gas,
                                                df_energy_commercial_other_gas], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Commercial|Gas')
        list_final_dataframes.append(df_energy_commercial_gas)
        # Final Energy|Buildings|Residential|Gas
        df_energy_residential_gas = pd.concat([df_energy_residential_appliances_gas,
                                               df_energy_residential_cooling_gas,
                                                df_energy_residential_heating_gas,
                                                df_energy_residential_other_gas], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Residential|Gas')
        list_final_dataframes.append(df_energy_residential_gas)


    
        # OIL
        # Final Energy|Buildings|Commercial|Gas
        df_energy_commercial_oil = pd.concat([df_energy_commercial_appliances_oil,
                                                df_energy_commercial_heating_oil,
                                                df_energy_commercial_other_oil], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Commercial|Oil')
        list_final_dataframes.append(df_energy_commercial_oil)
        # Final Energy|Buildings|Residential|Gas
        df_energy_residential_oil = pd.concat([df_energy_residential_appliances_oil,
                                                df_energy_residential_heating_oil,
                                                df_energy_residential_other_oil], axis=1).sum(axis=1).to_frame(emm + '*' + emission_title_piece + 'Residential|Oil')
        list_final_dataframes.append(df_energy_residential_oil)


    



        # General
        # Final Energy|Buildings|Gas
        df_energy_gas = pd.concat([df_energy_residential_gas,
                                    df_energy_commercial_gas], axis=1).sum(axis=1).to_frame(emm + '*' + 'Final Energy|Buildings|Gas')
        list_final_dataframes.append(df_energy_gas)

        # Final Energy|Buildings|Electricity
        df_energy_electricity = pd.concat([df_energy_residential_electricity,
                                        df_energy_commercial_electricity], axis=1).sum(axis=1).to_frame(emm + '*' + 'Final Energy|Buildings|Electricity')
        list_final_dataframes.append(df_energy_electricity)
        
        # Final Energy|Buildings|Oil
        df_energy_oil = pd.concat([df_energy_residential_oil,
                                        df_energy_commercial_oil], axis=1).sum(axis=1).to_frame(emm + '*' + 'Final Energy|Buildings|Oil')
        list_final_dataframes.append(df_energy_oil)

        # Final Energy|Buildings
        df_energy = pd.concat([df_energy_gas,
                            df_energy_electricity,
                              df_energy_oil,
                              df_energy_residential_bio, df_energy_commercial_bio], axis=1).sum(axis=1).to_frame(emm + '*' + 'Final Energy|Buildings')
        list_final_dataframes.append(df_energy)
        

    return list_final_dataframes

def concat_and_filter_years(list_final_dataframes):
    final_df = pd.concat(list_final_dataframes, axis=1)
    final_df = final_df.transpose()
    final_df = final_df[['2025', '2030','2035', '2040', '2045', '2050']]
    return final_df



emm_regions = ['TRE', 'FRCC', 'MISW', 'MISC', 'MISE', 'MISS', 'ISNE', 'NYCW', 'NYUP', 'PJME', 
               'PJMW', 'PJMC', 'PJMD', 'SRCA', 'SRSE', 'SRCE', 'SPPS', 'SPPC', 'SPPN', 'SRSG', 
               'CANO', 'CASO', 'NWPP', 'RMRG', 'BASN']


# ecm_results_2
#global list_keys
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





# ================== 2) LOAD BASELINE
def walk_baseline(json_dict, list_keys_baseline, key_list=[]):
    
    # Explore the data structure from the current location
    for key, item in json_dict.items():
        # If there are additional levels in the dict, call the function
        # again to advance another level deeper into the data structure
        if isinstance(item, list):
            nothing = 1
        elif isinstance(item, dict):
            walk(item, list_keys_baseline, key_list + [key])
        else:
            if (key == '2013') | (key == '2014') | (key == '2015') | (key == '2016'):    #<---- this is just to select firt set of keys, not the same set for all the years
                list_keys_baseline.append(key_list)

def retrieve_values_baseline(list_args, json_dict_baseline):
    i = 0
    item = json_dict_baseline[list_args[i]]
    while (isinstance(item, dict)) and (i<len(list_args)-1):
        i += 1
        item = item[list_args[i]] 
    return item

def is_subset(l1, l2):
    c1, c2 = Counter(l1), Counter(l2)
    return not c1 - c2

def extract_sum(keywords, list_keys_baseline, name):
    building_types = ['assembly', 'education', 'food sales', 'food service',
                      'health care', 'lodging', 'large office', 'small office', 
                      'mercantile/service', 'warehouse', 'unspecified']
    list_selection = []
    list_keywords = []
    for list_ in list_keys_baseline:
        if is_subset(keywords, list_):
            if ('ventilation' in keywords):
                if 'demand' not in list_:
                    list_keywords.append(list_)
                    vals = retrieve_values_baseline(list_, json_dict_baseline)
                    df = pd.DataFrame.from_dict(vals, orient='index')
                    list_selection.append(df)
            elif keywords[1] == 'other':    #this means that other is a building type, not an enduse
                if not any(x in list_ for x in building_types):
                    list_keywords.append(list_)
                    vals = retrieve_values_baseline(list_, json_dict_baseline)
                    df = pd.DataFrame.from_dict(vals, orient='index')
                    list_selection.append(df)
            else:
                list_keywords.append(list_)
                vals = retrieve_values_baseline(list_, json_dict_baseline)
                df = pd.DataFrame.from_dict(vals, orient='index')
                list_selection.append(df)
    if len(list_selection)>0:
        df_sum = pd.concat(list_selection, axis=1).sum(axis=1).to_frame(name)
    else:
        years = ['2016','2017','2018','2019','2020','2021',
                 '2022','2023','2024','2025','2026','2027','2028','2029','2030',
                '2031','2032','2033','2034','2035','2036','2037','2038','2039',
                '2040','2041','2042','2043','2044','2045','2046','2047','2048',
                '2049','2050']
        years = ['2013','2014','2015','2016','2017','2018','2019','2020','2021',
         '2022','2023','2024','2025','2026','2027','2028','2029','2030',
        '2031','2032','2033','2034','2035','2036','2037','2038','2039',
        '2040','2041','2042','2043','2044','2045','2046','2047','2048',
        '2049','2050']
        df_sum = pd.DataFrame(index=years)
        df_sum[name] = 0
    return df_sum

def get_data_baseline(emm_regions, list_final_dataframes, com_bldg, res_bldg):
    unspecified = ['unspecified']
    
    for emm in emm_regions:
        print(emm)
        MMBtu_to_EJ = 1.05505585262e-9
        #==========================   GAS  ==========================   
        name = emm + '*' + 'Final Energy|Buildings|Commercial|Appliances|Gas'
        list_dfs = []
        for com in com_bldg:
            list_dfs.append(extract_sum([emm, com, 'natural gas', 'water heating', 'energy'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, com, 'natural gas', 'cooking', 'energy'], list_keys_baseline, name))
        df_energy_commercial_appliances_gas = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_commercial_appliances_gas)
        df_energy_commercial_appliances_gas
        
        name = emm + '*' + 'Final Energy|Buildings|Commercial|Heating|Gas'
        list_dfs = []
        for com in com_bldg:
            list_dfs.append(extract_sum([emm, com, 'natural gas', 'heating', 'energy', 'supply'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, com, 'natural gas', 'secondary heating', 'energy', 'supply'], list_keys_baseline, name))
        df_energy_commercial_heating_gas = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_commercial_heating_gas)
        #   
        name = emm + '*' + 'Final Energy|Buildings|Commercial|Other|Gas'
        list_dfs = []
        for com in com_bldg:
            list_dfs.append(extract_sum([emm, com, 'natural gas', 'other', 'energy'], list_keys_baseline, name))
        df_energy_commercial_other_gas = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_commercial_other_gas)
        #
        name = emm + '*' + 'Final Energy|Buildings|Commercial|Cooling|Gas'
        list_dfs = []
        for com in com_bldg:
            list_dfs.append(extract_sum([emm, com, 'natural gas', 'cooling', 'energy', 'supply'], list_keys_baseline, name))
        df_energy_commercial_cooling_gas = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_commercial_cooling_gas)
        # 
        name = emm + '*' + 'Final Energy|Buildings|Commercial|Gas'
        df_energy_commercial_gas = pd.concat([df_energy_commercial_appliances_gas, 
                                                 df_energy_commercial_heating_gas,
                                                 df_energy_commercial_other_gas, 
                                                   df_energy_commercial_cooling_gas ], axis=1).sum(axis=1).to_frame(name)
        list_final_dataframes.append(df_energy_commercial_gas)  
        #
        #
        #----------------RESIDENTIAL
        #
        #
        name = emm + '*' + 'Final Energy|Buildings|Residential|Heating|Gas'
        list_dfs = []
        for res in res_bldg:
            list_dfs.append(extract_sum([emm, res, 'natural gas', 'heating', 'energy', 'supply'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, res, 'natural gas', 'secondary heating', 'energy', 'supply'], list_keys_baseline, name))
        df_energy_residential_heating_gas = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_residential_heating_gas)
        # 
        #
        name = emm + '*' + 'Final Energy|Buildings|Residential|Heating|Gas_lpg'
        list_dfs = []
        for res in res_bldg:
            list_dfs.append(extract_sum([emm, res, 'other fuel', 'secondary heater (LPG)', 'energy'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, res, 'other fuel', 'furnace (LPG)', 'energy'], list_keys_baseline, name))
        df_energy_residential_heating_gas_lpg = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_residential_heating_gas_lpg)
        #   
        #           Seems right but not aligned with Tab 4
        name = emm + '*' + 'Final Energy|Buildings|Residential|Appliances|Gas'
        list_dfs = []
        for res in res_bldg:
            list_dfs.append(extract_sum([emm, res, 'natural gas', 'water heating', 'energy'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, res, 'natural gas', 'cooking', 'energy'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, res, 'natural gas', 'drying', 'energy'], list_keys_baseline, name))
        df_energy_residential_appliances_gas = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_residential_appliances_gas)
        
        name = emm + '*' + 'Final Energy|Buildings|Residential|Cooling|Gas'
        list_dfs = []
        for res in res_bldg:
            list_dfs.append(extract_sum([emm, res, 'natural gas', 'cooling', 'energy', 'supply'], list_keys_baseline, name))
        df_energy_residential_cooling_gas = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_residential_cooling_gas)
        # com
        name = emm + '*' + 'Final Energy|Buildings|Residential|Other|Gas'
        list_dfs = []
        for res in res_bldg:
            list_dfs.append(extract_sum([emm, res, 'natural gas', 'other', 'energy'], list_keys_baseline, name))
        df_energy_residential_other_gas = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_residential_other_gas)
         
        #
        name = emm + '*' + 'Final Energy|Buildings|Residential|Gas'
        df_energy_residential_gas = pd.concat([df_energy_residential_heating_gas, 
                                                 df_energy_residential_appliances_gas,
                                                 df_energy_residential_cooling_gas,
                                                 df_energy_residential_other_gas,
                                                df_energy_residential_heating_gas_lpg], axis=1).sum(axis=1).to_frame(name)
        list_final_dataframes.append(df_energy_residential_gas) 

        #         ==========================   ELECTRICITY  ==========================  
          
        name = emm + '*' + 'Final Energy|Buildings|Commercial|Appliances|Electricity'
        list_dfs = []
        for com in com_bldg:
            list_dfs.append(extract_sum([emm, com, 'electricity', 'water heating', 'energy'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, com, 'electricity', 'refrigeration', 'energy'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, com, 'electricity', 'cooking', 'energy'], list_keys_baseline, name))
        df_energy_commercial_appliances_electricity = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_commercial_appliances_electricity)
        #   
        name = emm + '*' + 'Final Energy|Buildings|Commercial|Cooling|Electricity'
        list_dfs = []
        for com in com_bldg:
            list_dfs.append(extract_sum([emm, com, 'electricity', 'cooling', 'energy', 'supply'], list_keys_baseline, name))
        df_energy_commercial_cooling_electricity = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_commercial_cooling_electricity)
        #   
        name = emm + '*' + 'Final Energy|Buildings|Commercial|Heating|Electricity'
        list_dfs = []
        for com in com_bldg:
            list_dfs.append(extract_sum([emm, com, 'electricity', 'heating', 'energy', 'supply'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, com, 'electricity', 'secondary heating', 'energy', 'supply'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, com, 'electricity', 'ventilation', 'energy'], list_keys_baseline, name))
        df_energy_commercial_heating_electricity = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_commercial_heating_electricity)
          
        name = emm + '*' + 'Final Energy|Buildings|Commercial|Lighting|Electricity'
        list_dfs = []
        for com in com_bldg:
            list_dfs.append(extract_sum([emm, com, 'electricity', 'lighting', 'energy'], list_keys_baseline, name))
        df_energy_commercial_lighting_electricity = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_commercial_lighting_electricity)    
        #   
        name = emm + '*' + 'Final Energy|Buildings|Commercial|Other|Electricity'
        list_dfs = []
        for com in com_bldg:
            list_dfs.append(extract_sum([emm, com, 'electricity', 'PCs', 'energy'], list_keys_baseline, name))    #0.31
            list_dfs.append(extract_sum([emm, com, 'electricity', 'non-PC office equipment', 'energy'], list_keys_baseline, name))   #0.52
            list_dfs.append(extract_sum([emm, com, 'electricity', 'MELs', 'energy'], list_keys_baseline, name))   #0.47
        df_energy_commercial_other_electricity = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_commercial_other_electricity)
        #   
        name = emm + '*' + 'Final Energy|Buildings|Commercial|Electricity'
        df_energy_commercial_electricity = pd.concat([df_energy_commercial_cooling_electricity, 
                                                      df_energy_commercial_appliances_electricity,
                                                      df_energy_commercial_heating_electricity,
                                                      df_energy_commercial_lighting_electricity,
                                                      df_energy_commercial_other_electricity], axis=1).sum(axis=1).to_frame(name)
        list_final_dataframes.append(df_energy_commercial_electricity)
        #
        #
        ##---------------Residential---------------------
        #
        #
        name = emm + '*' + 'Final Energy|Buildings|Residential|Cooling|Electricity'
        list_dfs = []
        for res in res_bldg:
            list_dfs.append(extract_sum([emm, res, 'electricity', 'cooling', 'energy', 'supply'], list_keys_baseline, name))
        df_energy_residential_cooling_electricity = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_residential_cooling_electricity)
          
        name = emm + '*' + 'Final Energy|Buildings|Residential|Appliances|Electricity'
        list_dfs = []
        for res in res_bldg:
            list_dfs.append(extract_sum([emm, res, 'electricity', 'ceiling fan', 'energy'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, res, 'electricity', 'water heating', 'energy'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, res, 'electricity', 'refrigeration', 'energy'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, res, 'electricity', 'cooking', 'energy'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, res, 'electricity', 'drying', 'energy'], list_keys_baseline, name))
        df_energy_residential_appliances_electricity = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_residential_appliances_electricity)
        #     
        name = emm + '*' + 'Final Energy|Buildings|Residential|Heating|Electricity'
        list_dfs = []
        for res in res_bldg:
            list_dfs.append(extract_sum([emm, res, 'electricity', 'heating', 'energy', 'supply'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, res, 'electricity', 'secondary heating', 'energy', 'supply'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, res, 'electricity', 'fans and pumps', 'energy'], list_keys_baseline, name))
        df_energy_residential_heating_electricity = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_residential_heating_electricity)
          
        name = emm + '*' + 'Final Energy|Buildings|Residential|Lighting|Electricity'
        list_dfs = []
        for res in res_bldg:
            list_dfs.append(extract_sum([emm, res, 'electricity', 'lighting', 'energy'], list_keys_baseline, name))
        df_energy_residential_lighting_electricity = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_residential_lighting_electricity)    
          
        name = emm + '*' + 'Final Energy|Buildings|Residential|Other|Electricity'
        list_dfs = []
        for res in res_bldg:
            list_dfs.append(extract_sum([emm, res, 'electricity', 'TVs', 'energy'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, res, 'electricity', 'computers', 'energy'], list_keys_baseline, name))
            list_dfs.append(extract_sum([emm, res, 'electricity', 'other', 'energy'], list_keys_baseline, name))
        df_energy_residential_other_electricity = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_residential_other_electricity)
        # 
        name = emm + '*' + 'Final Energy|Buildings|Residential|Electricity'
        df_energy_residential_electricity = pd.concat([df_energy_residential_cooling_electricity, 
                                                      df_energy_residential_appliances_electricity,
                                                      df_energy_residential_heating_electricity,
                                                      df_energy_residential_lighting_electricity,
                                                      df_energy_residential_other_electricity], axis=1).sum(axis=1).to_frame(name)
        list_final_dataframes.append(df_energy_residential_electricity)
        
        name = emm + '*' + 'Final Energy|Buildings|Commercial|Heating|Oil'
        list_dfs = []
        for com in com_bldg:
            keywords = [emm, com, 'distillate', 'heating', 'energy', 'supply']
            list_dfs.append(extract_sum(keywords, list_keys_baseline, name))
            keywords = [emm, com, 'distillate', 'secondary heating', 'energy', 'supply']
            list_dfs.append(extract_sum(keywords, list_keys_baseline, name))
        df_energy_commercial_heating_oil = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_commercial_heating_oil)
        #
        name = emm + '*' + 'Final Energy|Buildings|Residential|Heating|Oil'
        list_dfs = []
        for res in res_bldg:
            keywords = [emm, res, 'distillate', 'heating', 'energy', 'supply']
            list_dfs.append(extract_sum(keywords, list_keys_baseline, name))
            keywords = [emm, res, 'distillate', 'secondary heating', 'energy', 'supply']
            list_dfs.append(extract_sum(keywords, list_keys_baseline, name))
        df_energy_residential_heating_oil = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_residential_heating_oil )
        #
        name = emm + '*' + 'Final Energy|Buildings|Residential|Heating|Oil_kerosene'
        list_dfs = []
        for res in res_bldg:
            keywords = [emm, res, 'distillate', 'secondary heater (kerosene)', 'energy']
            list_dfs.append(extract_sum(keywords, list_keys_baseline, name))
        df_energy_residential_heating_oil_kerosene = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_residential_heating_oil_kerosene)
        
        #         
        name = emm + '*' + 'Final Energy|Buildings|Residential|Appliances|Oil'
        list_dfs = []
        for res in res_bldg:
            list_dfs.append(extract_sum([emm, res, 'distillate', 'water heating', 'energy'], list_keys_baseline, name))
        df_energy_residential_appliances_oil = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_residential_appliances_oil)
        
        name = emm + '*' + 'Final Energy|Buildings|Commercial|Appliances|Oil'
        list_dfs = []
        for com in com_bldg:
            list_dfs.append(extract_sum([emm, com, 'distillate', 'water heating', 'energy'], list_keys_baseline, name))
        df_energy_commercial_appliances_oil = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_commercial_appliances_oil)
        # 
        name = emm + '*' + 'Final Energy|Buildings|Residential|Other|Oil'
        list_dfs = []
        for res in res_bldg:
            list_dfs.append(extract_sum([emm, res, 'distillate', 'other', 'energy'], list_keys_baseline, name))
        df_energy_residential_other_oil = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_residential_other_oil)
        # 
        name = emm + '*' + 'Final Energy|Buildings|Commercial|Other|Oil'
        list_dfs = []
        for com in com_bldg:
            list_dfs.append(extract_sum([emm, com, 'distillate', 'other', 'energy'], list_keys_baseline, name))
        df_energy_commercial_other_oil = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_commercial_other_oil)
        
        #
        name = emm + '*' + 'Final Energy|Buildings|Commercial|Oil'
        df_energy_commercial_oil = pd.concat([df_energy_commercial_heating_oil,
                                  df_energy_commercial_other_oil,
                                  df_energy_commercial_appliances_oil], axis=1).sum(axis=1).to_frame(name)
        list_final_dataframes.append(df_energy_commercial_oil)
        #
        name = emm + '*' + 'Final Energy|Buildings|Residential|Oil'
        df_energy_residential_oil = pd.concat([df_energy_residential_heating_oil,
                                  df_energy_residential_other_oil,
                                  df_energy_residential_appliances_oil,
                                df_energy_residential_heating_oil_kerosene], axis=1).sum(axis=1).to_frame(name)
        list_final_dataframes.append(df_energy_residential_oil)        
        
        name = emm + '*' + 'Final Energy|Buildings|Residential|Heating|Biomass solids'
        list_dfs = []
        for res in res_bldg:
            keywords = [emm, res, 'other fuel', 'heating', 'energy', 'supply', 'stove (wood)']
            list_dfs.append(extract_sum(keywords, list_keys_baseline, name))
            keywords = [emm, res, 'other fuel', 'secondary heating', 'energy', 'supply', 'secondary heater (wood)']
            list_dfs.append(extract_sum(keywords, list_keys_baseline, name))
        df_energy_residential_heating_bio = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_residential_heating_bio)
        
        name = emm + '*' + 'Final Energy|Buildings|Residential|Biomass solids'
        list_dfs = []
        for res in res_bldg:
            keywords = [emm, res, 'other fuel', 'heating', 'energy', 'supply', 'stove (wood)']
            list_dfs.append(extract_sum(keywords, list_keys_baseline, name))
            keywords = [emm, res, 'other fuel', 'secondary heating', 'energy', 'supply', 'secondary heater (wood)']
            list_dfs.append(extract_sum(keywords, list_keys_baseline, name))
        df_energy_residential_bio = (pd.concat(list_dfs, axis=1).sum(axis=1)*MMBtu_to_EJ).to_frame(name)
        list_final_dataframes.append(df_energy_residential_bio)

        
        
        #       -----------General---------------
        #
        # Final Energy|Buildings|Electricity
        name = emm + '*' + 'Final Energy|Buildings|Electricity'
        df_energy_electricity = pd.concat([df_energy_residential_electricity,
                                           df_energy_commercial_electricity], axis=1).sum(axis=1).to_frame(name)
        list_final_dataframes.append(df_energy_electricity)
        #
        name = emm + '*' + 'Final Energy|Buildings|Gas'
        df_energy_gas = pd.concat([df_energy_residential_gas, 
                                   df_energy_commercial_gas], axis=1).sum(axis=1).to_frame(name)
        list_final_dataframes.append(df_energy_gas)
        #
        name = emm + '*' + 'Final Energy|Buildings|Oil'
        df_energy_oil = pd.concat([df_energy_residential_oil, df_energy_commercial_oil], axis=1).sum(axis=1).to_frame(name)
        list_final_dataframes.append(df_energy_oil)

        # Final Energy|Buildings
        name = emm + '*' + 'Final Energy|Buildings'
        df_energy = pd.concat([df_energy_electricity, 
                               df_energy_gas, 
                               df_energy_oil, 
                               df_energy_residential_heating_bio], axis=1).sum(axis=1).to_frame(name)
        list_final_dataframes.append(df_energy)
        
    return list_final_dataframes

def get_conversion_coeffs(emm_regions):
    path = './supporting_data/convert_data/emm_region_emissions_prices.json'
    convert_coeffs = get_json(path)
    list_coeffs = []
    for emm in emm_regions:
        list_coeffs.append(pd.DataFrame.from_dict(convert_coeffs['CO2 intensity of electricity']['data'][emm], orient='index', columns=[emm]))
    final_df_coeffs = pd.concat(list_coeffs, axis=1)
    final_df_coeffs = final_df_coeffs.transpose()
    final_df_coeffs = final_df_coeffs[['2025', '2030','2035', '2040', '2045', '2050']]    
    return final_df_coeffs
       
def convert_energy_to_co2(emm_regions, conv_coefficients):
    ej_to_quad = 0.9478
    
    ej_to_mt_co2_propane = ej_to_quad * 62.88
    ej_to_mt_co2_kerosene = ej_to_quad * 73.38
    ej_to_mt_co2_gas = ej_to_quad * 53.056
    ej_to_mt_co2_oil = ej_to_quad * 74.14
    ej_to_mt_co2_bio =ej_to_quad * 96.88
    pound_to_mt = 0.000453592
    ej_to_twh = 277.778
       
    
    for emm in emm_regions:
        dict_energy_emissions = {emm + "*Final Energy|Buildings":emm + "*Emissions|CO2|Energy|Demand|Buildings",
                                emm + "*Final Energy|Buildings|Commercial|Appliances|Gas":emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Appliances|Direct_gas",
                                emm + "*Final Energy|Buildings|Commercial|Appliances|Electricity":emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Appliances|Indirect",
                                emm + "*Final Energy|Buildings|Commercial|Appliances|Oil":emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Appliances|Direct_O_il", 
                                emm + "*Final Energy|Buildings|Commercial|Cooling|Electricity":emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Cooling|Indirect",
                                emm + "*Final Energy|Buildings|Commercial|Cooling|Gas":emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Cooling|Direct",
                                emm + "*Final Energy|Buildings|Commercial|Heating|Gas":emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Heating|Direct_gas",
                                emm + "*Final Energy|Buildings|Commercial|Heating|Electricity":emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Heating|Indirect",
                                emm + "*Final Energy|Buildings|Commercial|Heating|Oil":emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Heating|Direct_O_il",
                                emm + "*Final Energy|Buildings|Commercial|Heating|Biomass solids":emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Heating|Direct_bio",
                                emm + "*Final Energy|Buildings|Commercial|Lighting|Electricity":emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Lighting|Indirect",
                                emm + "*Final Energy|Buildings|Commercial|Other|Gas":emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Other|Direct_gas",
                                emm + "*Final Energy|Buildings|Commercial|Other|Electricity":emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Other|Indirect",
                                emm + "*Final Energy|Buildings|Commercial|Other|Oil":emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Other|Direct_O_il",
                                emm + "*Final Energy|Buildings|Commercial|Electricity":emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Indirect",
                                emm + "*Final Energy|Buildings|Commercial|Gas":emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Direct_gas",
                                emm + "*Final Energy|Buildings|Commercial|Oil":emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Direct_O_il",
                                emm + "*Final Energy|Buildings|Residential|Appliances|Gas":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Appliances|Direct_gas",
                                emm + "*Final Energy|Buildings|Residential|Appliances|Oil":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Appliances|Direct_O_il",
                                emm + "*Final Energy|Buildings|Residential|Appliances|Electricity":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Appliances|Indirect",
                                emm + "*Final Energy|Buildings|Residential|Cooling|Electricity":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Cooling|Indirect",
                                emm + "*Final Energy|Buildings|Residential|Cooling|Gas":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Cooling|Direct",
                                emm + "*Final Energy|Buildings|Residential|Heating|Gas":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Heating|Direct_gas",
                                emm + "*Final Energy|Buildings|Residential|Heating|Gas_lpg":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Heating|Direct_gas_lpg",
                                emm + "*Final Energy|Buildings|Residential|Heating|Electricity":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Heating|Indirect",
                                emm + "*Final Energy|Buildings|Residential|Heating|Oil":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Heating|Direct_O_il",
                                emm + "*Final Energy|Buildings|Residential|Heating|Oil_kerosene":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Heating|Direct_O_il_kerosene",
                                emm + "*Final Energy|Buildings|Residential|Heating|Biomass solids":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Heating|Direct_bio",
                                emm + "*Final Energy|Buildings|Residential|Lighting|Electricity":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Lighting|Indirect",
                                emm + "*Final Energy|Buildings|Residential|Other|Gas":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Other|Direct_gas",
                                emm + "*Final Energy|Buildings|Residential|Other|Oil":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Other|Direct_O_il",
                                emm + "*Final Energy|Buildings|Residential|Other|Electricity":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Other|Indirect",
                                emm + "*Final Energy|Buildings|Residential|Electricity":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Indirect",
                                emm + "*Final Energy|Buildings|Residential|Gas":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Direct_gas",
                                emm + "*Final Energy|Buildings|Residential|Biomass solids":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Direct_bio",
                                emm + "*Final Energy|Buildings|Residential|Oil":emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Direct_O_il",
                                emm + "*Final Energy|Buildings|Electricity":emm + "*Emissions|CO2|Energy|Demand|Buildings|Indirect",
                                emm + "*Final Energy|Buildings|Gas":emm + "*Emissions|CO2|Energy|Demand|Buildings|Direct_gas",
                                emm + "*Final Energy|Buildings|Oil":emm + "*Emissions|CO2|Energy|Demand|Buildings|Direct_O_il",}
        
        
        
        coeffs_emm = conv_coefficients[conv_coefficients.index == emm].values[0]
        for i in final_df.index:
            if (emm in i) and ('Electricity' in i):
                final_df.loc[dict_energy_emissions[i]] = (final_df[final_df.index==i].values[0]) * coeffs_emm * ej_to_twh
            if (emm in i) and ('Gas_lpg' in i):
                final_df.loc[dict_energy_emissions[i]] = (final_df[final_df.index==i].values[0]) * ej_to_mt_co2_propane
            elif (emm in i) and ('Gas' in i):
                final_df.loc[dict_energy_emissions[i]] = (final_df[final_df.index==i].values[0]) * ej_to_mt_co2_gas
            if (emm in i) and ('Oil_kerosene' in i):
                final_df.loc[dict_energy_emissions[i]] = (final_df[final_df.index==i].values[0]) * ej_to_mt_co2_kerosene
            elif (emm in i) and ('Oil' in i):
                final_df.loc[dict_energy_emissions[i]] = (final_df[final_df.index==i].values[0]) * ej_to_mt_co2_oil
            elif (emm in i) and ('Biomass' in i):
                final_df.loc[dict_energy_emissions[i]] = (final_df[final_df.index==i].values[0]) * ej_to_mt_co2_bio
                
        emissions_string = "*Emissions|CO2|Energy|Demand|Buildings|"
        #Now let's add the combinations for the emissions
        final_df.loc[emm + emissions_string + "Commercial|Appliances"] = (final_df[final_df.index==emm + emissions_string + "Commercial|Appliances|Direct_gas"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Commercial|Appliances|Indirect"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Commercial|Appliances|Direct_O_il"].values[0]) 
        final_df.loc[emm + emissions_string + "Commercial|Cooling"]  = (final_df[final_df.index==emm + emissions_string + "Commercial|Cooling|Direct"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Commercial|Cooling|Indirect"].values[0])
        final_df.loc[emm + emissions_string + "Commercial|Heating"] = (final_df[final_df.index==emm + emissions_string + "Commercial|Heating|Direct_gas"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Commercial|Heating|Indirect"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Commercial|Heating|Direct_O_il"].values[0])
        final_df.loc[emm + emissions_string + "Commercial|Lighting"] = (final_df[final_df.index==emm + emissions_string + "Commercial|Lighting|Indirect"].values[0])
        final_df.loc[emm + emissions_string + "Commercial|Other"] = (final_df[final_df.index==emm + emissions_string + "Commercial|Other|Direct_gas"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Commercial|Other|Indirect"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Commercial|Other|Direct_O_il"].values[0])
        final_df.loc[emm + emissions_string + "Residential|Appliances"]= (final_df[final_df.index==emm + emissions_string + "Residential|Appliances|Direct_gas"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Appliances|Indirect"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Appliances|Direct_O_il"].values[0]) 
        final_df.loc[emm + emissions_string + "Residential|Cooling"]  = (final_df[final_df.index==emm + emissions_string + "Residential|Cooling|Direct"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Cooling|Indirect"].values[0])
        final_df.loc[emm + emissions_string + "Residential|Heating"] = (final_df[final_df.index==emm + emissions_string + "Residential|Heating|Direct_gas"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Heating|Direct_gas_lpg"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Heating|Indirect"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Heating|Direct_O_il"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Heating|Direct_O_il_kerosene"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Heating|Direct_bio"].values[0])
        final_df.loc[emm + emissions_string + "Residential|Lighting"] = (final_df[final_df.index==emm + emissions_string + "Residential|Lighting|Indirect"].values[0])
        final_df.loc[emm + emissions_string + "Residential|Other"] = (final_df[final_df.index==emm + emissions_string + "Residential|Other|Direct_gas"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Other|Indirect"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Other|Direct_O_il"].values[0])
        #Combine different fuels
        final_df.loc[emm + emissions_string + "Commercial|Appliances|Direct"] = (final_df[final_df.index==emm + emissions_string + "Commercial|Appliances|Direct_gas"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Commercial|Appliances|Direct_O_il"].values[0]) 
        final_df.loc[emm + emissions_string + "Commercial|Heating|Direct"] = (final_df[final_df.index==emm + emissions_string + "Commercial|Heating|Direct_gas"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Commercial|Heating|Direct_O_il"].values[0])
        final_df.loc[emm + emissions_string + "Commercial|Other|Direct"] = (final_df[final_df.index==emm + emissions_string + "Commercial|Other|Direct_gas"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Commercial|Other|Direct_O_il"].values[0])
        final_df.loc[emm + emissions_string + "Commercial|Cooling|Direct"] = (final_df[final_df.index==emm + emissions_string + "Commercial|Cooling|Direct"].values[0])
        final_df.loc[emm + emissions_string + "Residential|Appliances|Direct"]= (final_df[final_df.index==emm + emissions_string + "Residential|Appliances|Direct_gas"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Appliances|Direct_O_il"].values[0]) 
        final_df.loc[emm + emissions_string + "Residential|Cooling|Direct"] = (final_df[final_df.index==emm + emissions_string + "Residential|Cooling|Direct"].values[0])
        final_df.loc[emm + emissions_string + "Residential|Heating|Direct"] = (final_df[final_df.index==emm + emissions_string + "Residential|Heating|Direct_gas"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Heating|Direct_gas_lpg"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Heating|Direct_O_il"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Heating|Direct_O_il_kerosene"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Heating|Direct_bio"].values[0])
        final_df.loc[emm + emissions_string + "Residential|Other|Direct"] = (final_df[final_df.index==emm + emissions_string + "Residential|Other|Direct_gas"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Other|Direct_O_il"].values[0])
        final_df.loc[emm + emissions_string + "Residential|Direct"] = (final_df[final_df.index==emm + emissions_string + "Residential|Appliances|Direct"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Heating|Direct"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Cooling|Direct"].values[0])+ (final_df[final_df.index==emm + emissions_string + "Residential|Other|Direct"].values[0])
        final_df.loc[emm + emissions_string + "Commercial|Direct"] = (final_df[final_df.index==emm + emissions_string + "Commercial|Appliances|Direct"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Commercial|Heating|Direct"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Commercial|Cooling|Direct"].values[0])+ (final_df[final_df.index==emm + emissions_string + "Commercial|Other|Direct"].values[0])
        final_df.loc[emm + emissions_string + "Residential"] = (final_df[final_df.index==emm + emissions_string + "Residential|Direct"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Indirect"].values[0]) 
        final_df.loc[emm + emissions_string + "Commercial"] = (final_df[final_df.index==emm + emissions_string + "Commercial|Direct"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Commercial|Indirect"].values[0]) 
        final_df.loc[emm + emissions_string + "Direct"] = (final_df[final_df.index==emm + emissions_string + "Commercial|Direct"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential|Direct"].values[0])       
        final_df.loc[emm + "*Emissions|CO2|Energy|Demand|Buildings"] = (final_df[final_df.index==emm + emissions_string + "Commercial"].values[0]) + (final_df[final_df.index==emm + emissions_string + "Residential"].values[0]) 
        
    for emm in emm_regions:
        final_df.drop(labels=[emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Appliances|Direct_gas",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Appliances|Direct_O_il",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Direct_gas",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Direct_O_il",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Heating|Direct_gas",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Heating|Direct_O_il",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Other|Direct_gas",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Commercial|Other|Direct_O_il",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Appliances|Direct_gas",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Appliances|Direct_O_il",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Direct_gas",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Direct_O_il",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Direct_bio",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Direct_gas",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Direct_O_il",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Heating|Direct_bio",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Heating|Direct_gas",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Heating|Direct_gas_lpg",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Heating|Direct_O_il",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Heating|Direct_O_il_kerosene",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Other|Direct_gas",
            emm + "*Emissions|CO2|Energy|Demand|Buildings|Residential|Other|Direct_O_il",
            emm + "*Final Energy|Buildings|Residential|Heating|Gas_lpg",
            emm + "*Final Energy|Buildings|Commercial|Cooling|Gas",
            emm + "*Final Energy|Buildings|Residential|Cooling|Gas",
            emm + "*Final Energy|Buildings|Residential|Heating|Oil_kerosene"
        ], axis=0, inplace=True)
    return final_df
                
        

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



# ================== 3) PLOT OUT EVERYTHING
import matplotlib.pyplot as plt
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
    


# ================== 4) AREAS AND PRICES
def get_prices_electricity(emm_regions, res_com):
    kwh_to_GJ = 1/0.0036
    path = 'emm_region_emissions_prices.json'
    convert_coeffs = get_json(path)
    list_coeffs = []
    for emm in emm_regions:
        if res_com  == 'residential':
            list_coeffs.append(pd.DataFrame.from_dict(convert_coeffs['End-use electricity price']['data'][res_com][emm], orient='index', columns=[emm + '*Price|Final Energy|Residential|Electricity']))
        else:
            list_coeffs.append(pd.DataFrame.from_dict(convert_coeffs['End-use electricity price']['data'][res_com][emm], orient='index', columns=[emm + '*Price|Final Energy|Commercial|Electricity']))
    final_df_coeffs = pd.concat(list_coeffs, axis=1)
    final_df_coeffs = final_df_coeffs.transpose()
    final_df_coeffs = final_df_coeffs[['2025', '2030','2035', '2040', '2045', '2050']]/1.023 * kwh_to_GJ
    return final_df_coeffs

def get_prices_gas_oil(emm_regions, res_com, fuel):
    MMBtu_to_GJ = 1/1.055056
    path = 'site_source_co2_conversions.json'
    convert_coeffs = get_json(path)
    list_coeffs = []
    for emm in emm_regions:
        if fuel == 'gas':
            if res_com  == 'residential':
                list_coeffs.append(pd.DataFrame.from_dict(convert_coeffs['natural gas']['price']['data'][res_com], orient='index', columns=[emm + '*Price|Final Energy|Residential|Gas']))
            else:
                list_coeffs.append(pd.DataFrame.from_dict(convert_coeffs['natural gas']['price']['data'][res_com], orient='index', columns=[emm + '*Price|Final Energy|Commercial|Gas']))
        else:
            if res_com  == 'residential':
                list_coeffs.append(pd.DataFrame.from_dict(convert_coeffs['distillate']['price']['data'][res_com], orient='index', columns=[emm + '*Price|Final Energy|Residential|Oil']))
            else:
                list_coeffs.append(pd.DataFrame.from_dict(convert_coeffs['distillate']['price']['data'][res_com], orient='index', columns=[emm + '*Price|Final Energy|Commercial|Oil']))
    final_df_coeffs = pd.concat(list_coeffs, axis=1)
    final_df_coeffs = final_df_coeffs.transpose()
    final_df_coeffs = final_df_coeffs[['2025', '2030','2035', '2040', '2045', '2050']]/1.023/1.04*MMBtu_to_GJ
    return final_df_coeffs

def get_areas(emm_regions):
    sqft_to_Mm2 = 0.092903/1000000
    com_bldg = ['assembly', 'education', 'food sales', 'food service', 
                'health care', 'lodging', 'large office', 'small office', 'mercantile/service', 'warehouse', 'other']
    res_bldg = ['single family home', 'multi family home', 'mobile home']
    path = 'mseg_res_com_emm_NEW.json'
    convert_coeffs = get_json(path)
    list_areas = []
    list_coeffs_com = []
    list_coeffs_res = []
    for emm in emm_regions:
        tmp_list = []
        for com in com_bldg:
            tmp_list.append(pd.DataFrame.from_dict(convert_coeffs[emm][com]['total square footage'], orient='index', columns=[emm + '*Energy Service|Floor Space|Commercial|Value'])*sqft_to_Mm2)
        com_df = pd.concat(tmp_list, axis=1).sum(axis=1).to_frame(emm + '*Energy Service|Floor Space|Commercial|Value').transpose()[['2025', '2030','2035', '2040', '2045', '2050']]
        list_areas.append(com_df)
        #
        #
        tmp_list = []
        for res in res_bldg:
            tmp_list.append(pd.DataFrame.from_dict(convert_coeffs[emm][res]['total square footage'], orient='index', columns=[emm + '*Energy Service|Floor Space|Residential|Value'])*sqft_to_Mm2)
        res_df = pd.concat(tmp_list, axis=1).sum(axis=1).to_frame(emm + '*Energy Service|Floor Space|Residential|Value').transpose()[['2025', '2030','2035', '2040', '2045', '2050']]
        list_areas.append(res_df)
        #
        #
        tot_area = pd.concat([com_df, res_df], axis=0).sum(axis=0).to_frame(emm+'*Energy Service|Floor Space|Buildings|Value').transpose()
        list_areas.append(tot_area)
    final_df = pd.concat(list_areas, axis=0)
    return final_df


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


