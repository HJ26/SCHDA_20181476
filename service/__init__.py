from flask import Flask
from flask import request
import os
from src import user, mylogger, myconfig
import pdb

app = Flask(__name__)

# create a logger.
project_root_path = os.getenv("SCHDA_20181476")
cfg = myconfig.get_config('{}/share/project.config'.format(
    project_root_path))
log_directory = cfg['logger'].get('log_directory')
logger = mylogger.get_logger('login', log_directory)

@app.route('/login', methods=["POST"])
def login():
    user_id = request.json.get('user_id')
    passwd = request.json.get('passwd')
    logger.info('{}: login'.format(user_id))

    ret = {"result": None,
        "session_key": None,
        "msg": ""}

    session_key = user.login(user_id, passwd, logger)
    logger.info('{}: session_key = {}'.format(user_id, session_key))
    if not session_key:
        ret["result"] = False
        ret["msg"] = "Failed to login"
    else:
        ret["result"] = True
        ret["session_key"] = session_key

    logger.info('{}: login result = {}'.format(user_id, ret))
    return ret

