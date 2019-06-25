from flask import Flask

app = Flask(__name__, instance_relative_config=True)

from idefix.webui import views

from idefix.webui import config
app.config.from_object(config)