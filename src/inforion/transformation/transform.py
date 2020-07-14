# Transformation of Staging Data into M3 format via mapping file
import datetime
import decimal
import logging
from functools import partial
from multiprocessing import Pool

import numpy as np
import pandas as pd

# from logger import get_logger


def parallelize_tranformation(
    mappingfile, mainsheet, stagingdata, outputfile=None, n_cores=4
):
    # Read the file from given location
    xls = pd.ExcelFile(mappingfile)

    # to read all sheets to a map
    sheet_to_df_map = {}
    for sheet_name in xls.sheet_names:
        sheet_to_df_map[sheet_name] = xls.parse(sheet_name)

    main_cache = getMainSheetCache(sheet_to_df_map, mainsheet)
    tabs_cache = getTabsMappingCache(sheet_to_df_map, main_cache)

    df_split = np.array_split(stagingdata, n_cores)
    func = partial(transform_data, sheet_to_df_map, mainsheet, main_cache, tabs_cache)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()

    if outputfile is not None:
        logging.info("Save to file: " + outputfile)
        writer = pd.ExcelWriter(outputfile, engine="xlsxwriter")
        df.to_excel(writer, sheet_name="Log Output", index=False)
        writer.save()

    return df


def getMainSheetCache(sheet_to_df_map, mainsheet):
    mapping_cache = []

    for index, row in sheet_to_df_map[mainsheet].iterrows():
        if index >= 9:
            row = row.replace(np.nan, "", regex=True)

            map = {}
            map["API_FIELD"] = row[15]

            if row[33] and not row[33] is np.nan:
                map["SOURCE"] = row[33]
            else:
                map["SOURCE"] = None

            map["FUNC_TYPE"] = row[36].strip().lower()

            map["FUNC_VAL"] = row[37]
            map["FUNC_ARG"] = row[38]

            mapping_cache.append(map)

    return mapping_cache


def getTabsMappingCache(sheet_to_df_map, mapping_cache):
    mapping_sheets_cache = {}

    for map in mapping_cache:
        if map["FUNC_TYPE"] == "tbl":
            tab_key = map["FUNC_VAL"].strip()
            if tab_key not in mapping_sheets_cache:
                tab = {}
                for i, val in sheet_to_df_map[tab_key].iterrows():
                    if i >= 7:
                        if str(val[0]) == "nan":
                            val[0] = ""
                        tab[str(val[0])] = str(val[1])
                mapping_sheets_cache[tab_key] = tab

    return mapping_sheets_cache


def transform_data(_sheet_to_df_map, _mainsheet, sheet_cache, tabs_cache, stagingdata):
    rows_list = []

    for _, tb_row in stagingdata.iterrows():
        row_dict = {}

        for map in sheet_cache:

            if map["SOURCE"]:
                row_dict[map["API_FIELD"]] = str(tb_row[map["SOURCE"]])
            else:
                if map["FUNC_TYPE"] == "tbl":
                    if map["FUNC_ARG"] and not map["FUNC_ARG"] is np.nan:
                        tab = tabs_cache[map["FUNC_VAL"]]
                        if tb_row[map["FUNC_ARG"]] in tab:
                            row_dict[map["API_FIELD"]] = str(
                                tab[tb_row[map["FUNC_ARG"]]]
                            )
                        elif "*" in tab:
                            row_dict[map["API_FIELD"]] = str(tab["*"])
                        else:
                            row_dict[map["API_FIELD"]] = str(tb_row[map["FUNC_ARG"]])
                elif map["FUNC_TYPE"] == "func":
                    if map["FUNC_VAL"].strip().lower() == "div":
                        data_values = map["FUNC_ARG"].split("|")
                        with decimal.localcontext() as ctx:
                            if data_values[2] != "":
                                ctx.prec = int(data_values[2])
                            division = decimal.Decimal(
                                tb_row[data_values[0]]
                            ) / decimal.Decimal(data_values[1])
                    row_dict[map["API_FIELD"]] = division
                elif map["FUNC_TYPE"] == "const":
                    if isinstance(map["FUNC_VAL"], datetime.datetime):
                        val = map["FUNC_VAL"].strftime("%Y%m%d")
                        row_dict[map["API_FIELD"]] = str(val)
                    else:
                        row_dict[map["API_FIELD"]] = str(map["FUNC_VAL"])

        rows_list.append(row_dict)

    df = pd.DataFrame(rows_list).replace("nan", "", regex=True)

    return df
