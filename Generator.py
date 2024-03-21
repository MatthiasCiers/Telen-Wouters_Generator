import TransactionData
import ParticipantData
import pandas as pd
import random
import arrivals



if __name__ == '__main__':

    #Initializations
    days_list = ["2024-03-01","2024-03-02"] 
    amount_transactions = 1250 # Amount of DVP transactions per day, x2 transactions/day
    amount_participants = 6
    amount_securities = 3
    #min_transaction_value = 100000
    #max_transaction_value = 100000000
    min_balance_value = 1000000
    max_balance_value = 50000000000

    # parameters arrivals
    transactions = 2*1250
    arrival_factor_before_10 = 50  
    arrival_factor_after_4 = 50   
    arrival_factor_closed=5
    arrival_factor_day=20
    start_year,start_month,start_day=2024,1,1
    end_year,end_month,end_day=2024,1,10

    #Generate participants
    balance_df = ParticipantData.generate_participant_data_modified(amount_participants, amount_securities, min_balance_value, max_balance_value)
    #Generate transactions
    transaction_df = TransactionData.generate_transaction_data(amount_transactions, amount_participants, amount_securities, days_list, balance_df)
    #print(transaction_df)
    
    arrivals_list=arrivals.simulate_arrivals(transactions, start_year,start_month,start_day,end_year,end_month,end_day, arrival_factor_before_10, arrival_factor_after_4,arrival_factor_closed,arrival_factor_day )
    transaction_df['Time'] = arrivals_list
    #transaction_arrivals_df = pd.concat([transaction_df.drop("Time", axis=1), arrivals_df], axis=1, ignore_index=True)
    #transaction_arrivals_df.columns = ['TID', 'Value', 'FromParticipantId', 'FromAccountId', 'ToParticipantId', 'ToAccountId', 'Linkcode', 'ArrivalTimes']
    
    

    #Export  as CSV
    transaction_df.to_csv("TRANSACTION1.csv", index=False, sep=';')
    balance_df.to_csv("PARTICIPANTS1.csv", index=False, sep=';')
    #transaction_arrivals_df.to_csv("TRANSACTION_ARRIVALS.csv", index=False, sep=';')