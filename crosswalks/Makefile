CSVS  = regions.csv
CSVS += building_types.csv
CSVS += structure_types.csv
CSVS += fuel_types.csv

all : $(CSVS)

%.csv : %.py
	python $<
