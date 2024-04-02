import pandas as pd
import random
import datetime
from concurrent.futures import ProcessPoolExecutor

def generate_transactions_portion(start_date, end_date, amount_participants, amount_securities, transactions_per_process, balance_df, starting_linkcode):
    transactions = []
    linkcode = starting_linkcode  # Initialize with the starting value
    
    for _ in range(transactions_per_process):
        linkcode += 1
        Sending_ID = random.randint(1, amount_participants)
        Receiving_ID = random.randint(1, amount_participants)

        while Sending_ID == Receiving_ID:
            Sending_ID = random.randint(1, amount_participants)
            Receiving_ID = random.randint(1, amount_participants)

        monetary_funds_df = balance_df.loc[(balance_df['Part ID'] == Receiving_ID) & (balance_df['Account ID'] == 0)]
        balance_value = monetary_funds_df['Balance'].iloc[0] if not monetary_funds_df.empty else 0
        transaction_value = generate_transaction_value(balance_value)
        

        day_delta = end_date - start_date
        random_days = random.randint(0, day_delta.days)
        random_date_1 = start_date + datetime.timedelta(days=random_days)

        # New code to generate random_date_2 based on random_date_1
        offsets_counter = [-1, 0, 1]  # Possible offsets: day before, same day, day after
        weights_counter = [0.1, 0.8, 0.1]  # Corresponding weights for each offset

        # Choose an offset
        offset_choice_counter = random.choices(offsets_counter, weights=weights_counter)[0]

        # Compute random_date_2 by adding the chosen offset to random_date_1
        # Make sure that random_date_2 is within the range [start_date, end_date]
        if offset_choice_counter == -1 and random_date_1 > start_date:
            random_date_2 = random_date_1 + datetime.timedelta(days=offset_choice_counter)
        elif offset_choice_counter == 1 and random_date_1 < end_date:
            random_date_2 = random_date_1 + datetime.timedelta(days=offset_choice_counter)
        else:
            random_date_2 = random_date_1  # Default to same day if outside range

        offset_deadline = [0, 1, 2]
        weights_deadline = [0.5, 0.4, 0.1]

        offset_choice_deadline = random.choices(offset_deadline, weights=weights_deadline)[0]
        earliest_date = min(random_date_1, random_date_2)

        if offset_choice_deadline == 0:
            deadline_date = earliest_date + datetime.timedelta(days=offset_choice_deadline)
        elif offset_choice_deadline == 1:
            deadline_date = earliest_date + datetime.timedelta(days=offset_choice_deadline)
        elif offset_choice_deadline == 2:
            deadline_date = earliest_date + datetime.timedelta(days=offset_choice_deadline)
        

        random_insertion_1 = weighted_random_datetime(random_date_1) #, end_date
        random_insertion_2 = weighted_random_datetime(random_date_2) #, end_date
        Security_number = random.randint(1, amount_securities)
        
        new_transaction = {
            'Time': random_insertion_1, 
            'Value': transaction_value, 
            'FromParticipantId': Sending_ID,
            'FromAccountId': Security_number, 
            'ToParticipantId': Receiving_ID,
            'ToAccountId': Security_number, 
            'Linkcode': linkcode,
            'SettlementDeadline': deadline_date
        }
        
        new_counter_transaction = {
            'Time': random_insertion_2, 
            'Value': transaction_value, 
            'FromParticipantId': Receiving_ID,
            'FromAccountId': 0, 
            'ToParticipantId': Sending_ID,
            'ToAccountId': 0, 
            'Linkcode': linkcode,
            'SettlementDeadline': deadline_date
        }
        
        transactions.extend([new_transaction, new_counter_transaction])
    
    return transactions

def generate_transaction_data_parallel(amount_transactions, amount_participants, amount_securities, days_list, balance_df):
    num_processes = 10  # Adjust based on your system capabilities
    transactions_per_process = amount_transactions // num_processes
    
    datetime_list = [datetime.datetime.strptime(day, "%Y-%m-%d") for day in days_list]
    start_date, end_date = min(datetime_list), max(datetime_list)
    
    # Calculate starting linkcodes for each process
    args = [(start_date, end_date, amount_participants, amount_securities, transactions_per_process, balance_df.copy(), i * transactions_per_process + 1) for i in range(num_processes)]
    
    transactions = []
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [executor.submit(generate_transactions_portion, *arg) for arg in args]
        for future in futures:
            transactions.extend(future.result())
    
    transaction_df = pd.DataFrame(transactions)
    transaction_df = transaction_df.sort_values(by='Time').reset_index(drop=True)
    tid_column = range(1, len(transaction_df) + 1)
    transaction_df.insert(0, 'TID', tid_column)
    
    return transaction_df

def random_datetime(start_date, end_date):
    delta = end_date - start_date
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_date + datetime.timedelta(seconds=random_seconds)

def weighted_random_datetime(start_date): #, end_date

    intervals = [
        (datetime.time(0, 0, 0), datetime.time(1, 29, 59), 1), 
        (datetime.time(1, 30, 0), datetime.time(19, 29,59), 4),  
        (datetime.time(19, 30, 0), datetime.time(23, 59, 59), 1)  
    ]
    weights = [interval[2] for interval in intervals]
    
    # Select an interval based on the weights
    selected_interval = random.choices(intervals, weights=weights, k=1)[0]
    
    # Generate a random datetime within the selected interval
    start_interval_time, end_interval_time, _ = selected_interval
    start_interval_datetime = datetime.datetime.combine(start_date, start_interval_time)
    end_interval_datetime = datetime.datetime.combine(start_date, end_interval_time)
    
    # Compute delta and generate random seconds within the interval
    delta = end_interval_datetime - start_interval_datetime
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_interval_datetime + datetime.timedelta(seconds=random_seconds)

def generate_transaction_value(balance):
    transaction_value = random.uniform(0.005, 0.1) * balance
    transaction_value = round(transaction_value,2)
    return transaction_value