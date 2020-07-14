import xml.etree.ElementTree as et

import pandas as pd


def get_data_frame_from_XML_Nodes_List(nodes_list, df_cols):
    rows = []
    for node in nodes_list:
        res = []
        for el in df_cols[0:]:
            # print(el)
            if node is not None and node.find(el) is not None:
                res.append(node.find(el).text)
            else:
                res.append(None)
        rows.append({df_cols[i]: res[i] for i, _ in enumerate(df_cols)})

    out_df = pd.DataFrame(rows, columns=df_cols)

    return out_df


def get_leaf_node_names(elem):
    elemList = []

    for selem in elem.iter():
        # print(selem)
        if len(list(selem)) == 0:
            elemList.append(selem.tag)
    return elemList


def get_main_node_names(elem):
    elemList = []

    children = elem.getchildren()
    for child in children:
        if len(list(child)) == 0:
            elemList.append(child.tag)
    return elemList
