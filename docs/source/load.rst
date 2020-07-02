============
Loading
============

Example is to load data from Excel to Infor Application for example M3.

inforion load --help    

Options:
-u, --url TEXT         The full URL to the API is needed. Please note you need to enter the full url like .../M3/m3api-rest/v2/execute/CRS610MI  [required]
-f, --ionfile TEXT     IONFile is needed to login in to Infor OS. Please go into ION and generate a IONFile. If not provided, a prompt will allow you to type the input text. [required]
-p, --program TEXT     What kind of program to use by the load  [required]
-m, --method TEXT      Select the method as a list  [required]
-i, --inputfile TEXT   File to load the data. Please use XLSX or CSV format. If not provided, the input text will just be printed [required]
-o, --outputfile TEXT  File as Output File - Data are saved here for the load
-s, --start INTEGER    Dataload can be started by 0 or by a number
-e, --end INTEGER      Dataload can be end
-z, --configfile TEXT  Use a Configfile instead of parameters

inforion load -u https://mingle-ionapi.eu1.inforcloudsuite.com/Tendat_DEV/M3/m3api-rest/v2/execute -f FellowKey.ionapi -p CRS610MI -m "Add,ChgBasicData,ChgOrderInfo,ChgFinancial" -i excel/T-KundenNeu1.xlsx  -o load_full_200.xlsx -s 0 -e 2