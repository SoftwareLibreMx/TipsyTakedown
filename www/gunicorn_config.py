from glob import glob

bind = '0.0.0.0'
port = 8000
workers = 1
loglevel = 'info'
reload = True
reload_extra_files = sum(
    [
        glob(
            'webapp/static/**/*.' +
            ext,
            recursive=True) +
        glob(
            'webapp/templates/**/*.' +
            ext,
            recursive=True) for ext in [
            'html',
            'css',
            'js']],
    [])
errorlog = '-'
accesslog = '-'
