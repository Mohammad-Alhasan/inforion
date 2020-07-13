=======================
Data Lake
=======================

Data Lake commands:

list
-----

Arguments:
~~~~~~~~~~~~~~
- ionfile

- list_filter

- sort

- page

- records

Example:
~~~~~~~~~~~~~~
*$inforion datalake list --ionfile credentials/credentials.ionapi --list_filter "dl_document_name eq 'CSVSchema2'"*


get
---

Arguments:
~~~~~~~~~~~~~~
- ionfile

- stream_id


Example:
~~~~~~~~~~~~~~
*$inforion datalake get --ionfile credentials/credentials.ionapi -id 1-7e476691-b17c-3e8d-8f0c-ea13222f56ef*


upload
-------

Arguments:
~~~~~~~~~~~~~~
- ionfile

- schema

- logical_id

- file

Example:
~~~~~~~~~~~~~~
*inforion datalake upload --ionfile credentials/credentials.ionapi --schema CSVSchema2 --logical_id lid://infor.ims.mongooseims --file data/sample.csv*


purge
------

Arguments:
~~~~~~~~~~~~~~
- ionfile

- ids

- purge_filter


Example:
~~~~~~~~~~~~~~
*$ inforion datalake purge --ionfile credentials/credentials.ionapi --ids 1-dd6aa276-b34d-3905-b378-cdb5452ca17f,1-02d3ed52-5602-36ac-b3b1-fa670dbfeb72*

*$ inforion datalake purge --ionfile credentials/credentials.ionapi -f "dl_id eq '1-d358de11-4658-3c2d-a6ec-88c028f46315'"*

