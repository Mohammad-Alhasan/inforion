=======================================
Generate M3 Excel Mapping File
=======================================

Description
-----------

The **Excel mapping file generation** part generates an excel mapping file for a particular API program of M3.

It populates the mapping file with all the available fields for the specific M3 API program. This will be used by the Infor Consultant or the customer to map the M3 fields with the source database fields.

Once the mappings are specified, this mapping file is used to validate data from the source file (provided by the customer) and load it to M3.


inforion extract --help    

Parameters
----------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
   * - -p or --program
     - This parameter is used to provide the API program for which mapping file should be generated. e.g MMS301MI, CRS610MI, AAS320MI
   * - -o or --outputfile
     - This parameter is used to provide the output file path where the generated mapping file should be saved.

Example
-------

inforion extract -p CRS610MI -o CRS610MI-Mappings.xlsx

**Note:**
this command should always be executed in terminal as this needs user permissions, if you do not use the DM_ION Workflow manager.