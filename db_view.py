import tkinter as tk
from sqlite3 import OperationalError
from tkinter import ttk
from tkinter import messagebox
from functools import partial
import tkinter.filedialog as fd
import pathlib
import sqlite3
import csv


class DB_act:
    """ represents the communication and interaction with the database"""
    def __init__(self, base):

        self.conn = sqlite3.connect(base)
        self.curs = self.conn.cursor()
        self.basis = pathlib.Path(base).stem
        self.create_db()
        self.anal()

    def anal(self):
        """ Analyzing table for later """
        erg = self.curs.execute('SELECT * FROM shelly')
        anal = erg.description
        print(anal)
        cols = []
        for i in anal:
            print(i[0])
            cols.append(i[0])
        print(cols)
        # a = self.basis
        # e = pathlib.Path.stem(a)
        print(self.basis)
        showtables = """SELECT name FROM sqlite_schema WHERE type='table'; """
        showtables2 = """SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%';"""

    def all(self):
        data = self.curs.execute('SELECT * FROM shelly')
        self.view(data)

    def create_db(self):
        pass
        # statement = """
        # CREATE TABLE IF NOT EXISTS personen (
        # geb_id INTEGER PRIMARY KEY,
        # vorname VARCHAR(20),
        # nachname VARCHAR(30),
        # geburtstag DATE);
        # """
        # self.curs.execute(statement)

    def del_set(self):
        """ delete one data-set indicated by id """
        if messagebox.askyesno('Datensatz löschen?', 'Wollen Sie wirklich diesen Datensatz löschen???'):
            id = self.read_fields()[1][0]
            self.curs.execute(("DELETE FROM shelly WHERE id=" + id))
            self.conn.commit()
            self.all()
        else:
            return

    def dub_check(self):
        pass
        # """ Delete double entries in database """
        # order = """
        # DELETE FROM personen
        # WHERE EXISTS (
        #     SELECT geb_id FROM personen a
        #     WHERE personen.nachname = a.nachname AND personen.vorname = a.vorname AND
        #     personen.geburtstag = a.geburtstag AND personen.geb_id > a.geb_id
        # )
        # """
        # self.curs.execute(order)
        # self.conn.commit()
        # self.all()

    def exec(self):
        """ for the command window """
        try:
            query = base.sqlpad.ent.get()
            data = self.curs.execute(query)
            self.view(data)
        except OperationalError as e:
            print('Fehler', e)
            messagebox.showerror('Command Line SQL-Fehler', e)

    def fifi(self):
        """ find file for import """
        verz = pathlib.Path.cwd()
        filetypes = (('Csv-Dateien', '*.csv'),)
        try:
            filename = fd.askopenfilename(title='CSV-Datei öffnen', initialdir=verz, filetypes=filetypes)
        except:
            filename = ''
        return filename

    def import_csv(self):
        pass
        # """ importing from csv files"""
        # file = self.fifi()
        # print(file)
        # if file == '':
        #     print('nenene')
        #     return
        # else:
        #     statement = """
        #     INSERT INTO personen (nachname, vorname, geburtstag) VALUES (:nachname, :vorname, :geburtstag);
        #     """
        #     with open(file, 'r', encoding='utf-8') as csvfile:
        #         csv_read = csv.reader(csvfile, delimiter=';')
        #         next(csv_read, None)
        #         self.curs.executemany(statement, csv_read)
        #     self.conn.commit()
        #     self.all()
        # # 'geburtstage_bundeskanzler_politiker.csv'

    def insert_db(self):
        pass
        # """ single entries in db"""
        # fields = self.read_fields()
        # daten = (fields[1][1], fields[1][2], fields[1][3])
        # print(daten)
        # if daten[0] == '' and daten[1] == '' and daten[2] == '':
        #     return
        # order ="""INSERT INTO personen
        # (vorname, nachname, geburtstag)
        # VALUES(?, ?, ?)"""
        # self.curs.execute(order, daten)
        # self.conn.commit()
        # self.all()

    @staticmethod
    def read_fields():
        """ Matrix of entries from the mask """
        fields = [[base.actpad.var1.get(), base.actpad.var2.get(),
                   base.actpad.var3.get(), base.actpad.var4.get(), base.actpad.var5.get()],
                  [base.actpad.en1.get(), base.actpad.en2.get(),
                   base.actpad.en3.get(), base.actpad.en4.get(), base.actpad.en5.get()],
                  ['id', 'time', 'power', 'energy', 'temperature']]
        return fields

    def select_db(self):
        """ Searching for sets or items """
        order = []
        fields = self.read_fields()
        print(fields)
        for i in range(len(fields[0])):
            if fields[0][i] == 1:
                if fields[1][i].find('*') == -1:
                    order.append((fields[2][i] + "='" + fields[1][i] + "'"))
                else:
                    like = fields[1][i].replace('*', '%')
                    order.append((fields[2][i] + " LIKE '" + like + "'"))
            else:
                continue
        print(order)
        if not order:
            return
        where = order[0]
        if len(order) > 1:
            for com in range(1, len(order)):
                where = where + " AND " + order[com]
        query = "SELECT * FROM shelly WHERE " + where
        data = self.curs.execute(query)
        self.view(data)
        # self.conn()
        print(query)

    def sort_db(self):
        pass

    def update_db(self):
        """ changes in data-sets"""
        order = []
        fields = self.read_fields()
        # vier werden gelesen, drei werden gebraucht
        # id nicht veränderbar
        print(fields)
        for i in range(1, len(fields[0])):
            print(fields[0][i])
            print(fields[1][i])
            print(fields[2][i])
            print(fields[3][i])
            if fields[0][i] == 1:
                order.append((fields[2][i] + "='" + fields[1][i] + "'"))
            else:
                continue
        print(order)
        if not order:
            return
        where = order[0]
        if len(order) > 1:
            for com in range(1, len(order)):
                where = where + " AND " + order[com]
        query = "UPDATE shelly SET " + where + " WHERE " + fields[2][0] + "=" + fields[1][0]
        # data = self.curs.execute(query)
        data = self.curs.execute((query))
        self.view(data)
        self.conn.commit()
        data = self.curs.execute("SELECT * FROM shelly WHERE "+ fields[2][0] + "=" + fields[1][0])
        self.view(data)
        print(query)

    def view(self, data):
        """ selected data to show """
        rows = self.curs.fetchall()
        print(rows)
        base.table.show_view(rows)


class Base(tk.Tk):
    """ GUI root, frames and windows """
    def __init__(self):
        super().__init__()
        self.title(('Meine kleine Datenbank: ' + pers.basis))
        self.geometry('800x500')
        self.minsize(600, 500)
        frametab = Frame(self)
        framepad = Frame(self)
        framesql = Frame(self)
        self.table = Table(frametab)
        self.sqlpad = SqlPad(framesql)
        self.actpad = ActPad(framepad)



class Frame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)


class Table(ttk.Treeview):
    """ Presentation of dates as a table"""
    def __init__(self, container):
        super().__init__(container)
        container.pack(side='top', fill='both', expand='yes')

        self.style = ttk.Style()
        self.style.theme_use(('default'))
        self.style.configure('Treeview', background='#D3D3D3', foreground='black', fieldbackground='white')
        self.style.map('Treeview', background=[('selected', '#990033')])
        scrollbar = ttk.Scrollbar(container, orient='vertical')
        scrollbar['command'] = self.yview
        scrollbar.pack(side='right', fill='y')
        columns = ('id', 'time', 'power', 'energy', 'temperature')
        self['columns'] = columns
        self['show'] = 'headings'
        self['selectmode'] = 'browse'
        self['yscrollcommand'] = scrollbar.set
        self.create_view()
        self.pack(side='left', fill='both', expand='yes')
        self.tag_configure("even", background='lightgrey')
        self.tag_configure("odd", background='white')
        self.bind('<ButtonRelease-1>', self.show_item)

    def create_view(self):
        """ definition of columns """
        self.column('#1', anchor=tk.CENTER, width=100)
        self.heading('#1', text="'id'", command=partial(self.sort, '#1', False))
        self.column('#2', anchor=tk.CENTER, width=100)
        self.heading('#2', text="'time'", command=partial(self.sort, '#2', False))
        self.column('#3', anchor=tk.CENTER, width=100)
        self.heading('#3', text="'power' in W", command=partial(self.sort, '#3', False))
        self.column('#4', anchor=tk.CENTER, width=100)
        self.heading('#4', text="'energy' in kWh", command=partial(self.sort, '#4', False))
        self.column('#5', anchor=tk.CENTER, width=100)
        self.heading('#5', text="'temperature' in °C", command=partial(self.sort, '#5', False))

    def deltab(self):
        # for item in self.get_children():
        #     self.delete(item)
        self.delete(*self.get_children())

    def show_view(self, rows):
        zahl = 0
        self.deltab()
        for row in rows:
            if zahl % 2 == 0:
                self.insert('', tk.END, values=row, tags=('even'))
            else:
                self.insert('', tk.END, values=row, tags=('odd'))
            zahl += 1

    def show_item(self, event):
        """ put marked data set in entry boxes"""
        region = self.identify("region", event.x, event.y)
        if region != "heading":
            base.actpad.clear_fields()
            current_item = self.focus()
            id, vorname, nachname, geburt, temp = self.item(current_item, 'values')
            base.actpad.en1.insert(0, id)
            base.actpad.en2.insert(0, vorname)
            base.actpad.en3.insert(0, nachname)
            base.actpad.en4.insert(0, geburt)
            base.actpad.en5.insert(0, temp)
            # messagebox.showinfo('Nimm', f'{table.item(current_item)}')

    def sort(self, column, reverse: bool):
        l = [(self.set(k, column), k) for k in self.get_children('')]
        l.sort(reverse=reverse)
        print(l.sort(reverse=reverse))
        for index, (k, v) in enumerate(l):
            self.move(v, '', index)
        self.heading(column=column, command=partial(self.sort, column, not reverse))


class ActPad(tk.Frame):
    """ places buttons, boxes and entries in GUI """
    def __init__(self, container):
        super().__init__(container)
        container.pack()
        self.pack(side='bottom')
        # container.pack(side='bottom')
        # self.pack(side='bottom')
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)
        self.columnconfigure(index=2, weight=1)
        self.columnconfigure(index=3, weight=1)
        self.columnconfigure(index=4, weight=1)
        self.var1 = tk.IntVar()
        self.var2 = tk.IntVar()
        self.var3 = tk.IntVar()
        self.var4 = tk.IntVar()
        self.var5 = tk.IntVar()
        self.labels()
        self.entries()
        self.checkboxes()
        self.buttons()

    def clear_fields(self):
        self.en1.delete(0, tk.END)
        self.en2.delete(0, tk.END)
        self.en3.delete(0, tk.END)
        self.en4.delete(0, tk.END)
        self.en5.delete(0, tk.END)
        self.var1.set(0)
        self.var2.set(0)
        self.var3.set(0)
        self.var4.set(0)
        self.var5.set(0)

    def labels(self):
        text = """Bitte ankreuzen, was gesucht werden soll.
        Wildcards sind erlaubt.
            ZUM ÄNDERN:
        Es wird nur das geändert, wo ein Häkchen gesetzt ist.
        Pro Klick nur eine Änderung (Häkchen) möglich.
        Die ID kann nicht geändert werden!
        """
        lab1 = tk.Label(self, text='id')
        lab1.grid(column=0, row=1, sticky='w', padx=5, pady=0)
        lab2 = tk.Label(self, text='time')
        lab2.grid(column=1, row=1, sticky='w', padx=5, pady=0)
        lab3 = tk.Label(self, text='power')
        lab3.grid(column=2, row=1, sticky='w', padx=5, pady=0)
        lab4 = tk.Label(self, text='energy')
        lab4.grid(column=3, row=1, sticky='w', padx=5, pady=0)
        # lab5 = tk.Label(self, text=text)
        # lab5.grid(column=3, row=6, rowspan=4, sticky='ew', padx=5, pady=5)
        lab6 = tk.Label(self, text='Haken setzen, Wildcards erlaubt', padx=5, pady=5)
        lab6.grid(column=3, row=2, padx=5, pady=5)
        # lab7 = tk.Label(self, text='Haken setzen', padx=5, pady=5)
        # lab7.grid(column=3, row=3, padx=5, pady=5)
        # lab8 = tk.Label(self, text='Wildcards erlaubt', padx=5, pady=5)
        # lab8.grid(column=3, row=4, padx=5, pady=5)
        lab9 = tk.Label(self, text='temperature')
        lab9.grid(column=4, row=1, sticky='w', padx=5, pady=0)

    def entries(self):
        self.en1 = tk.Entry(self, bg='white', font='Calibri 11')
        self.en1.grid(column=0, row=0, sticky='ew', padx=5, pady=0)
        self.en2 = tk.Entry(self, bg='white', font='Calibri 11')
        self.en2.grid(column=1, row=0, sticky='ew', padx=5, pady=0)
        self.en3 = tk.Entry(self, bg='white', font='Calibri 11')
        self.en3.grid(column=2, row=0, sticky='ew', padx=5, pady=0)
        self.en4 = tk.Entry(self, bg='white', font='Calibri 11')
        self.en4.grid(column=3, row=0, sticky='ew', padx=5, pady=0)
        self.en5 = tk.Entry(self, bg='white', font='Calibri 11')
        self.en5.grid(column=4, row=0, sticky='ew', padx=5, pady=0)

    def checkboxes(self):
        check1 = tk.Checkbutton(self, variable=self.var1)
        check1.grid(column=0, row=1, sticky='e', padx=5, pady=0)
        check2 = tk.Checkbutton(self, variable=self.var2)
        check2.grid(column=1, row=1, sticky='e', padx=5, pady=0)
        check3 = tk.Checkbutton(self, variable=self.var3)
        check3.grid(column=2, row=1, sticky='e', padx=5, pady=0)
        check4 = tk.Checkbutton(self, variable=self.var4)
        check4.grid(column=3, row=1, sticky='e', padx=5, pady=0)
        check5 = tk.Checkbutton(self, variable=self.var5)
        check5.grid(column=4, row=1, sticky='e', padx=5, pady=0)

    def kill(self):
        base.destroy()

    def buttons(self):
        # b_store = tk.Button(self, text='Datensatz speichern', command=pers.insert_db)
        # b_store.grid(column=1, row=2, sticky='ew', padx=5, pady=5)
        # b_csv = tk.Button(self, text='CSV-Import', command=pers.import_csv)
        # b_csv.grid(column=1, row=3, sticky='ew', padx=5, pady=5)
        # b_dub = tk.Button(self, text='Dubletten löschen', command=pers.dub_check)
        # b_dub.grid(column=1, row=4, sticky='ew', padx=5, pady=5)
        b_cls = tk.Button(self, text='Eingabefelder löschen', command=self.clear_fields)
        b_cls.grid(column=1, row=5, sticky='ew', padx=5, pady=5)
        b_search = tk.Button(self, text='Suchen', command=pers.select_db)
        b_search.grid(column=2, row=2, sticky='ew', padx=5, pady=5)
        # b_res = tk.Button(self, text='Datensatz ändern', command=pers.update_db)
        # b_res.grid(column=2, row=3, sticky='ew', padx=5, pady=5)
        # b_del = tk.Button(self, text='Datensatz löschen', command=pers.del_set)
        # b_del.grid(column=2, row=4, sticky='ew', padx=5, pady=5)
        b_end = tk.Button(self, text='Beenden', command=self.kill)
        b_end.grid(column=2, row=5, sticky='ew', padx=5, pady=5)


class SqlPad(ttk.LabelFrame):
    """ command line for sql-statements"""
    def __init__(self, container):
        super().__init__(container)
        container.pack(fill=tk.X, expand=tk.YES, padx=5, pady=5)
        self.pack(fill=tk.X, expand=tk.YES) #, side='bottom')
        self['text'] = 'SQL Command Line 4 table: "shelly" '
        self.ent = tk.Entry(self, bg='white', font='Calibri 11')
        self.ent.pack(fill=tk.X, expand=tk.YES, padx=5, pady=5)
        self.but = tk.Button(self, text='ausführen', command=pers.exec).pack(side='left', padx=10, pady=1)
        self.cls = tk.Button(self, text='SQL löschen', command=self.clear).pack(side='left', padx=10, pady=1)

    def clear(self):
        self.ent.delete(0, tk.END)


db = 'strom.db'
#print(pathlib.Path(db).stem)
pers = DB_act(db)


if __name__== "__main__":
    base = Base()
    pers.all()
    base.mainloop()