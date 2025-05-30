from quart import Quart, render_template
import config

app = Quart(__name__)
app.secret_key = 'MS114514'


@app.template_global()
def appVersion() -> str:
    return 'v1.2'


@app.template_global()
def appName() -> str:
    return 'Simon Game'


@app.errorhandler(404)
async def page_not_found(e):
    # NOTE: we set the 404 status explicitly
    return (await render_template('404.html'), 404)


@app.errorhandler(500)
async def page_not_found(e):
    # NOTE: we set the 500 status explicitly
    return (await render_template('500.html'), 500)


from blueprints.frontend import frontend

app.register_blueprint(frontend)

from blueprints.api import api

app.register_blueprint(api, url_prefix='/api')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.port)
