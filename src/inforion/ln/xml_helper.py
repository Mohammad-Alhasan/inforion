import xml.etree.ElementTree as et
import pandas as pd

def get_data_frame_from_XML_Nodes_List (nodes_list, df_cols): 
    """Parse the input XML file and store the result in a pandas 
    DataFrame with the given columns. 
    
    The first element of df_cols is supposed to be the identifier 
    variable, which is an attribute of each node element in the 
    XML data; other features will be parsed from the text content 
    of each sub-element. 
    """

    rows = []
    for node in nodes_list: 
        res = []
        for el in df_cols[0:]: 
            #print(el)
            if node is not None and node.find(el) is not None:
                res.append(node.find(el).text)
            else: 
                res.append(None)
        rows.append({df_cols[i]: res[i] 
                     for i, _ in enumerate(df_cols)})
    
    out_df = pd.DataFrame(rows, columns=df_cols)
        
    return out_df


def get_leaf_node_names(elem):
    elemList = []
    for selem in elem.iter():
        #print(selem)
        if len(list(selem)) ==0:
            elemList.append(selem.tag)
    return elemList


def get_request_xml(company):

    xml_string = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
            <Header>
                <Activation xmlns="http://www.infor.com/businessinterface/BusinessPartner_v3">
                    <company xmlns="">{company}</company>
                </Activation>
            </Header>
            <Body>
                <List xmlns="http://www.infor.com/businessinterface/BusinessPartner_v3">
                    <ListRequest></ListRequest>
                </List>
            </Body>
        </Envelope>"""