CSVS := $(addsuffix .csv, $(basename $(shell find . -type f -name "*.py")))

all : $(CSVS)

%.csv : %.py
	python $<
