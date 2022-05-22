import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import model
import model_s





####defining variables

end_day = 366

#registration rewards
rg = 5

#declay rate
Decay = 0.01 #default 0.01

#percentage of issued registration rewards used in play
p = 0.05

#winning rewards
w = 6

#winning odds. chance of a win for each game is (1/c)
c = 5

#transaction fee
tf = (1/100)

#part of the fee burnt
br = 0.5 #50% of the fee is burnt

#yield of the liquidity pool
y1 = 0.1

#yield of the governance pool
y2 = 0.05

#Token in Liquidity Pool / Totalsupply
lps = 0.1

#Token Staked for governance / Total supply
gps = 0.1


#call the model
model.token_model(end_day, rg, Decay, p, w, c, tf, br, y1, y2, lps, gps)

Token_model = pd.read_csv("Token_model.csv")
##print(Token_model)


fig = plt.figure()
ax  = fig.add_subplot(111)
ax.plot(Token_model[['Day']],Token_model[['Total_Supply']] , c='k', label='Total Supply',linewidth=4.0)

ax.plot(Token_model[['Day']],Token_model[['Issuance_Registration']] , c='b', label='Issunce from Registration')
ax.plot(Token_model[['Day']],Token_model[['Issuance_Slot_Play']] , c='g', label='Issunce from Slot Play')
ax.plot(Token_model[['Day']],Token_model[['Issuance_Transaction_Fee']] , c='m', label='Issunce from Transaction Fee')
ax.plot(Token_model[['Day']],Token_model[['Issuance_Liquidity_Pool']] , c='y', label='Issunce from Liquidity Pool')
ax.plot(Token_model[['Day']],Token_model[['Issuance_Governance_Pool']] , c='aquamarine', label='Issunce from Governance Pool')
leg = plt.legend()

##plt.show()
plt.savefig("Token_model.png", dpi = 100)
plt.close()






#sensitivity analysis
pct_change = 1 #percentage change

change = (pct_change/100)

sensitivity = pd.DataFrame()

sensitivity['Variable'] = ['rg', 'Decay', 'p', 'w', 'c', 'tf', 'br', 'y1', 'y2', 'lps', 'gps']
sensitivity['initial_value'] = [rg, Decay, p, w, c, tf, br, y1, y2, lps, gps]

sensitivity['Changed_value'] = [rg*(1+change), Decay*(1+change), p*(1+change), w*(1+change), c*(1+change), tf*(1+change), br*(1+change), y1*(1+change), y2*(1+change), lps*(1+change), gps*(1+change)]

change_variables = [rg, Decay, p, w, c, tf, br, y1, y2, lps, gps]


sensitivity['base_terminal_supply'] = model_s.token_model(end_day, change_variables[0], change_variables[1], change_variables[2], change_variables[3], change_variables[4], change_variables[5], change_variables[6], change_variables[7], change_variables[8], change_variables[9], change_variables[10])

sensitivity['changed_terminal_supply'] = np.NaN

for i in range(len(change_variables)):
    
    change_variables[i]= (1+change)*change_variables[i]
    sensitivity['changed_terminal_supply'][i] = model_s.token_model(end_day, change_variables[0], change_variables[1], change_variables[2], change_variables[3], change_variables[4], change_variables[5], change_variables[6], change_variables[7], change_variables[8], change_variables[9], change_variables[10])
    ##print(change_variables)
    change_variables[i]= change_variables[i]/(1+change)
        
    ##sensitivity['changed_value'][i] = model_s.token_model(end_day, rg, Decay, p, w, c, tf, br, y1, y2, lps, gps)

    
sensitivity['percentage_change'] = ((sensitivity['changed_terminal_supply'] / sensitivity['base_terminal_supply'])-1)*100

##sensitivity.to_csv("sensitivity.csv")
##
##sensitivity = pd.read_csv("sensitivity.csv")


sensitivity.plot.barh(x= 'Variable', y= 'percentage_change',
             title='Change in Terminal Supply due to '+str(pct_change)+'% Change', color='red', width=0.5)

plt.xlabel("Percentage Change in Terminal Supply")
plt.ylabel("Variable")

##plt.show()
plt.savefig("Sensitivity.png", dpi = 100)
plt.close()





