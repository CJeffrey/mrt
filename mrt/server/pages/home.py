from mrt.server.mrt_app import mrt_app


@mrt_app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Welcome to MRT Search System</h1>'
