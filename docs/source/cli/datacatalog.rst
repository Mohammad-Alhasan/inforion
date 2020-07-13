=======================
Data Catalog
=======================

Data Catalog commands:

create
-------


Arguments:
~~~~~~~~~~~~~~
- ionfile

- name

- schema_type

- schema

- properties


Example:
~~~~~~~~~~~~~~
inforion catalog create --ionfile credentials/credentials.ionapi --name CSVSchema2 --schema_type DSV --schema data/catalog_schema.json --properties data/catalog_properties.json


delete
-------

Arguments:
~~~~~~~~~~~~~~
- ionfile

- name

Example:
~~~~~~~~~~~~~~
inforion catalog delete --ionfile credentials/credentials.ionapi --name CSVSchema2
