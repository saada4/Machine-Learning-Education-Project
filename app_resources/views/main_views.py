from .config import create_blueprint, render_template

main_views = create_blueprint("main")

@main_views.route("/")
def do_main_home():
    return render_template("index.html")