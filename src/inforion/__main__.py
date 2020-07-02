#!/usr/bin/env python3

import click

import inforion as infor
from inforion.excelexport import *
from inforion.ionapi.controller import *
from inforion.ionapi.model import *


@click.group()
def main():
    """ Generell section"""
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

    if configfile is not None:
        configfile = arg
        with open(configfile) as file:
            config_json = json.load(file)
                
            if all (k in config_json for k in ('url','ionfile','program','method','inputfile')):
                typ = "Load"
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


@click.command(name='datalake', help='Datalake Section')
@click.option('--lid',"-l",help='Please define the lid')
@click.option('--schema',"-c",help='Please define the Schema')
@click.option('--inputfile',"-i",help='File to load the data. Please use XLSX or CSV format''If not provided, the input text will just be printed, if you choose Typ=L',)
def datalake(url, ionfile, lid, inputfile, schema):
    print('datalake.......')
    # post_to_data_lake(url, ionfile, lid, inputfile, schema)


main.add_command(load)
main.add_command(transform)
main.add_command(extract)
main.add_command(datalake)

if __name__ == "__main__":
    main()
