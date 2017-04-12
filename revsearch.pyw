#!/usr/bin/python
from Tkinter import *
from os import system, path, chdir
from platform import system as platform
import subprocess


class Rev(object):

    def __init__(self, master):
        self.root = master
        self.v = 1
        self.root.wm_title("RevSearch (/)")
        self.searcher = Entry(self.root)
        confirm = Button(self.root, text="Search", command=self.search)
        self.listbox_thing = Listbox(self.root, width=180, height=15)
        chdir("/")
        m = subprocess.Popen("ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        k, y = m.communicate()
        self.insert_thing(k)
        self.listbox_thing.bind("<Double-1>", self.open_it) # Double left click = open
        self.listbox_thing.bind("<Left>", self.go_up) # left goes back
        self.listbox_thing.bind("<Right>", self.open_it) # right opens
        self.listbox_thing.bind("<Control-n>", self.new_fi) # Control + n = new file
        self.listbox_thing.bind("<Control-f>", self.focus_search) # Control + f = search bar
        self.listbox_thing.bind("<Control-d>", self.delete_file) # Control + d = delete file
        self.listbox_thing.bind("<Control-E>", self.empt) # Control + Shift + e = empty trash
        self.listbox_thing.bind("<Control-G>", self.recover_trash) # Control + Shift + g = recover trash
        self.listbox_thing.bind("<Control-m>", self.move_anywhere) # Control + m = move stuff
        self.listbox_thing.bind("<Control-N>", self.new_f) # Control + Shift + n = new folder
        self.listbox_thing.bind("<Control-c>", self.copy_anywhere) # Control + c = copy to place
        self.listbox_thing.bind("<Control-D>", self.dup) # Control + Shift + d = duplicate
        self.listbox_thing.bind("<Control-r>", self.rename_file) # Control + r = rename
        self.listbox_thing.bind("<Control-T>", self.open_in_terminal) # Control + Shift + t = open in terminal
        self.listbox_thing.bind("<Control-P>", self.show_contents) # Control + Shift + p = open contents
        self.searcher.bind("<Return>", self.search) # Enter = search thing
        up = Button(self.root, text="Up a folder", command=self.go_up)
        new_folder = Button(self.root, text="New Folder", command=self.new_f)
        new_window = Button(self.root, text="New Window", command=self.new_windo)
        new_file = Button(self.root, text="New File", command=self.new_fi)
        deleter = Button(self.root, text="Delete File", command=self.delete_file)
        empty = Button(self.root, text="Empty Trash", command=self.empt)
        recover = Button(self.root, text="Get back from Trash", command=self.recover_trash)
        move_things = Button(self.root, text="Move something", command=self.move_anywhere)
        copy_things = Button(self.root, text="Copy something", command=self.copy_anywhere)
        open_in_term = Button(self.root, text="Open dir in Terminal", command=self.open_in_terminal)
        duplicate = Button(self.root, text="Duplicate", command=self.dup)
        rename = Button(self.root, text="Rename", command=self.rename_file)
        system("mkdir ~/Trash/")
        self.searcher.pack()
        confirm.pack()
        self.listbox_thing.pack()
        up.pack(side=LEFT)
        new_window.pack(side=LEFT)
        new_folder.pack(side=LEFT)
        new_file.pack(side=LEFT)
        deleter.pack(side=LEFT)
        empty.pack(side=LEFT)
        recover.pack(side=LEFT)
        move_things.pack(side=LEFT)
        copy_things.pack(side=LEFT)
        open_in_term.pack(side=LEFT)
        duplicate.pack(side=LEFT)
        rename.pack(side=LEFT)
        self.window_front()
        self.listbox_thing.focus_force()
        self.root.mainloop()

    def window_front(self):
        system("""/usr/bin/osascript -e 'tell app "Finder" to set \
            frontmost of process "Python" to true' """)

    def focus_search(self, value=None):
        self.searcher.focus_force()

    def move_anywhere(self, value=None):
        self.top1 = Toplevel(self.root)
        new_m_lab = Label(self.top1, text="Path to original")
        self.old_place = Entry(self.top1)
        new_place_lab = Label(self.top1, text="New path")
        self.new_place = Entry(self.top1)
        confirm = Button(self.top1, text="Move", command=self.move_to)
        self.new_place.bind("<Return>", self.move_to)
        new_m_lab.pack()
        self.old_place.pack()
        new_place_lab.pack()
        self.new_place.pack()
        confirm.pack()

    def rename_file(self, value=None):
        self.top2 = Toplevel(self.root)
        new_name_lab = Label(self.top2, text="New name")
        self.new_name = Entry(self.top2)
        confirm = Button(self.top2, text="Rename", command=self.rename_to)
        self.new_name.bind("<Return>", self.rename_to)
        new_name_lab.pack()
        self.new_name.pack()
        confirm.pack()

    def format_full(self, full):
        i = ""
        for x in range(0, len(full)):
            if full[x] == " ":
                i += "\\"
            i += full[x]
        return i

    def rename_to(self, value=None):
        if str(path.dirname(path.realpath(self.listbox_thing.get(ACTIVE)))) == "/":
            self.full = "/" + str(self.listbox_thing.get(ACTIVE))
        else:
            self.full = str(path.dirname(path.realpath(self.listbox_thing.get(ACTIVE)))) + "/" + \
                str(self.listbox_thing.get(ACTIVE))
        o = subprocess.Popen("mv " + self.format_full(self.full) + " " + self.new_name.get() + "; ls", \
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        y, x = o.communicate()
        if x:
            self.warn(x)
        self.insert_thing(y)
        self.top2.destroy()

    def dup(self, value=None):
        t = ""
        if str(path.dirname(path.realpath(self.listbox_thing.get(ACTIVE)))) == "/":
            self.full = "/" + str(self.listbox_thing.get(ACTIVE))
        else:
            self.full = str(path.dirname(path.realpath(self.listbox_thing.get(ACTIVE)))) + "/" + \
                str(self.listbox_thing.get(ACTIVE))
        i = self.format_full(self.full)
        for m in range(0, len(i)):
            if i[m] == ".":
                t += str(self.v)
            t += i[m]
        o = subprocess.Popen("cp " + i + " " + t + "; ls", \
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        y, x = o.communicate()
        self.warn(x) if x else self.insert_thing(y)
        self.v += 1

    def move_to(self, value=None):
        o = subprocess.Popen("mv " + self.old_place.get() + \
            " " + self.new_place.get() + "; ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        y, x = o.communicate()
        self.warn(x) if x else self.insert_thing(y)
        self.top1.destroy()

    def copy_anywhere(self, value=None):
        self.top3 = Toplevel(self.root)
        new_m_lab = Label(self.top3, text="Path to original")
        self.old_place = Entry(self.top3)
        new_place_lab = Label(self.top3, text="New path")
        self.new_place = Entry(self.top3)
        confirm = Button(self.top3, text="Copy", command=self.copy_to)
        self.new_place.bind("<Return>", self.copy_to)
        new_m_lab.pack()
        self.old_place.pack()
        new_place_lab.pack()
        self.new_place.pack()
        confirm.pack()

    def copy_to(self, value=None):
        if path.isfile(self.old_place.get()):
            o = subprocess.Popen("cp " + self.old_place.get() + \
                " " + self.new_place.get() + "; ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            o = subprocess.Popen("cp -R " + self.old_place.get() + \
                " " + self.new_place.get() + "; ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        y, x = o.communicate()
        self.warn(x) if x else self.insert_thing(y)
        self.top3.destroy()

    def recover_trash(self, value=None):
        self.top4 = Toplevel(self.root)
        new_t_lab = Label(self.top4, text="Name of File")
        self.new_t_name = Entry(self.top4)
        go_to_lab = Label(self.top4, text="Move to")
        self.go_to = Entry(self.top4)
        confirm = Button(self.top4, text="Recover", command=self.move_from)
        self.go_to.bind("<Return>", self.move_from)
        new_t_lab.pack()
        self.new_t_name.pack()
        go_to_lab.pack()
        self.go_to.pack()
        confirm.pack()

    def open_in_terminal(self, value=None):
        m = subprocess.Popen("ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        k, y = m.communicate()
        system("open -a Terminal.app " + self.format_full(str(path.dirname(path.realpath(k)))))

    def move_from(self, value=None):
        o = subprocess.Popen("mv ~/Trash/" + self.new_t_name.get() + \
            " " + self.go_to.get() + "; ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        y, x = o.communicate()
        self.warn(x) if x else self.insert_thing(y)
        self.top4.destroy()

    def show_contents(self, value=None):
        self.full = str(path.dirname(path.realpath(self.listbox_thing.get(ACTIVE)))) + "/" + \
            self.listbox_thing.get(ACTIVE)
        if path.isdir(self.full):
            chdir(self.full)
            m = subprocess.Popen("ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            k, y = m.communicate()
            self.insert_thing(k)
            self.root.wm_title("RevSearch (" + str(path.dirname(path.realpath(self.listbox_thing.get(ACTIVE)))) + ")")
        else:
            self.full = self.listbox_thing.get(ACTIVE)
            system("open " + self.format_full(self.full))

    def delete_file(self, value=None):
        if str(path.dirname(path.realpath(self.listbox_thing.get(ACTIVE)))) == "/":
            self.full = "/" + str(self.listbox_thing.get(ACTIVE))
        else:
            self.full = str(path.dirname(path.realpath(self.listbox_thing.get(ACTIVE)))) + "/" + \
                str(self.listbox_thing.get(ACTIVE))
        o = subprocess.Popen("mv " + self.format_full(self.full) + " ~/Trash/ ; ls", shell=True, \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        y, x = o.communicate()
        self.warn(x) if x else self.insert_thing(y)

    def empt(self, value=None):
        system("rm -rf ~/Trash/*")

    def new_windo(self, value=None):
        Rev(Tk())

    def new_fi(self, value=None):
        self.top5 = Toplevel(self.root)
        self.new_f_name = Entry(self.top5)
        confirm = Button(self.top5, text="Make", command=self.new_fil)
        self.new_f_name.bind("<Return>", self.new_fil)
        self.new_f_name.pack()
        confirm.pack()

    def new_f(self, value=None):
        self.top = Toplevel(self.root)
        self.new_name = Entry(self.top)
        confirm = Button(self.top, text="Make", command=self.new_fol)
        self.new_name.bind("<Return>", self.new_fol)
        self.new_name.pack()
        confirm.pack()

    def new_fil(self, value=None):
        o = subprocess.Popen("touch " + str(self.new_f_name.get()), shell=True, stdout=subprocess.PIPE, \
            stderr=subprocess.PIPE)
        y, x = o.communicate()
        if x:
            self.warn(x)
        else:
            m = Popen("open " + str(self.new_f_name.get()) + "; ls", shell=True, \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            i, t = m.communicate()
            if t:
                self.warn(t)
            else:
                self.insert_thing(i)
        self.top5.destroy()

    def new_fol(self, value=None):
        o = subprocess.Popen("mkdir " + str(self.new_name.get()), shell=True, stdout=subprocess.PIPE, \
            stderr=subprocess.PIPE)
        y, x = o.communicate()
        if x:
            self.warn(x)
        else:
            chdir(self.new_name.get())
            m = subprocess.Popen("ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            k, y = m.communicate()
            self.insert_thing(k)
        self.top.destroy()

    def warn(self, value):
        top1 = Toplevel(self.root)
        lab = Label(top1, text=value)
        lab.pack()

    def go_up(self, value=None):
        chdir("../")
        m = subprocess.Popen("ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        k, y = m.communicate()
        self.insert_thing(k)
        self.root.wm_title("RevSearch (" + str(path.dirname(path.realpath(k))) + ")")

    def search(self, value=None):
        chdir("/")
        p = subprocess.Popen("find ~ -name " + self.searcher.get(), shell=True, stdout=subprocess.PIPE, \
            stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        self.listbox_thing.delete(0, END)
        self.insert_thing(stdout)
        self.root.wm_title("RevSearch (search)")
        self.listbox_thing.focus_force()

    def insert_thing(self, value):
        self.listbox_thing.delete(0, END)
        o = ""
        for x in range(0, len(str(value))):
            if str(value)[x] != "\n":
                o += value[x]
            else:
                if path.isdir(o):
                    o += "/"
                self.listbox_thing.insert(END, o)
                o = ""

    def open_it(self, value=None):
        self.full = str(path.dirname(path.realpath(self.listbox_thing.get(ACTIVE)))) + "/" + \
            self.listbox_thing.get(ACTIVE)
        if self.full[-5:] == ".app/":
            m = subprocess.Popen("open " + self.format_full(self.full), shell=True, stdout=subprocess.PIPE, \
                stderr=subprocess.PIPE)
            k, y = m.communicate()
            self.warn(y) if y else self.insert_thing(k)
        elif path.isdir(self.full):
            chdir(self.full)
            m = subprocess.Popen("ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            k, y = m.communicate()
            self.insert_thing(k)
            self.root.wm_title("RevSearch (" + str(path.dirname(path.realpath(self.listbox_thing.get(ACTIVE)))) + ")")
        else:
            self.full = self.listbox_thing.get(ACTIVE)
            m = subprocess.Popen("open " + self.format_full(self.full), shell=True, stdout=subprocess.PIPE, \
                stderr=subprocess.PIPE)
            k, y = m.communicate()
            if (y):
                self.warn(y)


if platform() == "Darwin" and __name__ == "__main__":
    Rev(Tk()) # TODO: zip, sort by kind, windows version
