""" Parse binary log file. """

from struct import unpack, unpack_from
from collections import namedtuple

def _get_bytes(filepath):
    """ Return string of bytes in file.

        >>> data = _get_bytes('txnlog.dat')
        >>> len(data)
        1377
        >>> data[0:4]
        b'MPS7'

    """

    with open(filepath, 'rb') as f:
        data = f.read()

    return data


def _has_valid_header(log, req_format=b"MPS7"):
    """ Returns True if log header validates to requested format.

        >>> log = _get_bytes('txnlog.dat')
        >>> _has_valid_header(log)
        True
    """

    return unpack_from('!4s', log, offset=0)[0] == req_format


def _get_records(log):
    """ Return Records as list of namedtuples.

        >>> log = _get_bytes('txnlog.dat')
        >>> records = _get_records(log)
        >>> records[0].user
        4136353673894269217

    """

    Record = namedtuple('Record', 'r_type time user amount')
    records = []
    r_types_with_amounts = [0, 1]

    offset = 9  # Bytes 0 thru 8 are the header
    while offset < len(log):
        r_type, time, user = unpack_from('!bLQ', log, offset=offset)

        # Capture the transaction amount for debits and credits
        if r_type in r_types_with_amounts:
            amount = unpack_from('!d', log, offset=offset+13)[0]
            offset += 21
        else:
            amount = None
            offset += 13

        records.append(Record(r_type, time, user, amount))

    return records

# Generally should probably raise an error if len(records) != num_records

def print_log(filepath, num=15):
    """ Print log in human readable format. """

    log = _get_bytes(filepath)
    # mainframe, version, num_recs,
    records = _get_records(log)
    if len(records) < num:
        num = len(records)

    # title = "{} v{} | {} Records".format(mainframe.decode('utf-8'),
    #                                      version,
    #                                      num_recs)
    title = None
    rec_cols = "| {:12} | {:14} | {:19} | {:17.17} |"
    header = rec_cols.format("Record type",
                             "Unix timestamp",
                             "User ID",
                             "Amount in dollars")
    print(title, "\n", header, sep='')

    record_types = ["Debit", "Credit", "StartAutopay", "EndAutopay"]
    for record in records[:num]:
        r_type = record_types[record.r_type]
        amount = str(record.amount) if record.amount else ""
        print(rec_cols.format(r_type, record.time, record.user, amount))


def answer_adhoc_questions():
    """ With Records, calculate and print answers to provided questions. """

    filepath = "txnlog.dat"
    log = _get_bytes(filepath)
    mainframe, version, num_recs, records = _get_records(log)

    total_debits = sum([r.amount for r in records  if r.r_type == 0])
    total_credits = sum([r.amount for r in records if r.r_type == 1])
    count_autopays_started = len([r for r in records if r.r_type == 2])
    count_autopays_ended = len([r for r in records if r.r_type == 3])
    user_bal = 0
    for record in records:
        if record.user != 2456938384156277127:
            continue
        if record.r_type == 0:
            user_bal -= record.amount
        if record.r_type == 1:
            user_bal += record.amount

    print("\n>>> What is the total amount in dollars of debits?\n",
          total_debits, sep="")
    print("\n>>> What is the total amount in dollars of credits?\n",
          total_credits, sep="")
    print("\n>>> How many autopays were started?\n",
          count_autopays_started, sep="")
    print("\n>>> How many autopays were ended?\n",
          count_autopays_ended, sep="")
    print("\n>>> What is balance of user ID 2456938384156277127?\n",
          "If they started from zero, the balance is ", user_bal, sep="")


################################################################################

if __name__ == '__main__':
    import doctest
    doctest.testmod()
