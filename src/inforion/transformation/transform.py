# Transformation of Staging Data into M3 format via mapping file 
import pandas as pd
import json
import numpy as np
import decimal

def tranform_data(mappingfile, mainsheet,stagingdata,outputfile=None):

    # Read the file from given location
    xls = pd.ExcelFile(mappingfile)

    # to read all sheets to a map
    sheet_to_df_map = {}
    for sheet_name in xls.sheet_names:
        sheet_to_df_map[sheet_name] = xls.parse(sheet_name)
        
    rows_list = []

    for tb_index,tb_row in stagingdata.iterrows():
        row_dict = {}
        for index,row in sheet_to_df_map[mainsheet].iterrows():
            #
            if index >=9:
                if row[33] and not row[33] is np.nan:
                    row_dict[row[15]] = str(tb_row[row[33]])
                else:
                    if row[36] == 'tbl':
                        tab = {}
                        for i,val in sheet_to_df_map[row[37]].iterrows():
                            if i >= 7:
                                if str(val[0]) == 'nan': val[0] = ''
                                tab[str(val[0])] = str(val[1])
                        if row[38] and not row[38] is np.nan:
                            if tb_row[row[38]] in tab:
                                row_dict[row[15]] = str(tab[tb_row[row[38]]])
                            else:
                                row_dict[row[15]] = str(tb_row[row[38]])
                    elif row[36] == 'func':
                        if row[37] == "DIV":
                            data_values = row[38].split('|')
                            with decimal.localcontext() as ctx:
                                if data_values[2] != "":
                                    ctx.prec = int(data_values[2])
                                division = decimal.Decimal(tb_row[data_values[0]]) / decimal.Decimal(data_values[1])
                        row_dict[row[15]] = division
                    elif row[36] == 'const':
                        row_dict[row[15]] = str(row[37])
        rows_list.append(row_dict)
    
    df = pd.DataFrame(rows_list).replace('nan', '', regex=True)

    if outputfile is not None:
        print ('Save to file: ' + outputfile)
        writer = pd.ExcelWriter(outputfile, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Log Output',index=False)
        writer.save()

    return df