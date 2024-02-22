import os

from flask import Blueprint, render_template

configs = {
    "STATIC_LOC" : "../../public",
    "TEMPLATE_LOC" : "../../public"
}

def create_blueprint(name: str, prefix:str = "") -> Blueprint:
    '''Creates a template blueprint
    
    Parameters
        name: prefix to view called in Flask (e.g., url_for("my_name.my_view")) 
        prefix: url prefix for the view (e.g., api which would lead to this /api/my_api_view)
    '''
    return Blueprint(name, __name__, static_folder=configs["STATIC_LOC"], template_folder=configs["TEMPLATE_LOC"], url_prefix=prefix)