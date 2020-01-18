import tkinter as tk
from tkinter import *
from tkinter import messagebox
import tkinter.font
from tkinter import colorchooser
from tkinter import ttk
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk
import os


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")
        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):

        cmd = (self._orig,) + args
        try:
            result = self.tk.call(cmd)
            if (args[0] in ("insert", "replace", "delete") or
                    args[0:3] == ("mark", "set", "insert") or
                    args[0:2] == ("xview", "moveto") or
                    args[0:2] == ("xview", "scroll") or
                    args[0:2] == ("yview", "moveto") or
                    args[0:2] == ("yview", "scroll")
                ):
                self.event_generate("<<Change>>", when="tail")
            return result
        except:
            print("Nothing selected")


class TextEditor(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self)
        self.vsb = tk.Scrollbar(orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set,undo=True)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

        self.root = root
        self.file_path = None
        self.TITLE = "TEXT EDITOR"
        self.set_title()
        self.file_name = ""
        self.current_font_family = "Liberation Mono"
        self.current_font_size = 12
        self.fontColor = '#000000'
        self.fontBackground = '#FFFFFF'

        # Shortcuts
        self.text.bind('<Control-n>', self.new)
        self.text.bind('<Control-N>', self.new)

        self.text.bind('<Control-o>', self.open_file)
        self.text.bind('<Control-O>', self.open_file)

        self.text.bind('<Control-s>', self.save)
        self.text.bind('<Control-S>', self.save)

        self.text.bind('<Control-Shift-s>', self.save_as)
        self.text.bind('<Control-Shift-S>', self.save_as)

        self.text.bind('<Alt-F4>', self.close)
        self.text.bind('<Alt-F4>', self.close)

        self.text.bind('<Control-a>', self.select_all)
        self.text.bind('<Control-A>', self.select_all)

        self.text.bind('<Control-c>', self.copy)
        self.text.bind('<Control-C>', self.copy)

        self.text.bind('<Control-p>', self.paste)
        self.text.bind('<Control-P>', self.paste)

        self.text.bind('<Control-h>', self.about)
        self.text.bind('<Control-H>', self.about)

        self.text.bind('<Control-f>', self.find_text)
        self.text.bind('<Control-F>', self.find_text)

        self.text.bind('<Control-Shift-i>', self.italic)
        self.text.bind('<Control-Shift-I>', self.italic)

        self.text.bind('<Control-b>', self.bold)
        self.text.bind('<Control-B>', self.bold)

        self.text.bind('<Control-u>', self.underline)
        self.text.bind('<Control-U>', self.underline)

        self.text.bind('<Control-Shift-l>', self.align_left)
        self.text.bind('<Control-Shift-L>', self.align_left)

        self.text.bind('<Control-Shift-r>', self.align_right)
        self.text.bind('<Control-Shift-R>', self.align_right)

        self.text.bind('<Control-Shift-c>', self.align_center)
        self.text.bind('<Control-Shift-C>', self.align_center)

        self.text.bind('<Control-y>', self.redo)
        self.text.bind('<Control-Y>', self.redo)

        # TOOLBAR
        self.toolbar = Frame(root, pady=2)

        # TOOLBAR BUTTONS
        # new
        self.new_button = Button(name="toobar_b2", borderwidth=1,
                                 command=self.new, width=20, height=20)
        self.photo_new = Image.open("icons/new.png")
        self.photo_new = self.photo_new.resize((18, 18), Image.ANTIALIAS)
        self.image_new = ImageTk.PhotoImage(self.photo_new)
        self.new_button.config(image=self.image_new)
        self.new_button.pack(in_=self.toolbar, side="left", padx=4, pady=4)

        # save
        self.save_button = Button(name="toolbar_b1", borderwidth=1,
                                  command=self.save, width=20, height=20)
        self.photo_save = Image.open("icons1/save.png")
        self.photo_save = self.photo_save.resize((18, 18), Image.ANTIALIAS)
        self.image_save = ImageTk.PhotoImage(self.photo_save)
        self.save_button.config(image=self.image_save)
        self.save_button.pack(in_=self.toolbar, side="left", padx=4, pady=4)

        # open
        self.open_button = Button(name="toolbar_b3", borderwidth=1,
                                  command=self.open_file, width=20, height=20)
        self.photo_open = Image.open("icons/open.png")
        self.photo_open = self.photo_open.resize((18, 18), Image.ANTIALIAS)
        self.image_open = ImageTk.PhotoImage(self.photo_open)
        self.open_button.config(image=self.image_open)
        self.open_button.pack(in_=self.toolbar, side="left", padx=4, pady=4)

        # copy
        self.copy_button = Button(name="toolbar_b4", borderwidth=1,
                                  command=self.copy, width=20, height=20)
        self.photo_copy = Image.open("icons1/copy.png")
        self.photo_copy = self.photo_copy.resize((18, 18), Image.ANTIALIAS)
        self.image_copy = ImageTk.PhotoImage(self.photo_copy)
        self.copy_button.config(image=self.image_copy)
        self.copy_button.pack(in_=self.toolbar, side="left", padx=4, pady=4)

        # cut
        self.cut_button = Button(name="toolbar_b5", borderwidth=1,
                            command=self.cut,width=20, height=20)
        self.photo_cut = Image.open("icons1/cut.png")
        self.photo_cut = self.photo_cut.resize((18, 18), Image.ANTIALIAS)
        self.image_cut = ImageTk.PhotoImage(self.photo_cut)
        self.cut_button.config(image=self.image_cut)
        self.cut_button.pack(in_=self.toolbar, side="left", padx=4, pady=4)

        # paste
        self.paste_button = Button(name="toolbar_b6", borderwidth=1,
                                   command=self.paste, width=20, height=20)
        self.photo_paste = Image.open("icons1/paste.png")
        self.photo_paste = self.photo_paste.resize((18, 18), Image.ANTIALIAS)
        self.image_paste = ImageTk.PhotoImage(self.photo_paste)
        self.paste_button.config(image=self.image_paste)
        self.paste_button.pack(in_=self.toolbar, side="left", padx=4, pady=4)

        # redo
        self.redo_button = Button(name="toolbar_b7", borderwidth=1,
                                  command=self.redo, width=20, height=20)
        self.photo_redo = Image.open("icons1/redo.png")
        self.photo_redo = self.photo_redo.resize((18, 18), Image.ANTIALIAS)
        self.image_redo = ImageTk.PhotoImage(self.photo_redo)
        self.redo_button.config(image=self.image_redo)
        self.redo_button.pack(in_=self.toolbar, side="left", padx=4, pady=4)

        # undo
        self.undo_button = Button(name="toolbar_b8", borderwidth=1,
                                  command=self.undo, width=20, height=20)
        self.photo_undo = Image.open("icons1/undo.png")
        self.photo_undo = self.photo_undo.resize((18, 18), Image.ANTIALIAS)
        self.image_undo = ImageTk.PhotoImage(self.photo_undo)
        self.undo_button.config(image=self.image_undo)
        self.undo_button.pack(in_=self.toolbar, side="left", padx=4, pady=4)

        # find
        self.find_button = Button(name="toolbar_b9", borderwidth=1,
                                  command=self.find_text, width=20, height=20)
        self.photo_find = Image.open("icons/find.png")
        self.photo_find = self.photo_find.resize((18, 18), Image.ANTIALIAS)
        self.image_find = ImageTk.PhotoImage(self.photo_find)
        self.find_button.config(image=self.image_find)
        self.find_button.pack(in_=self.toolbar, side="left", padx=4, pady=4)
        self.toolbar.pack(side="top", fill="x")

        # MENU BAR
        self.menu_bar = Menu(root)
        root.config(menu=self.menu_bar)

        # File
        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu, underline=0)
        file_menu.add_command(label="New", command=self.new, compound='left',
                image=self.image_new, accelerator='Ctrl+N', underline=0)
        file_menu.add_command(label="Open", command=self.open_file, compound='left',
                image=self.image_open, accelerator='Ctrl+O', underline=0)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save, compound='left',
                image=self.image_save, accelerator='Ctrl+S', underline=0)
        file_menu.add_command(label="Save As", command=self.save_as,
                              accelerator='Ctrl+Shift+S', underline=1)
        file_menu.add_separator()
        file_menu.add_command(label="Close", command=self.close,
                              accelerator='Alt+F4', underline=0)

        # Edit Menu
        edit_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu, underline=0)
        edit_menu.add_command(label="Undo", command=self.undo, compound='left',
                image=self.image_undo, accelerator='Ctrl+Z', underline=0)
        edit_menu.add_command(label="Redo", command=self.redo, compound='left',
                image=self.image_redo, accelerator='Ctrl+Y', underline=0)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut, compound='left',
                image=self.image_cut, accelerator='Ctrl+X', underline=0)
        edit_menu.add_command(label="Copy", command=self.copy, compound='left',
                image=self.image_copy, accelerator='Ctrl+C', underline=1)
        edit_menu.add_command(label="Paste", command=self.paste, compound='left',
                image=self.image_paste, accelerator='Ctrl+P', underline=0)
        edit_menu.add_command(label="Delete", command=self.delete, underline=0)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all,
                              accelerator='Ctrl+A', underline=0)
        edit_menu.add_command(
            label="Clear All", command=self.delete_all, underline=6)

        # TOOL Menu
        tool_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tools", menu=tool_menu,
                                  underline=0)
        tool_menu.add_command(label="Change Color", command=self.change_color)
        tool_menu.add_command(label="Search", command=self.find_text,
                compound='left', image=self.image_find, accelerator='Ctrl+F')

        # THEMES MENU
        themes_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Themes", menu=themes_menu,
                                  underline=0)
        self.color_schemes = {
            'Default': '#000000.#FFFFFF',
            'Greygarious': '#83406A.#D1D4D1',
            'Aquamarine': '#5B8340.#D1E7E0',
            'Bold Beige': '#4B4620.#FFF0E1',
            'Cobalt Blue': '#ffffBB.#3333aa',
            'Olive Green': '#D1E7E0.#5B8340',
            'Night Mode': '#FFFFFF.#000000',
        }
        self.theme_choice = StringVar()
        self.theme_choice.set('Default')
        for items in sorted(self.color_schemes):
            themes_menu.add_radiobutton(
                label=items, variable=self.theme_choice,
                command=self.change_theme
            )

        # HELP MENU
        help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_command(label="About", command=self.about,
                                  accelerator='Ctrl+H', underline=0)

        # Second toolbar
        self.formattingbar = Frame(root, padx=2, pady=2)

        # font combobox
        self.all_fonts = StringVar()
        self.font_menu = tkinter.ttk.Combobox(
            self.formattingbar, textvariable=self.all_fonts, state="readonly")
        self.font_menu.pack(in_=self.formattingbar,
                            side="left", padx=4, pady=4)
        self.font_menu['values'] = ('Courier', 'Helvetica', 'Liberation Mono',
         'OpenSymbol', 'Century Schoolbook L', 'DejaVu Sans Mono',
        'Ubuntu Condensed', 'Ubuntu Mono', 'Mukti Narrow', 
        'Symbola', 'Abyssinica SIL')
        self.font_menu.bind('<<ComboboxSelected>>', self.change_font)
        self.font_menu.current(2)

        # font size
        self.all_size = StringVar()
        self.size_menu = tkinter.ttk.Combobox(
            self.formattingbar, textvariable=self.all_size,
            state='readonly', width=5
        )
        self.size_menu.pack(in_=self.formattingbar,
                            side="left", padx=4, pady=4)
        self.size_menu['values'] = ('10', '12', '14', '16', '18',
                                    '20', '22', '24', '26', '28', '30')
        self.size_menu.current(1)
        self.size_menu.bind('<<ComboboxSelected>>', self.change_size)

        # FORMATBAR BUTTONS
        # bold
        self.bold_button = Button(name="formatbar_b1", borderwidth=1,
                    command=self.bold, width=20, height=20, pady=10, padx=10)
        self.photo_bold = Image.open("icons/bold.png")
        self.photo_bold = self.photo_bold.resize((18, 18), Image.ANTIALIAS)
        self.image_bold = ImageTk.PhotoImage(self.photo_bold)
        self.bold_button.config(image=self.image_bold)
        self.bold_button.pack(in_=self.formattingbar,
                              side="left", padx=4, pady=4)

        # italic
        self.italic_button = Button(name="formatbar_b2", borderwidth=1,
                                    command=self.italic, width=20, height=20)
        self.photo_italic = Image.open("icons/italic.png")
        self.photo_italic = self.photo_italic.resize((18, 18), Image.ANTIALIAS)
        self.image_italic = ImageTk.PhotoImage(self.photo_italic)
        self.italic_button.config(image=self.image_italic)
        self.italic_button.pack(in_=self.formattingbar,
                                side="left", padx=4, pady=4)

        # underline
        self.underline_button = Button(
            name="formatbar_b3", borderwidth=1,\
            command=self.underline, width=20, height=20)
        self.photo_underline = Image.open("icons/underline.png")
        self.photo_underline = self.photo_underline.resize(
            (18, 18), Image.ANTIALIAS)
        self.image_underline = ImageTk.PhotoImage(self.photo_underline)
        self.underline_button.config(image=self.image_underline)
        self.underline_button.pack(
            in_=self.formattingbar, side="left", padx=4, pady=4)

        # strike
        self.strike_button = Button(name="formatbar_b4", borderwidth=1,
                                    command=self.strike, width=20, height=20)
        self.photo_strike = Image.open("icons/strike.png")
        self.photo_strike = self.photo_strike.resize((18, 18), Image.ANTIALIAS)
        self.image_strike = ImageTk.PhotoImage(self.photo_strike)
        self.strike_button.config(image=self.image_strike)
        self.strike_button.pack(in_=self.formattingbar,
                                side="left", padx=4, pady=4)

        # font_color
        self.font_color_button = Button(
            name="formatbar_b5", borderwidth=1, command=self.change_color, width=20, height=20)
        self.photo_font_color = Image.open("icons/font-color.png")
        self.photo_font_color = self.photo_font_color.resize(
            (18, 18), Image.ANTIALIAS)
        self.image_font_color = ImageTk.PhotoImage(self.photo_font_color)
        self.font_color_button.config(image=self.image_font_color)
        self.font_color_button.pack(
            in_=self.formattingbar, side="left", padx=4, pady=4)

        # highlight
        self.highlight_button = Button(
            name="formatbar_b6", borderwidth=1,\
             command=self.highlight, width=20, height=20)
        self.photo_highlight = Image.open("icons/highlight.png")
        self.photo_highlight = self.photo_highlight.resize(
            (18, 18), Image.ANTIALIAS)
        self.image_highlight = ImageTk.PhotoImage(self.photo_highlight)
        self.highlight_button.config(image=self.image_highlight)
        self.highlight_button.pack(
            in_=self.formattingbar, side="left", padx=4, pady=4)

        # align_center
        self.align_center_button = Button(
            name="formatbar_b7", borderwidth=1,\
             command=self.align_center, width=20, height=20)
        self.photo_align_center = Image.open("icons/align-center.png")
        self.photo_align_center = self.photo_align_center.resize(
            (18, 18), Image.ANTIALIAS)
        self.image_align_center = ImageTk.PhotoImage(self.photo_align_center)
        self.align_center_button.config(image=self.image_align_center)
        self.align_center_button.pack(
            in_=self.formattingbar, side="left", padx=4, pady=4)

        # align_justify
        self.align_justify_button = Button(
            name="formatbar_b8", borderwidth=1,\
            command=self.align_justify, width=20, height=20)
        self.photo_align_justify = Image.open("icons/align-justify.png")
        self.photo_align_justify = self.photo_align_justify.resize(
            (18, 18), Image.ANTIALIAS)
        self.image_align_justify = ImageTk.PhotoImage(self.photo_align_justify)
        self.align_justify_button.config(image=self.image_align_justify)
        self.align_justify_button.pack(
            in_=self.formattingbar, side="left", padx=4, pady=4)

        # align_left
        self.align_left_button = Button(
            name="formatbar_b9", borderwidth=1,\
             command=self.align_left, width=20, height=20)
        self.photo_align_left = Image.open("icons/align-left.png")
        self.photo_align_left = self.photo_align_left.resize(
            (18, 18), Image.ANTIALIAS)
        self.image_align_left = ImageTk.PhotoImage(self.photo_align_left)
        self.align_left_button.config(image=self.image_align_left)
        self.align_left_button.pack(
            in_=self.formattingbar, side="left", padx=4, pady=4)

        # align_right
        self.align_right_button = Button(
            name="formatbar_b10", borderwidth=1,\
            command=self.align_right, width=20, height=20)
        self.photo_align_right = Image.open("icons/align-right.png")
        self.photo_align_right = self.photo_align_right.resize(
            (18, 18), Image.ANTIALIAS)
        self.image_align_right = ImageTk.PhotoImage(self.photo_align_right)
        self.align_right_button.config(image=self.image_align_right)
        self.align_right_button.pack(
            in_=self.formattingbar, side="left", padx=4, pady=4)

        root.protocol("WM_DELETE_WINDOW", self.close)
        self.status_bar = Label(root, text="", bd=1, relief=SUNKEN, anchor=W)
        self.formattingbar.pack(side="top", fill="x")
        self.status_bar.pack(side="bottom", fill="both", expand=True)

        self.new_button.bind("<Enter>", lambda event,
                str="New, Command - Ctrl+N": self.on_enter(event, str))
        self.new_button.bind("<Leave>", self.on_leave)

        self.save_button.bind("<Enter>", lambda event,
                str="Save, Command - Ctrl+S": self.on_enter(event, str))
        self.save_button.bind("<Leave>", self.on_leave)

        self.open_button.bind("<Enter>", lambda event,
                str="Open, Command - Ctrl+O": self.on_enter(event, str))
        self.open_button.bind("<Leave>", self.on_leave)

        self.copy_button.bind("<Enter>", lambda event,
                str="Copy, Command - Ctrl+C": self.on_enter(event, str))
        self.copy_button.bind("<Leave>", self.on_leave)

        self.cut_button.bind("<Enter>", lambda event,
                str="Cut, Command - Ctrl+X": self.on_enter(event, str))
        self.cut_button.bind("<Leave>", self.on_leave)

        self.paste_button.bind("<Enter>", lambda event,
                str="Paste, Command - Ctrl+P": self.on_enter(event, str))
        self.paste_button.bind("<Leave>", self.on_leave)

        self.undo_button.bind("<Enter>", lambda event,
                str="Undo, Command - Ctrl+Z": self.on_enter(event, str))
        self.undo_button.bind("<Leave>", self.on_leave)

        self.redo_button.bind("<Enter>", lambda event,
                str="Redo, Command - Ctrl+Y": self.on_enter(event, str))
        self.redo_button.bind("<Leave>", self.on_leave)

        self.find_button.bind("<Enter>", lambda event,
                str="Find, Command - Ctrl+F": self.on_enter(event, str))
        self.find_button.bind("<Leave>", self.on_leave)

        self.bold_button.bind("<Enter>", lambda event,
                str="Bold, Command - Ctrl+B": self.on_enter(event, str))
        self.bold_button.bind("<Leave>", self.on_leave)

        self.italic_button.bind("<Enter>", lambda event,
                str="Italic, Command - Ctrl+Shift+I": self.on_enter(event, str))
        self.italic_button.bind("<Leave>", self.on_leave)

        self.underline_button.bind("<Enter>", lambda event,
                str="Underline, Command - Ctrl+U": self.on_enter(event, str))
        self.underline_button.bind("<Leave>", self.on_leave)

        self.align_justify_button.bind("<Enter>", lambda event,
                str="Justify": self.on_enter(event, str))
        self.align_justify_button.bind("<Leave>", self.on_leave)

        self.align_left_button.bind("<Enter>", lambda event,
                str="Align Left, Command - Control-Shift-L": self.on_enter(event, str))
        self.align_left_button.bind("<Leave>", self.on_leave)

        self.align_right_button.bind("<Enter>", lambda event,
                str="Align Right, Command - Control-Shift-R": self.on_enter(event, str))
        self.align_right_button.bind("<Leave>", self.on_leave)

        self.align_center_button.bind("<Enter>", lambda event,
                str="Align Center, Command - Control-Shift-C": self.on_enter(event, str))
        self.align_center_button.bind("<Leave>", self.on_leave)

        self.strike_button.bind("<Enter>", lambda event,
                                str="Strike": self.on_enter(event, str))
        self.strike_button.bind("<Leave>", self.on_leave)

        self.font_color_button.bind("<Enter>", lambda event,
                        str="Font Color": self.on_enter(event, str))
        self.font_color_button.bind("<Leave>", self.on_leave)

        self.highlight_button.bind("<Enter>", lambda event,
                                   str="Highlight": self.on_enter(event, str))
        self.highlight_button.bind("<Leave>", self.on_leave)

        self.strike_button.bind("<Enter>", lambda event,
                                str="Strike": self.on_enter(event, str))
        self.strike_button.bind("<Leave>", self.on_leave)

    def change_theme(self, event=None):
        self.selected_theme = self.theme_choice.get()
        self.colors = self.color_schemes.get(self.selected_theme)
        fg_color, bg_color = self.colors.split('.')
        self.text.config(background=bg_color,
                         fg=fg_color)

    def save_if_modified(self, event=None):
        if self.text.edit_modified():
            response = messagebox.askyesnocancel(
                "Save?", "Documents Modified. Save changes?")
            if response == True:
                result = self.save()
                if result == "saved":
                    return True
                else:
                    return None
            else:
                return response
        else:
            return True

    def make_tag(self):
        current_tags = self.text.tag_names()
        if "bold" in current_tags:
            weight = "bold"
        else:
            weight = "normal"
        if "italic" in current_tags:
            slant = "italic"
        else:
            slant = "roman"
        if "underline" in current_tags:
            underline = 1
        else:
            underline = 0
        if "overstrike" in current_tags:
            overstrike = 1
        else:
            overstrike = 0
        big_font = tkinter.font.Font(self.text, self.text.cget("font"))
        big_font.configure(slant=slant, weight=weight, underline=underline,
            overstrike=overstrike,\
            family=self.current_font_family, size=self.current_font_size)
        self.text.tag_config("BigTag", font=big_font,
                foreground=self.fontColor, background=self.fontBackground)
        if "BigTag" in current_tags:
            self.text.tag_remove("BigTag", 1.0, END)
        self.text.tag_add("BigTag", 1.0, END)

    def open_file(self, event=None):
        self.new()
        file = filedialog.askopenfile()
        self.file_path = file.name
        self.set_title()
        self.text.insert(INSERT, file.read())

    def new(self, event=None):
        response = self.save_if_modified()
        if response is not None:
            self.text.delete(1.0, END)
            self.text.edit_modified(False)
            self.text.edit_reset()
            self.file_path = None
            self.set_title()

    def save(self, event=None):
        if self.file_path == None:
            response = self.save_as()
        else:
            response = self.save_as(filepath=self.file_path)

    def save_as(self, event=None, filepath=None):
        if filepath == None:
            filepath = filedialog.asksaveasfilename(filetypes=(
                ('Text files', '*.txt'), ('Python files',\
                 '*.py *.pyw'), ('All files', '*.*')))
        try:
            with open(filepath, 'wb') as file_name:
                text = self.text.get(1.0, END)
                file_name.write(bytes(text, 'UTF-8'))
                self.text.edit_modified(False)
                self.file_path = filepath
                self.set_title()
                return "Saved File"
        except FileNotFoundError as e:
            print(e)

    def set_title(self, event=None):
        if self.file_path != None:
            title = os.path.basename(self.file_path)
        else:
            title = "Untitled"
        self.root.title(title + " - " + self.TITLE)

    def close(self, event=None):
        response = self.save_if_modified()
        if response != None:
            self.root.destroy()

    def cut(self, event=None):
        self.text.clipboard_clear()
        self.text.clipboard_append(self.text.selection_get())
        self.text.delete(SEL_FIRST, SEL_LAST)
        return "break"

    def copy(self, event=None):
        print(self.text.index(SEL_FIRST))
        print(self.text.index(SEL_LAST))
        root.clipboard_clear()
        self.text.clipboard_append(string=self.text.selection_get())

    def paste(self, event=None):
        self.text.insert(INSERT, root.clipboard_get())

    def undo(self, event=None):
        self.text.event_generate("<<Undo>>")
        return

    def redo(self, event=None):
        self.text.event_generate("<<Redo>>")
        return "break"
        
    def select_all(self, event=None):
        self.text.tag_add(SEL, "1.0", END)
        return "break"

    def delete(self, event=None):
        self.text.delete(index1=SEL_FIRST, index2=SEL_LAST)

    def delete_all(self, event=None):
        self.text.delete(1.0, END)

    def on_enter(self, event, str):
        self.status_bar.configure(text=str)

    def on_leave(self, event):
        self.status_bar.configure(text="")

    def find_text(self, event=None):
        search_toplevel = Toplevel(root)
        search_toplevel.title('Find Or Replace')
        search_toplevel.transient(root)
        search_toplevel.resizable(False, False)
        Label(search_toplevel, text="Find All:").grid(
            row=0, column=0, sticky='e')
        Label(search_toplevel, text="Replace All:").grid(
            row=1, column=0, sticky='e')
        search_entry_widget = Entry(search_toplevel, width=25)
        search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
        search_entry_widget.focus_set()
        search_entry_widget1 = Entry(search_toplevel, width=25)
        search_entry_widget1.grid(row=1, column=1, padx=2, pady=2, sticky='we')

        Button(search_toplevel, text="Find", underline=0, command=lambda: \
        self.check(
            search_entry_widget.get(),'')).grid(row=0,
            column=2, sticky='e' + 'w', padx=2, pady=5)
        
        Button(search_toplevel, text="Replace All", underline=0, command=lambda: \
        self.check(
            search_entry_widget.get(),
            search_entry_widget1.get())).grid(row=1,
            column=2, sticky='e' + 'w', padx=2, pady=5)
        
        Button(search_toplevel, text="Cancel", underline=0,
            command=lambda: self.find_text_cancel_button(
            search_toplevel)).grid(row=3, column=1,
            sticky='e' + 'w', padx=2, pady=2)

    def find_text_cancel_button(self, search_toplevel):
        self.text.tag_remove('found', '1.0', END)
        search_toplevel.destroy()
        return "break"

    def bold(self, event=None):
        current_tags = self.text.tag_names()
        if "bold" in current_tags:
            self.text.tag_delete("bold", 1.0, END)
        else:
            self.text.tag_add("bold", 1.0, END)
        self.make_tag()

    def italic(self, event=None):
        current_tags = self.text.tag_names()
        if "italic" in current_tags:
            self.text.tag_add("roman",  1.0, END)
            self.text.tag_delete("italic", 1.0, END)
        else:
            self.text.tag_add("italic",  1.0, END)
        self.make_tag()

    def underline(self, event=None):
        current_tags = self.text.tag_names()
        if "underline" in current_tags:
            self.text.tag_delete("underline",  1.0, END)
        else:
            self.text.tag_add("underline",  1.0, END)
        self.make_tag()

    def strike(self):
        current_tags = self.text.tag_names()
        if "overstrike" in current_tags:
            self.text.tag_delete("overstrike",  1.0, END)
        else:
            self.text.tag_add("overstrike",  1.0, END)
        self.make_tag()

    def highlight(self):
        color = colorchooser.askcolor(initialcolor='white')
        color_rgb = color[1]
        self.fontBackground = color_rgb
        current_tags = self.text.tag_names()
        if "background_color_change" in current_tags:
            self.text.tag_delete("background_color_change", "1.0", END)
        else:
            self.text.tag_add("background_color_change", "1.0", END)
        self.make_tag()

    def remove_align_tags(self):
        all_tags = self.text.tag_names(index=None)
        if "center" in all_tags:
            self.text.tag_remove("center", "1.0", END)
        if "left" in all_tags:
            self.text.tag_remove("left", "1.0", END)
        if "right" in all_tags:
            self.text.tag_remove("right", "1.0", END)

    def align_center(self, event=None):
        self.remove_align_tags()
        self.text.tag_configure("center", justify='center')
        self.text.tag_add("center", 1.0, "end")

    def align_justify(self):
        self.remove_align_tags()

    def align_left(self, event=None):
        self.remove_align_tags()
        self.text.tag_configure("left", justify='left')
        self.text.tag_add("left", 1.0, "end")

    def align_right(self, event=None):
        self.remove_align_tags()
        self.text.tag_configure("right", justify='right')
        self.text.tag_add("right", 1.0, "end")

    def change_font(self, event):
        f = self.all_fonts.get()
        self.current_font_family = f
        self.make_tag()

    def change_size(self, event):
        sz = int(self.all_size.get())
        self.current_font_size = sz
        self.make_tag()

    def check(self, value, value1):
        if value=='':
            return
        self.text.tag_remove('found', '1.0', END)
        self.text.tag_config('found', background='red')
        list_of_words = value.split(' ')
        for word in list_of_words:
            idx = '1.0'
            while idx:
                idx = self.text.search(word, idx, nocase=1, stopindex=END)
                print(idx)
                if idx:
                    lastidx = '%s+%dc' % (idx, len(word))
                    self.text.tag_add('found', idx, lastidx)
                    print(lastidx)
                    self.text.delete(idx,lastidx)
                    if value1!='':
                        self.text.insert(idx,value1)
                    idx = lastidx
        return

    def change_color(self):
        color = colorchooser.askcolor(initialcolor='#ff0000')
        color_name = color[1]
        self.fontColor = color_name
        current_tags = self.text.tag_names()
        if "font_color_change" in current_tags:
            self.text.tag_delete("font_color_change", 1.0, END)
        else:
            self.text.tag_add("font_color_change", 1.0, END)
        self.make_tag()

    def about(self, event=None):
        messagebox.showinfo(
            "SIMPLE TEXT EDITOR",
            "Simple Text Editor using Tkinter in python - By Tanmay Sinha"
        )

    def _on_change(self, event):
        self.linenumbers.redraw()


if __name__ == "__main__":
    root = tk.Tk()
    TextEditor(root).pack()
    root.mainloop()
