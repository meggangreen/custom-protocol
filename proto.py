""" Parse binary log file. """

def _get_bin_to_utf_lines(file_path):
    """ Return array of lines in file. """

    with open(file_path, 'rb') as file_name:
        lines = file_name.readlines().decode()

    # return lines
    for line in lines:
        print(line)


def _convert_to_unicode(byte_s, utf_spec):
    """ Returns unicode string at specified encoding. """

    return byte_s.decode('utf-')
