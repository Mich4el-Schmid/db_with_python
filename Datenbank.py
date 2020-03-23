from tkinter import *
from PIL import *
import sqlite3

root = Tk()
root.title("Adressbuch")
root.configure(background="powderblue")
root.geometry("600x600")


#databases

conn = sqlite3.connect("address_book.db")


#creating a cursor
c = conn.cursor()





#creating table
'''
c.execute("""CREATE TABLE addresses (
    first_name text,
    last_name text,
    address text,
    city text,
    state text,
    zipcode integer
    )""")
'''

#function to update a record
def update():
    conn = sqlite3.connect("address_book.db")
    #creating a cursor
    c = conn.cursor()


    record_id = delete_box.get()
    c.execute("""UPDATE addresses SET
        first_name = :first,
        last_name = :last,
        address = :address,
        city = :city,
        state = :state,
        zipcode = :zipcode

        WHERE oid = :oid""",
        {
        'first': f_name_editor.get(),
        'last': l_name_editor.get(),
        'address': city_editor.get(),
        'city': city_editor.get(),
        'state': state_editor.get(),
        'zipcode': zipcode_editor.get(),

        'oid': record_id
        })


    #commit changes
    conn.commit()
    #close connection
    conn.close()

    editor.destroy()

def edit():
    global editor
    editor = Tk()
    editor.title("Eintrag aktualisieren")
    editor.geometry("400x600")


      
    conn = sqlite3.connect("address_book.db")
    #creating a cursor
    c = conn.cursor()

    # Query the database
    record_id = delete_box.get()
    c.execute("SELECT * FROM addresses WHERE oid = " + record_id)
    records = c.fetchall()



    #global textboxes
    global f_name_editor
    global l_name_editor
    global address_editor
    global city_editor
    global state_editor
    global zipcode_editor
    



    #creating textboxes 

    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))

    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=1, column=1)

    address_editor = Entry(editor, width=30)
    address_editor.grid(row=2, column=1)

    city_editor = Entry(editor, width=30)
    city_editor.grid(row=3, column=1)

    state_editor = Entry(editor, width=30)
    state_editor.grid(row=4, column=1)

    zipcode_editor = Entry(editor, width=30)
    zipcode_editor.grid(row=5, column=1)




    #Create text box labes
    f_name_label = Label(editor, text="Vorname")
    f_name_label.grid(row=0, column=0)

    l_name_label = Label(editor, text="Nachname")
    l_name_label.grid(row=1, column=0, pady=(3, 0))

    address_label = Label(editor, text="Addresse")
    address_label.grid(row=2, column=0)

    city_label = Label(editor, text="Stadt")
    city_label.grid(row=3, column=0)

    state_label = Label(editor, text="Kanton")
    state_label.grid(row=4, column=0)

    zipcode_label = Label(editor, text="Postleizahl")
    zipcode_label.grid(row=5, column=0)

        #loop thru result:
    for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        address_editor.insert(0, record[2])
        city_editor.insert(0, record[3])
        state_editor.insert(0, record[4])
        zipcode_editor.insert(0, record[5])

    # Create a Save Button so save edited record
    edit_btn = Button(editor, text="Eintrag speichern", command=update)
    edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)



# Create function to Delete a Record
def delete():
    #databases
    conn = sqlite3.connect("address_book.db")
    #creating a cursor
    c = conn.cursor()

    # delete a record
    c.execute("DELETE from addresses WHERE oid = " + delete_box.get())

    delete_box.delete(0, END)

    #commit changes
    conn.commit()
    #close connection
    conn.close()




#submit function for db:
def submit():
    #databases
    conn = sqlite3.connect("address_book.db")
    #creating a cursor
    c = conn.cursor()

    #insert into table
    c.execute("INSERT INTO addresses VALUES (:f_name, :l_name, :address, :city, :state, :zipcode)",
            {
                'f_name': f_name.get(),
                'l_name': l_name.get(),
                'address': address.get(),
                'city': city.get(),
                'state': state.get(),
                'zipcode': zipcode.get()
            })

    #commit changes
    conn.commit()
    #close connection
    conn.close()

    # Clear the text boxes
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)

# create query function
def query():

    #databases
    conn = sqlite3.connect("address_book.db")
    #creating a cursor
    c = conn.cursor()

    # Query the database
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()


    # loop thru results
    print_records = "REGISTRIERTE BENUTZER: \n\n"
    for record in records:
        print_records += str(record[0]) + " " + str(record[1]) + " " + "\t" + str(record[6]) + "\n"
    
    query_label = Label(root, text=print_records).grid(row=12, column=0, columnspan=2)


    #commit changes
    conn.commit()
    #close connection
    conn.close()


#creating textboxes:

f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20, pady=(10, 0))

l_name = Entry(root, width=30)
l_name.grid(row=1, column=1)

address = Entry(root, width=30)
address.grid(row=2, column=1)

city = Entry(root, width=30)
city.grid(row=3, column=1)

state = Entry(root, width=30)
state.grid(row=4, column=1)

zipcode = Entry(root, width=30)
zipcode.grid(row=5, column=1)

delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1)



#Create text box labes
f_name_label = Label(root, text="Vorname")
f_name_label.grid(row=0, column=0)

l_name_label = Label(root, text="Nachname")
l_name_label.grid(row=1, column=0, pady=(3, 0))

address_label = Label(root, text="Addresse")
address_label.grid(row=2, column=0)

city_label = Label(root, text="Stadt")
city_label.grid(row=3, column=0)

state_label = Label(root, text="Kanton")
state_label.grid(row=4, column=0)

zipcode_label = Label(root, text="Postleizahl")
zipcode_label.grid(row=5, column=0)

delete_box_label = Label(root, text="Eintrag wählen über ID").grid(row=9, column=0)



#Create Submit Button
submit_btn = Button(root, text="Eintrag zur Datenbank hinzufügen", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=88)


#create a query button
query_btn = Button(root, text="Zeige Einträge", command=query).grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=140)

#Create a Delete Button

delete_btn = Button(root, text="Eintrag Löschen", command=delete)
delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=135)

# create an update Button

edit_btn = Button(root, text="Eintrag bearbeiten", command=edit)
edit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=130)


#commit changes
conn.commit()


#close connection
conn.close()


root.mainloop()
