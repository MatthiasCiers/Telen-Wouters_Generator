import pandas as pd
import numpy as np
import random
import datetime
from concurrent.futures import ProcessPoolExecutor

def generate_transactions_portion(weights_matrix, start_date, end_date, amount_participants, amount_securities, transactions_per_process, balance_df, starting_linkcode):
    transactions = []
    linkcode = starting_linkcode  # Initialize with the starting value
    
    
    for _ in range(transactions_per_process):
        linkcode += 1
        Sending_ID = random.randint(0, amount_participants - 1)
        receiver_weights = weights_matrix[Sending_ID]
        Receiving_ID = random.choices(range(amount_participants), receiver_weights)[0]
        Sending_ID = Sending_ID + 1
        Receiving_ID = Receiving_ID + 1

        monetary_funds_df = balance_df.loc[(balance_df['Part ID'] == Receiving_ID) & (balance_df['Account ID'] == 0)]
        balance_value = monetary_funds_df['Balance'].iloc[0] if not monetary_funds_df.empty else 0
        transaction_value = generate_transaction_value(balance_value)
        

        day_delta = end_date - start_date
        random_days = random.randint(0, day_delta.days)
        random_date_1 = start_date + datetime.timedelta(days=random_days)

        # New code to generate random_date_2 based on random_date_1
        offsets_counter = [-1, 0, 1]  # Possible offsets: day before, same day, day after
        weights_counter = [0, 0.7, 0.3]  # Corresponding weights for each offset

        # Choose an offset
        offset_choice_counter = random.choices(offsets_counter, weights=weights_counter)[0]

        # Compute random_date_2 by adding the chosen offset to random_date_1
        # Make sure that random_date_2 is within the range [start_date, end_date]
        #if offset_choice_counter == -1 and random_date_1 > start_date:
        #    random_date_2 = random_date_1 + datetime.timedelta(days=offset_choice_counter)
        if offset_choice_counter == 1 and random_date_1 < end_date:
            random_date_2 = random_date_1 + datetime.timedelta(days=offset_choice_counter)
        else:
            random_date_2 = random_date_1  # Default to same day if outside range

        offset_deadline = [0, 1, 2]
        weights_deadline = [0, 15, 85] #[0.5, 0.4, 0.1] [0.2,0.3,0.5]

        offset_choice_deadline = random.choices(offset_deadline, weights=weights_deadline)[0]
        earliest_date = min(random_date_1, random_date_2)

        if offset_choice_deadline == 0:
            deadline_date = earliest_date + datetime.timedelta(days=offset_choice_deadline)
        elif offset_choice_deadline == 1:
            deadline_date = earliest_date + datetime.timedelta(days=offset_choice_deadline)
        elif offset_choice_deadline == 2:
            deadline_date = earliest_date + datetime.timedelta(days=offset_choice_deadline)
        

        random_insertion_1 = weighted_random_datetime(random_date_1)
        random_insertion_2 = weighted_random_datetime(random_date_2) 
        Security_number = random.randint(1, amount_securities)
        
        new_transaction = {
            'Time': random_insertion_1, 
            'Value': transaction_value, 
            'FromParticipantId': Sending_ID,
            'FromAccountId': Security_number, 
            'ToParticipantId': Receiving_ID,
            'ToAccountId': Security_number, 
            'Linkcode': linkcode,
            'SettlementDeadline': deadline_date,
            'T+x': offset_choice_deadline
        }
        
        new_counter_transaction = {
            'Time': random_insertion_2, 
            'Value': transaction_value, 
            'FromParticipantId': Receiving_ID,
            'FromAccountId': 0, 
            'ToParticipantId': Sending_ID,
            'ToAccountId': 0, 
            'Linkcode': linkcode,
            'SettlementDeadline': deadline_date,
            'T+x': offset_choice_deadline
        }
        
        transactions.extend([new_transaction, new_counter_transaction])
    
    return transactions

def generate_transaction_data_parallel(amount_transactions, amount_participants, amount_securities, days_list, balance_df):
    num_processes = 10  # Adjust based on your system capabilities
    transactions_per_process = amount_transactions // num_processes
    
    datetime_list = [datetime.datetime.strptime(day, "%Y-%m-%d") for day in days_list]
    start_date, end_date = min(datetime_list), max(datetime_list)
    weights_matrix = generate_symmetric_weight_matrix(amount_participants)
    
    
    # Calculate starting linkcodes for each process
    args = [(weights_matrix, start_date, end_date, amount_participants, amount_securities, transactions_per_process, balance_df.copy(), i * transactions_per_process + 1) for i in range(num_processes)]
    
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

def generate_transaction_value(balance):
    transaction_value = random.uniform(0.005, 0.1) * balance
    transaction_value = round(transaction_value,2)
    return transaction_value

def generate_weight_matrix(size):
    # Initialize an empty matrix with zeros
    matrix = np.zeros((size, size))
    
    for i in range(size):
        # Generate `size - 1` random numbers for each row, excluding the diagonal
        weights = np.random.rand(size - 1)
        # Normalize these weights to sum up to 1
        normalized_weights = weights / np.sum(weights)
        
        # Insert normalized weights into the matrix, skipping the diagonal
        matrix[i, :i] = normalized_weights[:i]
        matrix[i, i+1:] = normalized_weights[i:]
    
    return matrix

def generate_symmetric_weight_matrix(size):
    # Initialize an empty matrix with zeros
    matrix = np.zeros((size, size))
    
    for i in range(size):
        for j in range(i + 1, size):
            # Generate a single random number for each pair and set both (i, j) and (j, i)
            weight = np.random.rand()
            matrix[i, j] = weight
            matrix[j, i] = weight
    
    # Normalize rows excluding the diagonal to ensure row sums (excluding diagonal) are 1
    for i in range(size):
        row_sum = np.sum(matrix[i]) - matrix[i, i]  # Exclude the diagonal value from the sum
        matrix[i] /= row_sum  # Normalize the row
        matrix[i, i] = 0  # Ensure the diagonal is 0 after normalization
    #print(matrix)
    df = pd.DataFrame(matrix)
    csv_filename = "symmetric_weight_matrix.csv"
    df.to_csv(csv_filename, index=False)
    return matrix
    

def weighted_random_datetime(start_interval_datetime):
    # Time boundaries in seconds since start of the day
    start_of_day = 0  # 0:00 AM
    interval1_end = 1 * 60 * 60 + 30 * 60  # 1:30 AM
    interval2_end = 19 * 60 * 60 + 30 * 60  # 7:30 PM
    end_of_day = 24 * 60 * 60  # 24:00

    # Length of each period in seconds
    period1_length = interval1_end - start_of_day
    period2_length = interval2_end - interval1_end
    period3_length = end_of_day - interval2_end

    # Adjust period 2 length for increased chance
    # Example factor: 2 (making it twice as likely per hour compared to the others)
    adjusted_period2_length = period2_length * 5

    # Calculate adjusted total length
    adjusted_total_length = period1_length + adjusted_period2_length + period3_length

    # Probability of choosing each period (proportional to its adjusted length)
    p1 = period1_length / adjusted_total_length
    p2 = adjusted_period2_length / adjusted_total_length
    p3 = period3_length / adjusted_total_length

    # Choose a random float from 0 to 1 to determine the interval
    rand_choice = random.random()
    
    # Determine in which interval this choice falls
    if rand_choice < p1:
        # First period
        chosen_seconds = random.randint(start_of_day, interval1_end)
    elif rand_choice < p1 + p2:
        # Second period, with increased chance
        chosen_seconds = random.randint(interval1_end, interval2_end)
    else:
        # Third period
        chosen_seconds = random.randint(interval2_end, end_of_day)
    
    # Return the datetime with added seconds
    return start_interval_datetime + datetime.timedelta(seconds=chosen_seconds)