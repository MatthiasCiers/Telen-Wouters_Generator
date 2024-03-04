import TransactionData
import ParticipantData
import pandas as pd
import random



if __name__ == '__main__':

    #Initializations
    days_list = ["2024-03-01"] 
    amount_transactions = 200 # Amount of DVP transactions per day, x2 transactions/day
    amount_participants = 25
    amount_securities = 3
    min_transaction_value = 100000
    max_transaction_value = 100000000
    min_balance_value = 50000
    max_balance_value = 150000000

    #Generate transactions
    transaction_df = TransactionData.generate_transaction_data(amount_transactions, amount_participants, amount_securities, days_list, min_transaction_value,max_transaction_value)

    #Generate participants

    balance_df = ParticipantData.generate_transaction_data(amount_participants, amount_securities, min_balance_value, max_balance_value)

    #Export  as CSV
    transaction_df.to_csv("TRANSACTION1.csv", index=False, sep=';')
    balance_df.to_csv("PARTICIPANTS1.csv", index=False, sep=';')