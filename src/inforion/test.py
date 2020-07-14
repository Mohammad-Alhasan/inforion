import inforion as infor

import pandas as pd

dataframe = pd.read_excel('T-Vendor_Emailaddresse_CRS111_20200713.xlsx', dtype=str)

infor.main_load('https://mingle-ionapi.eu1.inforcloudsuite.com/BVB_DEV/M3/m3api-rest/v2/execute', 'FellowKey.ionapi', 'CRS111MI', "Add,Change", dataframe, "T-Vendor_Emailaddresse_CRS111_20200713_report.xlsx", 1, 200   )