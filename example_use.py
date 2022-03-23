import json
import pandas as pd
import re
import time
from import_ecm_results import import_ecm_results
from import_ecm_results import import_ecm_results_v1

# because _all_ ecms in ecm_results_1-1.json have the fuel type keys _v1 of the
# import function could be used.  This is done here only as an example to show
# how much faster it is to have a consistent data structure than to have to
# test for a possible fuel type.

ecm_1 = import_ecm_results_v1("./Results_Files_3/ecm_results_1-1.json")
ecm_1 = import_ecm_results("./Results_Files_3/ecm_results_1-1.json")
ecm_2 = import_ecm_results("./Results_Files_3/ecm_results_2.json")
ecm_3 = import_ecm_results("./Results_Files_3/ecm_results_3-1.json")
ecm_4 = import_ecm_results("ecm_results_4.json")

print(ecm_1)
print(ecm_2)
print(ecm_3)
print(ecm_4)

################################################################################
#                                 End of File                                  #
################################################################################

