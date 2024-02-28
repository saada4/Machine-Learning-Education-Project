''' Stores the individual blueprints for various portions of the web app

Main
    - Dummy Page for now
Login/Auth
    - TODO
        - consider a library
API
    - TODO
'''
from .config import create_blueprint, Blueprint
from .main_views import main_views

# create a parent view
all_views: Blueprint = create_blueprint("views")

# add all children
all_views.register_blueprint(main_views)

# publicly exposed things
__all__ = ["all_views"]