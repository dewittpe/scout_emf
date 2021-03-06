JSONS  = Results_Files_3/ecm_results_1-1.json
JSONS += Results_Files_3/ecm_results_2.json
JSONS += Results_Files_3/ecm_results_3-1.json
JSONS += supporting_data/convert_data/emm_region_emissions_prices.json
JSONS += supporting_data/convert_data/site_source_co2_conversions.json
JSONS += supporting_data/stock_energy_tech_data/mseg_res_com_emm

.PHONY: all test coverage

all: EMF_Scout_output/EMF_Scout.py.log example_use.py.log

% : %.gz
	gzip -dkf $<
	@touch $@ # needed to prevent make from decompressing these files over and over again.

EMF_Scout_output/EMF_Scout.py.log : EMF_Scout.py $(JSONS)
	mkdir -p EMF_Scout_output/test_aggregate
	python $< > $@

example_use.py.log : example_use.py $(JSONS) scout_emf_methods.py
	python $< > $@

test : 
	tox

coverage :
	@echo "Previous Coverage"
	coverage report
	coverage run --include="scout/*" -m unittest discover
	@echo "Current Coverage"
	coverage report
	coverage html

