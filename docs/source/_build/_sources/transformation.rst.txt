===============
Transformation
===============


**Description**
This step provides the functionality of tranforming the external data source into Infor data based on the mapping file.

**Parameters**

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
   * - -a or --mappingfile
     - This parameter is used to provide the mapping file based on which transformation will be done.
   * - -b or --mainsheet
     - This parameter is used to define the main sheet which will contain the mapping fields for transformation.
   * - -i or --inputfile
     - This parameter is used to provide the input data.
   * - -o or --outputfile
     - This parameter is used to write the transformed data into a file.

**Example**

inforion transform -a sample_mapping.xlsx -b Sheet1 -i sample_data.xlsx -o output.xlsx


