import TransactionData
import ParticipantData
import TransactionDataParallel
import pandas as pd
import random
import arrivals
import argparse
import sys



if __name__ == '__main__':

    '''
    parser = argparse.ArgumentParser(description='Settlement simulator input data generator')
    parser.add_argument('-i', "--input", help='ID of the parameters output file')
    args = parser.parse_args()

    if args.input is None:
        sys.exit("Please provide ID of the parameters output file! See --help")
    '''
    #Initializations
    days_list = ["2024-03-04","2024-03-08"] 
    amount_transactions = 50 # Amount of DVP transactions per day, x2 transactions/day
    amount_participants = 5
    amount_securities = 8
    #min_transaction_value = 100000
    #max_transaction_value = 100000000
    min_balance_value = 1000000
    max_balance_value = 10000000000

    #Log input parameters
    parameters_dataframe = pd.DataFrame({ 'amount transactions': amount_transactions,'amount participants': amount_participants, 'amount securities': amount_securities, 'min balance value': min_balance_value, 'max balance value':max_balance_value}, index=[0])  
    #parameters_dataframe.to_csv(f"InputParameters{args.input}.csv", index=False, sep=';')
    parameters_dataframe.to_csv("InputParameters.csv", index=False, sep=';')
    #Generate participants
    balance_df = ParticipantData.generate_participant_data_modified(amount_participants, amount_securities, min_balance_value, max_balance_value)
    #Generate transactions
    transaction_df = TransactionDataParallel.generate_transaction_data_parallel(amount_transactions, amount_participants, amount_securities, days_list, balance_df)

    #Export  as CSV
    transaction_df.to_csv("TRANSACTION1.csv", index=False, sep=';')
    balance_df.to_csv("PARTICIPANTS1.csv", index=False, sep=';')
    #transaction_arrivals_df.to_csv("TRANSACTION_ARRIVALS.csv", index=False, sep=';')