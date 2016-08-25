#!/usr/bin/python

from mist_api import mist_api

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



def record_clients(output_file, username, password, sample_interval_s=20):
    with open(output_file, 'w') as c:
        while True:
            dic = mist_api.execute_cmd(username, password, CLIENTS)
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


