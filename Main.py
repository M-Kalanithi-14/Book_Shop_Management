import tkinter as tk, datetime as dt, Book, os#, docx as dc
from tkinter import messagebox
from tempfile import mktemp
from importlib import reload
from sys import platform
#from os import startfile

try : import pymysql as cntr
except ImportError : import mysql.connector as cntr

if platform == "linux" :
        db=cntr.connect(host="localhost",user="kalanithi",password="manager",database="book")
else :
    db=cntr.connect(host="localhost",user="root",password="manager",database="book")
cur = db.cursor()

def Selling() :
    Quit = lambda event : root.destroy()

    root = tk.Tk()
    root.title('Book Shop Management')
    #root.iconbitmap("icon.ico")
    root.geometry(f'{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0')
    root.resizable(False,False)    
    root.bind("<Control_L><q>" , Quit)

    iDate = tk.StringVar()
    iDate.set(dt.date.today())

    BookID = tk.IntVar()

    Bookname = tk.StringVar()
    Author = tk.StringVar()
    Publisher = tk.StringVar()
    Qty = tk.IntVar()
    Rate = tk.DoubleVar()
    Tot = tk.DoubleVar()

    #=================================== Functions ===========================

    def view_stock() :
        root.destroy()
        Book.Stock()

    def check(event) :
        if bool(BookID.get()) :
            cur.execute(f"select * from stock where book_id = {BookID.get()}")
            L1 = cur.fetchall()
            if any(L1) :
                Bookname.set(L1[0][1])
                Author.set(L1[0][2])
                Publisher.set(L1[0][3])
                Rate.set(L1[0][6])
                txtQuantity.configure(state='normal')
            else :
                messagebox.showerror("Book Shop Management" , f"No Such a Book is in STOCK with the ID : {BookID.get()}")
        else :
            messagebox.showerror("Book Shop Management" , "You Haven't Entered any Book's ID.")

    def add() :
        net = str(round(Qty.get() * Rate.get() , 2))
        Tot.set(round(Tot.get() + eval(net) , 2))

        new_rate = str(Rate.get())
        index_deci_rate = new_rate.find('.') + 1
        if len(new_rate[index_deci_rate:]) == 1 : new_rate += '0'

        index_deci_net = net.find('.') + 1
        if len(net[index_deci_net:]) == 1 : net += '0'

        NoS_Name = (52 - (len(str(Qty.get())) - 1)) - len(Bookname.get())
        NoS_Qty = 12 - len(new_rate[-3::-1])
        NoS_Rate = (12 - (len(net[index_deci_net:]) - 1)) - len(net[-3::-1])

        txtReceipt.insert(5.0 , (f"{Bookname.get()}" +
                                " " * NoS_Name +
                                f"{Qty.get()}" +
                                " " * NoS_Qty +
                                f"{new_rate}" +
                                " " * NoS_Rate + f"{net}\n"))

    def iRESET() :
        BookID.set(0)
        Bookname.set('')
        Author.set('')
        Publisher.set('')
        lblQuantity.config(state="disabled")
        Qty.set(0)
        Rate.set(0.0)
        Tot.set(0.0)

        txtReceipt.delete('1.0','end')
        txtReceipt.insert('end' , "PARTICLULARS\t\t\t\tQuantity      Rate        Net\n")
        txtReceipt.insert('end' , "\t\t\t\t\t\t     Amount\n")
        txtReceipt.insert('end' , ('-'.center(316 , '-') + '\n\n\n'))
        txtReceipt.insert('end' , ('-'.center(316 , '-') + '\n\n\n'))

    def RESET():
        jRESET = messagebox.askyesno('Book Shop Management' , 'Do you want to reset ?')
        if jRESET > 0 :
            iRESET()
            return

    def RECEIPT() :
        Billno = Book.Bill_No()

        cur.execute(f"""insert into purchase values({BookID.get()} , '{iDate.get()}');""")
        cur.execute(f"""update stock
                    set book_stock = book_stock - 1
                    where book_id = {BookID.get()}""")
        db.commit()

        messagebox.showinfo('Stock Details' , 'Books Sold Successfully!!! Now Printing...')
        data = txtReceipt.get(4.0 , 'end-320c')

        SubTotal = str(Tot.get())
        index_deci = SubTotal.find('.') + 1
        if len(SubTotal[index_deci:]) == 1 : SubTotal += '0'
        NoS_SubTotal = 12 - len(SubTotal[-3::-1])

        roundoff = eval(SubTotal[index_deci:])
        NoS_roundoff = 18 - (len(str(roundoff)) + 7)

        TotalAmt = str(eval(SubTotal) - eval("0." + str(roundoff))) + "0"
        Total = Book.Ind_System(TotalAmt)
        NoS_Total = 12 - len(Total[-3::-1])

        Total_words = Book.no_to_words(Total)
        '''
        filename = mktemp('.txt')
        file = open(filename , 'w')
        '''
        file = open("Receipt.txt" , 'w')
        file.write("\t\t\t\tSainik Book Shop\n\n")
        file.write("\t\t\tAmaravathinagar, Tiruppur; PIN => 642102\n\n\n")
        file.write(f"Bill No.: {Billno}\t\t\t\t\t\t     Date : {Book.date_mod()}\n\n")
        file.write(('-'.center(80 , '-') + '\n'))
        file.write("PARTICULARS\t\t\t\t\tQuantity      Rate        Net\n")
        file.write("\t\t\t\t\t\t\t\t\t Amount\n")
        file.write(('-'.center(80 , '-') + '\n\n'))
        file.write(f"{data}\n")
        file.write(('-'.center(80 , '-') + '\n'))
        file.write((" " * 50) + "Sub Total : " + " " * NoS_SubTotal + f"Rs. {SubTotal}\n")
        file.write((" " * 50) + "Round Off : " + " " * NoS_roundoff + f"-Rs. 0.{roundoff}\n")
        file.write(('-'.center(80 , '-') + '\n\n'))
        file.write((" " * 54) + "Total : " + " " * NoS_Total + f"Rs. {Total}\n\n")
        file.write(('-'.center(80 , '-') + '\n\n'))
        file.write(f"Amount in Words : {Total_words}\n")
        file.write(18 * " " + "_" * (len(Total_words)) + '\n\n')
        file.write("\t\t\tThank You, Have a Nice Day!!!")
        '''
        doc = dc.Document()

        doc.add_paragraph("\t\t\t\tSainik Book Shop\n\n")
        doc.add_paragraph("\t\t\tAmaravathinagar, Tiruppur; PIN => 642102\n\n\n")
        doc.add_paragraph("Bill No.: {}\t\t\t\t\t\tDate : {}\n\n".format(Billno , Book.date_mod()))
        doc.add_paragraph(('-'.center(80 , '-') + '\n'))
        doc.add_paragraph("PARTICULARS\t\t\t\t\tQuantity      Rate        Net\n")
        doc.add_paragraph("\t\t\t\t\t\t\t\t\t Amount\n")
        doc.add_paragraph(('-'.center(80 , '-') + '\n\n'))
        doc.add_paragraph("{}\n".format(data))
        doc.add_paragraph(('-'.center(80 , '-') + '\n'))
        doc.add_paragraph((" " * NoS_Total) + "Total : Rs. {}\n\n".format(Total))
        doc.add_paragraph(NoS_Total_Words * " " + "Amount in Words : {}\n\n".format(Total_words))
        doc.add_paragraph("\t\t\tThank You, Have a Nice Day!!!")

        doc.save("Receipt.docx")
        '''
        #startfile(filename , 'print')

        txtReceipt.delete('1.0','end')
        txtReceipt.insert('end' , "PARTICLULARS\t\t\t\tQuantity      Rate        Net\n")
        txtReceipt.insert('end' , "\t\t\t\t\t\t     Amount\n")
        txtReceipt.insert('end' , ('-'.center(316 , '-') + '\n\n\n'))
        txtReceipt.insert('end' , ('-'.center(316 , '-') + '\n\n\n'))

        iRESET()

    #=================================== Widgets =============================

    Mainframe = tk.Frame(root)
    Mainframe.grid()

    Tops = tk.Frame(Mainframe , bd = 10 , relief = 'ridge')
    Tops.pack(side = 'top')

    lblTitle = tk.Label(Tops , width = 30 , font = ('arial' , 40 , 'bold') ,
                                text = 'Sell A Book' , justify = 'center')
    lblTitle.grid(padx = 150)

    Membername = tk.LabelFrame(Mainframe , bd = 10 , width = 1300 , height = 300 ,
                                font = ('arial' , 12 , 'bold') , text = 'Book Details' , relief = 'ridge')
    Membername.pack(padx = 38 , side = 'top')

    ReceiptButtonFrame = tk.LabelFrame(Mainframe , bd = 10 , width = 2000 , height = 200 ,
                                        font = ('arial' , 12 , 'bold') , text = 'Stock Details' , relief = 'ridge')
    ReceiptButtonFrame.pack(padx = 38 , side = 'top')

    #================================== Widgets ==============================

    lblBookID = tk.Label(Membername , font = ('arial' , 16 , 'bold') , \
                                text = 'Book Id' , bd = 7)
    lblBookID.grid(row = 0 , column = 0 , sticky = 'n')
    txtBookID = tk.Entry(Membername , font = ('arial' , 13 , 'bold') , \
                                textvariable = BookID , bd = 7 , insertwidth = 2)
    txtBookID.bind("<Return>" , check)
    txtBookID.grid(row = 0 , column = 1)

    lblBookName = tk.Label(Membername , font = ('arial' , 16 , 'bold') , \
                                text = 'Book Name' , bd = 7)
    lblBookName.grid(row = 1 , column = 0 , sticky = 'n')
    txtBookName = tk.Entry(Membername , font = ('arial' , 13 , 'bold') , \
                                textvariable = Bookname , bd = 7 , insertwidth = 2, state = 'disabled')
    txtBookName.grid(row = 1 , column = 1)

    lblAuthor = tk.Label(Membername , font = ('arial' , 16 , 'bold') , \
                                text = 'Author' , bd = 7)
    lblAuthor.grid(row = 2 , column = 0 , sticky = 'n')
    txtAuthor = tk.Entry(Membername , font = ('arial' , 13 , 'bold') , \
                                textvariable = Author , bd = 7 , insertwidth = 2, state = 'disabled')
    txtAuthor.grid(row = 2 , column = 1)

    lblPublisher = tk.Label(Membername , font = ('arial' , 16 , 'bold') , \
                                text = 'Publisher' , bd = 7)
    lblPublisher.grid(row = 3 , column = 0 , sticky = 'n')
    txtPublisher = tk.Entry(Membername , font = ('arial' , 13 , 'bold') , \
                                textvariable = Publisher , bd = 7 , insertwidth = 2, state = 'disabled')
    txtPublisher.grid(row = 3 , column = 1)


    lblQuantity = tk.Label(Membername , font = ('arial' , 16 , 'bold') , \
                                text = 'Qty No' , bd = 7)
    lblQuantity.grid(row = 0 , column = 2 , sticky = 'n')
    txtQuantity = tk.Spinbox(Membername , font = ('arial' , 13 , 'bold') , \
                                textvariable = Qty , bd = 7 , insertwidth = 2, from_=1, to=20, state = 'disabled')
    txtQuantity.grid(row = 0 , column = 3)

    #================================== Widgets ==============================

    lblRateOfEach = tk.Label(Membername , font = ('arial' , 16 , 'bold') , \
                                text = 'Rate Of Each' , bd = 7)
    lblRateOfEach.grid(row = 1 , column = 2 , sticky = 'n')
    txtRateOfEach = tk.Entry(Membername , font = ('arial' , 13 , 'bold') , \
                                textvariable = Rate , bd = 7 , insertwidth = 2, state = 'disabled')
    txtRateOfEach.grid(row = 1 , column = 3)
    
    lblTotalAmount = tk.Label(Membername , font = ('arial' , 16 , 'bold') , \
                                text = 'Total Amount' , bd = 7)
    lblTotalAmount.grid(row = 2 , column = 2 , sticky = 'n')
    txtTotalAmount = tk.Entry(Membername , font = ('arial' , 13 , 'bold') , \
                                textvariable = Tot , bd = 7 , insertwidth = 2 , state = 'disabled')
    txtTotalAmount.grid(row = 2 , column = 3)

    lblDate = tk.Label(Membername , font = ('arial' , 16 , 'bold') , \
                                text = 'Date' , bd = 7)
    lblDate.grid(row = 3 , column = 2 , sticky = 'n')
    txtDate = tk.Entry(Membername , font = ('arial' , 13 , 'bold') , \
                                textvariable = iDate , bd = 7 , insertwidth = 2 , state = 'disabled')
    txtDate.grid(row = 3 , column = 3)

    #============================== Textbox ===========================================

    txtReceipt = tk.Text(ReceiptButtonFrame , width = 181 , height = 20 , font = ('arial' , 10 , 'bold'))
    txtReceipt.grid(row = 0 , column = 0 , columnspan = 4)
    txtReceipt.insert('end' , "PARTICLULARS\t\t\t\tQuantity      Rate        Net\n")
    txtReceipt.insert('end' , "\t\t\t\t\t\t     Amount\n")
    txtReceipt.insert('end' , ('-'.center(316 , '-') + '\n\n\n'))
    txtReceipt.insert('end' , ('-'.center(316 , '-') + '\n\n\n'))

    #============================================== Buttons ==================

    btnAdd = tk.Button(Membername, bd = 5, #bg='#ff0000',
                                font = ('arial' , 16 , 'bold') , text = 'Add' , command = add)    
    btnAdd.grid(row = 5 , column = 0)

    btnReceipt = tk.Button(Membername, bd = 5,
                                font = ('arial' , 16 , 'bold') , text = 'Receipt' , command = RECEIPT)    
    btnReceipt.grid(row = 5 , column = 1)

    btnReset = tk.Button(Membername, bd = 5,
                                font = ('arial' , 16 , 'bold') , text = 'Reset' , command = RESET)    
    btnReset.grid(row = 5 , column = 2)

    btnStock = tk.Button(Membername, bd = 5,
                                font = ('arial' , 16 , 'bold') , text = 'View Stock' , command = view_stock)    
    btnStock.grid(row = 5 , column = 3)

    reload(Book)

    btnSales = tk.Button(Membername, bd = 5,
                                font = ('arial' , 16 , 'bold') , text = 'View Sales' , command = Book.View_Sales)    
    btnSales.grid(row = 5 , column = 4)    

    root.mainloop()    

Selling()

#=================================================================================
'''
def register(root) :
    root.destroy()

    root_reg = tk.Tk()
    root_reg.title("Register")
    #root_reg.iconbitmap("icon.ico")
    root_reg.group()

    name = tk.StringVar(root_reg)
    Phone = tk.IntVar(root_reg)
    username = tk.StringVar(root_reg)
    password = tk.StringVar(root_reg)
    password2 = tk.StringVar(root_reg)

    #===================================== Widgets ===============================

    lblName = tk.Label(root_reg , font = ('arial' , 16 , 'bold') ,
                           text = 'Enter Full Name : ')
    lblName.grid(row = 0 , column = 0)
    txtName  = tk.Entry(root_reg , font = ('arial' , 13 , 'bold') , bd = 7,
                            textvariable = name , insertwidth = 2)
    txtName.grid(row = 0 , column = 2)

    lblPhone = tk.Label(root_reg , font = ('arial' , 16 , 'bold') ,
                           text = 'Enter Phone No : ')
    lblPhone.grid(row = 2 , column = 0)
    txtPhone = tk.Entry(root_reg , font = ('arial' , 13 , 'bold') , bd = 7,
                            textvariable = Phone , insertwidth = 2)
    txtPhone.grid(row = 2 , column = 2)

    lblUsername = tk.Label(root_reg , font = ('arial' , 16 , 'bold') ,
                           text = 'Enter Username : ')
    lblUsername.grid(row = 4 , column = 0)
    txtUsername  = tk.Entry(root_reg , font = ('arial' , 13 , 'bold') , bd = 7,
                            textvariable = username , insertwidth = 2)
    txtUsername.grid(row = 4 , column = 2)

    lblPassword = tk.Label(root_reg , font = ('arial' , 16 , 'bold') ,
                           text = 'Enter Password : ')
    lblPassword.grid(row = 6 , column = 0)
    txtPassword  = tk.Entry(root_reg , font = ('arial' , 13 , 'bold') , bd = 7,
                            textvariable = password , insertwidth = 2 , show = '*')
    txtPassword.grid(row = 6 , column = 2)

    lblPassword2 = tk.Label(root_reg , font = ('arial' , 16 , 'bold') ,
                           text = 'Confirm Password : ')
    lblPassword2.grid(row = 8 , column = 0)
    txtPassword2 = tk.Entry(root_reg , font = ('arial' , 13 , 'bold') , bd = 7,
                            textvariable = password2 , insertwidth = 2 , show = '*')
    txtPassword2.grid(row = 8 , column = 2)

    #==================================== Inserting Data into MySQL ==============

    def reg() :
        if name.get() == '' :
            txtName.configure(bg = 'red' , fg = 'white')
            messagebox.showerror("Register" , "You've left the Name field EMPTY!!!  All fields are MUST.")
        elif Phone.get() == '' :
            txtPhone.configure(bg = 'red' , fg = 'white')
            messagebox.showerror("Register" , "You've left the Phone No field EMPTY!!!  All fields are MUST.")
        elif username.get() == '' :
            txtUsername.configure(bg = 'red' , fg = 'white')
            messagebox.showerror("Register" , "You've left the Username field EMPTY!!!  All fields are MUST.")
        elif password.get() == '' :
            txtPassword.configure(bg = 'red' , fg = 'white')
            messagebox.showerror("Register" , "You've left the Password field EMPTY!!!  All fields are MUST.")
        elif password2.get() == '' :
            txtPassword2.configure(bg = 'red' , fg = 'white')
            messagebox.showerror("Register" , "You've left the Password Confirmation field EMPTY!!!  All fields are MUST.")
        else :
            if password.get() == password2.get() :
                if password.get() != 'admin@123' :
                    cur.execute(f"insert into users values('{name.get()}' , {Phone.get()} , '{username.get()}' , '{password.get()}');")
                    db.commit()
                    messagebox.showinfo("Register" , "You've been REGISTERED Successfully.")
                    login(root_reg)
                else :
                    messagebox.showerror("Register" , "This Password is INVALID!!!  Please Enter a DIFFERENT Password")
                    password.set("")
                    password2.set("")
            else : messagebox.showerror("Register" , "You've Entered DIFFERENT Passwords!!")

    def Exit() :
        iExit = messagebox.askyesno('Register' , 'Do you want to quit ?')
        if iExit > 0 :
            root_reg.destroy()
            return

    def back() :
        root_reg.destroy()
        main()

    #==================================== Buttons ================================

    btnBack = tk.Button(root_reg , font=('arial', 16, 'bold'), text='<< Go Back' , command = back , bd = 7)
    btnBack.grid(row = 10 , column=0)

    btnRegister = tk.Button(root_reg , font=('arial', 16, 'bold'),
                         text='Register' , command = reg , bd = 7)
    btnRegister.grid(row=10, column=2)

    btnExit = tk.Button(root_reg , font=('arial', 16, 'bold'), text='Exit' , command = Exit , bd = 7)
    btnExit.grid(row = 10, column = 4)

    root_reg.mainloop()

#=================================================================================

def login(root) :
    root.destroy()

    root_login = tk.Tk()
    root_login.title("Login")
    #root_login.iconbitmap("icon.ico")
    root_login.group()


    username = tk.StringVar(root_login)
    password = tk.StringVar(root_login)

    #====================================== Widgets ==============================

    lblUsername = tk.Label(root_login , font = ('arial' , 16 , 'bold') ,
                           text = 'Enter Username')
    lblUsername.grid(row = 0 , column = 0)
    txtUsername  = tk.Entry(root_login , font = ('arial' , 13 , 'bold') , bd = 7,
                            textvariable = username , insertwidth = 2)
    txtUsername.grid(row = 0 , column = 2)

    lblPassword = tk.Label(root_login , font = ('arial' , 16 , 'bold') ,
                           text = 'Enter Password')
    lblPassword.grid(row = 2 , column = 0)
    txtPassword  = tk.Entry(root_login , font = ('arial' , 13 , 'bold') , bd = 7,
                            textvariable = password , insertwidth = 2 , show = '*')
    txtPassword.grid(row = 2 , column = 2)

    #==================================== Fetching Data from MySQL ===============

    def LOGIN() :
        if username.get() == '' :
            txtUsername.configure(bg = 'red' , fg = 'white')
            messagebox.showerror("Login" , "You've left the Username field EMPTY!!!  All fields are MUST.")
        elif password.get() == '' :
            txtPassword.configure(bg = 'red' , fg = 'white')
            messagebox.showerror("Login" , "You've left the Password field EMPTY!!!  All fields are MUST.")
        else :
            cur.execute(f"select * from users where username = '{username.get()}' and password = '{password.get()}';")
            L1 = cur.fetchall()
            if any(L1) :
                root_login.destroy()
                Selling()
            else : messagebox.showerror("Login" , "Such a User DOESNOT Exist!!   Please REGISTER Your")


    def Exit() :
        iExit = messagebox.askyesno('Login' , 'Do you want to quit ?')
        if iExit > 0 :
            root_login.destroy()
            return

    def back() :
        root_login.destroy()
        main()

    #==================================== Buttons ================================

    btnBack = tk.Button(root_login , font=('arial', 16, 'bold'), text='<< Go Back' , command = back , bd = 7)
    btnBack.grid(row = 4 , column=0)

    btnLogin = tk.Button(root_login , font=('arial', 16, 'bold'), text='Login' , command = LOGIN , bd = 7)
    btnLogin.grid(row=4, column=2)

    btnExit = tk.Button(root_login , font=('arial', 16, 'bold'), text='Exit' , command = Exit , bd = 7)
    btnExit.grid(row = 4 , column = 4)
    
    root_login.mainloop()

#=================================================================================

def main() :
    root = tk.Tk()
    root.title("Book Shop Management")
    #root.iconbitmap("icon.ico")
    root.geometry("575x170")
    root.group()
    #root.configure(bgpic = 'icon.ico')

    #============================= Buttons and Widgets ===========================

    lbltitle = tk.Label(root , font = ('Times new Roman' , 24 , 'bold') ,
                           text = '                Welcome To')
    lbltitle.grid(row = 0 , column = 0)

    lbltitle2 = tk.Label(root , font = ('Times new Roman' , 24 , 'bold') ,
                           text = '               Book Shop Management\n')
    lbltitle2.grid(row = 1 , column = 0)

    btnRegister = tk.Button(root , font=('arial', 16, 'bold'), text='Register' , command = lambda : register(root) , bd = 7)
    btnRegister.grid(row = 2 , column = 0 , sticky = 'w')

    btnLogin = tk.Button(root , font=('arial', 16, 'bold'), text='Login' , command = lambda : login(root) ,
                         bd = 7 , width = 6)
    btnLogin.grid(row=2 , column=1 , sticky = 'w')

    root.mainloop()
main()
'''