""" Parse binary log file. """

import struct
from collections import namedtuple

def _get_bytes(file_path):
    """ Return array of lines in file. """

    with open(file_path, 'rb') as file_name:
        data = file_name.read()

    return data


def _parse_log(log):
    """ Return header information and Records as namedtuples. """

    record_data = log[9:]
    Record = namedtuple('Record', 'r_type timestamp user amount')
    records = []

    mainframe = struct.unpack('>4s', bytes(log[0:4]))[0]
    version = struct.unpack('>b', bytes(log[4:5]))[0]
    num_recs = struct.unpack('>L', bytes(log[5:9]))[0]

    i = 0
    while i < len(record_data):
        r_type = struct.unpack('>b', bytes(record_data[i:i+1]))[0]  # [i] doesn't work
        ts = struct.unpack('>L', bytes(record_data[i+1:i+5]))[0]
        user = struct.unpack('>Q', bytes(record_data[i+5:i+13]))[0]
        if r_type in [0, 1]:
            amt = struct.unpack('>d', bytes(record_data[i+13:i+21]))[0]
            i += 21
        else:
            amt = ""
            i += 13
        records.append(Record(r_type, ts, user, amt))

    return (mainframe, version, num_recs, records)


def print_log(file_path):
    """ Print log in human readable format. """

    log = _get_bytes(file_path)
    mainframe, version, num_recs, records = _parse_log(log)

    title = "{} v{} | {} Records".format(mainframe.decode('utf-8'),
                                         version,
                                         num_recs)
    header = ("| Record type " +
              "| Unix timestamp " +
              "| User ID             " +
              "| Amount in dollars |")
    print(title, "\n", header, sep='')
    for record in records:
        print("| {:11} | {:14} | {:19} | {:17.17} |".format(str(record.r_type),
                                                            str(record.timestamp),
                                                            str(record.user),
                                                            str(record.amount)))


def answer_adhoc_questions():
    """  """

    file_path = "txnlog.dat"

