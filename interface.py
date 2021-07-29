import json
from PySimpleGUI.PySimpleGUI import Titlebar
from cryptography.fernet import Fernet
from time import sleep
import PySimpleGUI as sg
import os


def pysimp_interface():
    sg.theme('Reddit')
    icon_path = os.path.join(os.path.dirname(__file__), 'cc_small_png.png')    
    layout = [[Titlebar(title = "CrypticConvert", icon = icon_path, background_color= "black")],
            [sg.Text("Put your un-encrypted text here: "), sg.Text('Your encryption key is:', pad = ((165, 0), (0,0)))],
            [sg.Input(key='-IN-', size = ("50",None)), sg.Input(key = "-KEY-", size = ("50", None), readonly=True)],
            [sg.Button('Encrypt')],
            [sg.Text("Put your encrypted text here: "), sg.Text('Put your encryption key here: ', pad = ((182, 0), (0,0)))],
            [sg.Input(key='-EIN-', size = ("50",None)), sg.Input(key = "-EKEY-", size = ("50", None), readonly=False)],
            [sg.Button('Decrypt'), sg.Text(key = 'KeyCheck', justification = "right", font = ("arial", 8), text_color = "green", s = ("50", None), pad = ((256, 0), (0,0)))]]

    window = sg.Window('CrypticConvert', layout, button_color = "purple")
    #event loop for input, makes the window persistent
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Encrypt':
            try:
                key = Fernet.generate_key()
                big_key = key
                window['-KEY-'].update(key)
                window['-EKEY-'].update(key)
                window['KeyCheck'].update("Encryption-key copied from above.")
                fernet = Fernet(key)
                encoded = json.dumps(values['-IN-']).encode('utf-8')
                encrypted_bytes = fernet.encrypt(encoded)
                encrypted = encrypted_bytes.decode('utf-8')
                sg.clipboard_set(encrypted)
                sg.PopupNoFrame('See below for encrypted text: \n', encrypted, '(Copied to clipboard)')
            except:
                sg.PopupNoFrame('Could not decrypt as requested, try again.')
        elif event == "Decrypt":
            try:
                key = values['-EKEY-']
                key = key.strip('b')
                fernet = Fernet(key)
                encoded = values["-EIN-"].encode('utf-8')
                decrypted_bytes = fernet.decrypt(encoded)
                decrypted = decrypted_bytes.decode('utf-8')
                sg.clipboard_set(decrypted)
                sg.PopupNoFrame('See below for decrypted text: \n', decrypted, '(Copied to clipboard)')
            except:
                sg.PopupNoFrame('Could not decrypt as requested, try again.')
    #closes window when breaking out of event loop
    window.close()