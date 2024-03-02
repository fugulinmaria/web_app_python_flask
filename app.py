from flask import Flask, request, session, redirect, render_template, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField
from wtforms.validators import DataRequired, Email
from flask_session import Session
from datetime import datetime
import sqlite3
import random

app = Flask(__name__)


app.config['SECRET_KEY'] = "parola"
app.config['TESTING'] = True
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)







# Create a form class
class LoginForm(FlaskForm):
    mail = StringField("Email", validators=[DataRequired()])
    parola = PasswordField("Parola", validators=[DataRequired()])
    
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    mail = StringField("Email", validators=[DataRequired()])
    nume = StringField("Nume", validators=[DataRequired()])
    parola = PasswordField("Parola", validators=[DataRequired()])
    confirma = PasswordField("Confirma Parola", validators=[DataRequired()])
    adresa = StringField("Adresa", validators=[DataRequired()])
    telefon = StringField("Telefon", validators=[DataRequired()])
    card = StringField("Card", validators=[DataRequired()])
    
    submit = SubmitField("Submit")





@app.route('/', methods=['GET', 'POST'])

def login():
    mail = None
    parola = None
    form = LoginForm()
    session["logat"] = 0
    session["detalii_cont_curent"] = ''
    if request.method == 'POST':

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Validare
        if form.validate_on_submit():
            mail = form.mail.data
            form.mail.data = ''
            parola = form.parola.data
            form.parola.data = ''
            



            query = "SELECT mail, parola FROM Client WHERE mail='"+mail+"' AND parola = '"+parola+"'"

            cursor.execute(query)

            results = cursor.fetchall()
        

            if len(results) == 0:
                flash("Date incorecte")
                print("Date incorecte")
                
                return render_template("login.html", wrong_pass = True, form = form, user_in = False)
            else:
                
                print("Te-ai logat!")
                
                session["mail"] = mail
                session["parola"] = parola
                print(mail)


                if mail == "admin1234@yahoo.com":
                    session["logat"] = 1
                    print("adminul a intrat")
                    session["tip_cont"] = "admin"
                    return redirect("/profil_admin")
                else:

                    session["tip_cont"] = "client"
                    session["logat"] = 1
                    
                    query = "SELECT * FROM Client WHERE mail='"+mail+"' AND parola = '"+parola+"'"
                    cursor.execute(query)
                    results = cursor.fetchall()
                    session["detalii_cont_curent"] = results[0]
                    print(session["detalii_cont_curent"])
                    print(session["tip_cont"])

                    return redirect("/profil_client")
                
    return render_template("login.html", form = form)    





# Creaza formular inregistrare
@app.route('/register', methods=['GET', 'POST'])
def register():
    mail = None
    nume = None
    parola = None
    confirma = None
    adresa = None
    telefon = None
    card = None
    form = RegisterForm()

    if request.method == 'POST':
    
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        #Validare
        if form.validate_on_submit():
            
            mail = form.mail.data    # atribuire valoare
            form.mail.data = ''     # resetare valoare
            nume = form.nume.data
            form.nume.data = ''
            parola = form.parola.data
            form.parola.data = ''
            confirma = form.confirma.data
            form.confirma.data = ''
            adresa = form.adresa.data
            form.adresa.data = ''
            telefon = form.telefon.data
            form.telefon.data = ''
            card = form.card.data
            form.card.data = ''

            if (parola != confirma):
                flash("Parola nu corespunde!")
                return render_template('register.html',pass_no_match=True,user_created=False,user_not_found=True, form = form)
            else:
                cursor.execute("SELECT * FROM Client where mail ='{}' ".format(mail))

                results = cursor.fetchall()

                if len(results) != 0:
                    return render_template('register.html',pass_no_match=False,user_created=False,user_not_found=False, form = form)
                else:
                    flash("Profilul a fost inregistrat!")
                    cursor.execute("INSERT INTO Client(mail,nume,parola,adresa,telefon,card) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(mail,nume,parola,adresa,telefon,card))

                    conn.commit()
                    print("INSERT INTO Client(mail,nume,parola,adresa,telefon,card) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(mail,nume,parola,adresa,telefon,card))
                    return redirect('/')
                    
    return render_template("register.html", 
                           form = form)

@app.route('/profil_client')
def profil_client():
    
    if (session["logat"] != 1):
        return redirect('/')
    return render_template("profil_client.html", cont = session["detalii_cont_curent"])








@app.route('/editeaza_profil', methods=['GET', 'POST'])
def editeaza_profil():
    if (session["logat"] != 1):
        return redirect('/')
    
    if request.method == 'POST':
    
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        nume = request.form["nume"]
        adresa = request.form["adresa"]
        telefon = request.form["telefon"]
        mail = request.form["mail"]
        card = request.form["card"]

        query = "SELECT mail FROM Client WHERE mail='"+mail+"'"

        cursor.execute(query)

        results = cursor.fetchall()

        if (len(results)!=0 and session["detalii_cont_curent"][4]!=results[0][0]):
            print("Email deja folosit")
            return render_template("editeaza_profil.html", wrong_email = True, cont = session["detalii_cont_curent"])
        else:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            print(session["detalii_cont_curent"])
            parola = session["detalii_cont_curent"][5]
            ID_client = session["detalii_cont_curent"][0]
            print("Am editat profilul")            
            session["detalii_cont_curent"] = (ID_client, nume, adresa, telefon, mail, parola, card)

            cursor.execute("UPDATE Client SET nume = '{}', adresa ='{}', telefon = '{}', mail ='{}', card = '{}' WHERE ID_client = '{}'".format(nume, adresa, telefon, mail, card, ID_client))
            conn.commit()
            return redirect("/profil_client")


    return render_template("editeaza_profil.html", wrong_email = False, cont = session["detalii_cont_curent"])
    
@app.route('/delete_cont', methods=['GET', 'POST'])
def delete_cont():
    if (session["logat"] != 1):
        return redirect('/')   
     
    ID_client = session["detalii_cont_curent"][0]
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("DELETE FROM Client WHERE ID_client = '{}'".format(ID_client))
    conn.commit()
    return redirect('/')


@app.route('/profil_admin', methods=['GET', 'POST'])
def profil_admin():
    
    if (session["logat"] != 1 or session["tip_cont"] != "admin"):
        return redirect('/')
    
    return render_template("profil_admin.html")

@app.route('/profil_admin/locatii/', methods=['GET', 'POST'])
def locatii():
    if (session["logat"] != 1 or session["tip_cont"] != "admin"):
        return redirect('/')
    
    print("aici")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM Locatie"
    cursor.execute(query)
    lista_loc = cursor.fetchall()


    if request.method == 'POST':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        print("in if")
        try:
            nume_locatie = request.form["nume_locatie"]
            adresa = request.form["adresa"]
            capacitate = request.form["capacitate"]
            detalii = request.form["detalii"]
        except KeyError as e:
            print(f"KeyError: {e}")
            print(f"request.form keys: {list(request.form.keys())}")

        query = "SELECT nume_locatie FROM Locatie WHERE nume_locatie ='"+nume_locatie+"'"

        cursor.execute(query)

        results = cursor.fetchall()

        if (len(results)!=0):
            print("Date deja existente")
            return render_template("locatii.html", exista_loc = True, lista_loc = lista_loc )
        else: 
            

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Locatie(nume_locatie, adresa, capacitate, detalii) VALUES ('{}', '{}', '{}', '{}')".format(nume_locatie, adresa, capacitate, detalii))
            conn.commit()

            return redirect("/profil_admin/locatii")


    return render_template("locatii.html", exista_loc = False, lista_loc = lista_loc)

@app.route("/profil_admin/locatii/delete/<int:ID_locatie>")
def delete_loc(ID_locatie):
    if (session["logat"] != 1 or session["tip_cont"] != "admin"):
        return redirect('/')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("DELETE FROM Locatie WHERE ID_locatie = '{}'".format(ID_locatie))
    
    conn.commit()
    
    return redirect("/profil_admin/locatii") 
    
@app.route('/profil_admin/comedianti', methods=['GET', 'POST'])
def comedianti():
    if (session["logat"] != 1 or session["tip_cont"] != "admin"):
        return redirect('/')
    
    print("aici")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM Comediant ORDER BY nume"
    cursor.execute(query)
    lista_com = cursor.fetchall()

    if request.method == 'POST':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        print("in if")
        try:
            nume = request.form["nume_com"]
            telefon = request.form["telefon"]
            mail = request.form["mail"]
            descriere_comediant = request.form["descriere_comediant"]
            rating = request.form["rating"]

            query = "SELECT nume FROM Comediant WHERE nume ='"+nume+"'"

            cursor.execute(query)

            results = cursor.fetchall()

            if len(results) != 0:
                print("Date deja existente")
                return render_template("comedianti.html", exista_com=True, lista_com=lista_com)
            else:
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()

                cursor.execute("INSERT INTO Comediant(nume, telefon, mail, descriere_comediant, rating) VALUES ('{}', '{}', '{}', '{}', '{}')".format(nume, telefon, mail, descriere_comediant, rating))
                conn.commit()

                return redirect("/profil_admin/comedianti")

        except KeyError as e:
            print(f"KeyError: {e}")
            print(f"request.form keys: {list(request.form.keys())}")

    return render_template("comedianti.html", exista_com=False, lista_com=lista_com)

@app.route("/profil_admin/comedianti/delete/<int:ID_comediant>")
def delete_com(ID_comediant):
    if (session["logat"] != 1 or session["tip_cont"] != "admin"):
        return redirect('/')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("DELETE FROM Comediant WHERE ID_comediant = '{}'".format(ID_comediant))
    
    conn.commit()
    
    return redirect("/profil_admin/comedianti") 



@app.route('/profil_admin/spectacole', methods=['GET', 'POST'])
def spectacole():
    if (session["logat"] != 1):
        return redirect('/')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    #query simplu 1
    c="""
        SELECT s.ID_spectacol,s.nume_spectacol,s.data,s.ora,s.descriere_spectacol,s.bilete_max,s.pret_bilet,l.nume_locatie,l.adresa
        FROM Spectacol s INNER JOIN Locatie l ON s.ID_locatie = l.ID_locatie
"""
    cursor.execute(c)
    lista_spectacole=[]
    spectacole=cursor.fetchall()
    for spec in spectacole:
        #query simplu 2
        c="""
        SELECT c.nume, c.telefon, c.mail,c.descriere_comediant,c.rating
        FROM Comediant c INNER JOIN SpectacolComediant sc ON c.ID_comediant = sc.ID_comediant
        WHERE sc.ID_spectacol = {}
""".format(spec[0])
        cursor.execute(c)
        comedianti=cursor.fetchall()
        lista_spectacole.append((spec,comedianti))


    return render_template("spectacole.html",lista_spectacole=lista_spectacole)

@app.route('/profil_admin/spectacole/adauga_spectacol', methods=['GET', 'POST'])
def adauga_spectacol():
    if (session["logat"] != 1):
        return redirect('/')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Comediant")
    comedianti=cursor.fetchall()
    cursor.execute("SELECT * FROM Locatie")
    locatii=cursor.fetchall()
    if request.method == 'POST':
        nume = request.form["nume_spectacol"]
        data_spec = request.form["data_spec"]
        ora = request.form["ora"]
        descriere_spec = request.form["descriere_spec"]
        locatie = request.form["locatie"]
        bilete_max=request.form["bilete_max"]
        pret_bilet=request.form["pret_bilet"]
        com_ids=[]
        for i in locatii:
            print("locatie:")
            print(i)
            if int(i[0]) == int(locatie):
                print(i[0])
                print(locatie)
                print(i[3])
                print(bilete_max)
                if int(i[3]) < int(bilete_max):
                    return render_template("adauga_spectacol.html",comedianti=comedianti,locatii=locatii,no_space=True)
        
        print((nume,data_spec,ora,descriere_spec,locatie))
        for i in range(len(comedianti)):
            print("com"+str(comedianti[i][0]))
            if bool(request.form.getlist("com" + str(comedianti[i][0]))):
                com_ids.append(comedianti[i][0]) 
        print(com_ids)
        if(len(com_ids) == 0):
            return render_template("adauga_spectacol.html",comedianti=comedianti,locatii=locatii,no_com=True)
        cursor.execute("""INSERT INTO 
                        Spectacol(nume_spectacol,data,ora,descriere_spectacol,ID_locatie,bilete_max,pret_bilet)
                        VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}')"""\
                       .format(nume,data_spec,ora,descriere_spec,locatie,bilete_max,pret_bilet))
       
       
        c="""
                INSERT INTO SpectacolComediant(
                    ID_spectacol,
                    ID_comediant
                ) VALUES
                
            """
        
        for i in com_ids:
            c=c+"({},{} ),".format(cursor.lastrowid,i)
        c = c[:-1]
        print(c)
        cursor.execute(c)
        conn.commit()
        return redirect("/profil_admin/spectacole")

    return render_template("adauga_spectacol.html",comedianti=comedianti,locatii=locatii)

@app.route('/profil_admin/spectacole/editeaza_spectacol/<int:id_spec>', methods=['GET', 'POST'])
def editeaza_spectacol(id_spec):
    if (session["logat"] != 1):
        return redirect('/')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    c="""
        SELECT * FROM Spectacol WHERE ID_spectacol = {}
    """.format(id_spec)
    cursor.execute(c)
    spectacol=cursor.fetchall()[0]
    print(spectacol)
    cursor.execute("SELECT * FROM Comediant")
    comedianti=cursor.fetchall()
    cursor.execute("SELECT * FROM Locatie")
    locatii=cursor.fetchall()
    print(locatii)
    print(spectacol)
    c="""
        SELECT c.ID_comediant
        FROM Comediant c INNER JOIN SpectacolComediant sc ON c.ID_comediant = sc.ID_comediant
        WHERE sc.ID_spectacol = {}
    """.format(id_spec)
    cursor.execute(c)
    comediantii_mei=[item[0] for item in cursor.fetchall()] # unpack touple [(7,), (8,)] -> [7,8]
    
    print(comediantii_mei)

    if request.method == 'POST':
        nume = request.form["nume_spectacol"]
        data_spec = request.form["data_spec"]
        ora = request.form["ora"]
        descriere_spec = request.form["descriere_spec"]
        locatie = request.form["locatie"]
        bilete_max=request.form["bilete_max"]
        pret_bilet=request.form["pret_bilet"]
        com_ids=[]
        print((nume,data_spec,ora,descriere_spec,locatie))
        for i in range(len(comedianti)):
            print("com"+str(comedianti[i][0]))
            if bool(request.form.getlist("com" + str(comedianti[i][0]))):
                com_ids.append(comedianti[i][0]) 
        print(com_ids)
        if(len(com_ids) == 0):
            return render_template("adauga_spectacol.html",comedianti=comedianti,locatii=locatii,no_com=True)
        cursor.execute("""UPDATE Spectacol SET 
                        nume_spectacol='{}', data='{}', ora='{}',descriere_spectacol='{}',ID_locatie='{}',bilete_max='{}',pret_bilet='{}'
                        WHERE ID_spectacol = '{}'""".format(nume,data_spec,ora,descriere_spec,locatie,bilete_max,pret_bilet,id_spec))
        cursor.execute("PRAGMA foreign_keys = ON")               
        cursor.execute("DELETE FROM SpectacolComediant WHERE ID_spectacol = '{}'".format(id_spec))
       
        c="""
                INSERT INTO SpectacolComediant(
                    ID_spectacol,
                    ID_comediant
                ) VALUES
                
            """
        
        for i in com_ids:
            c=c+"({},{} ),".format(id_spec,i)
        c = c[:-1]
        print(c)
        cursor.execute(c)
        conn.commit()
        return redirect("/profil_admin/spectacole")
    return render_template ("editeaza_spectacol.html",spectacol=spectacol,comedianti=comedianti,locatii=locatii,comediantii_mei=comediantii_mei)

def sterge_spectacol_fn(id_spec):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("DELETE FROM Spectacol WHERE ID_spectacol = {}".format(id_spec))
   # cursor.execute("DELETE FROM SpectacolComediant WHERE ID_spectacol = '{}'".format(id_spec))
   # cursor.execute("DELETE FROM Bilete WHERE ID_spectacol = {}".format(id_spec))
    conn.commit()

@app.route('/profil_admin/spectacole/sterge_spectacol/<int:id_spec>', methods=['GET', 'POST'])
def sterge_spectacol(id_spec):
    if (session["logat"] != 1):
        return redirect('/')
    sterge_spectacol_fn(id_spec)
    return redirect("/profil_admin/spectacole")

@app.route('/comanda', methods=['GET', 'POST'])
def client_comanda():
    if (session["logat"] != 1):
        return redirect('/')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    c="""
        SELECT s.ID_spectacol,s.nume_spectacol,s.data,s.ora,s.descriere_spectacol,s.bilete_max,s.pret_bilet,l.nume_locatie,l.adresa
        FROM Spectacol s INNER JOIN Locatie l ON s.ID_locatie = l.ID_locatie
"""
    cursor.execute(c)
    lista_spectacole=[]
    spectacole=cursor.fetchall()
    for spec in spectacole:
       
        c="""
        SELECT c.nume, c.rating
        FROM Comediant c INNER JOIN SpectacolComediant sc ON c.ID_comediant = sc.ID_comediant
        WHERE sc.ID_spectacol = {}
""".format(spec[0])
        cursor.execute(c)
        comedianti=cursor.fetchall()
        #query simplu 3
        c="""
        SELECT AVG (c.rating)
        FROM Comediant c INNER JOIN SpectacolComediant sc ON c.ID_comediant = sc.ID_comediant
        WHERE sc.ID_spectacol = {}
""".format(spec[0])
        cursor.execute(c)
        med=round(cursor.fetchall()[0][0], 2)
        #query simplu 4
        c="""
        SELECT COUNT(*)
        FROM Bilete b INNER JOIN Spectacol s ON b.ID_spectacol = s.ID_spectacol
        WHERE s.ID_spectacol = {}
""".format(spec[0])
        cursor.execute(c)
        bilete_luate=cursor.fetchall()[0][0]
        bilete_disponibile=spec[5]-bilete_luate
        lista_spectacole.append((spec,comedianti,med,bilete_disponibile))
    cos_cumparaturi=[]
    if request.method == 'POST':
        total=0
        for spec in spectacole:
            nr_bil=int(request.form["nr_bilete_"+str(spec[0])])
            if nr_bil > 0:
                tip_bil=request.form["tip_bilet_"+str(spec[0])]
                cos_cumparaturi.append((spec[0],nr_bil,tip_bil))
                if tip_bil=="adult":
                    total=total + nr_bil*spec[6]
                else:
                    total=total + (nr_bil*spec[6])/2

        print(cos_cumparaturi)
        cursor.execute("""INSERT INTO Comanda (ID_client,metoda_platii,total,data_comanda)
                       VALUES ('{}','{}','{}','{}')
        """.format(session["detalii_cont_curent"][0],"card_bancar",total,datetime.now().date()))
        lastrow=cursor.lastrowid
        for item in cos_cumparaturi:
            c="""INSERT INTO Bilete (ID_spectacol,cod_bilet,tip_bilet,ID_comanda)
            VALUES"""
            for i in range(item[1]):
                c=c+"('{}','{}','{}','{}'),".format(item[0],random.randint(1, 10000000),item[2],lastrow)
            c = c[:-1]
            cursor.execute(c)
            
        conn.commit()
        return redirect("/comenzi")

    return render_template("comanda_spectacole.html",lista_spectacole=lista_spectacole)

@app.route('/comenzi', methods=['GET', 'POST'])
def client_comenzi():
    if (session["logat"] != 1):
        return redirect('/')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT c.ID_comanda, c.metoda_platii, c.total, c.data_comanda, cl.nume
                   FROM Comanda c INNER JOIN Client cl ON c.ID_client = cl.ID_client
                   WHERE c.ID_client = '{}'
    """.format(session["detalii_cont_curent"][0]))
    comenzi=cursor.fetchall()
    lista_comenzi=[]
    for comanda in comenzi:
        #query simplu 5 pentru extragere 
        cursor.execute("""SELECT s.nume_spectacol, s.data, s.ora, COUNT(s.ID_spectacol), b.tip_bilet, SUM(s.pret_bilet), s.pret_bilet
                        FROM Spectacol s INNER JOIN Bilete b ON s.ID_spectacol = b.ID_spectacol
                        INNER JOIN Comanda c ON c.ID_comanda = b.ID_comanda
                        WHERE c.ID_comanda ='{}'
                        GROUP BY s.ID_spectacol,b.tip_bilet
  """.format(comanda[0]))
        grup_bilete=cursor.fetchall()
        lista_comenzi.append((comanda,grup_bilete))




    return render_template("client_comenzi.html",lista_comenzi=lista_comenzi)


@app.route('/profil_client/comenzi/sterge_comanda/<int:id_com>', methods=['GET', 'POST'])
def sterge_comanda(id_com):
    if (session["logat"] != 1):
        return redirect('/')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("DELETE FROM Comanda WHERE ID_comanda = {}".format(id_com))
    #cursor.execute("DELETE FROM Bilete WHERE ID_comanda = '{}'".format(id_com))
    conn.commit()
    return redirect("/comenzi")


@app.route('/biletele_mele', methods=['GET', 'POST'])
def biletele_mele():
    if (session["logat"] != 1):
        return redirect('/')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    #query simplu 6
    cursor.execute("""SELECT cl.nume, s.nume_spectacol, s.data, s.ora,
                    l.nume_locatie, l.adresa, s.pret_bilet,b.tip_bilet,b.cod_bilet,c.data_comanda
FROM Client cl INNER JOIN Comanda c ON cl.ID_client = c.ID_client
INNER JOIN Bilete b ON b.ID_comanda = c.ID_comanda
INNER JOIN Spectacol s ON s.ID_spectacol = b.ID_spectacol 
INNER JOIN Locatie l ON l.ID_locatie = s.ID_locatie
WHERE cl.ID_client = '{}'""".format(session["detalii_cont_curent"][0]))
    bilete=cursor.fetchall()

    return render_template("biletele_mele.html",bilete=bilete)

@app.route('/profil_admin/statistici', methods=['GET', 'POST'])
def admin_statistici():
    if (session["logat"] != 1):
        return redirect('/')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    #query complex 1 Afiseaza clientii si numarul de comenzi ale lor care au totalul
    # peste media totalurilor comenzilor
    cursor.execute("""SELECT cl.nume , COUNT(cl.ID_client)
FROM Client cl INNER JOIN Comanda c on cl.ID_client = c.ID_client
WHERE c.total > (SELECT avg(total) FROM Comanda)
GROUP BY cl.ID_client""")
    
    cl_bogati=cursor.fetchall()
    # query complex 2 Afiseaza spectacolele care au ratingul mediu al comediantilor mai mare 
    # decat media ratingului tuturor comediantilor
    cursor.execute("""SELECT  s.nume_spectacol, AVG(c.rating)
FROM Spectacol s INNER JOIN SpectacolComediant sc ON s.ID_spectacol = sc.ID_spectacol
INNER JOIN Comediant c ON c.ID_comediant = sc.ID_comediant
GROUP BY s.ID_spectacol
HAVING AVG(c.rating) > (SELECT AVG(rating) FROM Comediant)""")
    spec_frumoase=cursor.fetchall()
    print(spec_frumoase)
    #query complex 3 afiseaza comediantii care nu sunt invitati la niciun spectacol
    cursor.execute("""SELECT c.nume FROM  Comediant c
    WHERE c.ID_comediant NOT IN (
    SELECT DISTINCT c2.ID_comediant
    FROM Comediant c2 INNER JOIN SpectacolComediant sc
    ON c2.ID_comediant = sc.ID_comediant) 
""")
    comedianti_lenesi=cursor.fetchall()
    #query complex 4 clientii care au plasat cel putin o comanda
    cursor.execute("""SELECT nume
FROM Client
WHERE EXISTS (
    SELECT 1
    FROM Comanda
    WHERE Comanda.ID_client = Client.ID_client
);""")
    clienti_activi=cursor.fetchall()
    #query complex 5 comenzile care contin bilete la toate spectacolele
    cursor.execute("""SELECT c.ID_comanda, c.metoda_platii, c.total, c.data_comanda, cl.nume
                    FROM Comanda c INNER JOIN Bilete b ON c.ID_comanda=b.ID_comanda
                    INNER JOIN Client cl ON cl.ID_client = c.ID_client
                    GROUP BY c.ID_comanda
                    HAVING count( DISTINCT b.ID_spectacol) = (SELECT COUNT(s.ID_spectacol)
                    FROM Spectacol s)""")
    

    comenzi=cursor.fetchall()
    lista_comenzi=[]
    for comanda in comenzi:
        
        cursor.execute("""SELECT s.nume_spectacol, s.data, s.ora, COUNT(s.ID_spectacol), b.tip_bilet, SUM(s.pret_bilet), s.pret_bilet
                        FROM Spectacol s INNER JOIN Bilete b ON s.ID_spectacol = b.ID_spectacol
                        INNER JOIN Comanda c ON c.ID_comanda = b.ID_comanda
                        WHERE c.ID_comanda ='{}'
                        GROUP BY s.ID_spectacol,b.tip_bilet
  """.format(comanda[0]))
        grup_bilete=cursor.fetchall()
        lista_comenzi.append((comanda,grup_bilete))


    return render_template("statistici.html",cl_bogati=cl_bogati,
                           spec_frumoase=spec_frumoase,
                            comedianti_lenesi=comedianti_lenesi,
                            clienti_activi=clienti_activi,lista_comenzi=lista_comenzi)