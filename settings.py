# settings 
from os import environ, path

cache_dir = path.join(path.realpath(environ["HOME"]), '.novelcache')
task_limit = 16
