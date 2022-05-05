from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image # "pip install Pillow"
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="db_praktikum"
)

dbcursor = mydb.cursor()

root = Tk()
root.title("Praktikum DPBO")


# Fungsi untuk mengambil data
def getMhs():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM mahasiswa")
    result = dbcursor.fetchall()

    return result

def getFasilitas():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM fasilitas")
    result = dbcursor.fetchall()

    return result


# Window Input Data
def inputs():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Input")
    dframe = LabelFrame(top, text="Input Data Mahasiswa", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)
    # Input 1
    label1 = Label(dframe, text="Nama Mahasiswa").grid(row=0, column=0, sticky="w")
    input_nama = Entry(dframe, width=30)
    input_nama.grid(row=0, column=1, padx=20, pady=10, sticky="w")
    # Input 2
    label2 = Label(dframe, text="NIM").grid(row=1, column=0, sticky="w")
    input_nim = Entry(dframe, width=30)
    input_nim.grid(row=1, column=1, padx=20, pady=10, sticky="w")
    # Input 3
    options = ["Filsafat Meme", "Sastra Mesin", "Teknik Kedokteran", "Pendidikan Gaming"]
    input_jurusan = StringVar(root)
    input_jurusan.set(options[0])
    label4 = Label(dframe, text="Jurusan").grid(row=2, column=0, sticky="w")
    input4 = OptionMenu(dframe, input_jurusan, *options)
    input4.grid(row=2, column=1, padx=20, pady=10, sticky='w')
    #input 4
    r = StringVar()
    r.set("Laki-laki")
    radio = [
        ("Laki-laki", "Laki-laki"),
        ("Perempuan", "Perempuan")
    ]

    label5 = Label(dframe, text="Jenis Kelamin").grid(row=3, column=0, sticky="w")
    inc = 3
    for (text, valjenis) in radio:
        Radiobutton(dframe, text=text, variable=r, value=valjenis).grid(row=inc, column=1, sticky="w", padx=20)
        inc += 1

    #input 5
    label6 = Label(dframe, text="Hobi").grid(row=5, column=0, sticky="w")
    # Combobox creation
    n = StringVar()
    hobi = ttk.Combobox(dframe, textvariable = n)
    # Adding combobox drop down list
    hobi['values'] = ('Bermain game', 'Baca Buku', 'Coding', 'Masak', 'Jalan-jalan')
    hobi.grid(row = 5, column = 1, sticky="w", padx=20, pady=10)

    # Button Frame
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    # Submit Button
    btn_submit = Button(frame2, text="Submit Data", anchor="s", command=lambda:[insertData(top, input_nama, input_nim, input_jurusan, r, n), top.withdraw()])
    btn_submit.grid(row=6, column=0, padx=10)

    # Cancel Button
    btn_cancel = Button(frame2, text="Gak jadi / Kembali", anchor="s", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=6, column=1, padx=10)

# Untuk memasukan data
def insertData(parent, nama, nim, jurusan, jkelamin, hobi):
    top = Toplevel()
    # Get data
    nama = nama.get()
    nim = nim.get()
    jurusan = jurusan.get()
    jkelamin = jkelamin.get()
    hobi = hobi.get()

    # cek semua input sudah terisi
    if((nama == '' or nama.isspace() == TRUE) or (nim == '' or nim.isspace() == TRUE) or (jurusan == '' or jurusan.isspace() == TRUE) or (jkelamin == '' or jkelamin.isspace() == TRUE) or (hobi == '' or hobi.isspace() == TRUE) ):
        Label(top, text="Semua input harus terisi!").pack(padx=10, pady=10)
        btn_ok = Button(top, text="Okayy!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)
    
    else:
        # Input data disini
        sqlquery = "INSERT INTO mahasiswa (nim, nama, jurusan, sex, hobi) VALUES (%s, %s, %s, %s, %s)"
        val = (nim, nama, jurusan, jkelamin, hobi)
        dbcursor.execute(sqlquery, val)
        mydb.commit()

        btn_ok = Button(top, text="Syap!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)
  
# Window Semua Mahasiswa
def viewAll():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Mahasiswa")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    # Get All Data
    result = getMhs()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1, relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="NIM", borderwidth=1, relief="solid", width=15, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Nama", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=2)
    title4 = Label(tableFrame, text="Jurusan", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=3)
    title5 = Label(tableFrame, text="Jenis Kelamin", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=4)
    title6 = Label(tableFrame, text="Hobi", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=5)

    # Print content
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1, relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid", height=2, width=15, padx=5).grid(row=i+1, column=1)
        label3 = Label(tableFrame, text=data[2], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=2)
        label4 = Label(tableFrame, text=data[3], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=3)
        label5 = Label(tableFrame, text=data[4], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=4)
        label6 = Label(tableFrame, text=data[5], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=5)
        i += 1

def viewFasilitas():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Fasilitas")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Fasilitas Yang Dapat Digunakan")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    # Get All Data
    result = getFasilitas()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1, relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="Nama Fasilitas", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Gambar", borderwidth=1, relief="solid", width=12, padx=5).grid(row=0, column=2 ,columnspan=2)

    # Print content
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1, relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=1)
        # view Button
        btn_lihatgambar = Button(tableFrame, text="View", anchor="w", command=lambda index=str(data[0]):[viewGambarFasilitas(top, index), top.withdraw()])
        btn_lihatgambar.grid(row=i+1, column=2)
        # swap Button
        btn_swapgambar = Button(tableFrame, text="Swap", anchor="w", command=lambda index=str(data[0]):[swapGambarFasilitas(top, index), top.withdraw()])
        btn_swapgambar.grid(row=i+1, column=3)
        i += 1

# Untuk melihat gambar fasilitas
def viewGambarFasilitas(parent, id):
    global mydb
    global dbcursor

    dbcursor.execute("SELECT gambar FROM fasilitas WHERE id=" + id)
    result = dbcursor.fetchone()

    top = Toplevel()
    photo = ImageTk.PhotoImage(Image.open(result[0]))
    label = Label(top ,image=photo)
    label.image = photo # keep a reference, agar gambar muncul
    label.pack()
    
    btn_ok = Button(top, text="Kembali", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
    btn_ok.pack(padx=10, pady=10)

# Untuk mengganti gambar fasilitas
def swapGambarFasilitas(parent, id):
    global mydb
    global dbcursor

    top = Toplevel()

    top.filename = filedialog.askopenfilename(initialdir = "/images", title="Select a File", filetypes=(("jpg", "*.jpg"), ("jpeg", "*.jpeg"), ("png", "*.png")))
    if(top.filename == '' or top.filename.isspace() == TRUE):
        Label(top, text="Swap Gambar Dibatalkan!").pack(padx=20, pady=10)
        btn_ok = Button(top, text="Oke...", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=20, pady=10)
    
    else:
        dbcursor.execute("UPDATE fasilitas SET gambar='"+ top.filename +"' WHERE id=" + id)
        mydb.commit()
        
        Label(top, text="Selamat, Gambar Berhasil Diganti!").pack(padx=20, pady=10)
        btn_ok = Button(top, text="Mantap!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=20, pady=10)

# Dialog konfirmasi hapus semua data
def clearAll():
    top = Toplevel()
    lbl = Label(top, text="Yakin mau hapus semua data?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), delAll()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=top.destroy)
    btn_no.grid(row=0, column=1, padx=10)

# Dialog konfirmasi keluar GUI
def exitDialog():
    global root
    root.withdraw()
    top = Toplevel()
    lbl = Label(top, text="Yakin mau keluar?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), root.destroy()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=lambda:[top.destroy(), root.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)

def delAll():
    top = Toplevel()
    # Delete data disini
    sqlquery = "DELETE FROM mahasiswa"
    dbcursor.execute(sqlquery)
    mydb.commit()

    btn_ok = Button(top, text="Zeeb", command=top.destroy)
    btn_ok.pack(pady=20)

# Title Frame
frame = LabelFrame(root, text="Praktikum DPBO", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# ButtonGroup Frame
buttonGroup = LabelFrame(root, padx=10, pady=10)
buttonGroup.pack(padx=10, pady=10)

# Title
label1 = Label(frame, text="Data Mahasiswa", font=(30))
label1.pack()

# Description
label2 = Label(frame, text="Ceritanya ini database mahasiswa ngab")
label2.pack()

# Input btn
b_add = Button(buttonGroup, text="Input Data Mahasiswa", command=inputs, width=30)
b_add.grid(row=0, column=0, pady=5)

# All data btn
b_add = Button(buttonGroup, text="Semua Data Mahasiswa", command=viewAll, width=30)
b_add.grid(row=1, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Hapus Semua Data Mahasiswa", command=clearAll, width=30)
b_clear.grid(row=2, column=0, pady=5)

b_clear = Button(buttonGroup, text="Data Fasilitas Kampus", command=viewFasilitas, width=30)
b_clear.grid(row=3, column=0, pady=5)

# Exit btn
b_exit = Button(buttonGroup, text="Exit", command=exitDialog, width=30)
b_exit.grid(row=4, column=0, pady=5)

root.mainloop()