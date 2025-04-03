from libs import PySimpleGUI as sg, os, asyncio,pygame,threading,random
from Functional import convert_image_for_sg,GENERATE_1,EXCEL_1

async def create_UI(func_name, *args, **kwargs):
    func = globals().get(func_name)
    if callable(func):
        result = await func(*args, **kwargs)
        if result is not None:
            return result
    else:
        print(f"Функция {func_name} не найдена")
async def Intro_1(intro_name="Intro", time_=5, fps=0.05, folder='..\Images', ammount=14, theme_=""):
    try:
        if theme_ == "":
            with open('../Files/theme', 'r',encoding='utf-8') as f:
                read = f.read()
                theme_ = str(read.split("\n")[0].split(":")[-1])

        image_folder = folder
        image_files = [f'{i}.png' for i in range(0, ammount)]
        duration = time_
        interval = fps

        sg.theme(theme_)

        for image_file in image_files:
            await convert_image_for_sg(os.path.join(image_folder, image_file))

        layout_intro = [
            [sg.Image(filename=os.path.join(image_folder, image_files[0]), key='-IMAGE-',pad=(0, 0, 0, 0))],
            [sg.ProgressBar(max_value=100, orientation='h', size=(73, 20), key='-PROGRESS-',relief=sg.RELIEF_SUNKEN,pad=(0, 0, 0, 0))],

        ]

        window_intro = sg.Window(intro_name, layout_intro, finalize=True, icon="..\icon.ico")

        for i in range(int(duration / interval)):
            #print(os.path.join(image_folder, image_files[i % len(image_files)]))
            print(i)
            window_intro['-IMAGE-'].update(filename=os.path.join(image_folder, image_files[i % len(image_files)]))
            window_intro['-PROGRESS-'].update((i + 1) * (100 / (duration / interval)))
            await asyncio.sleep(interval)

        window_intro.close()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
async def Main_Menu(menu_name="Main Menu", theme_=""):
    if theme_ == "":
        with open('../Files/theme', 'r',encoding='utf-8') as f:
            read = f.read()
            theme_ = str(read.split("\n")[0].split(":")[-1])

    sg.theme(theme_)

    menu_layout = [
        [sg.Button("WorkFlow", key='Workflow')],
        [sg.Button('Constructor', key='Constructor')],
        [sg.Button('Settings', key='Settings')],
        [sg.Button('Exit', key='Exit')],
    ]

    with open('../Files/Settings', 'r',encoding='utf-8') as f:
        read = f.read()
        size_x = int(read.split("\n")[0].split(":")[-1])
        size_y = int(read.split("\n")[1].split(":")[-1])

    menu_window = sg.Window(menu_name, menu_layout, size=(size_x, size_y), finalize=True, icon="..\icon.ico")

    while True:
        event, values = menu_window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            
            break
        elif event == 'Constructor':
            menu_window.close()
            await create_UI('Constructor_main', constructor_name="Constructor")
        elif event == 'Settings':
            menu_window.close()
            await create_UI('Settings_main', settings_name="Settings")
        elif event == 'Workflow':
            menu_window.close()
            await create_UI('Workflow_main', workflow_name="Workflow")
    menu_window.close()
async def Constructor_main(constructor_name="Constructor", theme_=""):
    if theme_ == "":
        with open('../Files/theme', 'r',encoding='utf-8') as f:
            read = f.read()
            theme_ = str(read.split("\n")[0].split(":")[-1])

    sg.theme(theme_)

    with open('../Files/Settings', 'r',encoding='utf-8') as f:
        read = f.read()
        size_x = int(read.split("\n")[0].split(":")[-1])
        size_y = int(read.split("\n")[1].split(":")[-1])

    constructor_layout = [
        [sg.Button("Add Kriterii", key='Add_Kriterii')],
        [sg.Button('Add Set', key='Add_Set')],
        [sg.Button('Back', key='Back')],
    ]

    window = sg.Window(constructor_name, constructor_layout, size=(size_x, size_y), finalize=True, icon="..\icon.ico")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            
            break
        elif event == 'Back':
            window.close()
            await create_UI("Main_Menu", menu_name="Main Menu")
        elif event == 'Add_Kriterii':
            #window.close()
            ret = await create_UI("Input_ammount_of_kriterii", add_kriterii_name="Add Kriterii")
            if ret != None:
                window.close()
                await create_UI("Constructor_kriterii", constructor_name="Constructor",ammount_of_kriterii=ret)
        elif event == 'Add_Set':
            window.close()
            await create_UI("Constructor_kriterii_set", constructor_name="Constructor")
    window.close()
async def Constructor_kriterii(constructor_name="Constructor", theme_="",ammount_of_kriterii=1):

    if theme_ == "":
        with open('../Files/theme', 'r',encoding='utf-8') as f:
            read = f.read()
            theme_ = str(read.split("\n")[0].split(":")[-1])

    sg.theme(theme_)

    with open('../Files/Settings', 'r',encoding='utf-8') as f:
        read = f.read()
        size_x = int(read.split("\n")[0].split(":")[-1])
        size_y = int(read.split("\n")[1].split(":")[-1])

    constructor_layout = [[sg.Text("Name"), sg.Input(key='Name',size=(14, 1))]]
    constructor_layout += [[sg.Text(f"Kriterii 1"), sg.Input(key=f'Input_1',size=(7, 1)), sg.Checkbox('not', key=f'Checkbox_1_1', enable_events=True)]]
    if ammount_of_kriterii > 1:
        constructor_layout += [[sg.Text(f"Kriterii {i+1}"), sg.Input(key=f'Input_{i+1}',size=(7, 1)), sg.Checkbox('not', key=f'Checkbox_1_{i+1}', enable_events=True), sg.Checkbox('or', key=f'Checkbox_2_{i+1}', enable_events=True), sg.Checkbox('and', key=f'Checkbox_3_{i+1}', enable_events=True)] for i in range(1,ammount_of_kriterii)]
    constructor_layout += [[sg.Button('process', key='process', enable_events=True)]]
    constructor_layout += [[sg.Button('Back', key='Back', enable_events=True)]]

    window = sg.Window(constructor_name, constructor_layout, size=(size_x, size_y), finalize=True, icon="..\icon.ico")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            
            break
        elif event == 'Back':
            window.close()
            await create_UI("Constructor_main", constructor_name="Constructor")
        elif event == 'process':

            with open('../Files/kriteries', 'r',encoding='utf-8') as f:
                lines = f.readlines()

            nam = values['Name']
            krit = ['if'] * ammount_of_kriterii
            sym = [values[f'Input_{i}'] for i in range(1, ammount_of_kriterii + 1)]
            no = [1 if values[f'Checkbox_1_{i}'] else 0 for i in range(1, ammount_of_kriterii + 1)]
            con = ['or' if values[f'Checkbox_2_{i}'] else 'and' for i in range(2, ammount_of_kriterii + 1)]

            lines[0] = lines[0].strip() + f",,,,{nam}\n"
            lines[1] = lines[1].strip() + f",,,,{krit}\n"
            lines[2] = lines[2].strip() + f",,,,{ammount_of_kriterii}\n"
            lines[3] = lines[3].strip() + f",,,,{sym}\n"
            lines[4] = lines[4].strip() + f",,,,{no}\n"
            lines[5] = lines[5].strip() + f",,,,{con}\n"

            with open('../Files/kriteries', 'w',encoding='utf-8') as f:
                f.writelines(lines)

            window.close()
            await create_UI("Main_Menu", menu_name="Main Menu")




        for i in range(1, ammount_of_kriterii+1):
            if event == f'Checkbox_2_{i}':
                window[f'Checkbox_3_{i}'].update(False)
            elif event == f'Checkbox_3_{i}':
                window[f'Checkbox_2_{i}'].update(False)
async def Constructor_kriterii_set(constructor_name="Constructor", theme_="",ammount_of_kriterii=1):
    if theme_ == "":
        with open('../Files/theme', 'r',encoding='utf-8') as f:
            read = f.read()
            theme_ = str(read.split("\n")[0].split(":")[-1])

    sg.theme(theme_)

    with open('../Files/Settings', 'r',encoding='utf-8') as f:
        read = f.read()
        size_x = int(read.split("\n")[0].split(":")[-1])
        size_y = int(read.split("\n")[1].split(":")[-1])


    with open('../Files/kriteries', 'r',encoding='utf-8') as f:
        Kriterii_list = f.readline().split('::::')[-1].split(',,,,')



    List_List =[]
    layout_left = [
        [sg.Button('Add', key='Add_Kriterii',size = (20, 1)),sg.Combo(Kriterii_list,default_value=Kriterii_list[0], key='Kriterii_list1',size = (24, 10))],
        [sg.Button('Delete', key='Delete_Kriterii',size = (20, 1)),sg.Combo([], key='Kriterii_list2',size = (24, 10))],
        [sg.Button('Save', key='Save_Kriterii',size = (20, 1)),sg.Input(default_text='Set1',key='Kriterii_name',size = (26, 10))],
        [sg.Button('Back', key='Back', enable_events=True)]
    ]
    layout_right = [
        [sg.Listbox(List_List, key='Kriterii_list3', size=(50, 40))],
        ]

    layout = [
        [sg.Column(layout_left, size=(size_x//2, size_y)),
         sg.Column(layout_right, size=(size_x//2, size_y))]
    ]

    window = sg.Window(constructor_name, layout, size=(size_x, size_y), finalize=True, icon="..\icon.ico")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            
            break
        elif event == 'Back':
            window.close()
            await create_UI("Constructor_main", constructor_name="Constructor")
        elif event == 'Add_Kriterii':
            if window['Kriterii_list1'].get() not in List_List:
                List_List.append(window['Kriterii_list1'].get())
                window['Kriterii_list3'].update(values=List_List)
                window['Kriterii_list2'].update(values=List_List,size=(24, 10),value=List_List[0])
        elif event == 'Delete_Kriterii':
            if window['Kriterii_list2'].get() in List_List:
                List_List.remove(window['Kriterii_list2'].get())
                window['Kriterii_list3'].update(values=List_List)
                if List_List:
                    window['Kriterii_list2'].update(values=List_List,size=(24, 10),value=List_List[0])
                else:
                    window['Kriterii_list2'].update(values=List_List,size=(24, 10))
        elif event == 'Save_Kriterii':
            with open('../Files/Kriterii_Sets', 'r',encoding='utf-8') as f:
                lines = f.read()

            if values['Kriterii_name'] not in lines.split('\n')[0].split('::::')[-1].split(',,,,'):
                print(window['Kriterii_list3'].get_list_values())
                lines = lines.split('\n')
                if lines[0] == 'Set_name::::':
                    lines[0] = lines[0]+values['Kriterii_name']
                    lines[1] = lines[1]+f"{window['Kriterii_list3'].get_list_values()}"
                else:
                    lines[0] = lines[0]+',,,,'+values['Kriterii_name']
                    lines[1] = lines[1]+',,,,'+f"{window['Kriterii_list3'].get_list_values()}"
                text = lines[0] + '\n' + lines[1]
                with open('../Files/Kriterii_Sets', 'w',encoding='utf-8') as f:
                    f.writelines(text)






    window.close()
async def Input_ammount_of_kriterii(add_kriterii_name="Add Kriterii", theme_=""):
    if theme_ == "":
        with open('../Files/theme', 'r',encoding='utf-8') as f:
            read = f.read()
            theme_ = str(read.split("\n")[0].split(":")[-1])
    size_x = 300
    size_y = 100
    # with open('../Files/Settings', 'r') as f:
    #     read = f.read()
    #     size_x = int(read.split("\n")[0].split(":")[-1])
    #     size_y = int(read.split("\n")[1].split(":")[-1])



    sg.theme(theme_)
    layout = [
        [sg.Text("Выберите количество критериев")],
        [sg.Checkbox('1', key='1', enable_events=True),
         sg.Checkbox('2', key='2', enable_events=True),
         sg.Checkbox('3', key='3', enable_events=True),
         sg.Checkbox('4', key='4', enable_events=True),
         sg.Checkbox('5', key='5', enable_events=True)],
        [sg.Button('OK', key='OK')],
    ]

    window = sg.Window('Add Kriterii', layout, size=(size_x, size_y), finalize=True, icon="..\icon.ico")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            return None

        elif event == 'OK':
            window.close()
            for i in range(1, 6):
                if values[str(i)]:
                    return i
            return 1
        for i in range(1, 6):
            if values[str(i)]:
                for j in range(1, 6):
                    if i != j:
                        window[str(j)].update(False)
                break
async def Settings_main(settings_name="Settings", theme_=""):
    if theme_ == "":
        with open('../Files/theme', 'r',encoding='utf-8') as f:
            read = f.read()
            theme_ = str(read.split("\n")[0].split(":")[-1])

    sg.theme(theme_)

    with open('../Files/Settings', 'r',encoding='utf-8') as f:
        read = f.read()
        size_x = int(read.split("\n")[0].split(":")[-1])
        size_y = int(read.split("\n")[1].split(":")[-1])

    settings_layout = [
        [sg.Button("Settings_UI", key='Settings_UI')],
        [sg.Button("Settings_music",key='Settings_music')],
        [sg.Button('Back', key='Back')],
    ]

    window = sg.Window(settings_name, settings_layout, size=(size_x, size_y), finalize=True, icon="..\icon.ico")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            
            break
        elif event == 'Back':
            window.close()
            await create_UI("Main_Menu", menu_name="Main Menu")
        elif event == 'Settings_UI':
            window.close()
            await create_UI("Settings_UI", settings_name="Settings_UI")
        elif event == 'Settings_music':
            window.close()
            await create_UI("Settings_music", settings_name="Settings_music")
async def Settings_UI(settings_name="Settings_UI", theme_=""):
    if theme_ == "":
        with open('../Files/theme', 'r',encoding='utf-8') as f:
            read = f.read()
            theme_ = str(read.split("\n")[0].split(":")[-1])

    sg.theme(theme_)

    with open('../Files/Settings', 'r',encoding='utf-8') as f:
        read = f.read()
        size_x = int(read.split("\n")[0].split(":")[-1])
        size_y = int(read.split("\n")[1].split(":")[-1])

    settings_layout = [
        [sg.Button("Theme", key='Theme'), sg.Combo(sg.theme_list(), default_value=theme_, key='-THEME_LIST-')],
        [sg.Button("Size", key='Size'), sg.Text("X"), sg.InputText(f"{size_x}", key='X', size=(5, 1)), sg.Text("Y"), sg.InputText(f"{size_y}", key='Y', size=(5, 1))],
        [sg.Button('Back', key='Back')],
    ]

    settings_window = sg.Window(settings_name, settings_layout, size=(size_x, size_y), finalize=True, icon="..\icon.ico")

    while True:
        event, values = settings_window.read()

        if event == sg.WIN_CLOSED:
            
            break
        elif event == 'Back':
            settings_window.close()
            await create_UI("Settings_main", settings_name="Settings")
        elif event == 'Theme':
            theme_ = values["-THEME_LIST-"]
            with open('../Files/theme', 'r',encoding='utf-8') as f:
                c = f.read()
            with open('../Files/theme', 'w',encoding='utf-8') as f:
                if values["-THEME_LIST-"] in sg.theme_list():
                    f.write(f'standart_theme:{values["-THEME_LIST-"]}')
                    f.close()
                    sg.theme(str(values["-THEME_LIST-"]))
                    settings_window.close()
                    await create_UI("Settings_UI", settings_name="Settings_UI")
                else:
                    f.write(c)
        elif event == 'Size':
            with open('../Files/Settings', 'r',encoding='utf-8') as f:
                c = f.readlines()
            with open('../Files/Settings', 'w',encoding='utf-8') as f:
                f.write(f'size_x:{values["X"]}\n')
                f.write(f'size_y:{values["Y"]}\n')
                f.writelines(c[2:])
                f.close()
                settings_window.close()
                await create_UI("Settings_UI", settings_name="Settings_UI")
async def Settings_music(settings_name="Settings_music", theme_=""):
    if theme_ == "":
        with open('../Files/theme', 'r',encoding='utf-8') as f:
            read = f.read()
            theme_ = str(read.split("\n")[0].split(":")[-1])

    sg.theme(theme_)

    with open('../Files/Settings', 'r',encoding='utf-8') as f:
        read = f.read()
        size_x = int(read.split("\n")[0].split(":")[-1])
        size_y = int(read.split("\n")[1].split(":")[-1])

    with open('../Files/music', 'r',encoding='utf-8') as f:
        vol = int(f.read().split(':')[-1])



    volume_layout = [
        [sg.Text('Volume Control')],
        [sg.Slider(range=(0, 100), default_value=vol, orientation='h', size=(20, 15), key='Volume_Slider',enable_events=True)],

        [sg.Text(f'You can change to next random track', key='Current_Track'),sg.Button('Next Track', key='Next_Track')],
        [sg.Button('Back', key='Back')]
    ]

    volume_window = sg.Window('Volume Control', volume_layout,size=(size_x, size_y), modal=True, icon="..\icon.ico")

    while True:
        vol_event, vol_values = volume_window.read()
        if vol_event == sg.WIN_CLOSED:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            break
        elif vol_event == 'Volume_Slider':
            pygame.mixer.music.set_volume(vol_values['Volume_Slider'] / 100)
            vol = int(vol_values['Volume_Slider'])
        elif vol_event == 'Back':
            with open('../Files/music', 'w',encoding='utf-8') as f:
                f.write(f'Volume:{vol}')
            volume_window.close()
            await create_UI("Settings_main", settings_name="Settings")
        elif vol_event == 'Next_Track':
            music_folder = '../music'
            tracks = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
            if tracks:
                next_track = random.choice(tracks)
                pygame.mixer.music.load(os.path.join(music_folder, next_track))
                pygame.mixer.music.play()
                volume_window['Current_Track'].update(f'You played: {next_track}')


    with open('../Files/music', 'w',encoding='utf-8') as f:
        f.write(f'Volume:{vol}')
    volume_window.close()
async def Workflow_main(workflow_name="Workflow", theme_=""):
    if theme_ == "":
        with open('../Files/theme', 'r',encoding='utf-8') as f:
            read = f.read()
            theme_ = str(read.split("\n")[0].split(":")[-1])

    sg.theme(theme_)

    with open('../Files/Settings', 'r',encoding='utf-8') as f:
        read = f.read()
        size_x = int(read.split("\n")[0].split(":")[-1])
        size_y = int(read.split("\n")[1].split(":")[-1])

    workflow_layout = [
        [sg.Button("Blitz_excel", key='Blitz_excel')],
        [sg.Button("Workwlow_change_delete_nickname", key='Workwlow_change_delete_nickname')],
        [sg.Button('Back', key='Back')],
    ]

    window = sg.Window(workflow_name, workflow_layout, size=(size_x, size_y), finalize=True, icon="..\icon.ico")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            
            break
        elif event == 'Back':
            window.close()
            await create_UI("Main_Menu", menu_name="Main Menu")
        elif event == 'Blitz_excel':
            window.close()
            await create_UI("Workflow_Blitz_excel", workflow_name="Workflow_Blitz_excel")
        elif event == 'Workwlow_change_delete_nickname':
            window.close()
            await create_UI("Workwlow_change_delete_nickname", workflow_name="Workwlow_change_delete_nickname")
async def Workflow_Blitz_excel(workflow_name="Blitz_excel", theme_=""):
    if theme_ == "":
        with open('../Files/theme', 'r',encoding='utf-8') as f:
            read = f.read()
            theme_ = str(read.split("\n")[0].split(":")[-1])

    sg.theme(theme_)

    with open('../Files/Settings', 'r',encoding='utf-8') as f:
        read = f.read()
        size_x = int(read.split("\n")[0].split(":")[-1])
        size_y = int(read.split("\n")[1].split(":")[-1])

    with open('../Files/Types_List', 'r',encoding='utf-8') as f:
        types_list = f.readlines()
    types_list = [i.split("\n")[0] for i in types_list if i.split("\n")[0] != '']

    with open('../Files/Kriterii_Sets', 'r',encoding='utf-8') as f:
        set_list = f.read().split('\n')[0].split("::::")[-1].split(",,,,")



    workflow_layout = [
        [sg.Text("Process type",size=(15, 1))],
        [sg.HorizontalSeparator()],
        [sg.Text('Ники',size=(15, 1)), sg.InputText("C:/Users/ivans/OneDrive/Рабочий стол/Changeble/Ники.txt",key='File_1', size=(40, 1)), sg.FileBrowse('Browse', key='Browse_1', file_types=(("Text Files", "*.txt"),), initial_folder='..'),sg.Combo(types_list, key='Combo_1', default_value=types_list[0]),sg.Checkbox('Process', key='Process_1', enable_events=True)],
        [sg.Text('Лидеры',size=(15, 1)), sg.InputText("C:/Users/ivans/OneDrive/Рабочий стол/Changeble/Лидеры.txt",key='File_2', size=(40, 1)), sg.FileBrowse('Browse', key='Browse_2', file_types=(("Text Files", "*.txt"),), initial_folder='..'),sg.Combo(types_list, key='Combo_2', default_value=types_list[0]),sg.Checkbox('Process', key='Process_2', enable_events=True)],
        [sg.Text('Часто бьют',size=(15, 1)), sg.InputText("C:/Users/ivans/OneDrive/Рабочий стол/Changeble/Солдаты.txt",key='File_3', size=(40, 1)), sg.FileBrowse('Browse', key='Browse_3', file_types=(("Text Files", "*.txt"),), initial_folder='..'),sg.Combo(types_list, key='Combo_3', default_value=types_list[0]),sg.Checkbox('Process', key='Process_3', enable_events=True)],
        [sg.HorizontalSeparator()],
        [sg.Text('Ники(старые)', size=(15, 1)), sg.InputText(key='File_4', size=(40, 1)),sg.FileBrowse('Browse', key='Browse_4', file_types=(("Text Files", "*.txt"),), initial_folder='..'),sg.Combo(types_list, key='Combo_4', default_value=types_list[0]),sg.Checkbox('Remember', key='Remember_1', enable_events=True,default=True)],
        [sg.Text('Лидеры(старые)', size=(15, 1)), sg.InputText(key='File_5', size=(40, 1)),sg.FileBrowse('Browse', key='Browse_5', file_types=(("Text Files", "*.txt"),), initial_folder='..'),sg.Combo(types_list, key='Combo_5', default_value=types_list[0]),sg.Checkbox('Remember', key='Remember_2', enable_events=True,default=True)],
        [sg.Text('Часто бьют(старые)', size=(15, 1)), sg.InputText(key='File_6', size=(40, 1)),sg.FileBrowse('Browse', key='Browse_6', file_types=(("Text Files", "*.txt"),), initial_folder='..'),sg.Combo(types_list, key='Combo_6', default_value=types_list[0]),sg.Checkbox('Remember', key='Remember_3', enable_events=True,default=True)],
        [sg.HorizontalSeparator()],
        [sg.Checkbox("Change", key='Change', enable_events=True,default=True),sg.Checkbox("Add", key='Add', enable_events=True)],
        [sg.HorizontalSeparator()],
        [sg.Button("Select Set", key='Select_Set'),sg.Combo(set_list,default_value=set_list[0], key='Set',size=(100, 10))],
        [sg.HorizontalSeparator()],
        [sg.Button('Back', key='Back',size=(14, 1)), sg.Button('Process', key='Process',size=(35, 1)), sg.Button('Save', key='Save',size=(15, 1))],
    ]
    window = sg.Window(workflow_name, workflow_layout, size=(size_x, size_y), finalize=True, icon="..\icon.ico")
    MAS_RET=[]
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            
            break
        elif event == 'Back':
            window.close()
            await create_UI("Workflow_main", workflow_name="Workflow")
        elif event == 'Change':
            window["Add"].update(False)
        elif event == "Add":
            window["Change"].update(False)
        elif event == 'Process':
            folders = []
            process_types = []
            flg_mas = []
            #folder_1
            if window["Process_1"].get() == True:
                folders.append(window["File_1"].get())
            else:
                folders.append("../Files/Last_nicknames")
            process_types.append(window["Combo_1"].get())
            flg_mas.append(window["Process_1"].get())

            #folder_2
            if window["Process_2"].get() == True:
                folders.append(window["File_2"].get())
            else:
                folders.append("../Files/Last_leaders")
            process_types.append(window["Combo_2"].get())
            flg_mas.append(window["Process_2"].get())

            #folder_3
            if window["Process_3"].get() == True:
                folders.append(window["File_3"].get())
            else:
                folders.append("../Files/Last_most_valuable")
            process_types.append(window["Combo_3"].get())
            flg_mas.append(window["Process_3"].get())

            #folder_4
            if window["Remember_1"].get() == False:
                folders.append(window["File_4"].get())
            else:
                folders.append("../Files/Last_nicknames")
            process_types.append(window["Combo_4"].get())
            flg_mas.append(window["Remember_1"].get())

            #folder_5
            if window["Remember_2"].get() == False:
                folders.append(window["File_5"].get())
            else:
                folders.append("../Files/Last_leaders")
            process_types.append(window["Combo_5"].get())
            flg_mas.append(window["Remember_2"].get())

            #folder_6
            if window["Remember_3"].get() == False:
                folders.append(window["File_6"].get())
            else:
                folders.append("../Files/Last_most_valuable")
            process_types.append(window["Combo_6"].get())
            flg_mas.append(window["Remember_3"].get())

            flg_mas.append(window["Change"].get())

            MAS_RET = await GENERATE_1(folders,process_types,flg_mas)
            print(MAS_RET[0])
            print(MAS_RET[1])
            print(MAS_RET[2])
            print(MAS_RET[3])
            print(MAS_RET[4])
            print(MAS_RET[5])

            sg.popup("FAILI OBRABOTALI!",title="GOOD, VERY GOOD")
        elif event == 'Save':
            path_name = await fast_choose_name_xlsx()
            if path_name != None:
                await EXCEL_1(MAS_RET,window["Set"].get(),path_name)
                print(MAS_RET)
                with open('../Files/Last_nicknames', 'w',encoding='utf-8') as f:
                    for i in MAS_RET[0]:
                        f.write(i + ('\n' if i != MAS_RET[0][-1] else ''))
                with open('../Files/Last_leaders', 'w',encoding='utf-8') as f:
                    for i in MAS_RET[1]:
                        f.write(i + ('\n' if i != MAS_RET[1][-1] else ''))
                with open('../Files/Last_most_valuable', 'w',encoding='utf-8') as f:
                    for i in MAS_RET[2]:
                        f.write(i + ('\n' if i != MAS_RET[2][-1] else ''))
                sg.popup("FAILI SOHRANILI!",title="GOOD, VERY GOOD")
        if window["Change"].get()==False and window["Add"].get()==False:
            window["Change"].update(True)

async def fast_choose_name_xlsx():
    layout = [
        [sg.Input(key='Folder_1', size=(40, 1))],
        [sg.Button('Back', key='Back',size=(14, 1)), sg.Button('Process', key='Process',size=(35, 1))],
    ]
    window = sg.Window('Input Excel name', layout, size=(400, 100), finalize=True, icon="..\icon.ico")
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            return None
        elif event == 'Back':
            window.close()
            return None
        elif event == 'Process':
            window.close()
            return values['Folder_1']
async def Workwlow_change_delete_nickname(workflow_name="Blitz_excel", theme_=""):
    if theme_ == "":
        with open('../Files/theme', 'r',encoding='utf-8') as f:
            read = f.read()
            theme_ = str(read.split("\n")[0].split(":")[-1])

    sg.theme(theme_)

    with open('../Files/Settings', 'r',encoding='utf-8') as f:
        read = f.read()
        size_x = int(read.split("\n")[0].split(":")[-1])
        size_y = int(read.split("\n")[1].split(":")[-1])

    with open('../Files/Last_nicknames', 'r',encoding='utf-8') as f:
        nicknames = f.read().split('\n')


    left_layout = [
        [sg.Button("Change", key='Change'),sg.Input(key='Nickname',size=(10, 1)),sg.Button("Delete", key='Delete'),sg.Combo(values=nicknames, key='Nickname_list',size=(10, 10))],
        [sg.Button('Back', key='Back',size=(14, 1)), sg.Button('Process', key='Process',size=(35, 1))],
        ]
    right_layout = [
        [sg.Listbox([], key='Nicknames_table', size=(40, 20), expand_x=True, expand_y=True)],
        [sg.Button("remove_from_table", key='remove_from_table')]
    ]

    layout = [
        [sg.Column(left_layout, element_justification='c'),sg.Column(right_layout, element_justification='c')]
    ]
    window = sg.Window(workflow_name, layout, size=(size_x,size_y), finalize=True, icon="..\icon.ico")
    mas_del = []
    mas_change = []
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            
            break
        elif event == 'Back':
            window.close()
            await create_UI("Workflow_main", workflow_name="Workflow")
        elif event == 'Change':
            if values["Nickname_list"] and values["Nickname"] and values["Nickname_list"] in nicknames:
                if [values["Nickname_list"], values["Nickname"]] not in mas_change:
                    mas_change.append([values["Nickname_list"], values["Nickname"]])
                    window["Nicknames_table"].update(values=mas_del + mas_change)
            print(mas_change)
            print(mas_del)
        elif event == 'Delete':
            if values["Nickname_list"] and values["Nickname_list"] in nicknames:
                if values["Nickname_list"] not in mas_del:
                    mas_del.append(values["Nickname_list"])
                    window["Nicknames_table"].update(values=mas_del + mas_change)
            print(mas_change)
            print(mas_del)
        elif event == 'remove_from_table':
            if values["Nicknames_table"]:
                selected_item = values["Nicknames_table"][0]
                if selected_item in mas_change:
                    mas_change.remove(selected_item)
                elif selected_item in mas_del:
                    mas_del.remove(selected_item)
                else:
                    sg.popup("Item not found in lists!", title="Error")
            else:
                sg.popup("No item selected from table!", title="Error")
            window["Nicknames_table"].update(values=mas_del + mas_change)
            print(mas_change)
            print(mas_del)
        elif event == 'Process':

            with open('../Files/Last_nicknames', 'r',encoding='utf-8') as f:
                last_nicknames = f.read().split('\n')
            with open('../Files/Last_leaders', 'r',encoding='utf-8') as f:
                last_leaders = f.read().split('\n')
            with open('../Files/Last_most_valuable', 'r',encoding='utf-8') as f:
                last_fighters = f.read().split('\n')

            for i in mas_del:
                if i in last_nicknames:
                    last_nicknames.remove(i)
                if i in last_leaders:
                    last_leaders.remove(i)
                if i in last_fighters:
                    last_fighters.remove(i)
            for i in mas_change:
                if i[0] in last_nicknames:
                    last_nicknames[last_nicknames.index(i[0])] = i[1]
                if i[0] in last_leaders:
                    last_leaders[last_leaders.index(i[0])] = i[1]
                if i[0] in last_fighters:
                    last_fighters[last_fighters.index(i[0])] = i[1]

            with open('../Files/Last_nicknames', 'w',encoding='utf-8') as f:
                f.write('\n'.join(last_nicknames))
            with open('../Files/Last_leaders', 'w',encoding='utf-8') as f:
                f.write('\n'.join(last_leaders))
            with open('../Files/Last_most_valuable', 'w',encoding='utf-8') as f:
                f.write('\n'.join(last_fighters))

            window["Nicknames_table"].update([])
            mas_del=[]
            mas_change=[]

            with open('../Files/Last_nicknames', 'r',encoding='utf-8') as f:
                nicknames = f.read().split('\n')

            window['Nickname_list'].update(values=nicknames,size=(10, 10))

            sg.popup("SDELAL!KRASAVO!",title="Done")

    window.close()
