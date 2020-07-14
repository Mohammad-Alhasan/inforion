=======================
Data Catalog CLI
=======================

Data Catalog (datacatalog) commands:

create
-------
Description:
~~~~~~~~~~~~~~
Add or update object metadata in the Data Catalog. Schema type of JSON and DSV requires that the name, type, and schema are provided, and you can optionally include the properties. For object type ANY requires the name and type only, and the schema and properties should be omitted.

Parameters:
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
   * - --ionfile or -i
     - Infor IONAPI credentials file.
   * - --name or -n
     - Object name.
   * - --schema_type or -t
     - Object schema type. Example DSV or ANY.
   * - --schema or -s
     - Schema file (JSON).
   * - --properties or -p
     - Additional schema properties file (JSON).

Example:
~~~~~~~~~~~~~~
$ inforion catalog create --ionfile credentials/credentials.ionapi --name CSVSchema2 --schema_type DSV --schema data/catalog_schema.json --properties data/catalog_properties.json


delete
-------
Description:
~~~~~~~~~~~~~~
Delete a schema object by name.

Parameters:
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
   * - --ionfile or -i
     - Infor IONAPI credentials file.
   * - --name or -n
     - Name of the schema object.

Example:
~~~~~~~~~~~~~~
$ inforion catalog delete --ionfile credentials/credentials.ionapi --name CSVSchema2


=======================
Data Lake CLI
=======================

Data Lake (datalake) commands:

list
-----
Description:
~~~~~~~~~~~~~~
List data object properties using a filter.

Parameters:
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
   * - --ionfile or -i
     - Infor IONAPI credentials file.
   * - --list_filter or -f
     - The restrictions to be applied on the returned records.
   * - --sort or -s
     - Field name followed by colon followed by direction (asc or desc; default asc). Example: 'event_date:desc'.
   * - --page or -p
     - The page number from which to start returning records. Starts from 1.
   * - --records or -r
     - The number of records that will be returned. Starts from 0

Example:
~~~~~~~~~~~~~~
$ inforion datalake list --ionfile credentials/credentials.ionapi --list_filter "dl_document_name eq 'CSVSchema2'"

get
---
Description:
~~~~~~~~~~~~~~
Retrieve payload based on id from datalake.

Parameters:
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
   * - --ionfile or -i
     - Infor IONAPI credentials file.
   * - --stream_id or -i
     - Object ID.

Example:
~~~~~~~~~~~~~~
$ inforion datalake get --ionfile credentials/credentials.ionapi -id 1-7e476691-b17c-3e8d-8f0c-ea13222f56ef


upload
-------
Description:
~~~~~~~~~~~~~~
This command use the ION Messaging Service to send documents into ION.

Parameters:
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
   * - --ionfile or -i
     - Infor IONAPI credentials file.
   * - --schema or -s
     -  Schema name.
   * - --logical_id or -l
     -  The Logical Id of the sending application (fromLogicalId parameter).
   * - ---file or -f
     -  File to upload.

Example:
~~~~~~~~~~~~~~
$ inforion datalake upload --ionfile credentials/credentials.ionapi --schema CSVSchema2 --logical_id lid://infor.ims.mongooseims --file data/sample.csv

purge
------
Description:
~~~~~~~~~~~~~~
Deletes Data Objects based on the given filter or a list of IDs. You cannot use both parameters together: ids and purge_filter.

Parameters:
~~~~~~~~~~~~~~
.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
   * - --ionfile or -i
     - Infor IONAPI credentials file.
   * - --ids or -id
     -  Object ids.
   * - --purge_filter or -f
     -  The restrictions to be applied to purge the records.

Example:
~~~~~~~~~~~~~~
$ inforion datalake purge --ionfile credentials/credentials.ionapi --ids 1-dd6aa276-b34d-3905-b378-cdb5452ca17f,1-02d3ed52-5602-36ac-b3b1-fa670dbfeb72

$ inforion datalake purge --ionfile credentials/credentials.ionapi -f "dl_id eq '1-d358de11-4658-3c2d-a6ec-88c028f46315'"