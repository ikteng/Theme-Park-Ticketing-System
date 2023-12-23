from tkinter import *
from tkinter import messagebox
# importing DateEntry from tkcalendar, you need to install tkcalendar-> pip install tkcalendar
from tkcalendar import DateEntry
from datetime import date
import sqlite3
import random
import string
from PIL import ImageTk, Image

# defining main window, geometry, and title
top = Tk()
top.title('Main Menu')

# connecting to database
conn = sqlite3.connect('ticket_booking_database.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS ticket (name TEXT, ticket_id TEXT PRIMARY KEY, ticket_date TEXT, number_of_ticket TEXT, total_price TEXT)")

# fetching database
cursor.execute('SELECT * FROM ticket')
tickets = cursor.fetchall()

# getting all tickets id
tickets_id = []
for i in tickets:
  tickets_id.append(i[1]) 

conn.commit() 

# display image
image = Image.open("C:\Python_Project\projects\PortAventuraSpainthemepark-5a34558bc7822d003737f9c9.jpg")
resized_image=image.resize((1000,275))
img=ImageTk.PhotoImage(resized_image)
#Label(top,image=img).grid(row=4,column=0,columnspan=2)
Label(top, image = img).place(x = 0,y = 0) 

Label(top, text='Welcome to SuperFun Theme Park', font=('Arial', 30), relief="solid",borderwidth=1,bg='#D2E5F6',padx=5,pady=5).grid(row=0, column=0, columnspan=2, padx=80, pady=10)
# ticketing maintenance
Label(top, text='Ticketing maintenance', font=('Arial', 20), relief="solid",borderwidth=1,bg='#D2E5F6',padx=5, pady=5).grid(row=1, column=0, padx=5,pady=5,columnspan=2)    
# new ticket transaction
Button(top, text='New Ticket Transaction', font=('Arial', 14), fg='black', command=lambda:NewTicket(), bg='#D2E5F6').grid(row=2, column=0,padx=5,pady=5)
# modify an existing ticket transaction
Button(top, text='Modify an existing ticket transaction', font=('Arial', 14), fg='black', command=lambda:ModifyTicket(), bg='#D2E5F6').grid(row=2, column=1,padx=5,pady=5)
# view all ticket transactions
Button(top, text='View All Ticket Transactions', font=('Arial', 14), fg='black', command=lambda:ViewTickets(), bg='#D2E5F6').grid(row=3, column=0,padx=5,pady=5)
# delete ticket transactions
Button(top, text='Delete Ticket Transaction', font=('Arial', 14), fg='black', command=lambda:DeleteTicket(), bg='#D2E5F6').grid(row=3, column=1,padx=5,pady=5)

#quit
Button(top, text='Exit', font=('Arial', 14), fg='black', command=lambda:top.destroy(), bg='#D2E5F6').grid(row=5, column=0,padx=5,pady=5,columnspan=2)

# defining functions
# this function will be used to show messages and errors
def show_message(title, message):
    messagebox.showerror(title, message)
    
# create random ticket id
def get_random_string():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(8))
  
# create a new ticket
def NewTicket():
    top1 = Tk()
    top1.title('New Ticket Transaction')
    today_date=date.today()
    name = StringVar(top1)
    ticket_id = StringVar(top1)
    ticket_date = StringVar(top1)
    ticket_date.set(today_date)
    number_of_ticket = StringVar(top1)
    
    # check whether the unique ticket id already exist in database
    while True:
        global tickets_id
        t_id = get_random_string()
        if t_id not in tickets_id: #if t_id is unique
            ticket_id.set(get_random_string()) # set t_id as the ticket_id
            break
        continue
    
    # confirm function to insert information to database
    def confirm():
        # validation
        if len(name.get())<=0 or not name.get().isalpha():
            show_message('Error', 'Invalid Name')
            name.set("")
            return

        if len(ticket_date.get())<7:
            show_message('Error','Invalid date')
            ticket_date.set("")
            return

        if int(number_of_ticket.get())<=0 or not number_of_ticket.get().isdigit():
            show_message('Error', 'Invalid Number of Ticket')
            number_of_ticket.set("")
            return

        top1.destroy()
        try:
            conn = sqlite3.connect("ticket_booking_database.db")
            cursor = conn.cursor()
            total_price=int(number_of_ticket.get())*100 # price of each ticket is $100
            cursor.execute("INSERT INTO ticket (name, ticket_id, ticket_date, number_of_ticket, total_price) VALUES (?, ?, ?, ?, ?)", 
                           (str(name.get()), str(ticket_id.get()), str(ticket_date.get()), str(number_of_ticket.get()), str(total_price)))
            conn.commit()
            show_message('Successful', 'Your booking is successful, your ticket id is {}\nTotal price: {}'.format(ticket_id.get(),total_price))
            top1.destroy()
        except sqlite3.Error as e:
            show_message('Error', e)
        finally:
            conn.close()
    
    Label(top1, text='Enter details', font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=10, columnspan=2)
    Label(top1, text='Name: ', font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
    Entry(top1, textvariable=name).grid(row=1, column=1)
    Label(top1, text='Ticket ID: ', font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
    Entry(top1, textvariable=ticket_id, state='disabled').grid(row=2, column=1)
    Label(top1, text='Ticket Date: ', font=('Arial', 12)).grid(row=3, column=0, padx=10, sticky='w', pady=10)
    DateEntry(top1,selectmode='day', textvariable=ticket_date).grid(row=3, column=1)
    Label(top1, text='Number of Ticket: ', font=('Arial', 12)).grid(row=4, column=0, padx=10, pady=10, sticky='w')
    Entry(top1, textvariable=number_of_ticket).grid(row=4, column=1)
    Button(top1, text='Confirm', bg='green', fg='white', font=('Arial', 17), command=lambda: confirm()).grid(row=5,column=1, pady=10)

# modify a ticket
def ModifyTicket():
    top2 = Tk()
    top2.title('Modifying a Ticket Transaction')

    # display the headers
    Label(top2, text='Customer Name', font=('Arial', 12), borderwidth=1, relief="solid", width=20).grid(row=0, column=0, pady=10)
    Label(top2, text='Ticket ID', font=('Arial', 12), borderwidth=1, relief="solid", width=20).grid(row=0, column=1, pady=10)
    Label(top2, text='Ticket Date', font=('Arial', 12), borderwidth=1, relief="solid", width=20).grid(row=0, column=2, pady=10)
    Label(top2, text='Number of Ticket', font=('Arial', 12), borderwidth=1, relief="solid", width=20).grid(row=0, column=3, pady=10)
    Label(top2, text='Total Price', font=('Arial', 12), borderwidth=1, relief="solid", width=20).grid(row=0, column=4, pady=10)
    
    # display the ticket transactions to modify
    cursor.execute('SELECT * FROM ticket')
    tickets = cursor.fetchall()
    for i in range(len(tickets)):
        Label(top2, text=tickets[i][0], borderwidth=1, relief="solid", width=20).grid(row=i+1,  column=0)
        Label(top2, text=tickets[i][1], borderwidth=1, relief="solid", width=20).grid(row=i+1,  padx=10, column=1)
        Label(top2, text=tickets[i][2], borderwidth=1, relief="solid", width=20).grid(row=i+1,  padx=10, column=2)
        Label(top2, text=tickets[i][3], borderwidth=1, relief="solid", width=20).grid(row=i+1,  padx=10, column=3)
        Label(top2, text=tickets[i][4], borderwidth=1, relief="solid", width=20).grid(row=i+1,  padx=10, column=4)
        Button(top2, text='Modify', command=lambda current_id=tickets[i][1]: modify_rows(top2,current_id)).grid(row=i+1, column=5)
    
    top2.mainloop()
    conn.close()

def modify_rows(top2,current_id):
    top2.destroy()
    top5 = Tk()
    top5.title('Modifying Ticket Transaction')

    name = StringVar(top5)
    ticket_id = StringVar(top5)
    ticket_date = StringVar(top5)
    today_date=date.today()
    number_of_ticket = StringVar(top5)

    # get data of the selected ticket transactions
    cursor.execute('SELECT * FROM ticket where ticket_id=?', (current_id,))
    tickets = cursor.fetchall()
    for i in range(len(tickets)):
       current_name=tickets[i][0]
       current_date=tickets[i][2]
       current_tickets=tickets[i][3]
    
    # set the orignal data into the fields
    name.set(current_name)
    ticket_id.set(current_id)
    ticket_date.set(current_date)
    number_of_ticket.set(current_tickets)

    #display the fields
    Label(top5, text='Ticket ID: ', font=('Arial', 15)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    Entry(top5, textvariable=ticket_id, state='disabled').grid(row=0, column=1)
    Label(top5, text='Name: ', font=('Arial', 15)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
    Entry(top5, textvariable=name).grid(row=1, column=1)
    Label(top5, text='Ticket Date: ', font=('Arial', 15)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
    DateEntry(top5, selectmode='day', textvariable=ticket_date).grid(row=2, column=1)
    Label(top5, text='Number of Tickets: ', font=('Arial', 15)).grid(row=3, column=0, padx=10, pady=10, sticky='w')
    Entry(top5, textvariable=number_of_ticket).grid(row=3, column=1)
    Button(top5, text='Confirm', bg='green', fg='white', font=('Arial', 15), command=lambda: confirm()).grid(row=4,column=0, pady=10)

    # update the ticket transaction
    def confirm():
        # validation
        if len(name.get())<=0 or not name.get().isalpha():
            show_message('Error', 'Invalid Name')
            name.set("")
            return

        if len(ticket_date.get())<7:
            show_message('Error','Invalid date')
            ticket_date.set("")
            return

        if int(number_of_ticket.get())<=0 or not number_of_ticket.get().isdigit():
            show_message('Error', 'Invalid Number of Ticket')
            number_of_ticket.set("")
            return

        top5.destroy()
        try:
            conn = sqlite3.connect("ticket_booking_database.db")
            cursor = conn.cursor()
            total_price=int(number_of_ticket.get())*100
            cursor.execute("UPDATE ticket SET name=?,ticket_date=?,number_of_ticket=?,total_price=? WHERE ticket_id=?", 
                            (str(name.get()),str(ticket_date.get()),str(number_of_ticket.get()),str(total_price),(current_id),))
            conn.commit()
            show_message('Success', 'Ticket updated')
            conn.close()
        except sqlite3.Error as e:
            show_message('Sqlite error', e)
        finally:
            conn.close()
            conn = sqlite3.connect('ticket_booking_database.db')
            cursor = conn.cursor()
        
# display all booked tickets 
def ViewTickets():
    top3 = Tk()
    top3.title('View All Ticket Transactions')
    
    # display headers
    Label(top3, text='Customer Name', font=('Arial', 12), borderwidth=1, relief="solid", width=20).grid(row=0, column=0, pady=10)
    Label(top3, text='Ticket ID', font=('Arial', 12), borderwidth=1, relief="solid", width=20).grid(row=0, column=1, pady=10)
    Label(top3, text='Ticket Date', font=('Arial', 12), borderwidth=1, relief="solid", width=20).grid(row=0, column=2, pady=10)
    Label(top3, text='Number of Tickets', font=('Arial', 12), borderwidth=1, relief="solid", width=20).grid(row=0, column=3, pady=10)
    Label(top3, text='Total Price', font=('Arial', 12), borderwidth=1, relief="solid", width=20).grid(row=0, column=4, pady=10)
    
    conn = sqlite3.connect('ticket_booking_database.db')
    cursor = conn.cursor()

    # display ticket transactions
    cursor.execute('SELECT * FROM ticket')
    tickets = cursor.fetchall()
    for i in range(len(tickets)):
        Label(top3, text=tickets[i][0], borderwidth=1, relief="solid", width=20).grid(row=i+1, column=0)
        Label(top3, text=tickets[i][1], borderwidth=1, relief="solid", width=20).grid(row=i+1, padx=10, column=1)
        Label(top3, text=tickets[i][2], borderwidth=1, relief="solid", width=20).grid(row=i+1, padx=10, column=2)
        Label(top3, text=tickets[i][3], borderwidth=1, relief="solid", width=20).grid(row=i+1, padx=10, column=3)
        Label(top3, text=tickets[i][4], borderwidth=1, relief="solid", width=20).grid(row=i+1, padx=10, column=4)
    top3.mainloop()
    conn.close()

# delete a ticket
def DeleteTicket():
    top4 = Tk()
    top4.title('Deleting a Ticket Transaction')
    
    # display the headers
    Label(top4, text='Customer Name', font=('Arial', 12), borderwidth=1, relief="solid", width=20).grid(row=0, column=0, pady=10)
    Label(top4, text='Ticket ID', font=('Arial', 12), borderwidth=1, relief="solid", width=20).grid(row=0, column=1, pady=10)
    Label(top4, text='Ticket Date', font=('Arial', 12), borderwidth=1, relief="solid", width=20).grid(row=0, column=2, pady=10)
    Label(top4, text='Number of Ticket', font=('Arial', 12), borderwidth=1, relief="solid", width=20).grid(row=0, column=3, pady=10)
    Label(top4, text='Total Price', font=('Arial', 12), borderwidth=1, relief="solid", width=20).grid(row=0, column=4, pady=10)
    
    # delete the ticket in the database
    def delete_rows(ticket_id):
        top4.destroy()
        try:
            conn = sqlite3.connect("ticket_booking_database.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ticket WHERE ticket_id = ?", (ticket_id,))
            conn.commit()
            show_message('Success', 'Ticket deleted')
            conn.close()
        except sqlite3.Error as e:
            show_message('Sqlite error', e)
        finally:
            conn.close()
    conn = sqlite3.connect('ticket_booking_database.db')
    cursor = conn.cursor()

    # display the ticket transactions
    cursor.execute('SELECT * FROM ticket')
    tickets = cursor.fetchall()
    for i in range(len(tickets)):
        Label(top4, text=tickets[i][0], borderwidth=1, relief="solid", width=20).grid(row=i+1,  column=0)
        Label(top4, text=tickets[i][1], borderwidth=1, relief="solid", width=20).grid(row=i+1,  padx=10, column=1)
        Label(top4, text=tickets[i][2], borderwidth=1, relief="solid", width=20).grid(row=i+1,  padx=10, column=2)
        Label(top4, text=tickets[i][3], borderwidth=1, relief="solid", width=20).grid(row=i+1,  padx=10, column=3)
        Label(top4, text=tickets[i][3], borderwidth=1, relief="solid", width=20).grid(row=i+1,  padx=10, column=4)
        Button(top4, text='Delete', command=lambda current_id=tickets[i][1]: delete_rows(current_id)).grid(row=i+1, column=5)
    top4.mainloop()
    conn.close()

# mainloop
top.mainloop()