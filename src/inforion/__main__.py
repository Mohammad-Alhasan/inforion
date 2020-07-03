#!/usr/bin/env python3

import click

import inforion as infor
from inforion.excelexport import *
from inforion.ionapi.controller import *
from inforion.ionapi.model import *

import logging
import os.path
import os

from inforion.datacatalog.datacatalog import post_datacatalog_object, delete_datacatalog_object, ObjectSchemaType
from inforion.messaging.messaging import post_messaging_v2_multipart_message
from inforion.ionapi.model import inforlogin

# TODO update to use multi modules log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main')


@click.group()
def main():
    """ Generell section\n
    Please see the dodcumentation on https://inforion.readthedocs.io/ """
    pass


@click.command(name='load', help='Section to load data to Infor ION. Right now we support Excel and CSV Data to load')
@click.option('--url',"-u",required=True,prompt='Please enter the url',help='The full URL to the API is needed. Please note you need to enter the full url like .../M3/m3api-rest/v2/execute/CRS610MI')
@click.option('--ionfile',"-f",required=True,prompt='Please enter the location ionfile',help='IONFile is needed to login in to Infor OS. Please go into ION and generate a IONFile. If not provided, a prompt will allow you to type the input text.',)
@click.option('--program',"-p",required=True,prompt='Please enter Program',help='What kind of program to use by the load')
@click.option('--method',"-m",required=True,prompt='Please enter the method',help='Select the method as a list')
@click.option('--inputfile',"-i",required=True,prompt='Please enter the InputFile',help='File to load the data. Please use XLSX or CSV format. If not provided, the input text will just be printed',)
@click.option('--outputfile',"-o",help='File as Output File - Data are saved here for the load')
@click.option('--start',"-s",type=int,help='Dataload can be started by 0 or by a number')
@click.option('--end',"-e",type=int,help='Dataload can be end')
@click.option('--configfile',"-z",help='Use a Configfile instead of parameters')
def load(url, ionfile, program, method, inputfile, outputfile, configfile, start=None, end=None):

    if os.path.exists(inputfile) == False:
        click.secho('Error:', fg='red', nl=True)
        click.echo("Inputfile does not exist")
        
        sys.exit(0)
    


    if configfile is not None:
        configfile = arg
        with open(configfile) as file:
            config_json = json.load(file)
                
            if all (k in config_json for k in ('url','ionfile','program','method','inputfile')):
                url = config_json['url']
                ionfile = config_json['ionfile']
                program = config_json['program']
                method = config_json['method']
                inputfile = config_json['inputfile']
                outputfile = config_json['outputfile']     
            else:
                print ("JSON File wrong config")
                sys.exit(0)
            if "start" in config_json:
                start = config_json["start"]
            else:
                start = None

            if "end" in config_json:
                end = config_json["end"]
            else:
                end = None
    
    dataframe = pd.read_excel(inputfile,dtype=str)
    
    return infor.main_load(url, ionfile, program, method, dataframe, outputfile, start, end)


@click.command(name='extract', help='Section to generate empty mapping sheets')
@click.option('--program',"-p",help='Choose the program to extract the sheets from')
@click.option('--outputfile',"-o",help='File as Output File - Data are saved here for the load')
def extract(program, outputfile):

    if not 'program' in locals() or not program:
        print('\033[91m' + "Error: Program name is missing" + '\033[0m')
    if not 'outputfile' in locals() or not outputfile:
        print('\033[91m' + "Error: Output filename is missing" + '\033[0m')
 
    if program and outputfile:
        generate_api_template_file(program, outputfile)


@click.command(name='transform', help='section to do the transformation')
@click.option('--mappingfile',"-a",help='Please define the Mapping file')
@click.option('--mainsheet',"-b",help='Please define the mainsheet')
@click.option('--inputfile',"-i",help='File to load the data. Please use XLSX or CSV format. If not provided, the input text will just be printed')
@click.option('--outputfile',"-o",help='File as Output File - Data are saved here for the load')
def transform(mappingfile, mainsheet, inputfile, outputfile):
        inputdata = pd.read_excel(inputfile)
        return infor.main_transformation(mappingfile,mainsheet,inputdata,outputfile)


@click.command(name='datacatalog_post', help='Datacatalog Section')
@click.option('--ionfile', "-i", help='Please define the ionapi file')
@click.option('--name', "-n", help='Please define the object name')
@click.option('--type', "-t", help='Please define the object type')
@click.option('--schema', "-s", help='Please define the schema file')
@click.option('--properties', "-p", help='Please define the schema properties file')
def datacatalog_post(ionfile, name, type, schema, properties):
    inforlogin.load_config(ionfile)
    inforlogin.login()

    if not os.path.isfile(schema):
        raise FileNotFoundError('Schema file not found.')

    if not os.path.isfile(properties):
        raise FileNotFoundError('Properties file not found.')

    with open(schema, "r") as file:
        schema_content = json.loads(file.read())
    with open(properties, "r") as file:
        properties_content = json.loads(file.read())
    response = post_datacatalog_object(name, ObjectSchemaType(type), schema_content, properties_content)

    if response.status_code == 200:
        logger.info('Data catalog schema {} was created.'.format(name))
    else:
        logger.error(response.content)


@click.command(name='datacatalog_delete', help='Datacatalog Section')
@click.option('--ionfile', "-i", help='Please define the ionfile file')
@click.option('--name', "-n", help='Please define the object name')
def datacatalog_delete(ionfile, name):
    inforlogin.load_config(ionfile)
    inforlogin.login()
    response = delete_datacatalog_object(name)

    if response.status_code == 200:
        logger.info('Data catalog schema {} was deleted.'.format(name))
    else:
        logger.error(response.content)


@click.command(name='messaging_post', help='Messaging Section')
@click.option('--ionfile', "-i", help='Please define the ionfile file')
@click.option('--schema', "-s", help='Please define the schema name')
@click.option('--logical_id', "-l", help='Please define the fromLogicalId')
@click.option('--file', "-f", help='Please define the file')
def messaging_post(ionfile, schema, logical_id, file):
    inforlogin.load_config(ionfile)
    inforlogin.login()
    parameter_request = {
        "documentName": schema,
        "fromLogicalId": logical_id,
        "toLogicalId": "lid://default",
        "encoding": "NONE",
        "characterSet": "UTF-8"
    }
    with open(file, "rb") as file:
        message_payload = file.read()
    response = post_messaging_v2_multipart_message(parameter_request, message_payload)

    if response.status_code == 201:
        logger.info('Document uploaded successfully.')
    else:
        logger.error(response.content)


main.add_command(messaging_post)
main.add_command(datacatalog_delete)
main.add_command(datacatalog_post)
main.add_command(load)
main.add_command(transform)
main.add_command(extract)


if __name__ == "__main__":
    main()
