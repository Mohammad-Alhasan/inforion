===============
Data Lake
===============


**Description**
Explain how to upload a CSV file to the data lake and query in inforion.

In this explanation, we will refer to:
======================================
* Create object and upload data
* Data query
* Delete data 
* Delete object

**How to create a new project and Upload data in datalake:**

Open your account, click on the App Menu,
then on ION Desk, click on Status overview, then Data Catalog,
then >>"Object Schemas" then see all projects.
Click the Create button >> "Add New Object".

Example:

.. image:: image/inforion_datalake1.png
  :width: 400


Here it shows you a set of options that you need:

Upload data you want to work with CSV, click on next.

.. image:: image/inforion_datalake2.png
  :width: 400

Then fill in options "Object Information"

.. image:: image/inforion_datalake3.png
  :width: 400

Then fill in options "Property Definitions" 

.. image:: image/inforion_datalake4.png
  :width: 400


Here review and then finish

.. image:: image/inforion_datalake6.png
  :width: 400

Here you see your project

.. image:: image/inforion_datalake7.png
  :width: 400


**Project testing:**

To verify that the project is working correctly:
Open your account, click on the App Menu,
then on Infor IONAPI, then >>"Infor ION"

Example:

.. image:: image/inforion_datalake8.png
  :width: 400

Click on the Document you want to test, for example Infor DataCatalog Rest AP

.. image:: image/inforion_datalake9.png
  :width: 400

Here in the documentation you find several test options


.. image:: image/inforion_datalake10.png
  :width: 400


Example: Get all information and metadata for an object

.. image:: image/inforion_datalake11.png
  :width: 400

.. image:: image/inforion_datalake18.png
  :width: 400
 
**How to Data query in inforion:**

Open your account, click on the App Menu,
then on ION Desk, click on Status overview, then Data Lake,
then >>"Compass" then see all CSV >> SQL >> SELECT 


.. image:: image/inforion_datalake12.png
  :width: 400

>> Run Query

.. image:: image/inforion_datalake13.png
  :width: 400

Example: where "id" is not null

.. image:: image/inforion_datalake14.png
  :width: 400

**How to delete data in inforion:** 

click on the App Menu, then on ION Desk,
click on Status overview, then Data Lake,
then >>"Purge" >> Purge by ID or Purge by Filter

* Select the date on which you want to delete the data
* Select the object name 

.. image:: image/inforion_datalake16.png
  :width: 400

Click on Purge >> YES and the data is removed.

.. image:: image/inforion_datalake17.png
  :width: 400






**How to delete object in inforion:** 

How to remove the project,click on the App Menu,
then on ION Desk, click on Status overview, then Data Catalog,
then >>"Object Schemas" Find the project you want to delete. Click on Delete >> YES
and the project is removed.



.. image:: image/inforion_datalake15.png
  :width: 400


