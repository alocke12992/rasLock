import functools
import threading
from werkzeug.local import LocalProxy

from flask import (
  flash, g, request, url_for, Blueprint, jsonify, Response, after_this_request,
  current_app
)

import time
from app.db import get_db

bp = Blueprint('alarm', __name__, url_prefix='/')

def set_alarm_status(arm=0, alarm_triggered=0):
  db = get_db()
  alarm = db.execute(
    'SELECT * FROM alarm WHERE name = "main"').fetchone()
  if not alarm:
    db.execute('INSERT INTO alarm (name) VALUES ("main")')
    db.commit()
  data = (arm, alarm_triggered)
  db.execute('UPDATE alarm SET armed=?, alarm_triggered=? WHERE name = "main"', data)
  db.commit()

def get_status():
  db = get_db()
  data = db.execute('SELECT armed, alarm_triggered FROM alarm WHERE name = "main"').fetchone()
  armed = bool(data[0])
  alarm_triggered = bool(data[1])
  return {"armed": armed, "alarm_triggered": alarm_triggered}

def sentry(app):
    print("Starting sentry")
    armed = True
    count = 0
    while armed:
      print("COUNT")
      print(count)
      with app.app_context():
        status = get_status()
        if not status["armed"]:
          print("breaking")
          armed = False
          break
      time.sleep(1)
      count += 1
      print("sleeping")

@bp.route('/status')
def status():
  status = get_status()
  return jsonify(status), 200

@bp.route('/arm')
def arm():
  set_alarm_status(arm=1)
  # print("CURRENTAPP CONTEXT")
  app = current_app._get_current_object()
  thread = threading.Thread(target=sentry, args=(app,))
  thread.start()
  return jsonify({"status": "armed"}), 200

@bp.route('/disarm')
def disarm():
  set_alarm_status()
  status = get_status()
  return jsonify(status), 200
