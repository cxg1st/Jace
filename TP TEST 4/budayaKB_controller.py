from budayaKB_model import BudayaItem, BudayaCollection
from flask import Flask, request, render_template
# from wtforms import Form, validators, TextField

app = Flask(__name__)
app.secret_key ="tp4"

#inisialisasi objek budayaData
databasefilename = ""
budayaData = BudayaCollection()

@app.route('/')
def hoempage():
	return render_template("homepage.html")
#merender tampilan default(index.html)
@app.route('/index')
def index():
	return render_template("index.html")

# Bagian ini adalah implementasi fitur Impor Budaya, yaitu:
# - merender tampilan saat menu Impor Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Import Data" diklik
# - menampilkan notifikasi bahwa data telah berhasil diimport 	
@app.route('/imporBudaya', methods=['GET', 'POST'])
def importData():
    if request.method == "GET":
        return render_template("imporBudaya.html")

    elif request.method == "POST":
        try:
            f = request.files['file']
            global databasefilename
            databasefilename = f.filename
            budayaData.importFromCSV(f.filename)
            n_data = len(budayaData.koleksi)
            return render_template("imporBudaya.html", result=n_data, fname=f.filename)
        except:
            error="File tidak dalam 1 folder dengan program"
            return render_template("imporBudaya.html",error=error)
        
#Untuk menambah budaya
@app.route('/tambahBudaya', methods=['GET', 'POST'])
def tambahBudaya():
    if request.method == "GET":
        return render_template("tambahBudaya.html")
    
    elif request.method == "POST":
        if databasefilename=="":
            return render_template("tambahBudaya.html", error="error")
        nama = request.form['Nama']
        provinsi = request.form["provinsi"]
        tipe = request.form["tipe"]
        url = request.form["referensi"]
        
        if nama[0::]==" " or tipe[0::]==" " or provinsi[0::]==" " or url[0::]:
            return render_template("tambahBudaya.html",spasi="spasi")
        elif budayaData.tambah(nama,tipe,provinsi,url)  :
            budayaData.exportToCSV(databasefilename)
            return render_template("tambahBudaya.html", res = True, abc=nama) 
        else :
            return render_template("tambahBudaya.html", res = False, abc=nama)
 
#Untuk Mengupdate Budaya
@app.route('/ubahBudaya', methods=['GET', 'POST'])
def ubahBudaya():
    if request.method == "GET":
        return render_template("ubahBudaya.html")

    elif request.method == "POST":
        if databasefilename=="":
            return render_template("ubahBudaya.html", error="error")
        nama = request.form['Nama']
        provinsi = request.form["provinsi"]
        tipe = request.form["tipe"]
        url = request.form["referensi"]
        
        if nama[0::]==" " or tipe[0::]==" " or provinsi[0::]==" " or url[0::]:
            return render_template("ubahBudaya.html",spasi="spasi")        
        elif budayaData.ubah(nama,tipe,provinsi,url):
            budayaData.exportToCSV(databasefilename)
            return render_template("ubahBudaya.html", res = True, abc=nama)
        else :
            return render_template("ubahBudaya.html", res = False, abc=nama)


#Untuk Menghapus Budaya
@app.route('/hapusBudaya', methods=['GET', 'POST'])
def hapusBudaya():
    if request.method == "GET":
        return render_template("hapusBudaya.html")
    elif request.method == "POST":
        if databasefilename==" ":
            return render_template("hapusBudaya.html", error="error")
        nama = request.form["Nama"]
        if nama[0::]==" " :
            return render_template("hapusBudaya.html",spasi="spasi")
        elif budayaData.hapus(nama):
            budayaData.exportToCSV(databasefilename)
            return render_template("hapusBudaya.html", res = True, abc=nama)
        
        else :
            return render_template("hapusBudaya.html", res = False, abc=nama)

#untuk Mencari Budaya
@app.route('/cariBudaya', methods=['GET', 'POST'])
def cariBudaya():
    if request.method == "GET":
        return render_template("cariBudaya.html")
    elif request.method == "POST":
        ag = request.form['cariB']
        if request.form.get("cari") == "Nama":
            return render_template("cariBudaya.html", result=budayaData.cariByNama(ag), res=True, jace=len(budayaData.cariByNama(ag)), ag=ag, hg="Nama Budaya")
        elif request.form.get("cari") == "Tipe":
            return render_template("cariBudaya.html", result=budayaData.cariByTipe(ag), res=True, jace=len(budayaData.cariByTipe(ag)), ag=ag, hg="Tipe Budaya")
        elif request.form.get("cari") == "Provinsi":
            return render_template("cariBudaya.html", result=budayaData.cariByProv(ag), res=True, jace=len(budayaData.cariByProv(ag)), ag=ag, hg="Asal Provinsi Budaya")        

#Menampilkan stat budaya
@app.route('/statsBudaya', methods=['GET', 'POST'])
def statBudaya():
    if request.method == "GET":
        return render_template("statBudaya.html")
    elif request.method == "POST":
        if request.form.get("cari") == "All":
            return render_template('statBudaya.html', result=budayaData.stat(), res=True, All="All")
        if request.form.get("cari") == "Tipe":
            return render_template('statBudaya.html', result=budayaData.statByTipe() ,res=True, Tipe="Tipe")
        if request.form.get("cari") == "Provinsi":
            return render_template('statBudaya.html',result=budayaData.statByProv(),res=True, Prov="Provinsi")



# run main app
if __name__ == "__main__":
	app.run(debug=True) 