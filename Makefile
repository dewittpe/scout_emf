JSONS  = Results_Files_3/ecm_results_1-1.json
JSONS += Results_Files_3/ecm_results_2.json
JSONS += Results_Files_3/ecm_results_3-1.json
JSONS += supporting_data/convert_data/emm_region_emissions_prices.json


path = './supporting_data/convert_data/emm_region_emissions_prices.json'
path = 'site_source_co2_conversions.json'
path = 'mseg_res_com_emm_NEW.json'
path = 'mseg_res_com_emm_NEW.json'

.PHONY: all

all: EMF_Scout.py.log

%.json : %.json.gz
	gzip -dkf $<
	@touch $@ # needed to prevent make from decompressing these files over and over again.

EMF_Scout.py.log : EMF_Scout.py $(JSONS)
	mkdir -p test_aggregate
	python EMF_Scout.py > $@
