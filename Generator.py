import ParticipantData
import TransactionDataParallel
import pandas as pd
import random



if __name__ == '__main__':

    #Initializations
    days_list = ["2024-03-02","2024-03-10"] # first 2 days warm-up, last day cool-down
    amount_transactions = 1500 # Amount of DVP transactions per day, x2 transactions/day
    amount_participants = 8
    amount_securities = 8
    min_balance_value = 1000000
    max_balance_value = 10000000000

    #Log input parameters
    parameters_dataframe = pd.DataFrame({ 'amount transactions': amount_transactions,'amount participants': amount_participants, 'amount securities': amount_securities, 'min balance value': min_balance_value, 'max balance value':max_balance_value}, index=[0])  
    
    parameters_dataframe.to_csv("InputParameters.csv", index=False, sep=';')
    #Generate participants
    balance_df = ParticipantData.generate_participant_data_modified(amount_participants, amount_securities, min_balance_value, max_balance_value)
    #Generate transactions
    transaction_df = TransactionDataParallel.generate_transaction_data_parallel(amount_transactions, amount_participants, amount_securities, days_list, balance_df)

    #preprocess warm-up period, freezing the accounts during warm-up:

    #transaction_df = transaction_df[~((transaction_df['Time'].dt.date == pd.to_datetime("2024-03-02").date()) & (transaction_df['T+x'].isin([0, 1])))]
    #transaction_df = transaction_df[~((transaction_df['Time'].dt.date == pd.to_datetime("2024-03-03").date()) & (transaction_df['T+x'].isin([0])))]


    #Export  as CSV
    transaction_df.to_csv("TRANSACTION1.csv", index=False, sep=';')
    balance_df.to_csv("PARTICIPANTS1.csv", index=False, sep=';')


#tqesttetmset