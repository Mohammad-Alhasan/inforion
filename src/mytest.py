import inforion as infor
import pandas as pd

df = pd.read_excel('/Applications/MAMP/htdocs/inforion/newoutput.xlsx')

print(infor.main_load('https://mingle-ionapi.eu1.inforcloudsuite.com/BVB_DEV/M3/m3api-rest/v2/execute',"/Applications/MAMP/htdocs/inforion/FellowKey.ionapi",'CRS610MI','ChgBasicData,ChgOrderInfo,ChgFinancial',df,None,0,3))

#db_data = pd.read_excel('/Applications/MAMP/htdocs/inforion/src/output.xlsx')
#newDF = infor.main_transformation("/Applications/MAMP/htdocs/inforion/src/BVB_Mapping_Kundenstamm.xlsx","Kunden",db_data)
#print(newDF)