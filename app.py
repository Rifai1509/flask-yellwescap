from flask import *
import json
app = Flask(__name__)
app.config["SECRET_KEY"] = "IN1 Ad4LaH ToKEN y4n6 s4ya Bu4T $EnDir1"

@app.route("/<email>", methods=["POST","GET"])
def sukses_req(email):
    if "email" in session:
        if request.method == "POST":
            term = request.form['term']
            lokasi = request.form['lokasi']
            daftar_term =['Accountans','Bars','Bakeries','Hospitals','Hotels','Pizzas','Plumbers','Schools','Shops',
                                  'ACCOUNTANS', 'BARS', 'BAKERIES', 'HOSPITALS', 'HOTELS', 'PIZZAS', 'PlUMBERS','SCHOOLS', 'SHOPS',
                                  'accountans', 'bars', 'bakeries', 'hospitals', 'hotels', 'pizzas', 'plumbers','schools', 'shops'
                                  ]
            daftar_lokasi=['Uk','London','Birmingham','Liverpool',
                            'UK', 'LONDON', 'BIRMINGHAM', 'LIVERPOOL'
                            'uk', 'london', 'Birmingham', 'Liverpool'
                            ]
            daftar_term_tanpa_s = ['Accountan', 'Bar', 'Hospital', 'Hotel', 'Pizza', 'Plumber', 'School', 'Shop',
                                   'ACCOUNTAN', 'BAR', 'HOSPITAL', 'HOTEL', 'PIZZA', 'PlUMBER', 'SCHOOL','SHOP',
                                   'accountan', 'bars', 'hospital', 'hotel', 'pizza', 'plumber','school', 'shop'
                                   ]
            bakeries = ['bakery', 'Bakery', 'BAKERY']
            if term in bakeries:
                term = term[:5]
                term = f'{term}IES'.lower()
                session['term'.lower()] = term
                session['lokasi'.lower()] = lokasi
                token = app.config["SECRET_KEY"]
                return redirect(url_for('hasil', email=email, token=token, term=term, lokasi=lokasi))

            elif term in daftar_term and lokasi in daftar_lokasi:
                session['term'.lower()] = term
                session['lokasi'.lower()] = lokasi
                token= app.config["SECRET_KEY"]
                return redirect(url_for('hasil', email=email,token=token, term=term, lokasi=lokasi))
            elif term in daftar_term_tanpa_s:
                term = term
                term = f'{term}S'.lower()
                session['term'.lower()] = term
                session['lokasi'.lower()] = lokasi
                token= app.config["SECRET_KEY"]
                return redirect(url_for('hasil', email=email,token=token, term=term, lokasi=lokasi))
            elif term == '' or lokasi == '':
                flash('Isi dong, jangan ada yang kosong', 'danger')
                return render_template("sukses.html")
            else:
                flash(f'Hasil untuk {term} di {lokasi} tidak ditemukan. Harap isi yang sesuai. Ingat! isi dengan huruf kecil', 'danger')
                return render_template("sukses.html")
        return render_template("sukses.html", email=email)
    else:
        flash('Silakan masuk dulu', 'danger')
        return redirect(url_for('index'))
@app.route("/", methods=["POST", "GET"])
def index():
    if "email" in session:
        email = session['email']
        return redirect(url_for('sukses_req', email=email))

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        if email == 'admin@wescap.com' and password == 'pass':
            session['email'] = email
            session['password'] = password
            flash('Selamat, Anda berhasil masuk!', 'success')
            return redirect(url_for('sukses_req', email=email))
        else:
            flash('Gagal Bos. Email atau password salah! ISI YANG BENER BOSKU!!!', 'danger')
            return redirect(url_for('index'))

    return render_template("index.html")

@app.route("/tentang")
def about():
    if "email" in session:
        return render_template("about.html")
    else:
        flash('Eitss, Tidak semudah itu ferguso, silakan log in dulu!!!', 'danger')
        return redirect(url_for('index'))

@app.route("/keluar")
def keluar():
    if "email" in session:
        session.pop("email")
        session.pop("password")
        return redirect(url_for('index'))
    else:    
        return redirect(url_for('index'))

@app.route("/lupa")
def lupa():
    return render_template("lupa.html")
@app.route("/saya")
def saya():
    return render_template("saya.html")
@app.route("/hasil")
def hasil():
    if "email" in session:
        try :
            download = "<a href=' /download' target='_blank' class='btn btn-success'>Download CSV</a>"
            term = session['term']
            lokasi = session['lokasi']
            with open(f'json_file/{term}_{lokasi}.json', 'r') as file:
                data = file.read()
            datas = json.loads(data)
            return render_template("hasil.html", datas=datas, term=term, lokasi=lokasi, download=download)
        except:
            flash(f'Hasil untuk {term} di {lokasi} tidak ditemukan', 'danger')
            return render_template("sukses.html")
    else:
        flash('Eitss, Tidak semudah itu ferguso, silakan log in dulu!!!', 'danger')
        return redirect(url_for('index'))


@app.route('/download')
def download():
    term = session['term']
    lokasi = session['lokasi']
    path = f'csv_files/{term}_{lokasi}.csv'
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
