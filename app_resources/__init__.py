''' Stores routes, configurations, etc. for the Flask app

Configurations
    - MongoDB login TODO
Views
    - all_views: Blueprint of page views to feed to the Flask app
'''
from .views import all_views

# Publicly exposed items from the module

__all__ = ["all_views"]