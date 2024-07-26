import pandas as pd
from utils import *

pd.options.mode.copy_on_write = True
pd.options.mode.chained_assignment = None  # default='warn'

start_date = "2024-07-25T00:00:00"
end_date = "2024-07-25T23:59:59"

########### INSTAGRAM ###########

### COMMUNITY INSTAGRAM ###
print('---Getting data from Emplifi for Instagram Community---')
ig_community = get_data(date_start=start_date, date_end=end_date, platform='instagram')
print(f'Retrieving data from Emplifi for Instagram Community completed, there are {len(ig_community)} comments')

### DATA PRE-PROCESSING ###
ig_community.fillna('VUOTO', inplace=True)
ig_community = ig_community[ig_community['community_type'] != 'post']

### CREATE FINAL DATASET ###
conversazioni = create_conversations(ig_community, 'instagram', start_date, end_date)
df_final_ig = create_final_df(conversazioni)
community_ig = before_deadline(df_final_ig, platform='instagram')
print(community_ig.head())


########### FACEBOOK ###########

### COMMUNITY FACEBOOK ###
print('---Getting data from Emplifi for Facebook Community---')
fb_community = get_data(date_start=start_date, date_end=end_date, platform='facebook')
print(f'Retrieving data from Emplifi for Facebook Community completed, there are {len(fb_community)} comments')

### DATA PRE-PROCESSING ###
fb_community.fillna('VUOTO', inplace=True)
fb_community = fb_community[fb_community['community_type'] != 'post']

### CREATE FINAL DATASET ###
conversazioni = create_conversations(fb_community, 'facebook', start_date, end_date)
df_final_fb = create_final_df(conversazioni)
community_fb = before_deadline(df_final_fb, platform='facebook')
print(community_fb.head())


########### GENERATIVE AI ###########
print('---Generative AI---')

#### INSTAGRAM ####
community_ig['input ai'] = community_ig.agg(lambda x: f"{x['NOME UTENTE']} ha commentato {x['COMMENTO UTENTE']}", axis=1)
community_ig['Token Count'] = community_ig.iloc[:,-1].apply(count_token)

total_token = community_ig['Token Count'].sum()

print(f"Total tokens for Instagram Community {total_token}")

community_ig = generate_responses(community_ig)

print('Final Dataset of Instagram Community')
print(community_ig.head())

#### FACEBOOK ####
community_fb['input ai'] = community_fb.agg(lambda x: f"{x['NOME UTENTE']} ha commentato {x['COMMENTO UTENTE']}", axis=1)
community_fb['Token Count'] = community_fb.iloc[:,-1].apply(count_token)

total_token = community_fb['Token Count'].sum()

print(f"Total tokens for Facebook Community {total_token}")

community_fb = generate_responses(community_fb)

print('Final Dataset of Facebook Community')
print(community_fb.head())

#### CREAZIONE RISPOSTA ####
print("---Creazione risposte Community IG tramite Assistant")
community_ig = proposta_risposta(community_ig)
community_ig.iloc[:,:-2].to_excel(f"out/Instagram/ig_community_{start_date.split('T')[0]}_{end_date.split('T')[0]}.xlsx", index=None)

print("---Creazione risposte Community FB tramite Assistant")
community_fb = proposta_risposta(community_fb)
community_ig.iloc[:,:-2].to_excel(f"out/Instagram/ig_community_{start_date.split('T')[0]}_{end_date.split('T')[0]}.xlsx", index=None)

print("PROCESSO TERMINATO")


