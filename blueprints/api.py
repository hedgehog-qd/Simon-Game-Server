__all__ = ()

from quart import render_template, redirect, request, jsonify
from quart import Blueprint, send_file
import db
import os

from quart import session

api = Blueprint('api', __name__)
@api.route('/putpp')
async def putpp():
    session['pp'] = "asas"
    return "1"

@api.route('/getpp')
async def getpp():
    return session['pp']

@api.route('/login')
async def api_login():
    uname = str(request.args['uname'])
    passwd = str(request.args['passwd'])
    if uname == "" or passwd == "":
        return '2'  # empty uname or passwd
    if db.checklogin(uname, passwd) == 2:  # user does not exist
        db.register(uname, passwd)
        session['uname'] = uname
        return '0'  # OK
    if db.checklogin(uname, passwd) == 1:  # password incorrect
        return '1'  # wrong passwd
    else:
        session['uname'] = uname
        return '0'  # OK


@api.route('/getAvatar')  # Attention: Avatar image file should be 72 * 72 .png
async def apiGetAvatar():
    uname = session['uname']
    if os.path.exists('./data/avatar/' + uname + '.png'):
        return await send_file('./data/avatar/' + uname + '.png')
    else:
        return await send_file("./data/avatar/default.png")


@api.route('/frontendGetAvatar')
async def frontendGetAvatar():
    uname = session['username']
    if os.path.exists('./data/avatar/' + uname + '.png'):
        return await send_file('./data/avatar/' + uname + '.png')
    else:
        return await send_file("./data/avatar/default.png")


@api.route('/getAvatarByName')
async def getAvatarByName():
    uname = str(request.args['uname'])
    if os.path.exists('./data/avatar/' + uname + '.png'):
        return await send_file('./data/avatar/' + uname + '.png')
    else:
        return await send_file("./data/avatar/default.png")


@api.route('/getLeaderBoardData')
async def getLeaderBoardData():
    data = db.dbGetLeaderBoardData()
    json = {
        "status": "0",
        "result": data
    }
    return jsonify(json)


@api.route('/getLeaderBoardMyData')
async def getLeaderBoardMyData():
    uname = session['username']
    data = db.dbGetLeaderBoardMyData(uname)
    json = {
        "status": "0",
        "result": data
    }
    return jsonify(json)


@api.route('/updateScore')
async def updateScore():
    uname = session['uname']
    newscore = float(request.args['newscore'])
    print("Upload Score: " + uname + " - " + str(newscore))
    if newscore > float(db.getHighestScore(uname)):
        db.updateHighestScore(uname, newscore)
    return '0'  # OK


@api.route('/getHighestScore')
async def getHighestScore():
    uname = session['uname']
    return str(db.getHighestScore(uname))


@api.route('/getHighestScoreAchievedTime')
async def getHighestScoreAchievedTime():
    uname = session['uname']
    return str(db.getHighestScTime(uname))


@api.route('/uploadSave', methods=["POST"])
async def uploadSave():
    uname = session['uname']
    saveFileData = await request.data
    save_path = f"./data/saves/{uname}.ini"
    with open(save_path, "wb") as f:
        f.write(saveFileData)
    return "0"


@api.route('/checkSaveExists')
async def checkSaveExists():
    uname = session['uname']
    if os.path.exists('./data/saves/' + uname + '.ini'):
        return "0"
    return "1"


@api.route('/downlaodSave')
async def downloadSave():
    uname = session['uname']
    return await send_file('./data/saves/' + uname + '.ini')

