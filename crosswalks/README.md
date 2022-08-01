# Crosswalks

There are sevaral files in this directory used to define link tables.  These are
needed to translate from the energy conservation measures (ECM) files and the
energy modeling forum (EMF) definitions.

## Goals
Build as many tables as needed.  Each table should have as few columns as needed
to define a linkage.

## Link tables

### Regions

* Definition file: regions.py
* Output files: regions.csv, regions.md

Define two coloumns, region_set and region, denoting the different regions which
could be in the ECM definitions and used in the EMF summaries.  The following is
an example of the structure.

| region_set   | region   |
|:-------------|:---------|
| AIA          | AIA_CZ1  |
| AIA          | AIA_CZ2  |
| ...          | ...      |
| EMM          | TRE      |
| EMM          | FRCC     |
| ...          | ...      |
| States       | AL       |
| States       | AZ       |
| ...          | ..       |
| ...          | ..       |




