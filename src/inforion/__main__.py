#!/usr/bin/env python3
import logging
import os.path

import click
import inforion as infor
from inforion.datacatalog.datacatalog import delete_datacatalog_object
from inforion.datacatalog.datacatalog import ObjectSchemaType
from inforion.datacatalog.datacatalog import post_datacatalog_object
from inforion.datalake.datalake import delete_v1_purge_filter
from inforion.datalake.datalake import delete_v1_purge_id
from inforion.datalake.datalake import get_v1_payloads_list
from inforion.datalake.datalake import get_v1_payloads_stream_by_id
from inforion.excelexport import *
from inforion.helper.filehandling import *
from inforion.ionapi.controller import *
from inforion.ionapi.model import *

import logging
import os.path
import os

import logging
from logger import get_logger

from inforion.datacatalog.datacatalog import (
    post_datacatalog_object,
    delete_datacatalog_object,
    ObjectSchemaType,
)
from inforion.messaging.messaging import post_messaging_v2_multipart_message
from inforion.ionapi.model import inforlogin
from inforion.messaging.messaging import post_messaging_v2_multipart_message

# TODO update to use multi modules log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")


@click.group()
def main():
    """Generell section\n
    Please see the dodcumentation on https://inforion.readthedocs.io/
    """

    pass


@click.command(
    name="load",
    help="Section to load data to Infor ION. Right now we support Excel and CSV Data to load",
)
@click.option(
    "--url",
    "-u",
    required=True,
    prompt="Please enter the url",
    help="The full URL to the API is needed. Please note you need to enter the full url like .../M3/m3api-rest/v2/execute/CRS610MI",
)
@click.option(
    "--ionfile",
    "-f",
    required=True,
    prompt="Please enter the location ionfile",
    help="IONFile is needed to login in to Infor OS. Please go into ION and generate a IONFile. If not provided, a prompt will allow you to type the input text.",
)
@click.option(
    "--program",
    "-p",
    required=True,
    prompt="Please enter Program",
    help="What kind of program to use by the load",
)
@click.option(
    "--method",
    "-m",
    required=True,
    prompt="Please enter the method",
    help="Select the method as a list",
)
@click.option(
    "--inputfile",
    "-i",
    required=True,
    prompt="Please enter the InputFile",
    help="File to load the data. Please use XLSX or CSV format. If not provided, the input text will just be printed",
)
@click.option(
    "--outputfile", "-o", help="File as Output File - Data are saved here for the load"
)
@click.option(
    "--start", "-s", type=int, help="Dataload can be started by 0 or by a number"
)
@click.option("--end", "-e", type=int, help="Dataload can be end")
@click.option("--configfile", "-z", help="Use a Configfile instead of parameters")
def load(
    url,
    ionfile,
    program,
    method,
    inputfile,
    outputfile,
    configfile,
    start=None,
    end=None,
):

    if checkfile_exists(inputfile) is False:
        click.secho("Error:", fg="red", nl=True)
        click.echo("Inputfile does not exist")
        sys.exit(0)

    if configfile is not None:

        with open(configfile) as file:
            config_json = json.load(file)

            if all(
                k in config_json
                for k in ("url", "ionfile", "program", "method", "inputfile")
            ):
                url = config_json["url"]
                ionfile = config_json["ionfile"]
                program = config_json["program"]
                method = config_json["method"]
                inputfile = config_json["inputfile"]
                outputfile = config_json["outputfile"]
            else:
                logging.error("JSON File wrong config")
                sys.exit(0)
            if "start" in config_json:
                start = config_json["start"]
            else:
                start = None

            if "end" in config_json:
                end = config_json["end"]
            else:
                end = None

    dataframe = pd.read_excel(inputfile, dtype=str)

    return infor.main_load(
        url, ionfile, program, method, dataframe, outputfile, start, end
    )


@click.command(name="extract", help="Section to generate empty mapping sheets")
@click.option("--program", "-p", help="Choose the program to extract the sheets from")
@click.option(
    "--outputfile", "-o", help="File as Output File - Data are saved here for the load"
)
def extract(program, outputfile):

    if not "program" in locals() or not program:
        logging.info("\033[91m" + "Error: Program name is missing" + "\033[0m")
    if not "outputfile" in locals() or not outputfile:
        logging.info("\033[91m" + "Error: Output filename is missing" + "\033[0m")

    if program and outputfile:
        generate_api_template_file(program, outputfile)


@click.command(name="transform", help="section to do the transformation")
@click.option("--mappingfile", "-a", help="Please define the Mapping file")
@click.option("--mainsheet", "-b", help="Please define the mainsheet")
@click.option(
    "--inputfile",
    "-i",
    help="File to load the data. Please use XLSX or CSV format. If not provided, the input text will just be printed",
)
@click.option(
    "--outputfile", "-o", help="File as Output File - Data are saved here for the load"
)
def transform(mappingfile, mainsheet, inputfile, outputfile):
    inputdata = pd.read_excel(inputfile)
    return infor.main_transformation(mappingfile, mainsheet, inputdata, outputfile)


@main.group(name="catalog")
def catalog():
    """Commands related to Data Catalog."""
    pass


@main.group(name="datalake")
def datalake():
    """Commands related to Data Lake."""
    pass


@catalog.command(name="create", help="Catalog create")
@click.option("--ionfile", "-i", help="Please define the ionapi file")
@click.option("--name", "-n", help="Please define the object name")
@click.option("--schema_type", "-t", help="Please define the object schema type")
@click.option("--schema", "-s", help="Please define the schema file")
@click.option("--properties", "-p", help="Please define the schema properties file")
def create(ionfile, name, schema_type, schema, properties):
    inforlogin.load_config(ionfile)
    inforlogin.login()

    if not os.path.isfile(schema):
        raise FileNotFoundError("Schema file not found.")

    if not os.path.isfile(properties):
        raise FileNotFoundError("Properties file not found.")

    with open(schema, "r") as file:
        schema_content = json.loads(file.read())
    with open(properties, "r") as file:
        properties_content = json.loads(file.read())
    response = post_datacatalog_object(
        name, ObjectSchemaType(schema_type), schema_content, properties_content
    )

    if response.status_code == 200:
        logger.info("Data catalog schema {} was created.".format(name))
    else:
        logger.error(response.content)


@catalog.command(name="delete", help="Catalog delete")
@click.option("--ionfile", "-i", help="Please define the ionfile file")
@click.option("--name", "-n", help="Please define the object name")
def delete(ionfile, name):
    inforlogin.load_config(ionfile)
    inforlogin.login()
    response = delete_datacatalog_object(name)

    if response.status_code == 200:
        logger.info("Data catalog schema {} was deleted.".format(name))
    else:
        logger.error(response.content)


@datalake.command(name="upload", help="Datalake upload")
@click.option("--ionfile", "-i", help="Please define the ionfile file")
@click.option("--schema", "-s", help="Please define the schema name")
@click.option("--logical_id", "-l", help="Please define the fromLogicalId")
@click.option("--file", "-f", help="Please define the file")
def upload(ionfile, schema, logical_id, file):
    inforlogin.load_config(ionfile)
    inforlogin.login()
    parameter_request = {
        "documentName": schema,
        "fromLogicalId": logical_id,
        "toLogicalId": "lid://default",
        "encoding": "NONE",
        "characterSet": "UTF-8",
    }
    with open(file, "rb") as file:
        message_payload = file.read()
    response = post_messaging_v2_multipart_message(parameter_request, message_payload)

    if response.status_code == 201:
        logger.info("Document uploaded successfully.")
    else:
        logger.error(response.content)


@datalake.command(name="list", help="Datalake list")
@click.option("--ionfile", "-i", help="Please define the ionfile file")
@click.option("--list_filter", "-f", help="Please define the filter")
@click.option("--sort", "-s", help="Please define the sort")
@click.option("--page", "-p", help="Please define the page")
@click.option("--records", "-r", help="Please define the records")
def datalake_list(ionfile, list_filter=None, sort=None, page=None, records=None):
    """
    List data object properties using a filter.
    :param ionfile: Infor IONAPI credentials file.
    :param list_filter: The restrictions to be applied on the returned records.
    :param sort: Field name followed by colon followed by direction (asc or desc; default asc).
    Example: 'event_date:desc'.
    :param page: The page number from which to start returning records. Starts from 1.
    :param records: The number of records that will be returned. Starts from 0
    """
    inforlogin.load_config(ionfile)
    inforlogin.login()
    response = get_v1_payloads_list(list_filter, sort, page, records)

    if response.status_code == 200:
        click.echo(response.text)
    else:
        logger.error(response.content)


@datalake.command(name="purge", help="Datalake purge")
@click.option("--ionfile", "-i", help="Please define the ionfile file")
@click.option("--ids", "-id", help="Please define the ids")
@click.option("--purge_filter", "-f", help="Please define the filter")
def datalake_purge(ionfile, ids, purge_filter):
    """
    Deletes Data Objects based on the given filter or a list of IDs.
    You cannot define both arguments: ids and purge_filter.
    :param ionfile: Infor IONAPI credentials file.
    :param ids: Object ids.
    :param purge_filter: The restrictions to be applied to purge the records
    """
    if ids is not None and purge_filter is not None:
        raise ValueError("You cannot define both arguments: ids and purge_filter.")

    inforlogin.load_config(ionfile)
    inforlogin.login()

    if ids is not None:
        ids_list = ids.split(",")
        response = delete_v1_purge_id(ids_list)
        if response.status_code == 200:
            click.echo(response.text)
        else:
            logger.error(response.content)

    if purge_filter is not None:
        response = delete_v1_purge_filter(purge_filter)
        if response.status_code == 200:
            click.echo(response.text)
        else:
            logger.error(response.content)


@datalake.command(name="get", help="Datalake get")
@click.option("--ionfile", "-i", help="Please define the ionfile file")
@click.option("--stream_id", "-id", help="Please define the id")
def datalake_get(ionfile, stream_id):
    """
    Retrieve payload based on id from datalake.
    :param ionfile: Infor IONAPI credentials file.
    :param stream_id: Object ID.
    """
    inforlogin.load_config(ionfile)
    inforlogin.login()
    response = get_v1_payloads_stream_by_id(stream_id)

    if response.status_code == 200:
        click.echo(response.text)
    else:
        logger.error(response.content)


@main.group(name="check")
def check():
    """Commands to check soemthing"""
    pass


@check.command(name="Check_Token", help="Check Login Token")
@click.option("--url", "-u", help="URL to local ION")
@click.option("--ionfile", "-i", help="Please define the ionfile file")
def check_token(url, ionfile):
    """Check Login and display the token"""
    inforlogin.load_config(ionfile)
    inforlogin.login()


main.add_command(load)
main.add_command(transform)
main.add_command(extract)
main.add_command(check)

if __name__ == "__main__":
    main()
