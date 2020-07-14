import PySimpleGUI as sg
import pandas as pd

# from inforion import main_load

import inforion as infor

sg.theme("Dark Blue 3")
appFont = ("Helvetica", 16)
sg.set_options(font=appFont)


def show_main():

    METER_REASON_CANCELLED = "cancelled"
    METER_REASON_CLOSED = "closed"
    METER_REASON_REACHED_MAX = "finished"
    METER_OK = True
    METER_STOPPED = False

    layout = [
        [sg.Text("URL")],
        [sg.Input()],
        [sg.Text("ION File")],
        [sg.Input(), sg.FileBrowse(file_types=(("ION API File", "*.ionapi"),))],
        [sg.Text("Program")],
        [sg.Input()],
        [sg.Text("Method")],
        [sg.Input()],
        [sg.Text("Input File")],
        [sg.Input(), sg.FileBrowse()],
        [sg.Text("Output File")],
        [sg.Input(), sg.FileBrowse()],
        [sg.Text("Start")],
        [sg.Input(key="-INS-", enable_events=True)],
        [sg.Text("End")],
        [sg.Input(key="-INE-", enable_events=True)],
        [sg.Button("Ok"), sg.Button("Cancel")],
    ]

    window = sg.Window("Import Data", layout, margins=(10, 10))

    while True:  # Event Loop
        event, values = window.read()
        if event in (None, sg.WIN_CLOSED, "Exit", "Cancel"):
            break

        if event in ("-INS-", "-INE-"):
            if values[event] and values[event][-1] not in ("0123456789."):
                window[event].update(values[event][:-1])

        if event == "Ok":
            
            url = values[0]
            ionfile = values[1]
            program = values[2]
            method = values[3]
            inputfile = values[4]
            outputfile = values[5]
            start = int(values["-INS-"])
            end = int(values["-INE-"])
            

            dataframe = pd.read_excel(inputfile, dtype=str)

            infor.main_load(
                            url, ionfile, program, method, dataframe, outputfile, start, end, on_progress
                        )

    window.close()


def on_progress(total, processed):
    sg.one_line_progress_meter("My 1-line progress meter", processed, total, "single")


show_main()
