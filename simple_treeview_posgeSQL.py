import psycopg2
import tkinter as tk
from tkinter import ttk

frame_main = tk.Tk ()
frame_main.geometry ('600x400')
frame_main.config (background="#bffcce")
frame_main.title ('name_in_title')

main_color = "#bffcce"

frame_one=tk.Frame (frame_main,background=main_color)
frame_two=tk.Frame (frame_main,background=main_color)
frame_three = tk.Frame (frame_main,background=main_color)
frame_one.pack ()
frame_two.pack ()
frame_three.pack ()

def add_event ():
    def add_end_event ():
        conn=psycopg2.connect (
            host= "localhost",          #way to your database
            database="xxx",             #name your databese
            user="user",                
            password="your_passworld"
        )
        description_get=field_description.get()
        value_get=field_value.get()
        cursor=conn.cursor ()
        cursor.execute (            
            "INSERT INTO your_sql_table_name (description_data,value_data,create_time) VALUES (%s,%s,NOW())",(description_get,value_get)
        ) #description_data,value_data,create_time - names of columns in yor database table - your_sql_table_name
        conn.commit ()
        cursor.close()
        conn.close()
        print(conn.closed)
        field_description.destroy ()
        field_value.destroy ()
        button_ready.destroy ()
        
    field_description = tk.Entry (frame_two,width=40,textvariable=tk.StringVar)
    field_value = tk.Entry (frame_two,width=15,textvariable=tk.StringVar)
    button_ready = tk.Button (frame_two,text=('Hotovo'),background='#59c919',command=add_end_event)
    field_description.grid (column=1,row=2,sticky='n')
    field_value.grid (column=3,row=2,sticky='n')
    button_ready.grid (column=4,row=2,sticky='n')

def repair_event():
    def repair_end_event():
        conn=psycopg2.connect (
            host= "localhost",          #way to your database
            database="xxx",             #name your databese
            user="user",                
            password="your_passworld"
        )
        selected_item = tree.focus()
        column_value=tree.item(selected_item,)['values']
        print (selected_item)
        description_get=field_description.get()
        value_get=field_value.get()
        tree.item(selected_item,values=(description_get,value_get,column_value[2]))
        cursor=conn.cursor ()
        cursor.execute (
            "UPDATE your_sql_table_name SET description_data=%s,value_data=%s WHERE description_data=%s AND value_data=%s AND create_time=%s",(description_get,value_get,column_value[0],column_value[1],column_value[2])
        ) #description_data,value_data,create_time - names of columns in yor database table - your_sql_table_name
        conn.commit ()
        cursor.close()
        conn.close()
        print(conn.closed)
        field_description.destroy ()
        field_value.destroy ()
        button_ready.destroy ()
        
    field_description = tk.Entry (frame_two, width=40,textvariable=tk.StringVar)
    field_value = tk.Entry (frame_two,width=15,textvariable=tk.StringVar)
    button_ready = tk.Button (frame_two,text=('Hotovo'),background='#59c919',command=repair_end_event)
    field_description.grid (column=1,row=2,sticky='n')
    field_value.grid (column=3,row=2,sticky='n')
    button_ready.grid (column=4,row=2,sticky='n')

def delete_event():
    conn=psycopg2.connect (
            host= "localhost",          #way to your database
            database="xxx",             #name your databese
            user="user",                
            password="your_passworld"
        )
    selected_item = tree.focus()
    column_value=tree.item(selected_item,)['values']
    tree.delete(selected_item)
    print (selected_item)
    cursor=conn.cursor ()
    cursor.execute (
        "DELETE FROM your_sql_table_name WHERE description_data=%s AND value_data=%s AND create_time=%s",(column_value[0],column_value[1],column_value[2])
    ) #description_data,value_data,create_time - names of columns in yor database table - your_sql_table_name
    conn.commit ()
    cursor.close()
    conn.close()
    print(conn.closed)

conn=psycopg2.connect (
        host= "localhost",          #way to your database
        database="xxx",             #name your databese
        user="user",                
        password="your_passworld"
    )
cursor=conn.cursor ()
cursor.execute("SELECT * FROM your_sql_table_name ;")
vysledky=cursor.fetchall()
tree = ttk.Treeview(frame_three, column=("c1", "c2", "c3"), show='headings')
tree.column("#1", anchor=tk.CENTER,)
tree.heading("#1", text="Description")
tree.column("#2", anchor=tk.CENTER)
tree.heading("#2", text="Value")
tree.column("#3", anchor=tk.CENTER)
tree.heading("#3", text="Date")
tree.tag_configure('positive',background='#76ff76')
tree.tag_configure('negative', background='#f66')
tree.grid(column=0,row=0)
for row in vysledky:
    state_value = 'positive' if row[1] >=0 else 'negative'
    tree.insert ("",tk.END,values=row,tags=state_value)
cursor.close ()
conn.close ()

button_add= tk.Button (frame_one,text=('Add'),background='#59c919',width=6,height=3, command=add_event)
button_add.grid (column=0,row=0,padx=5,pady=5,ipadx=3)
button_add= tk.Button (frame_one,text=('Repair'),background='#59c919',width=6,height=3, command=repair_event)
button_add.grid (column=1,row=0,padx=5,pady=5,ipadx=3)
button_add= tk.Button (frame_one,text=('Delete'),background='#59c919',width=6,height=3, command=delete_event)
button_add.grid (column=2,row=0,padx=5,pady=5,ipadx=3)

print(conn.closed)

frame_main.mainloop ()