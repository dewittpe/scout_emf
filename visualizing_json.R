################################################################################
# This R script is useful for development of the EMF methods.  The
# tidyjson::json_structure method is extremely helpful for exploring the json
# files within scout.  None of this code is going to be part of the project,
# just useful for exploring the json files.

library(jsonlite)
library(tidyjson)
library(igraph)
library(data.table)

################################################################################
# Methods in the tidyjson package:
#
# * json_complexity : Compute the complexity (recursively unlisted length) of JSON data
# * json_get        : Get JSON from a tbl_json
# * json_get_column : Make the JSON data a persistent column
# * json_lengths    : Compute the length of JSON data
# * json_schema     : Create a schema for a JSON document or collection
# * json_structure  : Recursively structures arbitrary JSON data into a single data frame
# * json_types      : Add a column that tells the 'type' of the JSON data

# read in the json.  This will take a long time.
baseline <- tidyjson::read_json("./mseg_res_com_emm.json")

#baseline_complexity <- json_complexity(baseline)
#json_schema(baseline)


# get the structure of the json to build graphs
baseline_structure <- json_structure(baseline)

# select only the needed columns and omit the json strings to reduce the size of
# the object and make it possible to work with.
baseline_structure2 <- dplyr::select(baseline_structure, document.id:length)
baseline_structure2$..JSON <- NULL
data.table::setDT(baseline_structure2)
rm(baseline)
ls()




# get a subset of just the rows corresponding to the leafs, when the year is
# given.
baseline_structure3 <- subset(baseline_structure2, grepl("^\\d{4}", name))

# set as a data.table to make it easier to work with
data.table::setDT(baseline_structure3)

# get a count of of leaves by level, that is, how many levels down in the json
# does one need to go to get to the data.
baseline_structure3[, .N, by= level]

# exploring the result
baseline_structure3[level == 8 & name == '2035'][, do.call(c, seq), by = .(parent.id, level, child.id, name)]
baseline_structure3[name == '2035'][, paste(do.call(c, seq), collapse = "-"), by = .(parent.id, level, child.id, name)]
baseline_structure3[level >= 0 & name == '2035' & grepl("^1\\.1\\.", parent.id)]

baseline_structure3[, .N, keyby = .(level)]
baseline_structure3[level == 6 & name == 2035][1, seq]
baseline_structure3[level == 7 & name == 2035][1, seq]
baseline_structure3[level == 8 & name == 2035][1, seq]

d1 <- baseline_structure3[level == 1][, do.call(c, seq), by = .(parent.id, level, child.id, name)]
d2 <- baseline_structure3[level == 2][, do.call(c, seq), by = .(parent.id, level, child.id, name)]
d3 <- baseline_structure3[level == 3][, do.call(c, seq), by = .(parent.id, level, child.id, name)]
d4 <- baseline_structure3[level == 4][, do.call(c, seq), by = .(parent.id, level, child.id, name)]
d5 <- baseline_structure3[level == 5][, do.call(c, seq), by = .(parent.id, level, child.id, name)]
d6 <- baseline_structure3[level == 6][, do.call(c, seq), by = .(parent.id, level, child.id, name)]
d7 <- baseline_structure3[level == 7][, do.call(c, seq), by = .(parent.id, level, child.id, name)]
d8 <- baseline_structure3[level == 8][, do.call(c, seq), by = .(parent.id, level, child.id, name)]

# d1 
# d2
# d3
d4
# d5
d6
d7
d8

# REGIONS FOR V1
all(unique(d4$V1) == unique(d6$V1))
all(unique(d4$V1) == unique(d7$V1))
all(unique(d4$V1) == unique(d8$V1))

# BUILDING TYPE FOR V2
all(unique(d4$V2) == unique(d6$V2))
all(unique(d4$V2) == unique(d7$V2))
all(unique(d4$V2) == unique(d8$V2))

# branching starts here,
unique(d4$V3) # number of homes, squarefootage, ...
unique(d6$V3) # fuel types = "electricity" "natural gas" "distillate"  "other fuel"
unique(d7$V3) # fuel types = "electricity" "natural gas" "distillate"  "other fuel"
unique(d8$V3) # fuel types = "electricity" "natural gas" "distillate"  "other fuel"

# next
unique(d4$V4) # year

unique(d6$V4) # end uses? (fans and pumps....
# [1] "fans and pumps"          "ceiling fan"             "refrigeration"           "cooking"                 "drying"                  "onsite generation"       "water heating"          
# [8] "PCs"                     "non-PC office equipment"
unique(d7$V4) # more end uses? (lighting, ...
# [1] "lighting"      "water heating" "TVs"           "computers"     "other"         "ventilation"   "cooking"       "refrigeration" "MELs"         
unique(d8$V4) # more end uses? (heating, secondary heating, cooling)
# [1] "heating"           "secondary heating" "cooling"          

# V5
unique(d6$V5) # stock/energy
# [1] "stock"  "energy"
unique(d7$V5) # lots, and lots, of appliances/lightbulbs
#  [1] "linear fluorescent (T-12)"                "linear fluorescent (T-8)"                 "linear fluorescent (LED)"                 "general service (incandescent)"          
#  [5] "general service (CFL)"                    "general service (LED)"                    "reflector (incandescent)"                 "reflector (CFL)"                         
#  [9] "reflector (halogen)"                      "reflector (LED)"                          "external (incandescent)"                  "external (CFL)"                          
# [13] "external (high pressure sodium)"          "external (LED)"                           "electric WH"                              "solar WH"                                
# [17] "TV"                                       "set top box"                              "DVD"                                      "home theater and audio"                  
# [21] "video game consoles"                      "desktop PC"                               "laptop PC"                                "monitors"                                
# [25] "network equipment"                        "clothes washing"                          "dishwasher"                               "freezers"                                
# [29] "rechargeables"                            "coffee maker"                             "dehumidifier"                             "electric other"                          
# [33] "microwave"                                "pool heaters and pumps"                   "security system"                          "portable electric spas"                  
# [37] "wine coolers"                             "other appliances"                         "HP water heater"                          "Solar water heater"                      
# [41] "elec_water_heater"                        "CAV_Vent"                                 "VAV_Vent"                                 "electric_range_oven_24x24_griddle"       
# [45] "100W A19 Incandescent"                    "100W Equivalent A19 Halogen"              "100W Equivalent CFL Bare Spiral"          "Halogen Infrared Reflector (HIR) PAR38"  
# [49] "Halogen PAR38"                            "LED Integrated Luminaire"                 "LED PAR38"                                "Mercury Vapor"                           
# [53] "Metal Halide"                             "Sodium Vapor"                             "T5 4xF54 HO High Bay"                     "T5 F28"                                  
# [57] "T8 F28"                                   "T8 F32"                                   "T8 F59"                                   "T8 F96"                                  
# [61] "Commercial Beverage Merchandisers"        "Commercial Ice Machines"                  "Commercial Reach-In Freezers"             "Commercial Reach-In Refrigerators"       
# [65] "Commercial Refrigerated Vending Machines" "Commercial Supermarket Display Cases"     "Commercial Walk-In Freezers"              "Commercial Walk-In Refrigerators"        
# [69] "distribution transformers"                "security systems"                         "elevators"                                "escalators"                              
# [73] "non-road electric vehicles"               "coffee brewers"                           "kitchen ventilation"                      "laundry"                                 
# [77] "lab fridges and freezers"                 "fume hoods"                               "medical imaging"                          "large video boards"                      
# [81] "IT equipment"                             "office UPS"                               "data center UPS"                          "shredders"                               
# [85] "private branch exchanges"                 "voice-over-IP telecom"                    "gas_water_heater"                         "gas_range_oven_24x24_griddle"            
# [89] "oil_water_heater"                        
unique(d8$V5) # demand/supply
# [1] "demand" "supply"

# V6
unique(d6$V6) # year
#  [1] "2015" "2016" "2017" "2018" "2019" "2020" "2021" "2022" "2023" "2024" "2025" "2026" "2027" "2028" "2029" "2030" "2031" "2032" "2033" "2034" "2035" "2036" "2037" "2038" "2039" "2040"
# [27] "2041" "2042" "2043" "2044" "2045" "2046" "2047" "2048" "2049" "2050" "2013" "2014"
unique(d7$V6) # stock/energy
# [1] "stock"  "energy"
unique(d8$V6) # appliances?
#  [1] "windows conduction"          "windows solar"               "wall"                        "roof"                        "ground"                      "infiltration"               
#  [7] "people gain"                 "equipment gain"              "resistance heat"             "ASHP"                        "GSHP"                        "secondary heater"           
# [13] "central AC"                  "room AC"                     "furnace (NG)"                "boiler (NG)"                 "NGHP"                        "furnace (distillate)"       
# [19] "boiler (distillate)"         "furnace (LPG)"               "stove (wood)"                "resistance"                  "secondary heater (kerosene)" "secondary heater (wood)"    
# [25] "secondary heater (LPG)"      "secondary heater (coal)"     "floor"                       "ventilation"                 "lighting gain"               "other heat gain"            
# [31] "comm_GSHP-heat"              "elec_boiler"                 "electric_res-heat"           "rooftop_ASHP-heat"           "centrifugal_chiller"         "comm_GSHP-cool"             
# [37] "reciprocating_chiller"       "res_type_central_AC"         "rooftop_AC"                  "rooftop_ASHP-cool"           "screw_chiller"               "scroll_chiller"             
# [43] "wall-window_room_AC"         "gas_boiler"                  "gas_eng-driven_RTHP-heat"    "gas_furnace"                 "res_type_gasHP-heat"         "gas_chiller"                
# [49] "gas_eng-driven_RTAC"         "gas_eng-driven_RTHP-cool"    "res_type_gasHP-cool"         "oil_boiler"                  "oil_furnace"                

# V7
unique(d7$V7) # year
#  [1] "2015" "2016" "2017" "2018" "2019" "2020" "2021" "2022" "2023" "2024" "2025" "2026" "2027" "2028" "2029" "2030" "2031" "2032" "2033" "2034" "2035" "2036" "2037" "2038" "2039" "2040"
# [27] "2041" "2042" "2043" "2044" "2045" "2046" "2047" "2048" "2049" "2050"
unique(d8$V7) # energy/stock
# [1] "energy" "stock" 

# V8
unique(d8$V8) # year
#  [1] "2015" "2016" "2017" "2018" "2019" "2020" "2021" "2022" "2023" "2024" "2025" "2026" "2027" "2028" "2029" "2030" "2031" "2032" "2033" "2034" "2035" "2036" "2037" "2038" "2039" "2040"
# [27] "2041" "2042" "2043" "2044" "2045" "2046" "2047" "2048" "2049" "2050"









# build a graph
network <- baseline_structure3[level == 7 & name == '2035'][, paste(do.call(c, seq), collapse = "-+"), by = .(parent.id, level, child.id, name)][, V1]
network <- gsub(" ", "", network)
network <- gsub("/", "", network, fixed = TRUE)
network <- gsub("(", "", network, fixed = TRUE)
network <- gsub(")", "", network, fixed = TRUE)
network <- network[which(grepl("^TRE", network))]
length(network)

e <- parse(text = paste("graph_from_literal(", 
                        paste(network, collapse = ","),
                        ")\n"))
g <- eval(e)
plot(g, layout = layout_as_tree, simplify = TRUE)  # stack image
tkplot(g, layout = layout_as_tree, simplify = TRUE) # interactive

################################################################################
#                                 End of File                                  #
################################################################################

