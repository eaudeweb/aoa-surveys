from django_assets import Bundle, register


CSS_ASSETS = (
    'css/bootstrap.min.css',
    'css/bootstrap-datetimepicker.css',
    'css/jquery.dataTables.css',
    'css/jquery-ui.min.css',
    'css/jquery-ui.structure.min.css',
    'css/style.css',
)


JS_ASSETS = (
    'js/lib/jquery.min.js',
    'js/lib/bootstrap.min.js',
    'js/lib/moment.js',
    'js/lib/bootstrap-datetimepicker.min.js',
    'js/lib/jquery.dataTables.min.js',
    'js/lib/jquery-ui.min.js',
    'js/aoa.js',
)


css = Bundle(*CSS_ASSETS, filters='cssmin', output='packed.css')
js = Bundle(*JS_ASSETS, filters='jsmin', output='packed.js')
register('css', css)
register('js', js)
