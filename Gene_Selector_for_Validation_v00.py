# ---------------------------------------------
# Program: GeneSelectorForValidation-main.py
# Author: Márcio Wilson Dias de Brito
# ---------------------------------------------
# Description: 
# This program selects reference genes for RT-qPCR analysis.
# Reference genes are crucial for normalization in gene expression studies.
# The selected genes are important for accurate and reliable quantification.
# ---------------------------------------------



###         IMPORTS          ###
# Importing necessary libraries for GeneReferenceSelector.py
import numpy as np
import os
import pandas as pd
import time
import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk
from tkinter.filedialog import asksaveasfile
from pandastable import Table


### DEFINING FUNCTIONS      ###

class ToolTip(object): # Class to create the help message in the filters 

    def __init__(self, widget):
        # Constructor method to initialize the ToolTip object.
        # Takes a widget as a parameter.
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        # Display text in the tooltip window.
        # Takes the text to be displayed as a parameter.
        self.text = text
        if self.tipwindow or not self.text:
            return
        # Get the coordinates and dimensions of the text insertion point
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27

        # Create and configure the tooltip window
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        # Hide and destroy the tooltip window.
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

# Function to create a ToolTip for a given widget
def CreateToolTip(widget, text): # Function to create the help message in the filters
    
    # Create a ToolTip object for the specified widget
    toolTip = ToolTip(widget)
    
    # Event handler for mouse entering the widget
    def enter(event):
        toolTip.showtip(text)
    
    # Event handler for mouse leaving the widget
    def leave(event):
        toolTip.hidetip()
    
    # Bind the enter and leave events to the respective event handlers
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

total = None

def add_file(): # select file
    # Function to select and add files to the listbox

    # Open a file dialog to select multiple files with specified file types
    for file in filedialog.askopenfiles(filetypes= [
        ("All files", '*.*'),
        ('Excel file', '*.xlsx; *.xls'), 
        ('Salmon', '.sf'),
        ('csv file', '*.csv'), 
        ('Text Document', '*.txt')
        ]):
        selected.append(file)

    # Insert the names of selected files into the listbox   
    listbox.insert(END, *[file.name for file in selected])

    # Update the global variable 'total' with the count of selected files
    global total
    total = len(selected)
    #print.config(text = "\n".join((file.name for file in selected)))

    # configuring scrollbar for the listbox
    listbox.config(yscrollcommand=scrollbar_V.set, xscrollcommand=scrollbar_H.set)
   
    # Configure vertical and horizontal scrollbars
    scrollbar_V.config(command=listbox.yview)
    scrollbar_H.config(command=listbox.xview)

def remove_file(): # Function to remove mistakenly added files from the listbox and 'selected' list
    # Get the indices of the selected checkboxes in the listbox
    selected_checkboxs = listbox.curselection()
    
    # Iterate through the selected checkboxes in reverse order to avoid index issues
    for selected_checkbox in selected_checkboxs[::-1]:
        # Delete the selected file from the listbox
        listbox.delete(selected_checkbox)
        # Remove the corresponding file from the 'selected' list
        selected.pop(selected_checkbox)
    # Return the updated 'selected' list after removal
    return selected

def help_(): # Function to open the help window
    # Create a new Toplevel window for help
    page_help = tk.Toplevel(root)
    page_help.title('Help')  # Set window title

    # Set window icon   
    page_help.iconbitmap('image\help.ico')

    # Get screen dimensions
    screen_width = page_help.winfo_screenwidth()
    screen_height = page_help.winfo_screenheight()

    # Set window size
    width = 800
    height = 200

    # Set window position
    posx = screen_width / 2 - width / 2
    posy = screen_height / 2 - height / 2

    # Define window geometry
    page_help.geometry("%dx%d+%d+%d" % (width, height, posx, posy))

    # Make the window non-resizable
    page_help.resizable(False, False)

    # Create labels for the title and help text
    title_help = Label(page_help, text='Instructions for using the software', font='Arial 16 bold')
    helper_text = Label(page_help, text='''This program aims to assist in the selection of a reference gene for the validation of the TPM values ​​of your transcriptome.

This software accepts 3 types of files as input:

1 - Table files with .csv extension

2 - A single table relating the genes with the TPM values ​​of each library (.xls and .xlsx).

3 - A specific model file such as the Salmon software (.sf).''')

    title_help.pack()
    helper_text.pack()

def about_menu(): # Function to open the 'About' window

    # Create a new Toplevel window for the 'About' page
    about_page = tk.Toplevel(root)
    about_page.title('About')  # choosing title

    # Set window icon
    about_page.iconbitmap('image\icone.ico')

    # Get screen dimensions
    screen_width = about_page.winfo_screenwidth()
    screen_height = about_page.winfo_screenheight()

    # Set window size
    width = 700
    height = 150

    # Set window position
    posx = screen_width / 2 - width / 2
    posy = screen_height / 2 - height / 2

    # Make the window non-resizable
    about_page.geometry("%dx%d+%d+%d" % (width, height, posx, posy))

    about_page.resizable(False, False)

    # Create labels for the title and about text
    title_about = Label(about_page, text='About', font='Arial 16 bold')
    text_about = Label(about_page, text='''
    This software was developed by Márcio Wilson Dias de Brito, during his graduation in 
    Biological Sciences with Qualification in Biotechnology at the Federal Institute of Rio de Janeiro (IFRJ).
    The student carried out the project with the guidance of Professor Dr. Rafael Mesquita (Bioinformatics Laboratory - IQ - UFRJ)
    and the co-orientation of Dr. Maria Beatriz Mota at RioGen Startup.''')

    title_about.pack()
    text_about.pack()

def screen_filter(): # Function to open the filter window
    
    # Create a new Toplevel window for the filter screen
    screen_filters = tk.Toplevel(root)
    screen_filters.title('Filters')  # Set window title
    screen_filters.iconbitmap('image/filter.ico')  # Set window icon

    # Get screen dimensions
    screen_width = screen_filters.winfo_screenwidth()
    screen_height = screen_filters.winfo_screenheight()

    # Set window size
    width = 230
    height = 140

    # Set window position
    posx = screen_width / 2 - width / 2
    posy = screen_height / 2 - height / 2

    # Define window geometry
    screen_filters.geometry("%dx%d+%d+%d" % (width, height, posx, posy))
    screen_filters.resizable(False, False)

    # Define filter frames
    frame_filter = Frame(screen_filters, highlightbackground="black",
                         highlightthickness=1,
                         bd=5
                         )
    frame_filterII = Frame(frame_filter,
                           highlightbackground="black",
                           highlightthickness=0,
                           #bd=5
                           )
    frame_filter3 = Frame(frame_filter,
                          highlightbackground="black",
                          highlightthickness=0,
                          #bd=5
                          )
    
    ###----DEFINING FILTER VARIABLES for stable genes----###
    label_filter1 = Label(frame_filterII, text='Stable Genes')

    ###----first filter button----###
    label_fI = Label(frame_filterII, text='Filter I')
    text_fI = Label(frame_filterII, text='0')

    ###----second filter button----###
    label_fII = Label(frame_filterII, text='Filter II')
    text_fII = Entry(frame_filterII, justify=CENTER, width=10)

    ###----third filter button----###
    label_fIII = Label(frame_filterII, text='Filter III')
    text_fIII = Entry(frame_filterII, justify=CENTER, width=10)

    ###----fourth filter button----###
    label_fIV = Label(frame_filterII, text='Filter IV')
    text_fIV = Entry(frame_filterII, justify=CENTER, width=10)

    ###----fifth filter button----###
    label_fV = Label(frame_filterII, text='Filter V')
    text_fV = Entry(frame_filterII, justify=CENTER, width=10)

    ###----DEFINITION OF VARIABLES OF DIFFERENTIALLY EXPRESSED----###
    label_filter2 = Label(frame_filter3, text='Variable Expression:')
    
    ###----first filter button----###
    label_f1 = Label(frame_filter3, text='Filter I')
    text_f1 = Label(frame_filter3, text='0', )

    ###----second filter button----###
    label_f2 = Label(frame_filter3, text='Filter II')
    text_f2 = Entry(frame_filter3, justify=CENTER, width=10, highlightcolor="red")

    ###----third filter button----###
    label_f3 = Label(frame_filter3, text='Filter III')
    text_f3 = Entry(frame_filter3, justify=CENTER, width=10)

    # Setting default value
    text_fII.insert(0, filtersI[1])
    text_fIII.insert(0, filtersI[2])
    text_fIV.insert(0, filtersI[3])
    text_fV.insert(0, filtersI[4])
    text_f2.insert(0, filtersII[1])
    text_f3.insert(0, filtersII[2])

    # .pack of filters
    frame_filter.pack(anchor=NW, pady=0)
    frame_filterII.grid(row=0, column=0)

    label_filter1.grid(row=0, column=1, columnspan=2)

    label_fI.grid(row=1, column=1)
    text_fI.grid(row=1, column=2)

    label_fII.grid(row=2, column=1)
    text_fII.grid(row=2, column=2)

    label_fIII.grid(row=3, column=1)
    text_fIII.grid(row=3, column=2)

    label_fIV.grid(row=4, column=1)
    text_fIV.grid(row=4, column=2)

    label_fV.grid(row=5, column=1)
    text_fV.grid(row=5, column=2)

    frame_filter3.grid(row=0, column=2, sticky=N)

    label_filter2.grid(row=0, column=1, columnspan=2)

    label_f1.grid(row=1, column=1)
    text_f1.grid(row=1, column=2)

    label_f2.grid(row=2, column=1)
    text_f2.grid(row=2, column=2)

    label_f3.grid(row=3, column=1)
    text_f3.grid(row=3, column=2)

    
    
    def send_filter():
        # Function to send filter values to the main program
        filtersI[1] = int(text_fII.get())
        filtersI[2] = int(text_fIII.get())
        filtersI[3] = int(text_fIV.get())
        filtersI[4] = float(text_fV.get())

        filtersII[1] = int(text_f2.get())
        filtersII[2] = int(text_f3.get())

        print(filtersI, filtersII)

    button = Button(frame_filter3, text='Apply', command=send_filter)
    button.grid(row=6, column=1, columnspan=2)

    ###---- DEFINING HELP POP-UPS ----###
    CreateToolTip(label_fI, text='Filter I\n'
                                 'To guarantee expression in all tissue types or developmental stages (TPM>0)')
    CreateToolTip(label_fII, text='Filter II\n'
                                  'To select low variance over conditions \n'
                                  'by requiring standard-deviation [log2(TPM)] < 1 [Suggested value]')
    CreateToolTip(label_fIII, text='Filter III\n'
                                   'To avoid exceptional expression in any single condition\n'
                                   'by requiring no log2(TPM) differed from the mean log2(TPM) by two or more; [Suggested value]')
    CreateToolTip(label_fIV, text='Filter IV\n'
                                  'To select medium to high expression level\n'
                                  'by requiring mean [log2(TPM)] > 5. [Suggested value]')
    CreateToolTip(label_fV, text='Filter V\n'
                                 'To avoid high coefficient of variation (CV = stdev/mean).\n'
                                 'values are always less than 0.2. [Suggested value]')
    CreateToolTip(label_f1, text='Filter I\n'
                                 'To guarantee expression in all conditions (TPM>0)')
    CreateToolTip(label_f2, text='Filter II\n'
                                 'To avoid high variance between libraries\n'
                                 'by requiring standard-deviation [log2(TPM)] > 1 [Suggested value]')

    CreateToolTip(label_f3, text='Filter III\n'
                                 'To guarantee high expression level defined by mean log2(TPM)>5 [Suggested value]\n'
                                 'in at least one biological condition.')

genes = "Genes"   # Default name for the gene column
tpm = "TPM"       # Default name for the TPM values column
replica = 1        # Default number of replicas
type = 0           # Default input type (0 to 2)
separator = ';'    # Default separator used in the data (e.g., CSV, TSV)


def file_template():   # Function to open the file window

    # Create a new Toplevel window for the file screen
    screen_files = tk.Toplevel(root)
    screen_files.title('Files')  # Set window title
    screen_files.iconbitmap('image/file.ico')  # Set window icon

    # Get screen dimensions
    screen_width = screen_files.winfo_screenwidth()
    screen_height = screen_files.winfo_screenheight()

    # Set window size
    width = 340
    height = 170

    # Set window position
    posx = screen_width / 2 - width / 2
    posy = screen_height / 2 - height / 2

    # Define window geometry
    screen_files.geometry("%dx%d+%d+%d" % (width, height, posx, posy))
    screen_files.resizable(False, False)

    # Define file frames
    frame_file = Frame(screen_files, highlightbackground="black",
                         highlightthickness=1,
                         bd=5
                         )
    frame_fileII = Frame(frame_file,
                           highlightbackground="black",
                           highlightthickness=0,
                           #bd=5
                           )
    frame_file3 = Frame(frame_file,
                          highlightbackground="black",
                          highlightthickness=0,
                          #bd=5
                          )
    
    # Define labels and entry widgets for file properties
    page_type[1] = Label(frame_file3, text='Gene column name:')
    page_type2 = Entry(frame_file3, justify=CENTER, width=10)
    page_type[3] = Label(frame_file3, text='TPM column name:')
    page_type4 = Entry(frame_file3, justify=CENTER, width=10)
    page_type[5] = Label(frame_file3, text='How many replicas?')
    page_type6 = Entry(frame_file3, justify=CENTER, width=10)
    page_type[7] = Label(frame_file3, text="Separator character:")
    page_type8 = Entry(frame_file3, justify=CENTER, width=10)
    
    # Initialize a global variable 'type' as IntVar
    global type
    type = IntVar()

    # Define radio buttons for selecting file type
    file_type1 = Radiobutton(frame_fileII, 
                             text="Text\nfiles(.csv)", 
                             variable=type, 
                             value=1, 
                             indicatoron=0, 
                             command=lambda:[page_type8.grid(), page_type6.grid_remove(), page_type4.grid_remove(), page_type2.grid()])
    file_type2 = Radiobutton(frame_fileII, 
                             text="Single file with \nall libraries (.xls, .xlsx)", 
                             variable=type, 
                             value=2, 
                             indicatoron=0, 
                             command= lambda:[page_type8.grid_remove(), page_type6.grid_remove(), page_type4.grid_remove(), page_type2.grid()]
                            )
    file_type3 = Radiobutton(frame_fileII, 
                             text="Each library in  one\nfile (Ex: Salmon[.sf])", 
                             variable=type, 
                             value=3, 
                             indicatoron=0, 
                             command= lambda:[page_type8.grid_remove(), page_type6.grid(), page_type4.grid(), page_type2.grid()])

    # Pack file frames
    frame_file.pack(anchor=N, pady=0)
    frame_fileII.grid(row=1, column=1)
    frame_file3.grid(row=2, column=1)
    
    # Pack radio buttons and file properties
    file_type1.grid(row=0, column=1, padx=(10,0))
    file_type2.grid(row=0, column=2, padx=(10,0))
    file_type3.grid(row=0, column=3,padx=(10,0))
    page_type[7].grid(row=6, column=1)
    page_type8.grid(row=6, column=3, columnspan=2)
    page_type[1].grid(row=3, column=1, columnspan=2)
    page_type2.grid(row=3, column=3)
    page_type[3].grid(row=4, column=1, columnspan=2)
    page_type4.grid(row=4, column=3)
    page_type[5].grid(row=5, column=1, columnspan=2)
    page_type6.grid(row=5, column=3)

    # Set default values for file properties
    page_type2.insert(0, genes)
    page_type4.insert(0, tpm)
    page_type6.insert(0, replica)
    
    def send_file():
        # Function to send file properties to the main program
        global genes, tpm, replica, separator
        genes = str(page_type2.get())
        tpm= str(page_type4.get())
        replica= int(page_type6.get())
        separator= str(page_type8.get())
        print(genes, tpm, replica, separator)

    # Create 'Apply' button
    button_files = Button(frame_file3, text='Apply', command=send_file)
    button_files.grid(row=7, column=1, columnspan=3, pady=(10,0))

    # Print file properties (for testing purposes)
    print (genes, tpm, replica)
     
def btnCallBack (): # Function to delete the files from the listbox when the program has finished its analysis
    listbox.delete(0, END)
          
def to_analyze():
    global genes, tpm, replica, type, separator
    
    # Extracting the selected type from the radiobutton
    type2=type.get()
    print(type2)
    
    # Creating the results window
    screen_results = tk.Toplevel(root)
    screen_results.title('Results')  # CHOOSING TITLE
    screen_results.iconbitmap('image/analyze.ico')  #SETTING WINDOW ICON
    screen_width = screen_results.winfo_screenwidth()
    screen_height = screen_results.winfo_screenheight()


    # Setting up the results window size and position
    # root window size
    width = 680
    height = 550

    # window position
    posx = screen_width / 2 - width / 2 -50
    posy = screen_height / 2 - height / 2

    # define geometry
    screen_results.geometry("%dx%d+%d+%d" % (width, height, posx, posy))
    screen_results.resizable(False, False)
    
    # Defining frames within the results window
    frame_results = Frame(screen_results, highlightbackground="black",
                         highlightthickness=1,
                         bd=5
                         )
    frame_resultsII = Frame(frame_results,
                           highlightbackground="black",
                           highlightthickness=0,
                           #bd=5
                           )
    frame_results3 = Frame(frame_results,
                          highlightbackground="black",
                          highlightthickness=0,
                          #bd=5
                          )
    
    # Setting the First Table Variable and the Empty DataFrame
    isFirst = True
    dFrame = pd.DataFrame()

    # Creating a progress bar
    my_progress['value'] = 10
    
    if type2 == 3:
        # Criando um loop para abrir cada file .sf da mesma pasta
        
        for n in range(len(selected)):
            directory = listbox.get(n)  
            files = pd.read_table(directory)
            print(files)
            if isFirst:
                isFirst = False
                dFrame['Genes'] = files[genes]    
            title = os.path.basename(directory)
            title = os.path.splitext(title)[0]
            dFrame[title] = files[tpm]
            for col in dFrame.columns[1:]:
                dFrame[col] = dFrame[col].astype(float)
        print(dFrame)

        # Loop to rename replica columns with their corresponding sample names
        for column in dFrame.columns[1:]:
            if "_" in column:
                sample_name = column.split("_")[0]
                dFrame = dFrame.rename(columns={column:sample_name})

        # Loop to Average TPM Values for Identically-Named Samples
        sample_columns = dFrame.columns[1:].unique()
        for sample in sample_columns:
            col = dFrame.columns[dFrame.columns.str.contains(sample)]
            avg = dFrame.loc[:, col].mean(axis=1)
            dFrame[sample] = avg

        # Deletes remaining replica columns
        replica_columns = dFrame.columns[dFrame.columns.str.contains("_")]
        print(replica_columns)
        dFrame = dFrame.drop(columns=replica_columns)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print(dFrame)
        
        dFrame = dFrame.loc[:,~dFrame.columns.duplicated(keep='first')]
    elif type2==2:
        # Processing a single file with all libraries (type2=2)
        print(selected)
        directory = listbox.get(0)
        files = pd.read_excel(directory)
        dFrame = files
        dFrame = dFrame.rename(columns={genes:'Genes'})
        
    elif type2==1:
         # Processing text files (type2=1)
        print(selected)
        directory = listbox.get(0)
        files = pd.read_csv(directory, sep=separator, engine='python')
        dFrame = files
        
        for col in dFrame.columns[1:]:
            dFrame[col] = dFrame[col].str.replace(',','.').astype(float)
        dFrame = dFrame.rename(columns={genes:'Genes'})
        

    # Progress bar update
    dFrame2 = dFrame
    
    # Printing the table for monitoring
    #print(dFrame, "teste1")
    #dFrame.to_excel('teste.xlsx')

    # Filtering out zero values in any of the columns.
    for col in dFrame.columns[1:]:
        filtro = dFrame[col] > 0
        #print(dFrame[filtro])
        # Keep rows where the TPM value is greater than 0
        dFrame = dFrame[filtro]
    print(dFrame)
    my_progress['value'] = 20

    # Calculating LOG2 of each library's TPM
    criterio = pd.DataFrame()
    print(dFrame)
    criterio["Genes"] = dFrame["Genes"]
    for column in dFrame.columns[1:]:
        # Calculate the log2 of each TPM value
        criterio[column] = np.log2(dFrame[column])
    print(criterio)

    # Creating a table with the standard deviation of log2(TPM)
    results = pd.DataFrame()
    results['VB ID'] = criterio['Genes']
    results["SD"] = criterio.std(axis=1, numeric_only=True)
    print(results)

    # Filtering (standard deviation [log2(TPM)] < 1)
    filter = results["SD"] < filtersI[1]
    results = results[filter]
    criterio = criterio[filter]
    print(results)
    print(criterio)

    # Results table with Mean
    results["TPM AVRG"] = criterio.mean(axis=1, numeric_only=True, skipna=True)
    print(results)

    # Filtering (log2(TPM) +/- 2)
    for col in criterio.columns[1:]:
        filter = abs(criterio[col].sub(results["TPM AVRG"])) <= filtersI[2]
        criterio, results = criterio[filter], results[filter]
    print(criterio)
    print(results)

    # Filtering Mean Log2(TPM) > 5
    filter = results["TPM AVRG"] > filtersI[3]
    results = results[filter]
    print(results)

    # Adding a column with the value of standard deviation/Mean
    results["CV"] = results["SD"] / results["TPM AVRG"]
    print(results)

    # Filtering only values where Standard Deviation/Mean is less than 0.2
    filter = results["CV"] < filtersI[4]
    results = results[filter]
    results = results.sort_values(by=['CV'])
    results.insert(0, 'GSV ID', range(1, results.shape[0] + 1))
    print()
    
    result_title = Label(frame_results, text='Candidate: Reference genes',
                         font = "Arial 16 bold")
    result = Table(frame_resultsII, dataframe=results, showtoolbar=True, showstatusbar=True)
    result.show()
    
    my_progress['value'] = 50
    
    def save():
        # Define the file types available for saving
        files = [('Excel file', '.xlsx'),  
             ('csv file', '*.csv'), 
             ('Text Document', '*.txt')]
        # Open a file dialog to choose the save location and format
        file = asksaveasfile(mode='wb', filetypes = files, defaultextension = files)

        # Save the DataFrame 'results' to the selected file
        results.to_excel(file, index = False)
        
    def differential(dFrame2):
        # Creating a new top-level window for displaying differential analysis results
        screen_differential = tk.Toplevel(screen_results)
        screen_differential.title('Results')  # Setting the window title
        screen_differential.iconbitmap('image/analyze.ico')  # Setting the window icon
        screen_width = screen_differential.winfo_screenwidth()
        screen_height = screen_differential.winfo_screenheight()

        # Setting the size and position of the new window
        width = 680
        height = 550

        # window position
        posx = screen_width / 2 - width / 2
        posy = screen_height / 2 - height / 2 + 100

        # define geometry
        screen_differential.geometry("%dx%d+%d+%d" % (width, height, posx, posy))
        screen_differential.resizable(False, False)
        
        # Defining frames for organizing the layout
        frame_differential = Frame(screen_differential, highlightbackground="black",
                            highlightthickness=1,
                            bd=5
                            )
        frame_differentialII = Frame(frame_differential,
                            highlightbackground="black",
                            highlightthickness=0,
                            #bd=5
                            )
        frame_differential3 = Frame(frame_differential,
                            highlightbackground="black",
                            highlightthickness=0,
                            #bd=5
                            )
        
        # Updating the progress bar to 75% completion
        my_progress['value'] = 75

        # Filtering out zero values in any of the columns.
        for col in dFrame2.columns[1:]:
            filter = dFrame2[col] > filtersII[0]
            dFrame2 = dFrame2[filter]
        print(dFrame2)

        # Calculating LOG2 of each library's TPM

        criterio = pd.DataFrame()
        criterio["Genes"] = dFrame2["Genes"]
        for coluna in dFrame2.columns[1:]:
            criterio[coluna] = np.log2(dFrame2[coluna])

        print(criterio)

        # Creating a table with the standard deviation of log2(TPM)
        results2 = pd.DataFrame()
        results2['VB ID'] = criterio['Genes']
        results2["SD"] = criterio.std(axis=1, numeric_only=True)
        print(results2)

        # Filtering (standard deviation [log2(TPM)] > 1)
        filter = results2["SD"] > filtersII[1]
        results2 = results2[filter]
        criterio = criterio[filter]
        print(results2)
        print(criterio)

        #criterio.to_excel(r'tabela_teste.xlsx', index = False)

        # Results table with Mean
        results2["TPM Avrg"] = criterio.mean(axis=1, numeric_only=True, skipna=True)
        print(results2)


        # filtrando média Log2(tpm)>5
        filter = results2["TPM Avrg"] > filtersII[2]
        results2 = results2[filter]
        print(results2)

         # Adding a column with the standard deviation/Mean value
        #results2["CV"] = results2["standard deviation"] / results2["log2TPM AVRG"]
        print(results2)

        results2 = results2.sort_values(by=['SD'], ascending=False)
        results2.insert(0, 'GSV ID', range(1, results2.shape[0] + 1))
        
        # Creating a label for the results
        result_title = Label(frame_differential, text='Candidate: Validation genes',
                         font = "Arial 16 bold")
        
        # Creating a Table to display the results
        result2 = Table(frame_differentialII, dataframe=results2, showtoolbar=True, showstatusbar=True)
        result2.show()
        
        # Updating the progress bar to 100% completion
        my_progress['value'] = 100

        # Clearing the 'selected' list
        selected.clear()

        def save2():
            # Defining file types for saving
            files = [('Excel file', '.xlsx'),  
                     ('csv file', '*.csv'), 
                     ('Text Document', '*.txt')]
            
            # Opening a file dialog for saving the results2 DataFrame
            file = asksaveasfile(mode='wb', filetypes = files, defaultextension = files)

            # Saving the results2 DataFrame to the selected file
            results2.to_excel(file, index = False)
    
        # Creating a button for saving the results
        save_btn = Button(frame_differential3,
                    text = 'Save',
                    command = save2,
                    width = 15, height = 1,
                    highlightcolor = 'green',
                    bd = 2,
                    highlightbackground="black",
                    highlightthickness=1,
                    bg= "SkyBlue1"
                    )
        
        # Packing the frames and components into the window
        frame_differential.pack()
        result_title.grid()
        frame_differentialII.grid()
        frame_differential3.grid()
        save_btn.grid(row=0, column=0)
        
    # Creating a 'Save' button for the main results window    
    save_btn = Button(frame_results3,
                    text = 'Save',
                    command = save, # Calls the 'save' function when clicked
                    width = 15, height = 1,
                    highlightcolor = 'green',
                    bd = 2,
                    highlightbackground="black",
                    highlightthickness=1,
                    bg= "SkyBlue1"
                    )
    # Calling the 'differential' function with the DataFrame 'dFrame2'
    differential(dFrame2)

    # Packing the frames and components into the main results window
    frame_results.pack()
    result_title.grid()
    frame_resultsII.grid()
    frame_results3.grid()

    # Displaying the 'Save' button in the main results window
    save_btn.grid(row=0, column=0)


# Tkinter window initialization
root = Tk()
root.title('Gene Selector for Validation') # Set window title

# Setting default filter values
selected = []
filtersI =[0, 1, 2, 5, 0.2]
filtersII =[0, 1, 5]
page_type={} # Dictionary for storing page types

# Set window size and position
width = 1000
height = 400

# system resolution
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# window position
posx = screen_width/2 - width/2
posy = screen_height/2 - height/2

# define geometry
root.geometry("%dx%d+%d+%d" % (width, height, posx, posy))
root.resizable(False, False)
root.iconbitmap('image/minilogo.ico') # Set window icon

# Menubar creation
menubar = Menu(root)

# About menu
abt_menu = Menu(menubar, tearoff = 0)
abt_menu.add_command(label = "About", command = about_menu)
menubar.add_cascade(label="About", menu=abt_menu)

# Help menu
hlp_menu = Menu(menubar, tearoff = 0)
hlp_menu.add_command(label="Instructions for use", command = help_)
menubar.add_cascade(label="Help", menu=hlp_menu)

root.config(menu=menubar)


# Welcome frame
welcome_frame = Frame(root, highlightbackground="black",
                       #highlightthickness=1,
                       #bd= 5,
                       width = 10)

# Labels and text for the welcome frame
welcome_label = Label(welcome_frame,
                        text = 'Gene Selector for Validation',
                        font = 'Arial 16 bold')
label_description = Label(welcome_frame,
                        text ='''The GSV program was created for the identification of reference gene 
candidates by using filters based on Transcripts Per Million (TPM) expression values. 
The software identifies which genes are the most stable 
and expressed (reference candidates), as those with the greatest 
variation and expression, that can be used to validate the RNA-seq data by RT-qPCR.''',
                        font = 'Arial 12',
                        width = 100,
                        height = 5,
                        justify = CENTER)

# Images for the welcome frame
logo = PhotoImage(file="image/logo2small.png")
image_logo = Label(welcome_frame, image=logo)
logo_lab = PhotoImage(file="image/bioinfo_crop.png")
image_lab = Label(welcome_frame, image=logo_lab)

# File picker frame
frame_seletor = Frame(root, highlightbackground="black",
                       #highlightthickness=1,
                       #bd= 5
                      )

# Left block in file picker frame
frame_left = Frame(frame_seletor, highlightbackground="black",
                       #highlightthickness=1,
                       #bd= 5
                   )
frame_right = Frame(frame_seletor, highlightbackground="black",
                       #highlightthickness=1,
                       #bd= 5
                    )

# Select file area text
label_seletor = Label(frame_left,
                       text='1 - Select files:',
                       font='Arial 10')


# Button to add files
seletor_image = PhotoImage(file='image/adicionar.png').subsample(20,20)
seletorBTN = Button(frame_left,
                    image = seletor_image,
                    text = 'Select files',
                    command = add_file,
                    width = 15, height = 15,
                    activebackground = 'green')

# Button to remove files
remove_image = PhotoImage(file='image/remover.png').subsample(20,20)
removeBTN = Button(frame_left,
                   image = remove_image,
                   text = 'Remove files',
                   command = remove_file,
                   width = 15,
                   height = 15,
                   activebackground = 'red')

# Listbox for selected files
frame_listbox = Frame(root,highlightbackground="black",
                       highlightthickness=1,
                       bd= 5
                        )
scrollbar_V = Scrollbar(frame_listbox)  #setting the scrollbar
scrollbar_H = Scrollbar(frame_listbox, orient=HORIZONTAL)
listbox = Listbox(frame_listbox,
                  width = 128,
                  height = 10,
                  selectmode= MULTIPLE,
                  yscrollcommand=scrollbar_V.set,
                  xscrollcommand = scrollbar_H.set)

#Right block with inputs
frame_F = Frame(root, highlightbackground="black",
                       highlightthickness=0,
                       bd= 5)
frame_FII = Frame(frame_F,
                       highlightbackground="black",
                       highlightthickness=1,
                       bd= 5)
label_filter = Label(frame_right,
                       text=' '*150 + 'Adjust your settings below:',
                       font='Arial 10')

#page_type[1] = Label(frame_F, text='\nIndicate above which file model')
#page_type[2] = Label(frame_F, text='that will be used for your analysis.\n')

# Buttons and progress bar
files_btn = Button(frame_F,
                   text = '2 - Set files...',
                   command = file_template,
                   width = 15, height = 1,
                   highlightcolor = 'green',
                    bd = 2,
                    highlightbackground="black",
                    highlightthickness=1
                    )

Filters_btn = Button(frame_F,
                    text = '3 - Set filters...',
                    command = screen_filter,
                    width = 15, height = 1,
                    highlightcolor = 'green',
                    bd = 2,
                    highlightbackground="black",
                    highlightthickness=1
                    )
to_analyze_btn = Button(frame_F,
                    text = '4 - To analyze',
                    command = lambda:[to_analyze(), btnCallBack()],
                    width = 15, height = 1,
                    highlightcolor = 'green',
                    bd = 2,
                    highlightbackground="black",
                    highlightthickness=1,
                    #bg= "SkyBlue1"
                    )

my_progress = ttk.Progressbar(frame_F, orient=HORIZONTAL, length=100, mode='determinate')



###----.PACK AND .GRID DEFINITION----###
welcome_frame.pack(padx=0)
welcome_label.grid(row=0, column=0, sticky=N)
label_description.grid(row=0, column=0,sticky=S, padx=0)
image_logo.grid(row=0, column=0, rowspan=2, sticky=W, padx=0)
image_lab.grid(row=0, column=0, rowspan=2, sticky=E, padx=0)


frame_seletor.pack(side = TOP, anchor = NW, padx = 20)
frame_left.pack(side = LEFT, anchor = W)
frame_right.pack(side = RIGHT, anchor = E, ipadx = 160)


label_seletor.pack(side = LEFT, anchor = NW)
removeBTN.pack(side = RIGHT, padx = 10)
seletorBTN.pack(side = RIGHT)
label_filter.pack(side = RIGHT)

scrollbar_V.pack(side = 'right', fill = 'y')
scrollbar_H.pack(side = BOTTOM, fill = X)
listbox.pack(side=LEFT, anchor = W)
frame_listbox.pack(side=LEFT, anchor = NW, padx = 20, pady = 5)

frame_F.pack(anchor=NW, pady=5)
frame_FII.grid(row=1, column=0)

#page_type[1].grid(row=1, column=1, columnspan=3)
#page_type[2].grid(row=2, column=1, columnspan=3)

files_btn.grid(row=1, column=1, columnspan=2,pady=(10,0))
Filters_btn.grid(row=2, column=1, columnspan=2,pady=(25,0))
to_analyze_btn.grid(row=3, column=1,columnspan=2, pady=(25,0))
my_progress.grid(row=4, column=1,columnspan=2, pady=(25,0))

mainloop()

