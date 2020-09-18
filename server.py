#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, os
import datetime

from flask import Flask, request, Response
from slack import WebClient

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
    # Extra Credit: Uncomment out this section
    channelID = "C01BA6R20UR"
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
    # user_text = comments
    client.chat_postMessage(channel=channelID, text=user_text)
    return Response()
  
# Step 5: Payload is sent to this endpoint, we extract the `trigger_id` and call views.open
@app.route('/slashcommand', methods=['GET', 'POST'])
def slashcommand():
    with open("modal.txt") as modalfile:
        client.views_open(trigger_id=request.form["trigger_id"], view=json.load(modalfile))
    return Response()

if __name__ == '__main__':
    app.run()