#!/usr/bin/env python
from flask import session, request
from flask_socketio import Namespace, emit, join_room

class deployments(Namespace):
  """
  This class specifies the deployments namespace object
  """
  def on_room_subscribe_event(self, message):
    """
    Method to handle room subscriptions
    """
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('room_subscribe_event_callback', {'data': 'Joined successfully', 'room': message['room']}) 

  def on_connect(self):
    """
    Method to handle connection events
    """
    emit('connect_callback', {'data': 'Connected', 'count': 0})

  def on_disconnect(self):
    """
    Method to handle disconnect events
    """
    print('Client disconnected', request.sid)
