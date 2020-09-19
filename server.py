#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, os
import datetime

from flask import Flask, request, Response
from slack import WebClient
# from boto.s3.connection import S3Connection
# from slackclient import SlackClient

app = Flask(__name__, template_folder='')
# Set the token from the secret environment variables.
client = WebClient(token=os.environ.get('TOKEN'))

@app.route('/', methods=['GET'])
def main():
  return Response("To get started, remix this project and check out the README file!")

# Step 4: The path that allows for your server to receive information from the modal sent in Slack
@app.route('/interactive', methods=['POST'])
def interactive():
    payload = json.loads(request.form["payload"])

    type = payload["view"]["title"]["text"]

    if type == "Fitness scheduler":
        channelID = "C01BA6R20UR"
        user_text = fitnessOutput(payload)
        client.chat_postMessage(channel=channelID, link_names=1, text=user_text)

    elif type == "Backyard scheduler":
        channelID = "C01BA6R20UR"
        user_text = backyardOutput(payload)
        client.chat_postMessage(channel=channelID, link_names=1, text=user_text)

    return Response()

def fitnessOutput(payload):
  getall = payload["view"]["state"]["values"]

  hour= getall["hourBlock"]["hourAction"]["value"]
  type= getall["typeBlock"]["typeAction"]["selected_option"]["text"]["text"]

  if "coachBlock" in getall.keys():
    coach="with coach "+ getall["coachBlock"]["coachAction"]["selected_option"]["text"]["text"]
  else:
    coach=""

  if "durationBlock" in getall.keys():
    duration = getall["durationBlock"]["durationAction"]["value"] + " "
  else:
    duration = ""

  if "locationBlock" in getall.keys():
    location = getall["locationBlock"]["locationAction"]["value"] + " "
  else:
    location = ""

  text = "Hello <!channel>, who is down for {0}{1}{2} {3}at {4} today? ".format(duration,type,coach,location,hour)
  return text


def backyardOutput(payload):
  getall = payload["view"]["state"]["values"]

  number= getall["number"]["numberAction"]["value"]
  date = getall["dateBlock"]["dateAction"]["selected_date"]
  hour= getall["hourBlock"]["hourAction"]["selected_option"]["text"]["text"]
  print (payload)
  d = datetime.datetime(int(date.split("-")[0]),int(date.split("-")[1]),int(date.split("-")[2]))
  day = d.strftime('%A')
  user = payload["user"]["id"]

  if "commentBlock" in getall.keys():
    comments =  getall["commentBlock"]["commentAction"]["value"]
    finalComments= "They also mentiond that" + "" + comments
  else:
    finalComments = ""

  user_text= "Hello <!channel>,\n \n <@{6}> Is having {0} guests in the backyard on {1}, {2} {3} in the {4}. {5}".format(number,day, d.strftime("%B"), d.day, hour.split("(")[0], finalComments, user)

  return text

# Step 5: Payload is sent to this endpoint, we extract the `trigger_id` and call views.open
@app.route('/slashcommand', methods=['GET', 'POST'])
def slashcommand():
    with open("modal.txt") as modalfile:
        client.views_open(trigger_id=request.form["trigger_id"], view=json.load(modalfile))
    return Response()


@app.route('/fitcommand', methods=['GET', 'POST'])
def fitcommand():
    with open("fitness.txt") as fitfile:
        client.views_open(trigger_id=request.form["trigger_id"], view=json.load(fitfile))
    return Response()


if __name__ == '__main__':
    app.run()
