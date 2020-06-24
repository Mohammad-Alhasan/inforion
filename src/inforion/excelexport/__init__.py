import json
import os
import xlwings as xw
import xlsxwriter
import openpyxl

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

apiDirPath = dir_path + "/api-files"
templateFileName = dir_path + "/BVB_Mapping_Template.xlsx"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def getAPIFile(api_name):
    files = os.listdir(apiDirPath)
    for filename in files:
        file_path = os.path.join(apiDirPath, filename)
        with open(file_path) as json_file:
            data = json.load(json_file)
            file_api_name = data['info']['title'].split()[0]
            if file_api_name.startswith(api_name):
                return file_api_name, file_path


def getParametersList(filepath):
    parameters_list = {}
    with open(filepath) as json_file:
        data = json.load(json_file)
        for (k, v) in data['paths'].items():
            key = k.replace("/", "")
            if key.startswith('Add') or key.startswith('Chg') or key.startswith('Crt'):
                for jparam in v['get']['parameters']:
                    if jparam['name'].upper() not in parameters_list:
                        org_description = jparam['description']
                        ind = org_description.rfind('(')

                        jparam['api'] = key
                        if ind >= 0:
                            jparam['description'] = org_description[0:ind]
                            jparam['length'] = org_description[ind + 1:-1]
                        else:
                            jparam['description'] = org_description
                            jparam['length'] = ''

                        parameters_list[jparam['name'].upper()] = jparam

    #print(parameters_list)
    return parameters_list


def createEmptySheet(outputfilename, copytemplatesheet):
    # Create a workbook and add a worksheet.
    filename = outputfilename
    if(not outputfilename.endswith('.xlsx')):
        filename = filename + '.xlsx'

    workbook = xlsxwriter.Workbook(filename)
    # worksheet = workbook.add_worksheet(apiName)
    workbook.close()

    if(copytemplatesheet):

        wb1 = xw.Book(templateFileName)
        wb2 = xw.Book(filename)

        ws1 = wb1.sheets['Mapping Template']
        ws1.api.copy_worksheet(after_=wb2.sheets[0].api)

        wb2.save()
        wb2.app.quit()

    return True


def checkIfTemplateFileExists():
    return os.path.isfile(templateFileName)


def getTypeCode(type_str):
    if type_str == 'string':
        return 'A'
    elif type_str == 'number':
        return 'N'
    elif type_str == 'date':
        return 'D'


def updateSheetWithData(filename, apiName, params):
    xfile = openpyxl.load_workbook(filename)

    sheet = xfile.get_sheet_by_name('Mapping Template')

    current_row = 11
    for k, v in params.items():
        # Serial Number
        sheet['A' + str(current_row)] = current_row - 10
        sheet['B' + str(current_row)] = apiName

        sheet['P' + str(current_row)] = k
        sheet['Q' + str(current_row)] = apiName
        sheet['R' + str(current_row)] = v['api']
        sheet['S' + str(current_row)] = getTypeCode(v['type'])
        sheet['V' + str(current_row)] = v['length']
        sheet['W' + str(current_row)] = 1 if v['required'] else 0
        sheet['X' + str(current_row)] = v['description']

        current_row = current_row + 1

    xfile.save(filename)


def generate_api_template_file(program, outputfile):

    if not program:
        return '\033[91m' + "Error: Program name is missing" + '\033[0m'

    if not outputfile:
        return '\033[91m' + "Error: Output filename is missing" + '\033[0m'

    api_name = program
    filename = outputfile
    if(not outputfile.endswith('.xlsx')):
        filename = filename + '.xlsx'

    api_info = getAPIFile(api_name)

    if api_info is not None:
        #print(api_info)
        params = getParametersList(api_info[1])
        createEmptySheet(filename, True)
        updateSheetWithData(filename, api_info[0], params)
        print(bcolors.OKGREEN + "File generated successfully" + bcolors.ENDC)
    else:
        print(bcolors.FAIL +
              "Error: API specifications file not found in directory 'api-files'. Please make sure that specifications file exits" + bcolors.ENDC)

def getAPIProgramNames():
    files = os.listdir(apiDirPath)
    for filename in files:
        file_path = os.path.join(apiDirPath, filename)
        with open(file_path) as json_file:
            data = json.load(json_file)
            file_api_name = data['info']['title'].split()[0]
            print("\'" + file_api_name + "\'" +',')
