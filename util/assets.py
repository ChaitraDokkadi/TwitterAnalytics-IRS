# IRP4/util/assets.py

from flask_assets import Bundle, Environment
from .. import main

bundles = {

    'home_js': Bundle(
        'js/core/jquery.min.js',
        'js/core/popper.min.js',
        'js/core/bootstrap.min.js',
        'js/plugins/perfect-scrollbar.jquery.min.js',
        'js/plugins/chartjs.min.js',
        'js/plugins/bootstrap-notify.js',
        'js/dashboard-ui.js-1.2.0',
        'js/dashboard.js',
        output='gen/dashboard.js'),

    'home_css': Bundle(
        'css/bootstrap-ui.css',
        'css/dashboard.css',
        'css/index.css',
        'css/dashboard-ui.css',
        output='gen/dashboard.css'),
}
Bundle(depends='css/dashboard.scss')

assets = Environment(main)

assets.register(bundles)
