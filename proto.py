""" Parse binary log file. """

from struct import unpack
from collections import namedtuple

def _get_bytes(file_path):
    """ Return string of bytes in file. """

    with open(file_path, 'rb') as file_name:
        data = file_name.read()

    return data


def _parse_log(log):
    """ Return header information and Records as namedtuples. """

    record_data = log[9:]
    Record = namedtuple('Record', 'r_type timestamp user amount')
    records = []

    # The slicing in these struct commands is not nice to read
    mainframe = unpack('>4s', bytes(log[0:4]))[0]
    version = unpack('>b', bytes(log[4:5]))[0]
    num_recs = unpack('>L', bytes(log[5:9]))[0]

    i = 0
    while i < len(record_data):
        r_type = unpack('>b', bytes(record_data[i:i+1]))[0]  # [i] doesn't work
        ts = unpack('>L', bytes(record_data[i+1:i+5]))[0]
        user = unpack('>Q', bytes(record_data[i+5:i+13]))[0]

        if r_type in [0, 1]:
            amt = unpack('>d', bytes(record_data[i+13:i+21]))[0]
            i += 21
        else:
            amt = None
            i += 13

        records.append(Record(r_type, ts, user, amt))

    # Generally should probably raise an error if num_records != len(records)

    return (mainframe, version, num_recs, records)


def print_log(file_path, num=15):
    """ Print log in human readable format. """

    log = _get_bytes(file_path)
    mainframe, version, num_recs, records = _parse_log(log)
    if len(records) < num:
        num = len(records)

    title = "{} v{} | {} Records".format(mainframe.decode('utf-8'),
                                         version,
                                         num_recs)
    header = "| {:12} | {:14} | {:19} | {:17} |".format("Record type",
                                                        "Unix timestamp",
                                                        "User ID",
                                                        "Amount in dollars")
    print(title, "\n", header, sep='')
    for record in records[:num]:
        if record.r_type == 0:
            r_type = "Debit"
        elif record.r_type == 1:
            r_type = "Credit"
        elif record.r_type == 2:
            r_type = "StartAutopay"
        elif record.r_type == 3:
            r_type = "EndAutopay"
        amount = str(record.amount) if record.amount else ""
        print("| {:12} | {:14} | {:19} | {:17.17} |".format(r_type,
                                                            record.timestamp,
                                                            record.user,
                                                            amount))


def answer_adhoc_questions():
    """  """

    file_path = "txnlog.dat"
    log = _get_bytes(file_path)
    mainframe, version, num_recs, records = _parse_log(log)

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
