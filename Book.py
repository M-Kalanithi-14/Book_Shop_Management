import tkinter as tk, datetime as dt, matplotlib.pyplot as plt, os, Main# , Selling
from tkinter import messagebox
from random import shuffle
from tempfile import mktemp
from tkinter import ttk
from sys import platform
#from os import startfile

try : import pymysql as cntr
except ImportError : import mysql.connector as cntr

if platform == "linux" :
        db=cntr.connect(host="localhost",user="kalanithi",password="manager",database="book")
else :
    db=cntr.connect(host="localhost",user="root",password="manager",database="book")
    
cur = db.cursor()

#============================ Number to Words ====================================

def no_to_words(n) :    
    ones = {'0' : '' , '1' : ' One ' , '2' : ' Two ' ,
            '3' : ' Three ' , '4' : ' Four ' , '5' : ' Five ' ,
            '6' : ' Six ' , '7' : ' Seven ' , '8' : ' Eight ' , '9' : ' Nine '}
    tens = {'0' : ' Ten' , '1' : ' Eleven' , '2' : ' Twelve' , 
            '3' : ' Thirteen' , '4' : ' Fourteen' , '5' : ' Fifteen' , 
            '6' : ' Sixteen' , '7' : ' Seventeen' , '8' : ' Eighteen' , '9' : ' Nineteen'}
    decades = {'0' : '' , '2' : 'Twenty' ,
            '3' : ' Thirty' , '4' : ' Forty' , '5' : ' Fifty' ,
            '6' : ' Sixty' , '7' : ' Seventy' , '8' : ' Eighty' , '9' : ' Ninety'}
    hundreds = {'0' : '' , '1' : 'One hundred and' , '2' : 'Two hundred and' , 
                '3' : 'Three hundred and' , '4' : 'Four hundred and' , '5' : 'Five hundred and' ,
                '6' : 'Six hundred and' , '7' : 'Seven hundred and' , '8' : 'Eight hundred and' , 
                '9' : 'Nine hundred and'}
    comma_word = {'3' : ' Thousand, ' , '5' : 'Lakh' , '6' : 'Million, ' , '7' : 'Crore' , '9' : 'Billion, '}
    
    int_n_orig = ''    
    L1 = n.split(',')
    for i in L1 : int_n_orig += i
    int_n = int_n_orig[:-3]
    
    word = ''        
    len_int = len(int_n)
    change = 3
    
    while len_int > 0 :
        if n == 0 :
            word = 'zero'
            break
        if int_n[len_int-2] == '1' :
            for digit in tens :
                if int_n[len_int-1] == digit :
                    word = tens[digit] + word
        else :
            for digit_1 in ones :
                if int_n[len_int-1] == digit_1 :
                    word = ones[digit_1] + word
            if len_int > 1 :
                for digit_2 in decades :
                    if int_n[len_int-2] == digit_2 :
                        word = decades[digit_2] + word
        if len_int > 2 :
            for digit_3 in hundreds :
                if int_n[len_int-3] == digit_3 :
                    word = hundreds[digit_3] + word
        if len_int > 3 :
            word = comma_word[str(change)] + word
            
        change += 3
        len_int -= 3        
        
    return word + " Rupees Only"

#============================= Indian System of Currency =========================

def Ind_System(Rs) :
    index_deci = Rs.find('.')
    len_Rs = len(Rs[: index_deci])
    
    if len_Rs == 4 or len_Rs == 5 :
        if len_Rs == 4 :
            return str(Rs[0] + ',' + Rs[1:])
        elif len_Rs == 5 :
            return str(Rs[0:2] + ',' + Rs[2:])
    elif len_Rs == 6 or len_Rs == 7 :
        if len_Rs == 6 :
            return str(Rs[0] + ',' + Rs[1:3] + ',' + Rs[3:])
        elif len_Rs == 7 :
            return str(Rs[0:2] + ',' + Rs[2:4] + ',' + Rs[4:])

#============================= Date Modification ==================================

def date_mod() :
    Today = dt.date.today()
    if Today.month == 1 : Month = 'Jan'
    elif Today.month == 2 : Month = 'Feb'
    elif Today.month == 3 : Month = 'Mar'
    elif Today.month == 4 : Month = 'Apr'
    elif Today.month == 5 : Month = 'May'
    elif Today.month == 6 : Month = 'Jun'
    elif Today.month == 7 : Month = 'Jul'
    elif Today.month == 8 : Month = 'Aug'
    elif Today.month == 9 : Month = 'Sep'
    elif Today.month == 10 : Month = 'Oct'
    elif Today.month == 11 : Month = 'Nov'
    elif Today.month == 12 : Month = 'Dec'
    
    if len(str(Today.day)) == 1 : Day = '0' + str(Today.day)
    else : Day = str(Today.day)
    
    return Day + '-' + Month + ', ' + str(Today.year)

#============================= Bill No Generation =================================

def Bill_No() :
    L1 = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
          'N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    shuffle(L1)
    Bill_No = L1[0] + str(unique_id())
    
    return Bill_No

#============================= Unique ID Generation ===============================

def unique_id() :
    cur.execute("select max(book_id) from stock;")
    L1 = list(cur.fetchall())
    if any(L1[0]) :
        L2 = [i for i in range((L1[0][0]) , (L1[0][0] + 10000))]
        shuffle(L2)
        return L2.pop(0)
    else : return 1
    
#===================================== Displaying Graph ====================================

def View_Sales() :   
    root_vs = tk.Tk()
    root_vs.title("View Sales")
    #root_vs.iconbitmap("icon.ico")
    
    #================================= Variables =================================
    
    month = tk.StringVar(root_vs)
    year = tk.IntVar(root_vs)
    year.initialize(dt.date.today().year)
    
    #================================= Widgets ===================================
    
    lblMonth = tk.Label(root_vs , font = ('arial' , 16 , 'bold') ,
                                 text = 'Month')
    lblMonth.grid(row = 0 , column = 0)
    CboMonth = ttk.Combobox(root_vs , font = ('arial' , 16 , 'bold') , textvariable = month,
                               state = 'readonly')
    months = ['' , 'January' , 'February' , 'March' , 'April' , 'May' , 'June',
                        'July' , 'August' , 'September' , 'October' , 'November' , 'December']
    CboMonth['value'] = months
    CboMonth.current(0)
    CboMonth.grid(row = 0 , column = 1)
    
    lblYear = tk.Label(root_vs , font = ('arial' , 16 , 'bold') ,
                                 text = 'Year')
    lblYear.grid(row = 0 , column = 2)
    txtYear = tk.Entry(root_vs , font = ('arial' , 13 , 'bold') , width = 10 ,
                                 textvariable = year , bd = 7 ,
                                 insertwidth = 2 , state = 'disabled')
    txtYear.grid(row = 0 , column = 3)
    
    #=================================== Functions ===================================
    
    is_leapyear = lambda year : (year % 4 == 0)
    
    def last_date(month , year) :
        if month == 2 and is_leapyear(year) : return '29'
        elif month == 2 : return '28'
        elif month in (4,6,9,11) : return '30'
        else : return '31'    

    def get_month() :
        if month.get() == '' : return None            
        elif month.get() == 'January' : return '01'
        elif month.get() == 'February' : return '02'
        elif month.get() == 'March' : return '03'
        elif month.get() == 'April' : return '04'
        elif month.get() == 'May' : return '05'
        elif month.get() == 'June' : return '06'
        elif month.get() == 'July' : return '07'
        elif month.get() == 'August' : return '08'
        elif month.get() == 'September' : return'09'
        elif month.get() == 'October' : return '10'
        elif month.get() == 'November' : return '11'
        else : return '12'        
    
    def plot() :
        if not bool(get_month()) :
            messagebox.showerror("View Sales" , "You Haven't Choosen ANY MONTH!!! Please Choose ANY ONE.")
        else :
            count = 0
            D1 = {}
            cur.execute(f"""select * from purchase
                        where Date between '2020-{get_month()}-01' and '2020-{get_month()}-{last_date(get_month() , year.get())}'""")
            L1 = cur.fetchall()
            for i in L1 :
                for j in i :
                    for k in i :
                        if j == k : count += 1
                    else :
                        cur.execute(f"""select book_name from stock
                                    where book_id = {j}""")
                        L2 = cur.fetchall()
                        D1[L2[0][0]] = count
                        count = 0
            L1 = D1.keys()
            L2 = D1.values()
            plt.bar(L1 , L2)
            plt.title(f"Sales as of {month.get()}, {year.get()}")
            #plt.xticks(L1)
            plt.xlabel("Books")
            plt.ylabel("Sales")
            plt.show()
        
    #================================== Buttons ===================================    
     
    btnView = tk.Button(root_vs , font=('arial', 16, 'bold'),
                         text='OK' , command = plot)
    btnView.grid(row = 1 , column = 0)
    
    btnCan = tk.Button(root_vs , font=('arial', 16, 'bold'),
                 text='Cancel' , command = root_vs.destroy)
    btnCan.grid(row = 1 , column = 2)
    
    root_vs.mainloop()
    
#======================================== Stock =============================================


def Stock():
    Quit = lambda event : root.destroy()
    
    root = tk.Tk()
    root.title('Stock Details')
    #root.iconbitmap("icon.ico")
    root.geometry(f'{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0')
    root.resizable(False,False)
    root.bind("<Control_L><q>" , Quit)
    
    iDate = tk.StringVar()
    iDate.set(dt.date.today())       
    
    BookID = tk.IntVar()
    BookID.initialize(unique_id())
    
    Bookname = tk.StringVar()
    Author = tk.StringVar()
    Publisher = tk.StringVar()        
    Qty = tk.IntVar()       
    Rate = tk.DoubleVar()
    Tot = tk.DoubleVar()                    
    
    #=================================== Functions ===========================
    
    def back() :
        root.destroy()
        Main.Selling()    
    
    def disp() :
        cur.execute("select * from stock;")
        L1 = cur.fetchall()
        T1 = ()        
        if any(L1) : 
            for i in L1 : 
                T1 += (f"{i[0]}\t\t {i[1]}\t\t\t {i[2]}\t\t\t {i[3]}\t\t\t\t {i[5]}\t\t {i[6]}\n" + '-'.center(316 , '-') + '\n',)
        return T1
    
    def PRINT() :
        root_pwd = tk.Tk()
        root_pwd.group()            
        #root_pwd.iconbitmap("icon.ico")
        
        pwd = tk.StringVar(root_pwd)
        
        lblPassword = tk.Label(root_pwd , font = ('arial' , 16 , 'bold'),
                                text = 'Enter admin password' , bd = 7)
        lblPassword.grid(row = 0 , column = 0)
        txtPassword = tk.Entry(root_pwd , font = ('arial' , 16 , 'bold'),
                                bd = 7 , textvariable = pwd , insertwidth = 3)
        txtPassword.grid(row = 0 , column = 1)
        
        def Print() :
            cur.execute(f"select * from users where password = '{pwd.get()}';")
            if any(cur.fetchall()) :
                q = txtReceipt.get('1.0' , 'end-1c')
                filename = mktemp('.txt')
                open(filename , 'w').write(q)
                #os.startfile(filename , 'print')
            else : messagebox.showerror('Print All' , "You've entered the WRONG password!!  Please recheck it.")
            
        btnOk = tk.Button(root_pwd , font=('arial', 16, 'bold'),
                        text='OK' , command = Print)
        btnOk.grid(row = 1 , column = 0)
        
        btnCan = tk.Button(root_pwd , font=('arial', 16, 'bold'),
                        text='Cancel' , command = root_pwd.destroy)
        btnCan.grid(row = 1 , column = 1)
        
        root_pwd.mainloop()           
        
    def iRESET() :
        BookID.set(unique_id())
        Bookname.set('')
        Author.set('')
        Publisher.set('')            
        Qty.set(0)            
        Rate.set(0.0)
        Tot.set(0.0)
                    
        txtReceipt.delete('1.0','end')
        txtReceipt.insert('end' , ('-'.center(316 , '-') + '\n'))
        txtReceipt.insert('end' , 'Book ID\t\t Book Name\t\t\t Author\t\t\t Publisher\t\t\t Available Stock\t\t\t Rate Of Each\n')
        txtReceipt.insert('end' , ('-'.center(316 , '-') + '\n'))        
        for i in disp() : txtReceipt.insert('end' , i)
        
    def RESET():
        jRESET = messagebox.askyesno('Book Shop Management' , 'Do you want to reset ?')
        if jRESET > 0 : 
            iRESET()
            return           
        
    def RECEIPT() :            
        txtReceipt.insert('end' , f"{BookID.get()}\t\t {Bookname.get()}\t\t\t {Author.get()}\t\t\t \
                        {Publisher.get()}\t\t\t {iDate.get()}\t\t\t {Qty.get()}\t\t\t {Rate.get()}\t\t\t\n")
        txtReceipt.insert('end' , ('-'.center(316 , '-') + '\n'))
        cur.execute(f"insert into stock values \
                    ({BookID.get()},'{Bookname.get()}','{Author.get()}',\
                    '{Publisher.get()}','{iDate.get()}',{Qty.get()}, {Rate.get()});")
        db.commit()            
        messagebox.showinfo('Stock Details' , 'Data Inserted Successfully')
        iRESET()       
    
    def update() :
        root_update = tk.Tk()    
        root_update.title("Update An Existing Stock")
        #root_update.iconbitmap("icon.ico")
        
        #================================== Variables =========================    
        
        BID = tk.IntVar(root_update)
        
        #================================== Widgets ===========================   
        
        lblBookID = tk.Label(root_update , font = ('arial' , 16 , 'bold') ,
                                    text = 'Book ID' , bd = 7)
        lblBookID.grid(row = 1 , column = 0 , sticky = 'n')        
        txtBookID = tk.Entry(root_update , font = ('arial' , 13 , 'bold') ,
                                    textvariable = BID , bd = 7 , insertwidth = 2)
        txtBookID.grid(row = 1 , column = 1)   
        
        #============================== Checking, Updating And Exit Functions =============
        
        def Update() :
            root_update.destroy()
            root_upd = tk.Tk()
            root_upd.title("Update Stock")
            #root_upd.iconbitmap("icon.ico")
            
            #==================================== Variables ======================        
            
            Estock = tk.IntVar(root_upd)              
            Estock.initialize(L1[0][5])
            
            Nstock = tk.IntVar(root_upd)
            
            #================================ Widgets ============================
            
            lblExist_stock = tk.Label(root_upd , font = ('arial' , 16 , 'bold') ,
                                text = 'Existing Stock' , bd = 7)
            lblExist_stock.grid(row = 0 , column = 0 , sticky = 'n')        
            txtExist_stock = tk.Entry(root_upd , font = ('arial' , 13 , 'bold') ,
                                        textvariable = Estock , bd = 7 , insertwidth = 2 , state = 'disabled')
            txtExist_stock.grid(row = 0 , column = 1)
            
            
            lblNew_stock = tk.Label(root_upd , font = ('arial' , 16 , 'bold') ,
                                        text = 'Newly Bought Stock' , bd = 7)
            lblNew_stock.grid(row = 1 , column = 0 , sticky = 'n')        
            txtNew_stock = tk.Entry(root_upd , font = ('arial' , 13 , 'bold') ,
                                        textvariable = Nstock , bd = 7 , insertwidth = 2)
            txtNew_stock.grid(row = 1 , column = 1)
            
            #================================ Ok and Exit functions ==================
            
            def ok() :
                cur.execute(f"""update stock 
                            set book_stock = book_stock + {Nstock.get()} 
                            where book_id = {L1[0][0]}""")
                db.commit()
                messagebox.showinfo("Update Stock" , "Stock UPDATED SUCCESSFULLY !!!")
                root_upd.destroy()
                root_update.destroy()
                
                txtReceipt.delete('1.0','end')
                txtReceipt.insert('end' , ('-'.center(316 , '-') + '\n'))
                txtReceipt.insert('end' , 'Book ID\t\t Book Name\t\t\t Author\t\t\t Publisher\t\t\t Available Stock\t\t\t Rate Of Each\n')
                txtReceipt.insert('end' , ('-'.center(316 , '-') + '\n'))        
                for i in disp() : txtReceipt.insert('end' , i)
                
            def Exit() :    
                iExit = messagebox.askyesno('Register' , 'Do you want to quit ?')
                if iExit > 0 : 
                    root_upd.destroy()
                    return
            
            #=============================== Buttons =================================
            
            btnok = tk.Button(root_upd , font = ('arial' , 16 , 'bold') , text = 'Update' , command = ok, bd=7)
            btnok.grid(row = 2 , column = 0)
            
            btnEXIT = tk.Button(root_upd , font = ('arial' , 16 , 'bold') , text = 'Exit' , command = Exit, bd=7)
            btnEXIT.grid(row = 2 , column = 1)
        
            root_upd.mainloop()
            
        def check() :
            global L1
            
            if (not bool(BID.get())) : 
                messagebox.showerror("Update Stock" , "You Haven't ENTERED the Book's ID!!! Please Enter it.")
            else :
                cur.execute(f"select * from stock where book_id = {BID.get()}")
                L1 = cur.fetchall()
                if any(L1) : Update()
                else : messagebox.showinfo("Update Stock" , "No Such Book Exists in Stock!!!")
        
        def Exit() :    
            iExit = messagebox.askyesno('Register' , 'Do you want to quit ?')
            if iExit > 0 : 
                root_update.destroy()
                return
        
        #=================================== Buttons ==================================
        
        btnCheck = tk.Button(root_update , font = ('arial' , 16 , 'bold') , text = 'Check' , command = check, bd=7)
        btnCheck.grid(row = 4 , column = 0)
        
        btnExit = tk.Button(root_update , font = ('arial' , 16 , 'bold') , text = 'Exit' , command = Exit, bd=7)
        btnExit.grid(row = 4 , column = 4)
        
        root_update.mainloop()
        
    #update()
    
    #=================================== Widgets =============================        
    
    Mainframe = tk.Frame(root)
    Mainframe.grid()
    
    Tops = tk.Frame(Mainframe , bd = 10 , relief = 'ridge')
    Tops.pack(side = 'top')
    
    lblTitle = tk.Label(Tops , width = 30 , font = ('arial' , 40 , 'bold') ,
                                text = 'Stock Details' , justify = 'center')
    lblTitle.grid(padx = 150)
    
    Membername = tk.LabelFrame(Mainframe , bd = 10 , width = 1300 , height = 300 ,
                                font = ('arial' , 12 , 'bold') , text = 'Add a new Book' , relief = 'ridge')
    Membername.pack(padx = 38 , side = 'top')
    
    ReceiptButtonFrame = tk.LabelFrame(Mainframe , bd = 10 , width = 2000 , height = 200 ,
                                        font = ('arial' , 12 , 'bold') , text = 'Stock Details' , relief = 'ridge')
    ReceiptButtonFrame.pack(padx = 38 , side = 'top')        
    
    #================================== Widgets ==============================        
    
    lblBookID = tk.Label(Membername , font = ('arial' , 16 , 'bold') ,
                                text = 'Book Id')
    lblBookID.grid(row = 0 , column = 0 , sticky = 'n')        
    txtBookID = tk.Entry(Membername , font = ('arial' , 13 , 'bold') ,
                                textvariable = BookID , bd = 7 , insertwidth = 2 , state = 'disabled')
    txtBookID.grid(row = 0 , column = 1)
    
    
    lblBookName = tk.Label(Membername , font = ('arial' , 16 , 'bold') ,
                                text = 'Book Name' , bd = 7)
    lblBookName.grid(row = 1 , column = 0 , sticky = 'n')        
    txtBookName = tk.Entry(Membername , font = ('arial' , 13 , 'bold') ,
                                textvariable = Bookname , bd = 7 , insertwidth = 2)
    txtBookName.grid(row = 1 , column = 1)
    
    
    lblAuthor = tk.Label(Membername , font = ('arial' , 16 , 'bold') ,
                                text = 'Author' , bd = 7)
    lblAuthor.grid(row = 2 , column = 0 , sticky = 'n')        
    txtAuthor = tk.Entry(Membername , font = ('arial' , 13 , 'bold') ,
                                textvariable = Author , bd = 7 , insertwidth = 2)
    txtAuthor.grid(row = 2 , column = 1)
    
    
    lblPublisher = tk.Label(Membername , font = ('arial' , 16 , 'bold') ,
                                text = 'Publisher' , bd = 7)
    lblPublisher.grid(row = 3 , column = 0 , sticky = 'n')        
    txtPublisher = tk.Entry(Membername , font = ('arial' , 13 , 'bold') ,
                                textvariable = Publisher , bd = 7 , insertwidth = 2)
    txtPublisher.grid(row = 3 , column = 1)
    
    
    lblQuantity = tk.Label(Membername , font = ('arial' , 16 , 'bold') ,
                                text = 'Qty No' , bd = 7)
    lblQuantity.grid(row = 0 , column = 2 , sticky = 'n')        
    txtQuantity = tk.Entry(Membername , font = ('arial' , 13 , 'bold') ,
                                textvariable = Qty , bd = 7 , insertwidth = 2)
    txtQuantity.grid(row = 0 , column = 3)
            
    
    lblRateOfEach = tk.Label(Membername , font = ('arial' , 16 , 'bold') ,
                                text = 'Rate Of Each' , bd = 7)
    lblRateOfEach.grid(row = 1 , column = 2 , sticky = 'n')        
    txtRateOfEach = tk.Entry(Membername , font = ('arial' , 13 , 'bold') ,
                                textvariable = Rate , bd = 7 , insertwidth = 2)
    txtRateOfEach.grid(row = 1 , column = 3)        
    
    
    lblTotalAmount = tk.Label(Membername , font = ('arial' , 16 , 'bold') ,
                                text = 'Total Amount' , bd = 7)
    lblTotalAmount.grid(row = 2 , column = 2 , sticky = 'n')        
    txtTotalAmount = tk.Entry(Membername , font = ('arial' , 13 , 'bold') ,
                                textvariable = Tot , bd = 7 , insertwidth = 2 , state = 'disabled')
    txtTotalAmount.grid(row = 2 , column = 3)
    
                    
    lblDate = tk.Label(Membername , font = ('arial' , 16 , 'bold') ,
                                text = 'Date' , bd = 7)
    lblDate.grid(row = 3 , column = 2 , sticky = 'n')        
    txtDate = tk.Entry(Membername , font = ('arial' , 13 , 'bold') ,
                                textvariable = iDate , bd = 7 , insertwidth = 2 , state = 'disabled')
    txtDate.grid(row = 3 , column = 3)
    
    #=========================================================================     
    
    txtReceipt = tk.Text(ReceiptButtonFrame , width = 181 , height = 20 , font = ('arial' , 10 , 'bold'))
    txtReceipt.grid(row = 0 , column = 0 , columnspan = 4)
    txtReceipt.insert('end' , ('-'.center(316 , '-') + '\n'))
    txtReceipt.insert('end' , 'Book ID\t\t Book Name\t\t\t Author\t\t\t Publisher\t\t\t Date Of Purchase\t\t\t Quantity\t\t\t Rate\n')
    txtReceipt.insert('end' , ('-'.center(316 , '-') + '\n'))
    for i in disp() :                    
        txtReceipt.insert('end' , i)

    #============================================== Buttons ==================        
    
    btnGo_Back = tk.Button(Membername, bd = 5, 
                                font = ('arial' , 16 , 'bold') , text = '<< Go Back' , command = back)    
    btnGo_Back.grid(row = 4 , column = 0)
    
    btnReceipt = tk.Button(Membername, bd = 5,
                                font = ('arial' , 16 , 'bold') , text = 'Receipt' , command = RECEIPT)    
    btnReceipt.grid(row = 4 , column = 1)
    
    btnPrint = tk.Button(Membername, bd = 5,
                                font = ('arial' , 16 , 'bold') , text = 'Print All' , command = PRINT)    
    btnPrint.grid(row = 4 , column = 2)
    
    btnReset = tk.Button(Membername, bd = 5, 
                                font = ('arial' , 16 , 'bold') , text = 'Reset' , command = RESET)    
    btnReset.grid(row = 4 , column = 3)
    
    btnUpdate = tk.Button(Membername, bd = 5, 
                                font = ('arial' , 16 , 'bold') , text = 'Update An Existing Stock' , command = update)    
    btnUpdate.grid(row = 4 , column = 4)
    
    btnView_Sales = tk.Button(Membername, bd = 5, 
                                font = ('arial' , 16 , 'bold') , text = 'View Sales' , command = View_Sales)    
    btnView_Sales.grid(row = 4 , column = 5)

    root.mainloop()

#Stock()    