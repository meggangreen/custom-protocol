""" Parse binary log file. """

import struct

def _get_bytes(file_path):
    """ Return array of lines in file. """

    with open(file_path, 'rb') as file_name:
        data = file_name.read()

    return data


def _convert_to_unicode(byte_s, utf_spec):
    """ Returns unicode string at specified encoding. """

    return byte_s.decode('utf-')
