__all__ = ()

from quart import render_template, redirect, request, send_file, jsonify, session
from quart import Blueprint
from functools import wraps
from blueprints.utils import flash
import db
import os
from blueprints.utils import crop_image
from PIL import Image


frontend = Blueprint('frontend', __name__)


def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not session:
            return await flash('error', 'You must be logged in to access that page.', 'login')
        if 'username' not in session:
            return await flash('error', 'You must be logged in to access that page.', 'login')
        return await func(*args, **kwargs)

    return wrapper


@frontend.route('/')
@frontend.route('/home')
async def home_page():  # put application's code here
    return await render_template('home.html')


@frontend.route('/lb')
@frontend.route('/leaderboard')
async def leaderboard():  # put application's code here
    return await render_template('leaderboard.html')


@frontend.route('/login', methods=['GET', "POST"])
async def login():
    if request.method == 'GET':
        goto = request.args.get("goto")
        if goto:
            session['goto'] = goto
        else:
            session['goto'] = '/dashboard'
        if "username" in session:  # if the user already logged in, we don't need him to login again
            togo = session['goto']
            session['goto'] = '/dashboard'
            return redirect(togo)
        return await render_template('login.html')
    user = (await request.form).get('email')
    pwd = (await request.form).get('password')
    print("Login User: " + user)
    print("with passwd: " + str(pwd))
    status = db.checklogin(user, pwd)
    if status == 0:
        togo = session['goto']
        session['username'] = user
        session['goto'] = '/dashboard'
        return redirect(togo)
    elif status == 1:
        return await flash('error', 'Wrong username or password.', 'login')
    else:
        return await flash('error', 'User does not exist. You can register in the game.', 'login')


@frontend.route('/logout')
@login_required
async def logout():
    del session['username']
    return await flash('success', 'Logout successful!', 'login')


@frontend.route('/dashboard')
@login_required
async def dashboard():
    return await render_template('dashboard.html')


@frontend.route('/settings', methods=['GET', 'POST'])
@login_required
async def accountsettings():
    if request.method == 'GET':
        return await render_template('settings.html')
    ALLOWED_EXTENSIONS = ['.jpeg', '.jpg', '.png']
    avatara = (await request.files).get('avatar')
    if avatara is None or not avatara.filename:
        return await flash('error', 'No image was selected!', 'settings')
    filename, file_extension = os.path.splitext(avatara.filename.lower())
    # bad file extension; deny post
    if not file_extension in ALLOWED_EXTENSIONS:
        return await flash('error', 'The image you select must be either a .JPG, .JPEG, or .PNG file!',
                           'settings')
    pilavatar = Image.open(avatara.stream)
    pilavatar = crop_image(pilavatar)
    newname = str(session['username']) + '.png'
    pilavatar.convert("RGB").save(os.path.join('data/avatar', newname))
    return await flash('success', 'Successfully uploaded the new avatar', 'settings')

@frontend.route('/downloads/simon.exe')
async def getLatestExe():
    return await send_file('./data/release/simon.exe')
