import os

# apply eventlet monkey-patching if we're in production mode (serving via eventlet)
from datastem_rest_api_template.config import config
if not config.DEBUG:
    import eventlet
    eventlet.monkey_patch()

from datastem_rest_api_template import create_app, celery, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=os.getenv('PORT', 8081), debug=False)
