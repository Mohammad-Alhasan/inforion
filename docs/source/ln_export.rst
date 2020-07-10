=======================================
Export LN Data
=======================================

**Description**

This part helps user to export data from LN to Excel files using Infor ION API.

Currently it only supports following sevices:

- SalesOrder
- Business_Partner_v3

inforion ln ExportData --help    

**Parameters**

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
   * - -u, --url
     - The full URL to the API is needed. Please note you need to enter the full url like .../LN/c4ws/services/SalesOrder  [required]
   * - -i, --ionfile
     - IONFile is needed to login in to Infor OS. Please go into ION and generate a IONFile. If not provided, a prompt will allow you to type the input text. [required]
   * - -c, --company
     - Company for which you want to export data. e.g 121. [required]
   * - -s, --service_name
     - Service name for which you want to export data. See above for currently supported sevice names. [required]
   * - -o, --outputfile
     - File as Output File - Data will be exported to this file.


**Example**
inforion ln ExportData -s BusinessPartner_v3 -u https://Xi2016.gdeinfor2.com:7443/infor/LN/c4ws/services/ -i LN.ionapi -c 121 -o BusinessPartners.xlsx 
