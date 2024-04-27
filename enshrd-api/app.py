import sys, subprocess, json, shlex
from flask import Flask, request, render_template
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
# Provide proper enshrouded_server.json location"
json_conf = '/home/enshrouded/enshroudedserver/enshrouded_server.json'
app.secret_key = '5Z1uFfQ6TvsdgHVfnNuogTi9n14xCk9yIeM3FSWdEU9UAivznk63'
auth = HTTPBasicAuth()

with open(json_conf, 'r') as jsonfile: 
    jsondata = json.load(jsonfile)
pwresp = jsondata['password']

@auth.verify_password
def verify_password(username, password):
    if password == pwresp:
        return True
    return False

@app.route('/')
@auth.login_required
def steamquery():
    output = subprocess.check_output(shlex.split('./enshrd_query -c'))
    output = output.decode('utf-8')
    return render_template('result.html', info=output)

if __name__ == '__main__':
    app.run()

