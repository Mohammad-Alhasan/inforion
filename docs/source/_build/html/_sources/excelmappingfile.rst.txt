=======================================
Generate Excel Mapping File
=======================================

**Description**

Excel mapping file generation part generates an excel mapping file for a particular API program.

It already populates the mapping file with all the available fields for that API program. This can be then sent to the customer to map these fields with their database fields.

Once the customer specifies all the mappings, this mapping file is used to push the data to M3.

inforion extract --help    

**Parameters**

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
   * - -p or --program
     - This parameter is used to provide the API program for which mapping file should be generated. e.g MMS301MI, CRS610MI, AAS320MI
   * - -o or --outputfile
     - This parameter is used to provide the output file path where the generated mapping file should be saved.

**Example**

inforion extract -p CRS610MI -o CRS610MI-Mappings.xlsx

**Note**
This command should always be executed in terminal as this needs user permissions.
