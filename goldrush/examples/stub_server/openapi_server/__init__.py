from gevent import monkey
monkey.patch_all()

from openapi_server.__main__ import app
