# Transformation of Staging Data into M3 format via mapping file 
import pandas as pd
import json
import numpy as np
import decimal
import datetime
from multiprocessing import  Pool
from functools import partial

def parallelize_tranformation(mappingfile, mainsheet,stagingdata,outputfile=None,n_cores=4):

    # Read the file from given location
    xls = pd.ExcelFile(mappingfile)

    # to read all sheets to a map
    sheet_to_df_map = {}
    for sheet_name in xls.sheet_names:
        sheet_to_df_map[sheet_name] = xls.parse(sheet_name)
    
    df_split = np.array_split(stagingdata, n_cores)
    func = partial(transform_data, sheet_to_df_map, mainsheet)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()

    if outputfile is not None:
        print ('Save to file: ' + outputfile)
        writer = pd.ExcelWriter(outputfile, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Log Output',index=False)
        writer.save()

    return df

def transform_data(sheet_to_df_map, mainsheet, stagingdata):
    rows_list = []

    for tb_index,tb_row in stagingdata.iterrows():
        row_dict = {}
        for index,row in sheet_to_df_map[mainsheet].iterrows():
            row =  row.replace(np.nan, '', regex=True)
            if index >=9:
                if row[33] and not row[33] is np.nan:
                    row_dict[row[15]] = str(tb_row[row[33]])
                else:
                    if row[36].strip().lower() == 'tbl':
                        tab = {}
                        for i,val in sheet_to_df_map[row[37].strip()].iterrows():
                            if i >= 7:
                                if str(val[0]) == 'nan': val[0] = ''
                                tab[str(val[0])] = str(val[1])
                        if row[38] and not row[38] is np.nan:
                            tb_row_val = str(tb_row[row[38]])
                            if tb_row_val in tab:
                                row_dict[row[15]] = str(tab[tb_row_val])
                            elif '*' in tab:
                                row_dict[row[15]] = str(tab['*'])
                            else:
                                row_dict[row[15]] = tb_row_val
                    elif row[36].strip().lower() == 'func':
                        if row[37].strip().lower() == "div":
                            data_values = row[38].split('|')
                            with decimal.localcontext() as ctx:
                                if data_values[2] != "":
                                    ctx.prec = int(data_values[2])
                                division = decimal.Decimal(tb_row[data_values[0]]) / decimal.Decimal(data_values[1])
                        row_dict[row[15]] = division
                    elif row[36].strip().lower() == 'const':
                        if isinstance(row[37], datetime.datetime):
                            row[37] = row[37].strftime("%Y-%m-%d")
                        row_dict[row[15]] = str(row[37])
        rows_list.append(row_dict)
    
    df = pd.DataFrame(rows_list).replace('nan', '', regex=True)

    return df