from site import addsitedir
addsitedir("../../")
import db

from .config import create_blueprint, render_template

main_views = create_blueprint("main")

@main_views.route("/")
def do_main_home():    
    id_ = db.insert_one({"val" : "test2"})
    print(f"{type(id_)} {id_}")
    return render_template("index.html")