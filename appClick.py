from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = "healthclick"
app.config["MONGO_URI"] = "mongodb://localhost:27017/Health"
mongo = PyMongo(app)

#collections in db:Health
login_collection = mongo.db.users
cart_collection = mongo.db.cart
itemData = {49:'Ibuprofen', 39:'Crocin', 80:'Dolo', 120:'Gelusil', 100:'Accutane', 150:'Aspirin', 400:'Azathioprine', 749:'Citalopram', 1299:'Diazepam', 520:'Albuterol', 310:'Allegra', 60:'Benydryl'}

#Anasayfa
@app.route("/")
def home():
    return render_template("home.html")

#Hakkımızda
@app.route("/about")
def about():
    return render_template("about.html")

#Hizmetler
#Akıllı Asistan
@app.route("/faqchatbot")
def symptom():
    return render_template("symptom.html")

#ilaç sipariş
@app.route("/orderMeds")
def meds():
    items = []
    for i, data in itemData.items():
        cart1 = cart_collection.find_one({'item': data})
        items.append(cart1)
        print(items)
    return render_template("meds.html", data=data)

#CART
cart_list = []

@app.route("/cart")
@app.route("/cart/<id>")
def cart(id):
    global cart_list

    #items = []
    totalprice = 0
    ind = int(id.split('.')[0])
    cart1 = cart_collection.find_one({'i': ind})
    if cart1 != None:
        totalprice += int(cart1["price"])
        cart_list.append(cart1)
    else:
        totalprice = 0

    return render_template("addtochart.html", data=cart_list, totalprice=totalprice, id=ind)

#cart temizleme
@app.route("/clear")
def clear():
    cart_list = []
    # print(cart_list)
    return redirect(url_for('meds'))

#aylık takip (ilaç)
@app.route("/monthlySubs")
def monthlySubs():
    return render_template("monthlysubs.html")

#Randevu
@app.route("/bookappointments")
def bookAppointments():
    return render_template("bookappointments.html")

#Evde Testler
@app.route("/athomelab")
def atHomeLab():
    return render_template("athomelab.html")

#İlaç Hatırlatıcı
@app.route("/medreminder")
def medReminder():
    return render_template("medreminder.html")


#Anlaşmalı Kurumlar
@app.route("/insurance")
def insurance():
    return render_template("insurance.html")

#Giriş / Çıkış Yap Başarısız Giriş
@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form["email"]
        pwd = request.form["password"]
        user1 = login_collection.find_one({'user': user})

        if user1["user"]==user and user1["password"]==pwd:
            user=user.split('@')
            session["username"] = user[0]
            session["password"] = pwd
            return redirect(url_for("usersuccess"))
        else:
            msg = "Geçersiz kimlik bilgileri. Tekrar deneyin!"
            return render_template("login.html", msg=msg)
    else:
        if "username" in session:
            return redirect(url_for("usersuccess"))

        return render_template("login.html")

@app.route("/user")
def usersuccess():
    if "username" in session:
        usr = session["username"]
        if "password" in session:
            pw = session["password"]
            print(pw)
            return render_template("usrsuccess.html", user=usr)
    else:
        msg = 'Geçersiz Kullanıcı Adı veya Şifre!'
        return redirect(url_for("login", msg=msg))

@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('password', None)
    # print(session)
    msg = "Çıkış Başarılı!"
    return redirect(url_for('login', msg=msg))

#Kayıt Ol
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form["fname"]
        lname = request.form["lname"]
        user = request.form["email"]
        pwd = request.form["password"]
        cpwd = request.form["cpassword"]
        if cpwd == pwd:
            msg = "Başarılı bir şekilde kaydoldu!"

            login_collection.insert_one({'user' : user, 'password' : pwd})

            msg = "Başarılı Kayıt!"
            return redirect(url_for("login", msg=msg))
        else:
            msg = "Şifreler Eşleşmemektedir!"
            return render_template("register.html", msg=msg)
    else:
        return render_template("register.html")



if __name__ == "__main__":
    app.run(debug=True)



