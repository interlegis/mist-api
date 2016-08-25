#!/usr/bin/python

import md5
import json
import time
import requests
import argparse
from datetime import datetime

# MistServer API
# http://mistserver.org/doxygen/api.html

parser = argparse.ArgumentParser(description="""Get statistics from Mistserver,
                                                usage: python mist_logger.py \
                                                --host IP_address \
                                                --user admin_username \
                                                --pwd admin_password
                                             """)
parser.add_argument('--host', required=True, help='Mistserver IP address')
parser.add_argument('--port', required=False, help='Mistserver port address')
parser.add_argument('--user', required=True, help='admin username')
parser.add_argument('--pwd', required=True, help='admin password')
args = parser.parse_args()

HOST = args.host
PORT = int(args.port) if args.port is not None else 4242
MIST_URL = 'http://%s:%s/api' % (HOST, PORT)

USERNAME = args.user
PASSWORD = args.pwd

BASE_CMD = 'command={%s}'
AUTH_CMD = '"authorize": {"username": "%s", "password":"%s"}'
CAPABILITIES = '"capabilities": {}'  # capabilities doesn't have arguments
CLIENTS = '"clients":{"streams":[]}'  # get all clients from all streams
CHALLENGE = None


def hash_password(password, challenge=None):
    m = md5.new()
    m.update(password)
    secret = m.hexdigest()
    if challenge:
        m = md5.new()
        secret += challenge
        m.update(secret)
        secret = m.hexdigest()
    return secret


def get_challenge(username):
    command = BASE_CMD % (AUTH_CMD % (username, ""))
    resp = requests.post(MIST_URL, data=command)
    payload = json.loads(resp.text)
    return payload['authorize']['challenge']


def send_request(username, hashed_password, command=''):
    auth = (AUTH_CMD % (username, hashed_password))
    command = BASE_CMD % ','.join([auth, command])
    resp = requests.post(MIST_URL, data=command)
    payload = json.loads(resp.text)
    return payload


def execute_cmd(username, password, command=''):
    # if first time then retrieve CHALLENGE
    global CHALLENGE
    if CHALLENGE is None:
        CHALLENGE = get_challenge(username)

    # send request
    hashed_pwd = hash_password(password, CHALLENGE)
    resp = send_request(username, hashed_pwd, command)

    # CHALLENGE probably expired
    # get new challenge, re-hash password and send request again
    if resp["authorize"]["status"] == "CHALL":
        CHALLENGE = resp["authorize"]["challenge"]
        hashed_pwd = hash_password(password, CHALLENGE)
        resp = send_request(username, hashed_pwd, command)
    return resp


def record_clients(output_file, username, password, sample_interval_s=20):
    with open(output_file, 'w') as c:
        while True:
            dic = execute_cmd(username, password, CLIENTS)
            header = dic["clients"]["fields"]
            data = dic["clients"]["data"]
            curr_time = dic["clients"]["time"]
            fields = ['host', 'stream', 'protocol', 'conntime']
            # iterate over data
            if data is not None:
                for entry in data:
                    # add caption to data
                    t = zip(header, entry)
                    # print fields
                    line = []
                    for i in t:
                        if i[0] in fields:
                            line.append(str(i[1]))
                    t = datetime.fromtimestamp(curr_time)
                    line.append(t.strftime('%Y-%m-%d'))
                    line.append(t.strftime('%H:%M:%S'))
                    c.write(','.join(line) + '\n')
                    c.flush()
            time.sleep(sample_interval_s)


if __name__ == "__main__":
    output_file = 'mistserver-' + time.strftime('%y-%m-%d-%H-%M') + '.csv'
    record_clients(output_file, USERNAME, PASSWORD)
