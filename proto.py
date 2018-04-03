""" Parse binary log file. """

import struct

def _get_bytes(file_path):
    """ Return array of lines in file. """

    with open(file_path, 'rb') as file_name:
        data = file_name.read()

    return data


def print_log(file_path):
    """ Print log in human readable format. """

    log = _get_bytes(file_path)
    records = log[9:]

    index_map = {'mainframe:' ()}

    # Log format:
    # MPS7 vV | R Records
    # | Record type | Unix timestamp | user ID             | amount in dollars |
    mainframe = struct.unpack('>4s', bytes(log[0:4]))[0]
    version = struct.unpack('>b', bytes(log[4:5]))[0]
    num_recs = struct.unpack('>L', bytes(log[5:9]))[0]


    for i in range(len(records)):
        r_type = struct.unpack('>b', bytes(data[i:i+1]))[0]  # [i] doesn't work
        ts = struct.unpack('>L', bytes(data[9:10]))[0]




