#!/bin/bash

sudo pip3 uninstall inforion

sudo pip3 install inforion

inforion catalog create --ionfile credentials/credentials.ionapi --name CSVSchema2 --schema_type DSV --schema data/catalog_schema.json --properties data/catalog_properties.json

inforion catalog delete --ionfile credentials/credentials.ionapi --name CSVSchema2

inforion catalog create --ionfile credentials/credentials.ionapi --name CSVSchema2 --schema_type DSV --schema data/catalog_schema.json --properties data/catalog_properties.json

inforion datalake upload --ionfile credentials/credentials.ionapi --schema CSVSchema2 --logical_id lid://infor.ims.mongooseims --file data/sample.csv

inforion datalake list --ionfile credentials/credentials.ionapi --list_filter "dl_document_name eq 'CSVSchema2'"

# inforion datalake purge --ionfile credentials/credentials.ionapi --ids 1-4584f0ec-fcf1-3841-87b6-520efb256591

inforion datalake get --ionfile credentials/credentials.ionapi -id 1-7e476691-b17c-3e8d-8f0c-ea13222f56ef
