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

def answer_adhoc_questions(filepath):
    """ Manager function to calculate and print answers to provided questions. """

    log = _get_bytes(filepath)
    if not _has_valid_header(log):
        print("Invalid header")
        return

    records = _get_records(log)

    total_debit_amount = sum([r.amount for r in records  if r.r_type == 0])
    total_credit_amount = sum([r.amount for r in records if r.r_type == 1])
    num_autopays_started = len([r for r in records if r.r_type == 2])
    num_autopays_ended = len([r for r in records if r.r_type == 3])

    user_bal = 0
    for record in records:
        if record.user == 2456938384156277127:
            if record.r_type == 0:
                user_bal -= record.amount
            elif record.r_type == 1:
                user_bal += record.amount

    print(f"total credit amount={total_credit_amount}")
    print(f"total debit amount={total_debit_amount}")
    print(f"autopays started={num_autopays_started}")
    print(f"autopays ended={num_autopays_ended}")
    print(f"balance for user 2456938384156277127={user_bal}")


################################################################################

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    answer_adhoc_questions(filepath='txnlog.dat')
