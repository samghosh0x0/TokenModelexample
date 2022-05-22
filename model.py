import pandas as pd
import numpy as np



def token_model(end_day, rg, Decay, p, w, c, tf, br, y1, y2, lps, gps):


    #creating the initial model

    df = pd.DataFrame({'day': range(1,end_day,1)})

    df['registration'] = np.NaN
    df.registration[0] = 1

    #change the below formula to change the trend in registrations
    for j in range(1,len(df)):
        df.registration[j] = df.registration[j-1] + 1





    #populating joining bonus columm by applying decay rate 
    df['Registration_Bonus_per'] = df['day'].apply(lambda x: rg*(1-((x-1)*Decay)) if (rg*(1-((x-1)*Decay)))>=0 else 0)

    #calculating daily issuance due to registration
    df['NET_issunce_Registration_Bonus'] = df['registration'] * df['Registration_Bonus_per']

    #cumulating number of tokens issued
    df['CUMSUM_issunce_Registration_Bonus'] = df['NET_issunce_Registration_Bonus'].cumsum()

    #calculating number of tokens used in playing slot
    df['number_of_plays'] = df['CUMSUM_issunce_Registration_Bonus'].apply(lambda x: round(x*p,0))



    """Now, let is calculate the net daily issuance from the slot. Now, one token is used to play the game..so one token is
    burned with each play irrespective of the result.

    Now, chance of win for each game is (1/c)...c being the winning odds.

    and w is the winning reward. So, with each play on an average (w*(1/c)) tokens are issued from the slot

    So, net issuance from the slot = (w*(1/c)) - 1

    One important point, when, w = c the net issuance is (-1)...so, one token is burnt.


    as 1 token is used to play the slot. We are going to consider the transaction cost later"""


    # dailynet issuance from slot
    df['NET_issunce_Playing_slot'] = df['number_of_plays'].apply(lambda x: x* ((w/c)-1))


    #transaction fee from the winners 
    df['transaction_fee_collected'] = df['number_of_plays'].apply(lambda x: x* ((w/c))*tf)

    #burning of transactio fee
    df['transaction_fee_burned'] = df['transaction_fee_collected'].apply(lambda x: x*br)

    #transaction fee transfered to liquidity pool

    df['transaction_fee_pool'] = df['transaction_fee_collected'] - df['transaction_fee_burned']

    #daily net issuance from transaction fee
    df['NET_issunce_transaction_fee'] = df['transaction_fee_burned'].apply(lambda x: x*(-1))



    df['NET_issunce_liquiditypool_interest'] = np.NaN
    df['NET_issunce_governance_pool_interest'] = np.NaN
    df['Total_Supply'] = np.NaN

    df.NET_issunce_liquiditypool_interest[0] = 0
    df.NET_issunce_governance_pool_interest[0] = 0

    df.Total_Supply[0] = df.NET_issunce_Registration_Bonus[0] + df.NET_issunce_Playing_slot[0] + df.NET_issunce_transaction_fee[0] + df.NET_issunce_liquiditypool_interest[0] + df.NET_issunce_governance_pool_interest[0]


    for i in range(1, len(df)):
        df.NET_issunce_liquiditypool_interest[i] = df.Total_Supply[i-1] * (y1/365) * lps
        df.NET_issunce_governance_pool_interest[i] = df.Total_Supply[i-1] * (y2/365) * gps
        
        df.Total_Supply[i] = df.Total_Supply[i-1] + df.NET_issunce_Registration_Bonus[i] + df.NET_issunce_Playing_slot[i] + df.NET_issunce_transaction_fee[i] + df.NET_issunce_liquiditypool_interest[i] + df.NET_issunce_governance_pool_interest[i]
        #print(i)


    #calculating cumulative sums for saving. Cumulative value of registration is already done

    df['CUMSUM_issunce_Playing_slot'] = df['NET_issunce_Playing_slot'].cumsum()
    df['CUMSUM_issunce_transaction_fee'] = df['NET_issunce_transaction_fee'].cumsum()
    df['CUMSUM_issunce_liquiditypool_interest'] = df['NET_issunce_liquiditypool_interest'].cumsum()
    df['CUMSUM_issunce_governance_pool_interest'] = df['NET_issunce_governance_pool_interest'].cumsum()
    

    model = df[['day','CUMSUM_issunce_Registration_Bonus','CUMSUM_issunce_Playing_slot','CUMSUM_issunce_transaction_fee', 'CUMSUM_issunce_liquiditypool_interest', 'CUMSUM_issunce_governance_pool_interest', 'Total_Supply']]

    model.rename(columns={  'day': 'Day', 
                            'CUMSUM_issunce_Registration_Bonus': 'Issuance_Registration',
                            'CUMSUM_issunce_Playing_slot': 'Issuance_Slot_Play',
                            'CUMSUM_issunce_transaction_fee': 'Issuance_Transaction_Fee',
                            'CUMSUM_issunce_liquiditypool_interest': 'Issuance_Liquidity_Pool',
                            'CUMSUM_issunce_governance_pool_interest': 'Issuance_Governance_Pool',
                            'Total_Supply': 'Total_Supply',}, inplace=True)

    ##model.columns = ['Issuance_registration', 'Issuance_slot', 'Issuance_transaction_fee', 'Issuance_liquidity_pool', 'Issuance_governance', 'Total_Supply']

    model.to_csv("Token_model.csv",index=False)

