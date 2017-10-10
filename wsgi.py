from bottle import Bottle, request, response, abort, redirect
from bottle_sqlite import SQLitePlugin
from bcrypt import checkpw
from jwt import encode, decode, DecodeError, ExpiredSignature
import datetime
import inspect

app = application = Bottle()

app.config.load_config('oj.cfg')
app.install(SQLitePlugin(dbfile=app.config.get('sqlite.dbfile')))

exp_time = eval(app.config.get('jwt.exp_time'))
jwt_secret = app.config.get('jwt.secret')

class ErrorHandler:
    def get(self, ignore, default):
        def error_handler(error):
            from json import dumps
            from bottle import tob
            return tob(dumps({ "status_code": error.status_code, "status": error.status, "reason": error.body }))
        return error_handler

app.error_handler = ErrorHandler()

def require_auth(f):
    def wrapped_func(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            abort(401, 'The page needs authorization but no header is present')
        try:
            tok = decode(auth.encode('utf-8'), jwt_secret)
        except DecodeError:
            abort(401, 'You should provide a valid token')
        except ExpiredSignature:
            abort(401, 'Token Expired')
        argspec = inspect.getfullargspec(f)
        if 'user' in argspec.args:
            kwargs['user'] = tok['user_id']
        if 'role' in argspec.args:
            kwargs['role'] = tok['role']
        return f(*args, **kwargs)

    return wrapped_func


@app.post('/api/token')
def auth(db):
    user_info = request.json
    try:
        user_id = int(user_info['user_id'])
    except ValueError:
        abort(400, 'User id must be a number')
    row = db.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchone()
    if not row:
        abort(404, 'User {} not found'.format(user_id))
    _, secret, role = row
    if not checkpw(user_info['password'].encode('utf-8'), secret):
        abort(422, 'User {} provided a wrong password'.format(user_id))
    token = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=exp_time)
    }
    return {'token': encode(token, jwt_secret).decode('utf-8')}

@app.post('/api/submission')
@require_auth
def submit(user, role):
    if role is not "student":
        abort(401, 'Authorization failed')


@app.post('/api/status')

@app.get('/hello')
@require_auth
def hello(user):
    return "Welcome {}".format(user)

@app.get('/home')
def home():
    return "FUCK"

if __name__ == '__main__':
    app.run()
