from site import addsitedir
addsitedir("../../")
import db

from .config import create_blueprint, render_template

main_views = create_blueprint("main")

@main_views.route("/")
def do_main_home():    
    ids = db.insert_many([{"val" : "test3"}, {"val" : "test4"}])
    print(f"{type(ids)} {ids}")
    return render_template("index.html")