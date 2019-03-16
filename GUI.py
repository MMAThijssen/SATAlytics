from functools import partial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.backends.tkagg as tkagg
import matplotlib.pyplot as plt
import numpy as np
import os.path
import pandas as pd
import PIL.Image
import PIL.ImageTk
from reportlab_report import make_pdf
import sys
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import tkinter.messagebox
from updated_function import *
import winsound

bgcolor = "white"
fgcolor = "black"
root = Tk()
root.state()
root.configure(background=bgcolor)
#FOR LOGO:
# root.iconbitmap(r"\SATAlytics Support\LogoIco.ico"))

## Create the main window
root.title("SATAlytics")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (screen_width, screen_height / 11 * 10))
label = tkinter.Label(root,text="Welcome to SATAlytics")
label.config(font=("Comic", 20), bg=bgcolor, fg=fgcolor)
label.grid(row=0, column=2, columnspan=8)

root.columnconfigure(0, minsize=round(screen_width / 11))
root.columnconfigure(1, minsize=round(screen_width / 11))
root.columnconfigure(2, minsize=round(screen_width / 12))
root.columnconfigure(3, minsize=round(screen_width / 12))
root.columnconfigure(4, minsize=round(screen_width / 12))
root.columnconfigure(5, minsize=round(screen_width / 12))
root.columnconfigure(6, minsize=round(screen_width / 11))
root.columnconfigure(7, minsize=round(screen_width / 11))
root.columnconfigure(8, minsize=round(screen_width / 11))
root.columnconfigure(9, minsize=round(screen_width / 11))
root.columnconfigure(10, minsize=round(screen_width / 11))
root.rowconfigure(0, minsize=round(screen_height / 14))
root.rowconfigure(1, minsize=round(screen_height / 14))
root.rowconfigure(2, minsize=round(screen_height / 12))
root.rowconfigure(3, minsize=round(screen_height / 11))
root.rowconfigure(4, minsize=round(screen_height / 11))
root.rowconfigure(5, minsize=round(screen_height / 11))
root.rowconfigure(6, minsize=round(screen_height / 11))
root.rowconfigure(7,minsize=round(screen_height / 12))
root.rowconfigure(8, minsize=round(screen_height / 11))
root.rowconfigure(9, minsize=round(screen_height / 12))
root.rowconfigure(10,  minsize=round(screen_height / 14))


# FUNCTIONS OF HELP TO OTHER FUNCTIONS
global most_recent_function
most_recent_function = 0

global counter_to_save_the_day
counter_to_save_the_day = 0

check_excel_1_exist = False

check_excel_2_exist = False

def font_size():
    global fontsize
    try:
        fontsize = int(entryFont.get())
    except:
        fontsize = 20

def on_enter(x):
    L1.configure(text=x)

def colorchange():
    if most_recent_function == 5:
        buttonHide.config(text= "Show Client", bg="blue", fg="white")
        buttonDetails.config(text= "Show Details",bg= bgcolor, fg= fgcolor)
        buttonCut.config(bg = bgcolor, text= "Full Names", fg = fgcolor)        
    elif most_recent_function == 1 or most_recent_function == 6 or most_recent_function ==2:
        buttonDetails.config(text= "Show Details",bg= "blue", fg= "white")
        buttonCut.config(bg = bgcolor, text= "Full names", fg = fgcolor)
        buttonHide.config(text= "Show Client", bg=bgcolor, fg=fgcolor)
    elif most_recent_function == 3:
        buttonCut.config(bg = "blue", text= "Full Names", fg = "white")
        buttonHide.config(text= "Show Client", bg=bgcolor, fg=fgcolor)
        buttonDetails.config(text= "Show Details",bg= bgcolor, fg= fgcolor)
    else:
        buttonHide.config(text= "Show Client", bg=bgcolor, fg=fgcolor)
        buttonDetails.config(text= "Show Details",bg= bgcolor, fg= fgcolor)
        buttonCut.config(bg = bgcolor, text= "Full Names", fg = fgcolor)


def colorchange1():
    button_list = [button1, button2, button3, button4, button5, button6, button7, button8]
    for i in range(len(button_list)):
        if most_recent_function == (i + 1):
            button_i = button_list[i]
    button_i.config(bg="blue", fg="white")
    button_list.remove(button_i)
    for j in range(len(button_list)):
        button_list[j].config(bg=bgcolor, fg=fgcolor)


def change_add_button():
    selection = current_figure.rpartition(".")[0]
    for i in range(len(saved_list)):
        if selection in saved_list[i]:
            addbutton.config(bg="green", text="Saved")
            break
        else:
            addbutton.config(bg="blue", text="Add Item")


def scroll_fun(e):
    """ Adds scrollbars into the listboxes.
    """
    scrollbar_v = Scrollbar(e, orient= "vertical")
    scrollbar_v.config(command= e.yview)
    scrollbar_v.pack(side= "right", fill="y")
    scrollbar_v.pack_propagate(False)
    e.config(yscrollcommand= scrollbar_v.set)

    scrollbar_h = Scrollbar(e, orient = "horizontal")
    scrollbar_h.config(command= e.xview)
    scrollbar_h.pack(side= "bottom", fill= "x")
    scrollbar_h.pack_propagate(False)
    e.config(xscrollcommand= scrollbar_h.set)


def st_listbox(row, column):
    """ Returns standard Listbox.

    row -- int, row to place listbox
    column -- int, column to place listbox
    """
    a = Listbox(root, selectmode=SINGLE, exportselection=0, height=round(screen_height / 11))
    a.grid(row=row, column=column, sticky="nsew")
    ## Adding scrollbar for lb71
    scroll_fun(a)

    return(a)


def pre_proc(excel_file,column_name):  
    """ Returns column with unique values.

    excel_file -- pandas df, dataframe from Excel file
    column_name -- string, name of column
    """
    try:
        specific_column = excel_file[column_name]  # Here we chose the column that we want to choose a value from
        without_nan = specific_column[pd.isna(specific_column) == FALSE] # Here we keep the column without the NaN values
        unique_values = np.unique(without_nan) # Here we keep only the unique values
        return(unique_values)
    except KeyError:
        tkinter.messagebox.showinfo("Missing column", "The column \"{}\" is missing.".format(column_name))

 
def timed_msgbox(msg, top_title="Results", duration=1000):
    """ Display messagebox that closes after specified time.
    
    msg -- string, message to display
    top_title -- string, title of msgbox -default: "Results"
    duration -- integer, number of milliseconds -default: 1000
    """        
    top = Toplevel()
    top.geometry("%dx%d+%d+%d" % (150, 80, 800, 300))
    top.title(top_title)
    Message(top, text=msg, padx=20, pady=20).pack()
    top.after(duration, top.destroy)


def draw_image(fig):
    """ Displays image in canvas.

    fig -- string, figure to display
    """
    img = PIL.Image.open(fig)
    size = round(screen_height / 10.5 * 8)
    img = img.resize((size, size), PIL.Image.ANTIALIAS)
    resized = PIL.ImageTk.PhotoImage(img)
    label = Label(image=resized)
    label.img = resized
    label.grid(row=1,column=5,rowspan=9, columnspan=6, sticky="nwes")
    create_global_curr_fig(fig)


imagelist = []
back_next_counter = -1
def list(item):
    global imagelist
    imagelist.append(item)

def listcounter(x):
    global back_next_counter
    if x == True:
        back_next_counter = back_next_counter - 1
    else:
        back_next_counter = back_next_counter + 1


def create_global_curr_fig(fig):
    """ Creates global of current figure.
    fig -- string, name of figure
    """
    global current_figure
    current_figure = fig


hidecounter = False
def act_hide():
    global hidecounter
    if hidecounter == False:
        hidecounter = True
    else:
        hidecounter = False
    if hidecounter == False:
        buttonHide.config(bg = "blue", text= "Show Client", fg = "white")
    else:
        buttonHide.config(bg = "red", text= "Hide Client")

cutcounter = False
def act_cut():
    global cutcounter
    if cutcounter == False:
        cutcounter = True
    else:
        cutcounter = False
    if cutcounter == False:
        buttonCut.config(bg = "blue", text= "Full names", fg = "white")
    else:
        buttonCut.config(bg = "red", text= "Short Names")


detailscounter = False
def act_details():
    """ Action to display more details/graphs.
    """
    if most_recent_function == 2:    
        img_list = over_threshold(reduced1, reduced2, reduced3, reduced4)
        for img in img_list:
            draw_image(img)
            imagelist.append(img)
            listcounter(False)
        timed_msgbox("Function was executed successfully ({} graphs were drawn)".format(len(img_list)),
                "Created graphs", 1500)
    if most_recent_function == 1:
        img_list = samples_product_type(excel1, client=value11, date=value12, detail=True)
        for img in img_list:
            draw_image(img)
            imagelist.append(img)
            listcounter(False)
        timed_msgbox("Function was executed successfully ({} graphs were drawn)".format(len(img_list)),
                "Created graphs", 1500)
    if most_recent_function == 6:
        img_list = samples_product_type(excel1, client="all", date=value61, detail=True)
        for img in img_list:
            draw_image(img)
            imagelist.append(img)
            listcounter(False)
        timed_msgbox("Function was executed successfully ({} graphs were drawn)".format(len(img_list)),
                "Created graphs", 1500)


def _quit():
    """ Closes the program fully by destroying the images.
    """
    plt.close("all") # closes all images
    for filename in os.listdir():
        if (filename.endswith('.png') and ' font ' in filename) or " results detected " in filename:
            os.remove(filename)
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate



## FUNCTIONS OF EXCEL BUTTONS
        
def ex1_button():
    global filename
    global excel1
    global splitfilename11

    # used_cols = ["ANNO", "Cliente", "Data_Arrivo", "Gruppo_prodotto", 
    #     "dettaglio_prodotto", "Prova", "Risultato", "Risultato", "Limite",
    #     "N_Molecole", "Ris_Lim_perc", "Classi_Ris_Lim_perc", "N_campione"]

    filename = askopenfilename(title="Choose file on Prova") # open selection of files
    buttonex1.config(text = "Wait till I'm done...", bg= "red")
    buttonex1.update_idletasks()
    buttonex1.config(text= "Excel 1 - Prova", bg="green")
    splitfilename11 = filename.rsplit('/', 1)
    excel1 = pd.read_excel(filename, sheet_name=0)
    excel1 = drop_rows(excel1)       
    ## Button to confirm that the program have the file
    buttonshow1 = Button(root, text=splitfilename11[1], bg="blue", fg = "white")
    buttonshow1.grid(row=1, column=1, sticky="ew")
    global check_excel_1_exist
    check_excel_1_exist = True
    
    ## Some pre-process to the excel1 file. It is connected with help functions
    global excel1_specific_column_uniq_Cliente
    excel1_specific_column_uniq_Cliente = pre_proc(excel1,'Cliente')

    global excel1_specific_column_uniq_Gruppo_prodotto
    excel1_specific_column_uniq_Gruppo_prodotto = pre_proc(excel1,'Gruppo_prodotto')

    global excel1_specific_column_uniq_ANNO
    excel1_specific_column_uniq_ANNO = pre_proc(excel1,'ANNO')



def ex2_button():
    global filename2
    global excel2
    global splitfilename2

    # used_cols = ["ANNO", "Cliente", "Gruppo_prodotto", 
        # "N_Molecole", "Analisi_richiesta_EX_NOTE_LAB",
        # "N_campione"]

    filename2 = askopenfilename(title="Choose file on Campione")
    buttonex2.config(text = "Wait till I'm done...", bg= "red")
    buttonex2.update_idletasks()
    buttonex2.config(text="Excel 2 - Campione", bg="green")
    splitfilename2 = filename2.rsplit('/',1)
    excel2 = pd.read_excel(filename2, sheet_name=0)
    excel2 = drop_rows(excel2)
    buttonshow2 = Button(root, text=splitfilename2[1], bg="blue", fg = "white")
    buttonshow2.grid(row=1, column=3, sticky="ew")
    
    global check_excel_2_exist
    check_excel_2_exist = True

    global excel2_specific_column_uniq_ANNO
    excel2_specific_column_uniq_ANNO = pre_proc(excel2,'ANNO')

## FUNCTIONS OF STATISTIC BUTTONS
### actions for button 1
def act_button1():
    global most_recent_function
    most_recent_function = 1
    colorchange()
    colorchange1()

    if check_excel_1_exist == True:
        lb11 = st_listbox(2, 2)

        for i in excel1_specific_column_uniq_Cliente:
            lb11.insert(END, i)

        def cur_selection11(*x):
            global value11
            value11 = (lb11.get(lb11.curselection()))
            on_enter(value11)

            act_lb12()
        lb11.bind("<<ListboxSelect>>", cur_selection11)
    else:
        timed_msgbox("Excel file 1 is missing", top_title="ERROR", duration=1500)

def act_lb12():
    """ Changes selection for Listbox 2 of function 1.
    """    
    lb12 = st_listbox(2, 3)

    adjusted_excel = excel1.loc[excel1["Cliente"] == value11]
    unique_anno = pre_proc(adjusted_excel, "ANNO")
    for y in unique_anno:
        lb12.insert(END, y)
    lb12.insert(END, "all")
    def cur_selection12(*y):
        global value12
        value12 = lb12.get(lb12.curselection())
        on_enter(value12)

    lb12.bind("<<ListboxSelect>>", cur_selection12)

def act_button2():
    """ Action for button 2. Creates first listbox of three.
    """
    global most_recent_function
    most_recent_function = 2
    colorchange()
    colorchange1()

    if check_excel_1_exist == True and check_excel_2_exist == True:

        lb21 = st_listbox(3, 2)
        for i in excel1_specific_column_uniq_Cliente:
            lb21.insert(END, i)

        def cur_selection21(*x):
            global value21
            value21 = (lb21.get(lb21.curselection()))
            on_enter(value21)

            act_lb22()
        lb21.bind("<<ListboxSelect>>", cur_selection21)
    elif check_excel_2_exist == False and check_excel_1_exist == False:
        timed_msgbox("Both excel files are missing", top_title="ERROR", duration=1500)
    elif check_excel_1_exist == False and check_excel_2_exist == True:
        timed_msgbox("Excel file 1 is missing", top_title="ERROR", duration=1500)
    else:
        timed_msgbox("Excel file 2 is missing", top_title="ERROR", duration=1500)
        winsound.Beep("")

def act_lb22():
    """ Changes selection for Listbox 2 of function 2.
    """ 
    lb22 = st_listbox(3, 3)

    adjusted_excel = excel1.loc[excel1["Cliente"] == value21]
    unique_anno = pre_proc(adjusted_excel, "ANNO")
    for y in unique_anno:
        lb22.insert(END, y)
    lb22.insert(END, "all")
    def cur_selection22(*y):
        global value22
        value22 = lb22.get(lb22.curselection())
        on_enter(value22)

    lb22.bind("<<ListboxSelect>>", cur_selection22)



def act_button3():    
    """ Shows listboxes for client, product and year 
    to select from for function 1.  
    """   
    global most_recent_function
    most_recent_function = 3
    colorchange()
    colorchange1()

    if check_excel_1_exist == True:
        lb31 = st_listbox(4, 2)
        # Put the data into the listbox
        for i in excel1_specific_column_uniq_Cliente:
            lb31.insert(END, i)

        def cur_selection31(*x):
            global value31
            value31 = (lb31.get(lb31.curselection()))
            on_enter(value31)

            act_lb32()
        lb31.bind("<<ListboxSelect>>", cur_selection31)
    else:
        timed_msgbox("Excel file 1 is missing", top_title="ERROR", duration=1500)

def act_lb32():
    """ Changes selection for Listbox 2 of function 1.

    """ 
    lb32 = st_listbox(4, 3)

    adjusted_excel = excel1.loc[excel1["Cliente"] == value31]
    unique_gruppo_prodotto = pre_proc(adjusted_excel, "Gruppo_prodotto")
    for y in unique_gruppo_prodotto:
        lb32.insert(END, y)

    def cur_selection32(*y):
        global value32
        value32 = lb32.get(lb32.curselection())
        on_enter(value32)

        act_lb33()
    lb32.bind("<<ListboxSelect>>", cur_selection32)

def act_lb33():
    """ Changes selection for Listbox 3 of function 1.
    """    
    lb33 = st_listbox(4, 4)
    adjusted_excel = excel1.loc[(excel1["Cliente"] == value31) & (excel1["Gruppo_prodotto"] == value32)]
    unique_anno = pre_proc(adjusted_excel, "ANNO")
    for z in excel1_specific_column_uniq_ANNO:
        lb33.insert(END, z)
    lb33.insert(END, "all")

    def cur_selection33(*z):
        global value33
        value33 = (lb33.get(lb33.curselection()))
        on_enter(value33)

    lb33.bind("<<ListboxSelect>>", cur_selection33)


def act_button4():
    """ Action for button 4. Creates first listbox.
    """
    global most_recent_function
    most_recent_function = 4
    colorchange()
    colorchange1()

    if check_excel_2_exist == True:
        lb41 = st_listbox(5, 2)

        for i in excel2_specific_column_uniq_ANNO:
            lb41.insert(END, i)

        def cur_selection41(*x):
            global value41
            value41 = (lb41.get(lb41.curselection()))
            on_enter(value41)

        lb41.bind("<<ListboxSelect>>", cur_selection41)
    else:
        timed_msgbox("Excel file 2 is missing", top_title="ERROR", duration=1500)
    
def act_button5():
    """ Shows listboxes for product, compound and year 
    to select from for function 2.  
    """
    global most_recent_function
    most_recent_function = 5
    colorchange()
    colorchange1()

    if check_excel_1_exist == True and check_excel_2_exist == True:
    # create Listbox
        lb51 = st_listbox(6, 2)

        for i in excel1_specific_column_uniq_Gruppo_prodotto:
            lb51.insert(END, i)

        def cur_selection51(*x):
            global value51
            value51 = lb51.get(lb51.curselection())
            on_enter(value51)

            act_lb52()
        lb51.bind("<<ListboxSelect>>", cur_selection51)
    elif check_excel_2_exist == False and check_excel_1_exist == False:
        timed_msgbox("Both excel files are missing", top_title="ERROR", duration=1500)
    elif check_excel_1_exist == False and check_excel_2_exist == True:
        timed_msgbox("Excel file 1 is missing", top_title="ERROR", duration=1500)
    else:
        timed_msgbox("Excel file 2 is missing", top_title="ERROR", duration=1500)
        winsound.Beep("")


def act_lb52():
    """ Changes selection for Listbox 2 of function 5.
    """ 
    # create Listbox 
    lb52 = st_listbox(6, 3)

    adjusted_excel = excel1.loc[excel1["Gruppo_prodotto"] == value51]
    unique_prova = pre_proc(adjusted_excel, "Prova")
    for y in unique_prova:
        lb52.insert(END, y)

    def cur_selection52(*y):
        global value52
        value52 = lb52.get(lb52.curselection())
        on_enter(value52)

        act_lb53()
    lb52.bind("<<ListboxSelect>>", cur_selection52)

def act_lb53():
    """ Changes selection for Listbox 3 of function 5.
    """    
    lb53 = st_listbox(6, 4)
    adjusted_excel = excel1.loc[(excel1["Gruppo_prodotto"] == value51) & (excel1["Prova"] == value52)]
    unique_anno = pre_proc(adjusted_excel, "ANNO")
    for z in unique_anno:
        lb53.insert(END, z)
    lb53.insert(END, "all")

    def cur_selection53(*z):
        global value53
        value53 = (lb53.get(lb53.curselection()))
        on_enter(value53)
    lb53.bind("<<ListboxSelect>>", cur_selection53)

def act_button6():
    global most_recent_function
    most_recent_function = 6
    colorchange()
    colorchange1()

    if check_excel_1_exist == True:
        lb61 = st_listbox(7, 2)

        for i in excel1_specific_column_uniq_ANNO:
            lb61.insert(END, i)

        def cur_selection61(*x):
            global value61
            value61 = (lb61.get(lb61.curselection()))
            on_enter(value61)

        lb61.bind("<<ListboxSelect>>", cur_selection61)
    else:
        timed_msgbox("Excel file 1 is missing", top_title="ERROR", duration=1500)


def act_button7():
    """ Shows listboxes for product, client and year 
    to select from for function 3.  
    """
    global most_recent_function
    most_recent_function = 7
    colorchange()
    colorchange1()

    if check_excel_1_exist == True and check_excel_2_exist == True:
        lb71 = st_listbox(8, 2)

        for i in excel1_specific_column_uniq_Gruppo_prodotto:
            lb71.insert(END, i)
        a = lb71.curselection()

        def cur_selection71(*x):
            global value71
            value71 = (lb71.get(lb71.curselection()))
            on_enter(value71)

            act_lb72()
        lb71.bind("<<ListboxSelect>>", cur_selection71)
    elif check_excel_2_exist == False and check_excel_1_exist == False:
        timed_msgbox("Both excel files are missing", top_title="ERROR", duration=1500)
    elif check_excel_1_exist == False and check_excel_2_exist == True:
        timed_msgbox("Excel file 1 is missing", top_title="ERROR", duration=1500)
    else:
        timed_msgbox("Excel file 2 is missing", top_title="ERROR", duration=1500)
        winsound.Beep("")


def act_lb72():
    """ Changes selection for Listbox 2 of function 7.

    """    
    lb72 = st_listbox(8, 3)

    adjusted_excel = excel1.loc[excel1["Gruppo_prodotto"] == value71]
    unique_cliente = pre_proc(adjusted_excel, "Cliente")
    for y in unique_cliente:
        lb72.insert(END, y)

    def cur_selection72(*y):
        global value72
        value72 = lb72.get(lb72.curselection())
        on_enter(value72)

        act_lb73()
    lb72.bind("<<ListboxSelect>>", cur_selection72)

def act_lb73():
    """ Changes selection for Listbox 3 of function 7.
    """        
    lb73 = st_listbox(8, 4)
    
    adjusted_excel = excel1.loc[(excel1["Gruppo_prodotto"] == value71) & (excel1["Cliente"] == value72)]
    unique_prova = pre_proc(adjusted_excel, "Prova")
    for z in unique_prova:
        lb73.insert(END, z)

    def cur_selection73(*z):
        global value73
        value73 = (lb73.get(lb73.curselection()))
        on_enter(value73)

    lb73.bind("<<ListboxSelect>>", cur_selection73)    

def act_button8():
    global most_recent_function
    most_recent_function = 8
    colorchange()
    colorchange1()

    if check_excel_1_exist == True and check_excel_2_exist == True:
        lb81 = st_listbox(9, 2)

        for i in excel1_specific_column_uniq_ANNO:
            lb81.insert(END, i)

        def cur_selection81(*x):
            global value81
            value81 = (lb81.get(lb81.curselection()))
            on_enter(value81)

        lb81.bind("<<ListboxSelect>>", cur_selection81)
    elif check_excel_2_exist == False and check_excel_1_exist == False:
        timed_msgbox("Both excel files are missing", top_title="ERROR", duration=1500)
    elif check_excel_1_exist == False and check_excel_2_exist == True:
        timed_msgbox("Excel file 1 is missing", top_title="ERROR", duration=1500)
    else:
        timed_msgbox("Excel file 2 is missing", top_title="ERROR", duration=1500)
        winsound.Beep("") 

## FUNCTIONS OF SUPPORT BUTTONS
    
def act_download():
    """ Downloads PDF report. 

    saved_list -- list of tuples [(title, functions)]
    """
    try:
        if 'saved_list' not in globals() or saved_list == []:
             tkinter.messagebox.showinfo("ERROR", "No graphs were added to the report.") 
             return(None)
        make_pdf(saved_list)
    except:
        tkinter.messagebox.showinfo("Download report",
                "Unable to download report.")
        play = lambda: PlaySound("Error_sound.wmv", SND_FILENAME)
 
    
def act_go():
    buttonGo.config(text = "Wait till I'm done...", bg= "red")
    buttonGo.update_idletasks()
    if most_recent_function == 0:
        tkinter.messagebox.showinfo("ERROR","Pick a function first.")
    elif most_recent_function == 3:
        font_size()
        try:
            img_list = residues_graph(excel1, value31, value32, value33, hide=cutcounter, fsize=fontsize)
            buttonGo.config(text= "GO!", bg="blue")
        except NameError:
            timed_msgbox("A value is missing. Choose a client, product and year.", "Value missing", 1500)
    elif most_recent_function == 5:
        font_size()
        try:
            img_list = compound_per_client(excel1, excel2, compound=value52, crop=value51, date = value53, hide=hidecounter, fsize=fontsize)
            buttonGo.config(text= "GO!", bg="blue")
        except NameError:
            timed_msgbox("A value is missing. Choose a compound, product and year.", "Value missing", 1500)
    elif most_recent_function == 7:
        font_size()
        try:
            # print("Button 7 is residues_graph_esp")
            img_list = residues_graph_esp(excel1, excel2, client=value72, crop = value71, compound= value73, fsize=fontsize)
            buttonGo.config(text= "GO!", bg="blue")
        except NameError:
            timed_msgbox("A value is missing. Choose a client, product and compound.", "Value missing", 1500)
    elif most_recent_function == 4:
        font_size()
        try:
            img_list = number_of_molecules(excel2, date=value41, fsize=fontsize)
            buttonGo.config(text= "GO!", bg="blue")
        except NameError:
            timed_msgbox("A value is missing. Choose a year.", "Value missing", 1500)
    elif most_recent_function == 6:
        font_size()
        try:
            img_list = samples_product_type(excel1, client="all", date=value61, detail=False, fsize=fontsize)
            buttonGo.config(text= "GO!", bg="blue")
        except NameError:
            timed_msgbox("A value is missing. Choose a client and a year.", "Value missing", 1500)
    elif most_recent_function == 1:
        font_size()
        try:
            img_list = samples_product_type(excel1, client=value11, date=value12, detail=False, fsize=fontsize)
            buttonGo.config(text= "GO!", bg="blue")
        except NameError:
            timed_msgbox("A value is missing. Choose a client and a year.", "Value missing", 1500)
    elif most_recent_function == 2:
        font_size()
        try:
            global reduced1
            global reduced2
            global reduced3
            global reduced4
            img_list, reduced1, reduced2, reduced3, reduced4 = threshold_pie(excel1, excel2, date = value22, client=value21, detail=True, fsize=fontsize)
            buttonGo.config(text= "GO!", bg="blue")
        except NameError:
            timed_msgbox("A value is missing. Choose a year and a client.", "Value missing", 1500)
        except ValueError:
            img_list = threshold_pie(excel1, excel2, date = value22, client=value21, detail=False)
            buttonGo.config(text= "GO!", bg="blue")
    elif most_recent_function == 8:
        font_size()
        try:
            img_list = clients_graph(excel1, excel2, date=value81, fsize=fontsize)
            buttonGo.config(text= "GO!", bg="blue")
        except NameError:
            timed_msgbox("A value is missing. Choose a year.", "Value missing", 1500)
    else:
        tkinter.messagebox.showinfo("Error","Pick a function first.")    

    for img in img_list:
        draw_image(img)
        imagelist.append(img)
        listcounter(False)
    timed_msgbox("Function was executed successfully. {} results were produced. Use previous button to see all results.".format(len(img_list)),
            "Executed function", 2000)
    change_add_button()


def act_add():
    selection = current_figure.rpartition(".")[0]

    if most_recent_function == 5 and hidecounter == False:
        result = tkinter.messagebox.askquestion("WARNING", "This information is confidential. Are you sure you want to add it?", icon="warning")
        if result == "no":
            return(None)

    if not 'saved_list' in globals():
        global saved_list
        saved_list = [(selection, current_figure)]
    else:
        saved_list += [(selection, current_figure)]
    timed_msgbox("\"{}\" is added to the report.".format(selection), "Added figure to report")
    change_add_button() #gives NameError first time because global saved_list does not exist yet


def act_resetreport():
    result = tkinter.messagebox.askquestion("WARNING", "Are you sure you want to reset the summary?", icon="warning")
    if result == "no":
        return(None)
    global saved_list
    saved_list = []
    addbutton.config(bg="blue", text="Add Item")


def backbutton():
    if back_next_counter >= 1:
        draw_image(imagelist[back_next_counter - 1])
        listcounter(True)
    else:
        draw_image(imagelist[back_next_counter])
        timed_msgbox("No more graphs", "ERROR")
    change_add_button()


def forwardbutton():
    try:
        draw_image(imagelist[back_next_counter + 1])
        listcounter(False)
    except IndexError:
        draw_image(imagelist[back_next_counter])
        timed_msgbox("No more graphs", "ERROR")
    change_add_button()


def openInstrucktion():
    os.startfile("Manual.pdf")




## CREATE BUTTONS CODE

button1 = Button(root,text="1. Pie chart on total number of samples \n per product for one client", command=act_button1, bg=bgcolor, fg=fgcolor)
button1.grid(row=2, column=0, columnspan=2, sticky="nsew")

button2 = Button(root,text="2. Pie chart of samples by one client categorised \ninto groups based on their concentration\n relative to their threshold for one year", command=act_button2, bg=bgcolor, fg=fgcolor)
button2.grid(row=3, column=0, columnspan=2, sticky="nsew")

button3 = Button(root,text="3. Average concentrations of all compounds \n found in one product from one client \n in a certain time span", command=act_button3, bg=bgcolor, fg=fgcolor)
button3.grid(row=4, column=0, columnspan=2, sticky="nsew")

button4 = Button(root,text="4. Bar chart on average type of analysis of \n researched compounds for all clients \n in one year", command = act_button4, bg=bgcolor, fg=fgcolor)
button4.grid(row=5, column=0, columnspan=2, sticky="nsew")

button5 = Button(root,text="5. Average concentration of one compound \n found in one product \n by clients in a certain time span", command=act_button5, bg=bgcolor, fg=fgcolor)
button5.grid(row=6, column=0, columnspan=2, sticky="nsew")

button6 = Button(root,text="6. Pie chart of total number of samples \n per product for all SATA clients", command=act_button6, bg=bgcolor, fg=fgcolor) #command= lambda: [f() for f in [selection61, selection62]])
button6.grid(row=7, column=0, columnspan=2, sticky="nsew")

button7 = Button(root,text="7. Distribution of a certain compound \n throughout the years for one client \n and one product", command=act_button7, bg=bgcolor, fg=fgcolor)
button7.grid(row=8, column=0, columnspan=2, sticky="nsew")

button8 = Button(root,text="8. Pie chart on occurence of clients \n exceeding the limit per year", command=act_button8, bg=bgcolor, fg=fgcolor)
button8.grid(row=9, column=0, columnspan=2, sticky="nsew")

buttonDownload = Button(root, text="Download Summary", bg="blue", command=act_download, fg="white")
buttonDownload.grid(row=10, column=0, columnspan=2, sticky="nsew")

buttonResetReport = Button(root, text="Reset Summary", bg="red", command=act_resetreport, fg="white")
buttonResetReport.grid(row=10, column=2, sticky="ew")

buttonGo = Button(root, text="GO!", bg="blue", command= act_go, fg="white")
buttonGo.grid(row=10, column=4, sticky="nsew")

backbutton = Button(root, text= "Previous Screen", command = backbutton, bg="grey", fg=fgcolor)
backbutton.grid(row=10, column=5, sticky="ewsn")

forwardbutton = Button(root, text= "Next Screen", command = forwardbutton, bg="grey", fg=fgcolor)
forwardbutton.grid(row=10, column=6, sticky="ewsn")

buttonCut = Button(root, text="Full Names", bg=bgcolor, command=act_cut, fg=fgcolor)
buttonCut.grid(row=10, column=7, sticky="ew")

buttonDetails = Button(root, text="Show Details", bg=bgcolor, command= act_details, fg=fgcolor)
buttonDetails.grid(row=10, column=8, sticky="ew")

buttonHide = Button(root, text="Show Client", bg=bgcolor, command= act_hide, fg=fgcolor)
buttonHide.grid(row=10, column=9, sticky="ew")

addbutton = Button(root, text="Add Item", bg="blue", command=act_add, fg="white")
addbutton.grid(row=10, column=10, sticky="ewsn")

labelFont = Label(root, text="Font size:", bg=bgcolor)
labelFont.grid(row=0, column=7, sticky="e")
entryFont = Entry(root)
entryFont.grid(row=0, column=8, sticky="ew")

buttonex1 = Button(root, text="Excel 1 - Prova", command=ex1_button, bg="green", fg="white")
buttonex1.grid(row=1, column=0, sticky="ew")

buttonex2 = Button(root, text="Excel 2 - Campione", command=ex2_button, bg="green", fg="white")
buttonex2.grid(row=1, column=2, sticky="ew")

canvas = Canvas(root, bg=bgcolor)
canvas.grid(row=1,column=5,rowspan=9,columnspan=6, sticky="nwes")

buttoninfo = Button(root, text="INFO", command=openInstrucktion, bg="blue", fg="white")
buttoninfo.grid(row=0, column=9, sticky="ew")

L1 = Label(root,text="", bg=bgcolor)
L1.grid(row=0,column=0, columnspan=3, sticky='ew')

quit = Button(root, text="Quit", command=_quit, bg="red", fg=fgcolor)
quit.grid(row=0, column=10, sticky="ew")

root.mainloop()


