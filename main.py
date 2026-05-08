from flask import Flask, redirect, session, render_template, request, jsonify
from load_google_login import register_oath
from get_secret import app_secret_key
from load_database import *
from werkzeug.utils import secure_filename
import os
import uuid


init_db()
# add_admin("your email here")
app = Flask(__name__)
app.secret_key = app_secret_key
google = register_oath(app)

@app.route("/")
def base_path():
    if session.get("verified"):
        return redirect("/dashboard")
    else:
        return render_template("commission_intro.html")

@app.route("/usr_inf", methods=["POST"])
def user_inf():
    if session.get("verified"):
        return jsonify({"verified" : True,
                        "name" : session.get("user"),
                        "image" : session.get("picture")})
    else:
        return jsonify({"verified" : False})


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"status" : "ok"})

@app.route("/login_google")
def login_google():
    return google.authorize_redirect("http://127.0.0.1:5000/callback")

@app.route("/admin")
def admin_panel():
    fetch_db_inf = get_user(session.get("user"))
    is_verified = session.get("verified")
    print(fetch_db_inf)
    if fetch_db_inf[2] == "admin" and is_verified:
        return render_template("admin_page_ja.html",
                                request_len=get_commission_request("len", "requested"),
                                accepted_len=get_commission_request("len", "pending"),
                                completed_len=get_commission_request("len", "completed"),
                                rejected_len=get_commission_request("len", "cancelled"))
    elif is_verified:
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.route("/update_status", methods=["POST"])
def update_status():
    fetch_db_inf = get_user(session.get("user"))
    #turn received data from post into json response
    data = request.json
    #use get + json key to get value

    uid = data.get("uid")
    status = data.get("status")

    if fetch_db_inf[2] == "admin" and session.get("verified"):
        print(f"received : {uid}, {status}")
        update_commission_status(uid, status)
    else:
        return
    
@app.route("/update_sub_status_db", methods=["POST"])
def update_sub_status_db():
    fetch_db_inf = get_user(session.get("user"))
    #turn received data from post into json response
    data = request.json
    #use get + json key to get value
    uid = data.get("uid")
    sub_status = data.get("status")

    if fetch_db_inf[2] == "admin" and session.get("verified"):
        print(f"received : {uid}, {sub_status}")
        update_sub_status(uid, sub_status)
        return jsonify({"status" : "ok"})
    else:
        return


@app.route("/admin/request_panel")
def admin_request_panel():
    fetch_db_inf = get_user(session.get("user"))
    is_verified = session.get("verified")
    print(fetch_db_inf)
    raw_info=get_commission_request("get_all", "requested")
    work_list = []
    for work in raw_info:
        image = get_cms_oc(work[0])
        work_data = {
            "info" : work,
            "image" : image
        }

        work_list.append(work_data)
    print(work_list)
    
    if fetch_db_inf[2] == "admin":
        return render_template("admin_request.html",
                                request_len=get_commission_request("len", "requested"),
                                work_list=work_list)
    elif is_verified:
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.route("/admin/pending_panel")
def admin_pending_panel():
    fetch_db_inf = get_user(session.get("user"))
    is_verified = session.get("verified")
    raw_info=get_commission_request("get_all", "pending")
    pending_list = []
    for work in raw_info:
        image = get_cms_oc(work[0])
        work_data = {
            "info" : work,
            "image" : image
        }

        pending_list.append(work_data)
    print(pending_list)

    print(fetch_db_inf)
    
    if fetch_db_inf[2] == "admin" and is_verified:
        return render_template("admin_pending.html", 
                            pending_len = get_commission_request("len", "pending"),
                            pending_list = pending_list)
    elif is_verified:
        return redirect("/dashboard")
    else:
        return redirect("/")
    
@app.route("/admin/cancelled_panel")
def admin_cancel_panel():
    fetch_db_inf = get_user(session.get("user"))
    is_verified = session.get("verified")
    raw_info=get_commission_request("get_all", "cancelled")
    cancelled_list = []
    for work in raw_info:
        image = get_cms_oc(work[0])
        work_data = {
            "info" : work,
            "image" : image
        }

        cancelled_list.append(work_data)
    print(cancelled_list)

    if fetch_db_inf[2] == "admin" and is_verified:
        return render_template("admin_cancelled.html",
                            cancelled_len = get_commission_request("len", "cancelled"),
                            cancelled_list = cancelled_list)
    elif is_verified:
        return redirect("/dashboard")
    else:
        return redirect("/")
    
@app.route("/admin/completed_panel")
def admin_completed_panel():
    fetch_db_inf = get_user(session.get("user"))
    is_verified = session.get("verified")

    raw_info=get_commission_request("get_all", "completed")
    completed_list = []
    for work in raw_info:
        image = get_cms_oc(work[0])
        work_data = {
            "info" : work,
            "image" : image
        }

        completed_list.append(work_data)
    print(completed_list)

    if fetch_db_inf[2] == "admin" and is_verified:
        return render_template("admin_completed.html",
                            completed_len = get_commission_request("len", "completed"),
                            completed_list = completed_list)
    elif is_verified:
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.route("/admin/admin_commission")
def admin_commission():
    fetch_db_inf = get_user(session.get("user"))
    is_verified = session.get("verified")
    if fetch_db_inf[2] == "admin" and is_verified:
        return render_template("admin_commission_catalog.html",
                            commission_list = get_commission_list())
    elif is_verified:
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.route("/callback")
def callback():
    token = google.authorize_access_token()
    user = token["userinfo"]
    fetch_db_inf = get_user(user["email"])
    print(fetch_db_inf)
    session["user"] = user["email"]
    session["verified"] = True
    session["picture"] = user["picture"]
    session["role"] = fetch_db_inf[2]
    print(session.get("verified"))
    if session.get("verified"):
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.route("/dashboard")
def dashboard():
    print(session.get("verified"))
    if session.get("verified"):
        return render_template("commission_dashboard.html",
                            username=session.get("user"),
                            requested_len=get_commission_request("len", "requested", session.get("user")),
                            pending_len=get_commission_request("len", "pending", session.get("user")),
                            completed_len=get_commission_request("len", "completed", session.get("user")),
                            cancelled_len=get_commission_request("len", "cancelled", session.get("user"))
                            )
    else:
        return redirect("/")

@app.route("/dashboard/request_panel")
def request_panel():
    raw_list=get_commission_request("get_all", "requested", session.get("user"))
    requested_list = []

    #มา for ของเเต่ละ user order
    for info in raw_list:
        image=get_cms_oc(info[0])
        work_data = {
            "info" : info,
            "image" : image
        }
        requested_list.append(work_data)

                                    
    if session.get("verified"):
        return render_template("commission_request.html",
                            requested_len=get_commission_request("len", "requested", session.get("user")),
                            requested_list =requested_list
                            )
    else:
        return redirect("/")

@app.route("/dashboard/pending_panel")
def pending_panel():
    raw_list=get_commission_request("get_all", "pending", session.get("user"))
    pending_list = []

    #มา for ของเเต่ละ user order
    for info in raw_list:
        image=get_cms_oc(info[0])
        work_data = {
            "info" : info,
            "image" : image
        }
        pending_list.append(work_data)
    if session.get("verified"):
        return render_template("commission_pending.html",
                            pending_len = get_commission_request("len", "pending", session.get("user")),
                            pending_list = pending_list)
    else:
        return redirect("/")

@app.route("/dashboard/completed_panel")
def completed_panel():
    raw_list=get_commission_request("get_all", "completed", session.get("user"))
    completed_list = []

    #มา for ของเเต่ละ user order
    for info in raw_list:
        image=get_cms_oc(info[0])
        work_data = {
            "info" : info,
            "image" : image
        }
        completed_list.append(work_data)

    if session.get("verified"):
        return render_template("commission_completed.html",
                            completed_len = get_commission_request("len", "completed", session.get("user")),
                            completed_list = completed_list)
    else:
        return redirect("/")
    
@app.route("/dashboard/cancelled_panel")
def cancelled_panel():
    raw_list=get_commission_request("get_all", "cancelled", session.get("user"))
    cancelled_list = []

    #มา for ของเเต่ละ user order
    for info in raw_list:
        image=get_cms_oc(info[0])
        work_data = {
            "info" : info,
            "image" : image
        }
        cancelled_list.append(work_data)
    if session.get("verified"):
        return render_template("commission_cancelled.html",
                            cancelled_len = get_commission_request("len", "cancelled", session.get("user")),
                            cancelled_list = cancelled_list)
    else:
        return redirect("/")

@app.route("/commission")
def commission():
    if session.get("verified"):
        return render_template("commission_catalog.html",
                            commission_list = get_commission_list())
    else:
        return redirect("/")
    
@app.route("/create_commission", methods=["POST"])
def create_commission():

    file = request.files.get("image")
    name = request.form.get("name")
    price = request.form.get("price")
    desc = request.form.get("description")

    fetch_db_inf = get_user(session.get("user"))
    is_verified = session.get("verified")

    if fetch_db_inf[2] == "admin" and is_verified:
        if name and price and file and desc:
            print("received commission create function")
            print(f"file : {file}\nname : {name}\nprice : {price}\ndesc : {desc}")

            #CREATE FILE AND SAVE IN DESTINATED PATH

            #set the file name
            file_name = secure_filename(file.filename)
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            upload_dir = os.path.join(BASE_DIR, "static", "assets", "uploads")

            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            upload_path = os.path.join(upload_dir, file_name)

            file.save(upload_path)

            image_url = "/static/assets/uploads/" + file_name

            print("Saved to:", upload_path)
            print("URL:", image_url)

            print(image_url)

            create_comission_list(name, price, desc, image_url)
            return jsonify({"status" : "ok"})
    else:
        return jsonify({"status" : "error"})


@app.route("/make_request", methods=["POST"])
def make_request():
    
    title = request.form.get("title")
    description = request.form.get("description")
    usage = request.form.get("usage")
    total_price = request.form.get("total_price")
    cms_name = request.form.get("cms_name")

    images = request.files.getlist("images")
    print("*"*20)
    print(title)
    print(description)
    print(usage)

    rq_id = add_commission_request(cms_name, description, session.get("user"), total_price)
    
    for image in images:
        print(image.filename)
        #set the file name
        file_name = secure_filename(image.filename)
        ext = os.path.splitext(image.filename)[1]

        new_filename = f"{uuid.uuid4()}{ext}"
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        upload_dir = os.path.join(BASE_DIR, "static", "assets", "uploads")

        upload_path = os.path.join(upload_dir, new_filename)

        image.save(upload_path)

        image_url = "/static/assets/usr_upload/" + new_filename

        add_request_image(rq_id, image_url)
        
        print("Saved to:", upload_path)
        print("URL:", image_url)

        print(image_url)
    print("*"*20)



    return jsonify({
        "status": "success"
    })

app.run()