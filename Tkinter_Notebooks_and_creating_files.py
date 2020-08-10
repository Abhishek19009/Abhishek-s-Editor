import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

text_contents = dict()  # As we create new text_area we will populate the dictionary

def create_file(content="", title="Untitled"):          # this function will create new file after called
    container = ttk.Frame(notebook)  # Doing this notebook has two children container and scrollbar
    container.pack()
    text_area = tk.Text(container, font=("Helvetica", 32))       # Text is different from entry in a sense that it provide more area to write
    text_area.insert("end", content)    # .insert() inserts content into text_area. 'end' means we will insert at last character and because we are creating new text area each time, this will become start as well
    text_area.pack(side='left', fill='both', expand=True)    # fill= 'both' will make entire x and y available for texting
    notebook.add(container, text=title)
    notebook.select(container)      # select() will select the latest window opened , without using select() first window will be selected by default

    text_contents[str(text_area)] = hash(content)    # hashing means turning piece of data of arbitrary length into  piece of data with specific length, this is to keep track of text_areas we are creating
    # when contents of particular file is changed hash will also change so this serves our purpose of keeping record of whether changes are made or not
    # str[text_area] returns a string which contains name of the widget

    text_scroll = ttk.Scrollbar(container, orient="vertical", command= text_area.yview)
    text_scroll.pack(side="right", fill = 'y')
    text_area["yscrollcommand"] = text_scroll.set   # When we move the text_area , the scroll bar moves and when we move scroll bar text_area moves due to above command

def check_for_changes():        # This entire function will look for changes in text editor and put asterisk if that happens
    current= get_text_widget()
    content = current.get("1.0", "end-1c")
    name = notebook.tab('current')['text']

    if hash(content) != text_contents[str(current)]:        # Since hash kept record of any changes thus comparing it to original widget will inform us that it has changed
        if name[0] != "*":          # We want first character to be * if any changes has been made
            notebook.tab("current", text= "*" + name)       # this will make first character * if it is not
    elif name[0] == "*":        # if file has not been changed then asterisk should be removed from widget name
        notebook.tab("current", text= name[1:])


def get_text_widget():
    tab_widget = root.nametowidget(notebook.select())
    text_widget = tab_widget.winfo_children()[0]        # 0 is container and 1 is scrollbar
    return text_widget

def close_current_tab():        # this is used to close if current_tab
    current= get_text_widget()
    if current_tab_unsaved() and not confirm_close():
        return
    if len(notebook.tabs()) == 1:
        create_file()       # We have two options in this case either to create_file() or to do root.destroy()

    notebook.forget(current)

def current_tab_unsaved():
    text_widget = get_text_widget()
    content= text_widget.get('1.0','end-1c')
    return hash(content) != text_contents[str(text_widget)]

def confirm_close():
    return messagebox.askyesno(
        message= 'You have unsaved changes. Are you sure you want to close?',
        icon= 'question',
        title= 'Unsaved Changes'
    )

def save_file():
    file_path= filedialog.asksaveasfilename()    # this will open saveas dialogbox and get file name from user, then store it as absolute path

    try:
        filename = os.path.basename(file_path)  #this will extract basename for example  C:\Users\file.txt will get converted to file.txt
        tab_widget = root.nametowidget(notebook.select())      # This may be little bit confusing but what is happening here is that widget corresponding to tab we are working is selected
        text_widget = tab_widget.winfo_children()[0]
        content= text_widget.get('1.0','end-1c')   #After we selected the widget we will use .get() to extract its contents
        #1.0 means first character of first line till last character , but since last character is new line we will subtract it using -1c

        with open(file_path, 'w') as file: # Now we will write the contents to file having file_path
            file.write(content)

    except(AttributeError,FileNotFoundError):
        print('Save operation cancelled')
        return

    notebook.tab('current', text=filename)  # this will select current tab and rename Untitled with filename


def confirm_quit():
    unsaved = False

    for tab in notebook.tabs():
        tab_widget = root.nametowidget(tab)
        text_widget= tab_widget.winfo_children()[0]
        content= text_widget.get("1.0","end-1c")

        if hash(content) != text_contents[str(text_widget)]:
            unsaved = True
            break

    if unsaved and not confirm_close():
            return

    root.destroy()


def open_file():
    file_path= filedialog.askopenfilename()
    try:
        filename= os.path.basename(file_path)

        with open(file_path, 'r') as file:
            content= file.read()
    except(AttributeError, FileNotFoundError):
        print("Open operation cancelled")
        return
    create_file(content, filename)

def show_about_info():
    messagebox.showinfo(
        title="About",
        message="Abhishek's Editor  designed by Abhishek Kuriyal.....\n\n\n"
                "Version = 1.00\n\n"
                "Copyright @Abhishek Inc.\n\n"
    )

root = tk.Tk()
root.title("Abhishek's Editor")
root.option_add('*tearoff', False)      # tearoff True is used in some cases when the option added are not attached at app window, setting tearoff to be False will attach options to main window

main = ttk.Frame(root)
main.pack(fill='both', expand=True, padx=1, pady=(4, 0))    # padx= 1 will create greyish borderline of 1 width and pady= (4,0) will create borderline at 4 position at top and 0 at bottom

notebook = ttk.Notebook(main)       # Notebook was introduced in ttk which create a beautiful window with widgets at top left displaying the files which are opened
notebook.pack(fill='both', expand=True)

menubar= tk.Menu()                 # These two command create a menubar i.e the bar we see at top
root.config(menu=menubar)

file_menu= tk.Menu(menubar)             # These two command will add File menu to menubar
help_menu= tk.Menu(menubar)
menubar.add_cascade(menu=file_menu, label='File')       # adding cascade means adding drop down menu
menubar.add_cascade(menu=help_menu, label='Help')

file_menu.add_command(label= "New...", command= create_file, accelerator= 'Ctrl+N')       # This command will add options to File drop_down
file_menu.add_command(label= 'Save...', command= save_file, accelerator= 'Ctrl+S')      # accelerator will create a shortcut but we need to bind it too
file_menu.add_command(label= "Open...", command= open_file, accelerator= 'Ctrl+O')
file_menu.add_command(label= "Exit...", command= confirm_quit, accelerator= 'Alt+E')

help_menu.add_command(label= "About...", command= show_about_info, accelerator= 'Ctrl+I')
create_file()

root.bind('<KeyPress>', lambda event: check_for_changes())      # Remember we have to call the function here because after pressing these commands we want function to respond
root.bind('<Control-n>', lambda event: create_file())
root.bind('<Control-o>', lambda event: open_file())
root.bind('<Control-s>', lambda event: save_file())
root.bind('<Alt-e>', lambda event: confirm_quit())
root.bind('<Control-q>', lambda event: close_current_tab())
root.bind('<Control-i>', lambda event: show_about_info())

root.mainloop()
