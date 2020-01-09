# Author :- Aryan Khandelwal

"""
This is a simple Text Editor
Made with Tkinter Module in Python
"""

import tkinter as tk
from tkinter import ttk
from tkinter import *
from functools import partial
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
import os
import pyttsx3
import enchant
from ttkthemes import ThemedTk


class MyScroll(Text):
    """
    Class used to Make a TextWidget
    having horizontal and vertical
    scrollbars
    """

    def __init__(self, master=None, **kw):
        self.frame = ttk.Frame(master)
        self.vbar = ttk.Scrollbar(self.frame, command=self.yview)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.hbar = ttk.Scrollbar(
            self.frame, orient="horizontal", command=self.xview)
        self.hbar.pack(side=BOTTOM, fill=X)
        kw.update({'yscrollcommand': self.vbar.set})
        kw.update({'xscrollcommand': self.hbar.set})
        Text.__init__(self, self.frame, **kw)
        self.pack(side=LEFT, fill=BOTH, expand=True)
        text_meths = vars(Text).keys()
        methods = vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frame)


class Editor:
    """
    Base Class of Editor Made using Tkinter
    """
    window = ThemedTk()
    style = ttk.Style()
    window.title("Notepad")
    window.geometry(
        "{0}x{1}+0+0".format(window.winfo_screenwidth(),
                             window.winfo_screenheight()))
    menuBar = Menu(window)
    # the text and entry frames column
    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(0, weight=1)
    # window.grid_rowconfigure(1, weight=1)  # all frames row
    window.config(menu=menuBar)
    fileMenu = Menu(menuBar, tearoff=0)
    editMenu = Menu(menuBar, tearoff=0)
    viewMenu = Menu(menuBar, tearoff=0)
    helpMenu = Menu(menuBar, tearoff=0)
    txt = MyScroll(window, undo=True)
    txt.grid(row=0, column=1, sticky="NSEW")
    lineNumber = Canvas(window, width="30", height="500")
    lineNumber.grid(row=0, column=0, sticky='NS', pady=1, rowspan=3)
    wordCount = StringVar()
    wordCount.set("Word Count -> 0")
    statusBar = ttk.Label(window, textvariable=wordCount)
    statusBar.grid(row=2, column=1, columnspan=2, sticky="EW")
    txt['wrap'] = 'none'
    fontType = "Calibre"
    fontSize = "10"
    fontColor = "black"
    txt.config(font=str(fontType + ' ' + fontSize))
    currentFile = "No File"
    spellCheck = 0

    def __init__(self):
        self.fileMenu.add_command(
            label="New", command=self.new_file, accelerator="Ctrl+N")
        self.window.bind_all('<Control-n>', self.new_file)
        self.fileMenu.add_command(
            label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.window.bind_all('<Control-o>', self.open_file)
        self.fileMenu.add_command(
            label="Save", command=self.save_file,  accelerator="Ctrl+S")
        self.window.bind_all('<Control-s>', self.save_file)
        self.fileMenu.add_command(
            label="Save As", command=self.save_file_as,
            accelerator="Ctrl+Shift+S")
        self.window.bind_all('<Control-S>', self.save_file_as)
        self.fileMenu.add_command(label="Exit", command=self.exit)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        self.editMenu = Menu(self.menuBar, tearoff=0)
        self.editMenu.add_command(label="Cut", command=self.cut)
        self.editMenu.add_command(
            label="Copy", command=self.copy, accelerator="Ctrl+C")
        # self.window.bind_all('<Control-c>', self.copy)
        self.editMenu.add_command(
            label="Paste", command=self.paste, accelerator="Ctrl+V")
        # self.window.bind_all('<Control-v>', self.paste)
        self.editMenu.add_command(
            label="Undo", command=self.undo, accelerator="Ctrl+Z")
        self.window.bind_all('<Control-z>', self.undo)
        self.editMenu.add_command(
            label="Redo", command=self.redo, accelerator="Ctrl+R")
        self.window.bind_all('<Control-r>', self.redo)
        self.editMenu.add_command(
            label="Find", command=self.find, accelerator="Ctrl+F")
        self.window.bind_all('<Control-f>', self.find)
        self.viewMenu.add_command(label="Font Size", command=self.font_size)
        self.viewMenu.add_command(label="Speak It", command=self.speak)
        spellMenu = Menu(self.viewMenu)

        def switch_on():
            self.spellCheck = 1

        def switch_off():
            self.txt.tag_delete('misspell')
            self.spellCheck = 0

        spellMenu.add_radiobutton(label="Yes", command=switch_on)
        spellMenu.add_radiobutton(label="No", command=switch_off)
        self.viewMenu.add_cascade(label="Spell Checker", menu=spellMenu)
        self.editMenu.add_command(
            label="Replace All", command=self.replace,
            accelerator="Ctrl+Shift+R")
        self.window.bind_all('<Control-R>', self.replace)
        self.menuBar.add_cascade(label="Edit", menu=self.editMenu)
        self.menuBar.add_cascade(label="View", menu=self.viewMenu)
        self.helpMenu.add_command(label="About", command=self.about)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)
        self.window.bind_all('<Return>', self.redraw)
        self.window.bind_all('<BackSpace>', self.redraw)
        self.window.bind_all('<Key>', self.redraw)
        self.window.bind_all('<Button-4>', self.redraw)
        self.window.bind_all('<Button-5>', self.redraw)
        self.window.bind_all('<Configure>', self.redraw)
        self.window.bind_all('<Motion>', self.redraw)
        self.editMenu.add_command(
            label="Select All", command=self.selectall, accelerator="Ctrl+A")
        self.window.bind_all('<Control-a>', self.selectall)
        themeBar = Menu(self.viewMenu)
        themeBar.add_command(label="Blacko", command=partial(
            self.change_theme, "blacko"))
        themeBar.add_command(label="Whity", command=partial(
            self.change_theme, "whity"))
        themeBar.add_command(label="Gyona", command=partial(
            self.change_theme, "gyona"))
        self.viewMenu.add_cascade(label="Themes", menu=themeBar)

        self.window.mainloop()

    def new_file(self, event=None):
        if(messagebox.askyesno("Save?", "Do you wish to save current file?")):
            self.save_file()
            self.txt.delete('1.0', END)
            self.window.title("Notepad")
            self.currentFile = "No File"
        else:
            self.txt.delete('1.0', END)
            self.window.title("Notepad")
            self.currentFile = "No File"

    def open_file(self, event=None):
        print("opening file")
        myFile = filedialog.askopenfile(
            parent=self.window, mode="rb", title="My New File")
        if myFile is not None:
            self.window.title(os.path.basename(myFile.name))
            content = myFile.read()
            self.txt.delete('1.0', END)
            self.txt.insert(1.0, content)
            self.currentFile = myFile.name
            myFile.close()
            self.redraw(event)

    def save_file_as(self, event=None):
        print("saving file")
        myFile = filedialog.asksaveasfile(mode="w")
        if myFile is not None:
            myFile.write(self.txt.get('1.0', END))
            self.currentFile = myFile.name
            myFile.close()
            self.window.title(os.path.basename(myFile.name))

    def save_file(self, event=None):
        print(self.currentFile)
        if (self.currentFile == "No File"):
            self.save_file_as(event)
        else:
            myFile = open(self.currentFile, "w")
            myFile.write(self.txt.get('1.0', END))
            myFile.close()

    def copy(self):
        # print("copying")
        self.txt.clipboard_clear()
        self.txt.clipboard_append(self.txt.selection_get())

    def cut(self):
        self.copy()
        self.txt.delete(SEL_FIRST, SEL_LAST)

    def paste(self):
        self.txt.insert(INSERT, self.txt.clipboard_get())
        self.redraw(event)

    def undo(self, event=None):
        self.txt.edit_undo()

    def redo(self, event=None):
        self.txt.edit_redo()

    def find(self, event=None):
        root = Toplevel(self.window)
        root.title("Find")
        root.transient(self.window)
        root.focus_force()
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        e1 = ttk.Entry(root)
        e1.grid(row=0, column=0, pady="10",
                padx="10", columnspan=2, sticky="EW")

        def sub():
            findString = e1.get()
            self.set_mark(findString)

        def on_closing():
            self.txt.tag_delete('highlight')
            root.destroy()

        findBtn = ttk.Button(root, text="Find", command=sub)
        findBtn.grid(row=1, column=0, pady="10", padx="10", sticky="EWS")
        closeBtn = ttk.Button(root, text="Close", command=on_closing)
        closeBtn.grid(row=1, column=1, pady="10", padx="10", sticky="EWS")
        root.protocol("WM_DELETE_WINDOW", on_closing)

    def selectall(self, event=None):
        self.txt.tag_add('sel', '1.0', 'end')
        return "break"

    def set_mark(self, findString):
        print("Coming to set mark")
        self.find_string(findString)
        self.txt.tag_config('highlight', foreground='red')
        self.txt.focus_force()

    def find_string(self, findString):
        startInd = '1.0'
        while(startInd):
            startInd = self.txt.search(findString, startInd, stopindex=END)
            if startInd:
                startInd = str(startInd)
                lastInd = startInd+f'+{len(findString)}c'
                print(startInd, lastInd)
                self.txt.tag_add('highlight', startInd, lastInd)
                startInd = lastInd

    def replace(self, event=None):
        print("coming replace")
        root = Toplevel(self.window)
        root.title("Find and Replace")
        root.transient(self.window)
        root.focus_force()
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        e1 = ttk.Entry(root)
        e1.grid(row=0, column=0, pady=5, columnspan=2, padx=10)
        e2 = ttk.Entry(root)
        e2.grid(row=1, column=0, pady=5, columnspan=2, padx=10)

        def find():
            findString = e1.get()
            self.set_mark(findString)

        def replace():
            findString = e1.get()
            replaceString = e2.get()
            myText = self.txt.get('1.0', END)
            myText = myText.replace(findString, replaceString)
            self.txt.delete('1.0', END)
            self.txt.insert('1.0', myText)
            root.destroy()

        def on_closing():
            self.txt.tag_delete('highlight')
            root.destroy()

        findButton = ttk.Button(root, text="Find", command=find)
        replaceButton = ttk.Button(root, text="Replace", command=replace)
        findButton.grid(row=2, column=0, padx=10, pady=5)
        replaceButton.grid(row=2, column=1, padx=10, pady=5)
        root.protocol("WM_DELETE_WINDOW", on_closing)

    def redraw(self, event=NONE):
        self.update_count(event)
        if (self.spellCheck == 1):
            self.spell_check()
        self.lineNumber.delete("all")
        self.objectIds = []
        si = self.txt.index("@0,0")
        while True:
            dline = self.txt.dlineinfo(si)
            if dline is None:
                break
            y = dline[1]
            liNum = str(si).split(".")[0]
            self.lineNumber.create_text(
                2, y, anchor="nw", text=liNum, fill=self.fontColor)
            si = self.txt.index(f"{si}+1line")

    def update_count(self, event):
        count = self.txt.get('1.0', END)
        self.wordCount.set(f"Word Count -> {len(count)-1}")

    def font_size(self):
        """Adjust Font Size"""
        newFontSize = simpledialog.askstring(
            "Font", "Enter font size", parent=self.window)
        self.txt.config(font=str(self.fontType + ' ' + newFontSize))
        self.txt.update

    def speak(self):
        engine = pyttsx3.init()
        engine.say(self.txt.selection_get())
        engine.runAndWait()

    def spell_err(self, findString):
        """Check for Spelling Errors"""
        startInd = '1.0'
        while(startInd):
            startInd = self.txt.search(findString, startInd, stopindex=END)
            if startInd:
                startInd = str(startInd)
                lastInd = startInd+f'+{len(findString)}c'
                # print(startInd, lastInd)
                self.txt.tag_add('misspell', startInd, lastInd)
                startInd = lastInd

    def spell_check(self, event=NONE):
        self.txt.tag_delete('misspell')
        words = self.txt.get('1.0', "end-1c").split()
        for word in words:
            # print(word)
            if (self.word_exist(word) == FALSE):
                self.spell_err(word)

        self.txt.tag_config('misspell', background="red", foreground="white")

    def word_exist(self, word):
        d = enchant.Dict("en_US")
        return d.check(word)

    def change_theme(self, theme):
        if (theme == "blacko"):
            self.fontColor = "white"
            self.window['theme'] = 'black'
            self.txt.config(bg="black", fg="white", insertbackground="white")
            self.txt['fg'] = 'white'
            self.lineNumber.config(bg="black")
            self.menuBar.config(bg="black", fg="white")
            pass
        elif (theme == "whity"):
            self.fontColor = "black"
            self.window['theme'] = 'aquativo'
            self.lineNumber.config(bg="white")
            self.txt.config(bg="white", fg="black", insertbackground="black")
            self.menuBar.config(bg="white", fg="black")
            pass
        elif (theme == "gyona"):
            self.fontColor = "black"
            self.window['theme'] = 'arc'
            self.lineNumber.config(bg="#9de1fd")
            self.txt.config(bg="white", fg="black", insertbackground="black")
            self.menuBar.config(bg="#9de1fd", fg="black", relief=RAISED)

    def about(self):
        print("about")
        messagebox.showinfo("About", "Your Own Personalized Notepad")

    def exit(self):
        if(messagebox.askyesno('Quit', 'Are you sure you want to quit')):
            self.window.destroy()


a = Editor()
