JSONS  = Results_Files_3/ecm_results_1-1.json
JSONS += Results_Files_3/ecm_results_2.json
JSONS += Results_Files_3/ecm_results_3-1.json

.PHONY: all

all: $(JSONS)

%.json : %.json.gz
	gzip -dkf $<

