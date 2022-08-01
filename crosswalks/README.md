# Crosswalks

There are sevaral files in this directory used to define link tables.  These are
needed to translate from the energy conservation measures (ECM) files and the
energy modeling forum (EMF) definitions.

Column naming will have one of several prefixes:

* None
* `ecm_definition`
* `ecm_prep`
* `ecm_results`
* `emf_`

No prefix, as seen with `building_class` implies that the `building_class`
values are consistent between the ECM defintions, (as taken from the
documentation page for Scout), a `ecm_prep.json` (the result of the scout script
`ecm_prep.py`), a `ecm_results.json` (the restuls of the scout script
`ecm_results.py`), or EMF definitions.

## Goals
Build as many tables as needed.  Each table should have as few columns as needed
to define a linkage.

## Link tables

| Table                               | Columns                           |
| :-----                              | :-------                          |
| [Building Types](#building-types)   | `building_class`, `building_type` |
| [EMM to Avert](#emm-to-avert)       | `emm_region`, `avert_region` |
| [End Uses](#end-uses)               | `building_class`, `ecm_definition_fuel_type`, `ecm_definition_end_use`, `ecm_results_end_use`, `emf_end_use` |
| [Fuel Types](#fuel-types)           | `building_class`, `ecm_definition_fuel_type` |
| [Regions](#regions)                 | `region_set`, `region`            |
| [State to Census Reion](#state-to-census-region) | `state`, `census_region`|
| [Structure Types](#structure-types) | `building_class`, `structure_type`, `ecm_prep_building` |
| [Technologies](#technologies)       | `building_class`, `ecm_definition_supply_demand`, `ecm_definition_end_use`, `ecm_definition_fuel_type`, `ecm_definition_technology` |

### Building Types

* Definition file: `building_types.py`
* Output file: `building_types.csv`

Mapping of `building_class`, e.g., residential or commerical, to specific
`building_type`, e.g., "single family home", "food service", etc.

### EMM to Avert

* Definition file: `emm_to_avert.py`
* Output file: `emm_to_avert.csv`

Mapping from emm regions to AVERT regions


### End Uses

* Definition file: `end_uses.py`
* Output file: `end_uses.csv`

Mapping of the documented `end_uses` within the ECM definition.

### Fuel Types

* Definition file: `fuel_types.py`
* Output file: `fuel_types.csv`

A small table noting the valid fuel types within the ECM definiton for each
`building_class`.

### Regions

* Definition file: `regions.py`
* Output file: `regions.csv`

Define two coloumns, `region_set` and `region`, denoting the different regions
which could be in the ECM definitions and used in the EMF summaries.  The
following is an example of the structure.

### State to Census Region

* Definition file: `state_to_census_region.py`
* Output file: `state_to_census_region.csv`

A mapping for the 50 United States to Census Regions.

### Structure Types

* Definition file: `structure_types.py`
* Output file: `structure_types.csv`

ECM Prep, and ECM results, have fields which combine the concepts of building
class and structure type, e.g., "Residential (New)" and "Residential
(Existing)".  This link table is an easy way to split the combined column into
two columns.

