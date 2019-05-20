from tkinter import *
from DB_Py import *


class GUI(object):

    def __init__(self, db):
        self.sql =db
        self.window = Tk()
        self.window.wm_title("BookStore")
        self.window.wm_iconbitmap('book.png')

        l1 = Label(self.window, text="Title")
        l1.grid(row=0, column=0)

        l2 = Label(self.window, text="Author")
        l2.grid(row=0, column=2)

        l3 = Label(self.window, text="Year")
        l3.grid(row=1, column=0)

        l4 = Label(self.window, text="ISBN")
        l4.grid(row=1, column=2)

        self.title_text = StringVar()
        self.e1 = Entry(self.window, textvariable=self.title_text)
        self.e1.grid(row=0, column=1)

        self.author_text = StringVar()
        self.e2 = Entry(self.window, textvariable=self.author_text)
        self.e2.grid(row=0, column=3)

        self.year_text = StringVar()
        self.e3 = Entry(self.window, textvariable=self.year_text)
        self.e3.grid(row=1, column=1)

        self.isbn_text = StringVar()
        self.e4 = Entry(self.window, textvariable=self.isbn_text)
        self.e4.grid(row=1, column=3)

        self.list1 = Listbox(self.window, height=6, width=35)
        self.list1.grid(row=2, column=0, rowspan=6, columnspan=2)

        sb1 = Scrollbar(self.window)
        sb1.grid(row=2, column=2, rowspan=6)

        self.list1.configure(yscrollcommand=sb1.set)
        sb1.configure(command=self.list1.yview)

        self.list1.bind('<<ListboxSelect>>', self.get_selected_row)

        b1 = Button(self.window, text="View all", width=12, command=self.view_command)
        b1.grid(row=2, column=3)

        b2 = Button(self.window, text="Search entry", width=12, command=self.search_command)
        b2.grid(row=3, column=3)

        b3 = Button(self.window, text="Add entry", width=12, command=self.add_command)
        b3.grid(row=4, column=3)

        b4 = Button(self.window, text="Update", width=12, command=self.update_command)
        b4.grid(row=5, column=3)

        b5 = Button(self.window, text="Delete", width=12, command=self.delete_command)
        b5.grid(row=6, column=3)

        b6 = Button(self.window, text="Close", width=12, command=self.window.destroy)
        b6.grid(row=7, column=3)

        self.window.mainloop()

    def get_selected_row(self, event):
        try:
            global selected_row
            index = self.list1.curselection()[0]
            selected_row = self.list1.get(index)
            self.e1.delete(0, END)
            self.e1.insert(END, selected_row[1])
            self.e2.delete(0, END)
            self.e2.insert(END, selected_row[2])
            self.e3.delete(0, END)
            self.e3.insert(END, selected_row[3])
            self.e4.delete(0, END)
            self.e4.insert(END, selected_row[4])
        except IndexError:
            pass

    def clear(self):
        self.list1.delete(0, END)

    def view_command(self):
        self.clear()
        for rows in self.sql.view():
            self.list1.insert(END, rows)

    def search_command(self):
        self.clear()
        for rows in self.sql.search(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()):
            self.list1.insert(END, rows)

    def add_command(self):
        self.sql.insert(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        self.clear()
        self.list1.insert(END, (self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()))

    def update_command(self):
        self.sql.update(selected_row[0], self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        self.view_command()

    def delete_command(self):
        self.sql.delete(selected_row[0])
        self.view_command()


if __name__=='__main__':
    database = SQL("books.db")
    GUI(database)

