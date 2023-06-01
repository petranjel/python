import psycopg2
import tkinter as tk
from tkinter import ttk

main_color = "#bffcce"
db_table='pokladna'
db_columns='description,value_data,c_time,row_id'
connection_string=()
           
def config(): #Creating new server config - only if doesnt exist
    def set_server_config():
        global connection_string
        host='host='+"'"+entry_host.get()+"' "
        dbname='dbname='+"'"+entry_dbname.get()+"' "
        user='user='+"'"+entry_user.get()+"' "
        password='password='+"'"+entry_password.get()+"' "
        config_frame.destroy()
        value=host+dbname+user+password
        connection_string=value
        with open('server_config.txt','w',encoding='utf-8') as write_cfg:
            write_cfg.write(value)
    config_frame=tk.Tk()
    config_frame.geometry ('400x200')
    config_frame.config (background=main_color)
    config_frame.title ('server_config')
    label_host=tk.Label(config_frame,text='Host:')
    label_host.grid(column=1,row=1)
    label_dbname=tk.Label(config_frame,text='Database name:')
    label_dbname.grid(column=1,row=2)
    label_user=tk.Label(config_frame,text='User:')
    label_user.grid(column=1,row=3)
    label_password=tk.Label(config_frame,text='Password:')
    label_password.grid(column=1,row=4)
    entry_host=tk.Entry(config_frame)
    entry_host.grid(column=2,row=1)
    entry_host.insert(0,'localhost')
    entry_dbname=tk.Entry(config_frame)
    entry_dbname.grid(column=2,row=2)
    entry_dbname.insert(0,'name')
    entry_user=tk.Entry(config_frame)
    entry_user.grid(column=2,row=3)
    entry_user.insert(0,'postgres')
    entry_password=tk.Entry(config_frame)
    entry_password.grid(column=2,row=4)
    entry_password.insert(0,'password')
    ok_button=tk.Button(config_frame,text='OK',command=set_server_config)
    ok_button.grid(column=2,row=5)
    config_frame.mainloop()

try: #appent connecting string from text document
    with open('server_config.txt','r',encoding='utf-8') as read_cfg:
        for value in read_cfg:
            connection_string=value    
except: print('open connection string error')
#If server_config.txt doesnt exist, activate creating new config
if connection_string == ():
    config()
else: pass


frame_main = tk.Tk ()
frame_main.geometry ('600x400')
frame_main.config (background=main_color)
frame_main.title ('in_title')

frame_one=tk.Frame (frame_main,background=main_color)
frame_two=tk.Frame (frame_main,background=main_color)
frame_three = tk.Frame (frame_main,background=main_color)
frame_one.pack ()
frame_two.pack ()
frame_three.pack ()

def link_up(): # Connect to your database and create cursor
    global conn,cursor
    conn=psycopg2.connect(connection_string)
    cursor=conn.cursor()
def link_down(): # Close connection and cursor - must by after any operation with dababase
    conn.close()
    cursor.close()
def add_event (): # Add row into database table and treewiev 
    def add_end_event ():
        description_get=field_description.get()
        value_get=field_value.get()
        link_up()
        cursor.execute (            
            "INSERT INTO "+db_table(db_columns)+" VALUES (%s,%s,NOW())",(description_get,value_get)
        ) #description_data,value_data,create_time - names of columns in yor database table - your_sql_table_name
        conn.commit ()
        link_down()
        field_description.destroy ()
        field_value.destroy ()
        button_ready.destroy ()
    def cancel():
        field_description.destroy()
        field_value.destroy()
        button_ready.destroy()
        button_cancel.destroy()
    field_description = tk.Entry (frame_two,width=40,textvariable=tk.StringVar)
    field_value = tk.Entry (frame_two,width=15,textvariable=tk.StringVar)
    button_ready = tk.Button (frame_two,text=('Add new'),background='#59c919',command=add_end_event)
    button_cancel = tk.Button (frame_two,text=('Cancel'),background='#59c919',command=cancel)
    button_cancel.grid (column=5,row=2,sticky='n')
    field_description.grid (column=1,row=2,sticky='n')
    field_value.grid (column=3,row=2,sticky='n')
    button_ready.grid (column=4,row=2,sticky='n')
def repair_event(): # Update/repair row in database table and treewiev
    def repair_end_event():
        selected_item = tree.focus()
        column_value=tree.item(selected_item,)['values']
        description_get=field_description.get()
        value_get=field_value.get()
        tree.item(selected_item,values=(description_get,value_get,column_value[2]))
        link_up()
        cursor.execute (
            "UPDATE "+db_table+" SET description=%s,value_data=%s WHERE description=%s AND value_data=%s AND c_time=%s",(description_get,value_get,column_value[0],column_value[1],column_value[2])
        ) #description_data,value_data,create_time - names of columns in yor database table - your_sql_table_name
        conn.commit ()
        link_down()
        field_description.destroy ()
        field_value.destroy ()
        button_ready.destroy ()
    def cancel():
        field_description.destroy()
        field_value.destroy()
        button_ready.destroy()
        button_cancel.destroy()
    field_description = tk.Entry (frame_two, width=40,textvariable=tk.StringVar)
    field_value = tk.Entry (frame_two,width=15,textvariable=tk.StringVar)
    button_ready = tk.Button (frame_two,text=('Repair'),background='#59c919',command=repair_end_event)
    button_cancel = tk.Button (frame_two,text=('Cancel'),background='#59c919',command=cancel)
    button_cancel.grid (column=5,row=2,sticky='n')
    field_description.grid (column=1,row=2,sticky='n')
    field_value.grid (column=3,row=2,sticky='n')
    button_ready.grid (column=4,row=2,sticky='n')
def delete_event(): # Remove row from database table and treewiev
    selected_item = tree.focus()
    column_value=tree.item(selected_item,)['values']
    tree.delete(selected_item)
    link_up()
    cursor.execute (
        "DELETE FROM "+db_table+" WHERE description=%s AND value_data=%s AND c_time=%s",(column_value[0],column_value[1],column_value[2])
    ) #description_data,value_data,create_time - names of columns in yor database table - your_sql_table_name
    conn.commit ()
    link_down()

#First select form table
link_up()
cursor.execute("SELECT * FROM "+db_table)
rows=cursor.fetchall()
link_down()
#Create and setup treewiev
tree = ttk.Treeview(frame_three, column=("c1", "c2", "c3"), show='headings')
tree.column("c1", anchor=tk.CENTER,)
tree.heading("c1", text="Description")
tree.column("c2", anchor=tk.CENTER)
tree.heading("c2", text="Value")
tree.column("c3", anchor=tk.CENTER)
tree.heading("c3", text="Date")
tree.tag_configure('positive',background='#76ff76')
tree.tag_configure('negative', background='#f66')
tree.grid(column=0,row=0)
#Make tag for any row in treewiev - if row in column2 is negative value intiger/float, row will have red background
for row in rows:
    state_value = 'positive' if row[1] >=0 else 'negative'
    tree.insert ("",tk.END,values=row,tags=state_value)
#Create buttons for functions
button_add= tk.Button (frame_one,text=('Add'),background='#59c919',width=6,height=3, command=add_event)
button_add.grid (column=0,row=0,padx=5,pady=5,ipadx=3)
button_repair= tk.Button (frame_one,text=('Repair'),background='#59c919',width=6,height=3, command=repair_event)
button_repair.grid (column=1,row=0,padx=5,pady=5,ipadx=3)
button_delete= tk.Button (frame_one,text=('Delete'),background='#59c919',width=6,height=3, command=delete_event)
button_delete.grid (column=2,row=0,padx=5,pady=5,ipadx=3)

frame_main.mainloop ()