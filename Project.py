#!/usr/bin/env python
# coding: utf-8

# In[17]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.model_selection import train_test_split
import time
from sklearn.metrics import mean_squared_error, mean_absolute_error
#pd.options.display.max_rows = 100
#pd.options.display.max_columns = 20


# # DATA EXPLORATION AND PREPROCESSING

# In[2]:


#Loading the Dataset
zomato = pd.read_csv("C:/Users/Kemal/Desktop/zomato.csv")


# In[3]:


#The Dataset's shape
zomato.shape


# In[4]:


#Columns of the Dataset
zomato.columns


# #### Descriptions of column labels;
#     url: contains the url of the restaurant in the zomato website
#     address: contains the address of the restaurant in Bengaluru
#     name: contains the name of the restaurant
#     online_order: whether online ordering is available in the restaurant or not
#     book_table: table book option available or not
#     rate: contains the overall rating of the restaurant out of 5
#     votes: contains total number of rating for the restaurant
#     phone: contains the phone number of the restaurant
#     location: contains the neighborhood in which the restaurant is located
#     rest_type: type of the restaurant
#     dish_liked: dishes people liked in the restaurant
#     cuisines: food styles, separated by comma
#     approx_cost(for two people): contains approximate meal cost for two people
#     reviews_list: list of tuples containing reviews for the restaurant
#     menu_item: contains list of menus available in the restaurant
#     listed_in(type): type of meal
#     listed_in(city): contains city in which the restaurant is located
# 
# 
# 
# 

# In[5]:


#Changing some columns' names
zomato = zomato.rename(columns={"approx_cost(for two people)":"approx_cost","listed_in(type)":"meals","listed_in(city)":"city"})


# In[6]:


#Cleaning redundant columns; "url","address" and "phone" - keeping "location" column for address information
zomato = zomato.drop(['url','address','phone'], axis=1)
#"location" and "city" columns contain same information but "location" has wider range so drop the "city" column
zomato = zomato.drop(['city'], axis=1) #"location" and "city" columns contain same information but "location" has wider range


# In[7]:


#Datatypes of attributes
zomato.dtypes


# In[8]:


#Changing datatype of "approx_cost" column from object to float
zomato['approx_cost'] = zomato['approx_cost'].astype(str).apply(lambda x: x.replace(',',''))
zomato['approx_cost'] = zomato['approx_cost'].astype(float)


# In[9]:


#For "rate" column: drop "/5" part - change datatype from object to float - fix noisy entries
zomato['rate'] = zomato['rate'].astype(str).apply(lambda x: x.split('/')[0])
while True:
    try:
        zomato['rate'] = zomato['rate'].astype(float)
        break
    except ValueError as e1:
        noise_entry = str(e1).split(":")[-1].strip().replace("'", "")
        zomato['rate'] = zomato['rate'].apply(lambda x: x.replace(noise_entry, str(np.nan)))


# In[10]:


# Correcting the noisy restaurant name entries
zomato['name'] = zomato['name'].apply(lambda x: 'Santa Spa Cuisine' if x == 'SantÃ\x83Â\x83Ã\x82Â\x83Ã\x83Â\x82Ã\x82Â\x83Ã\x83Â\x83Ã\x82Â\x82Ã\x83Â\x82Ã\x82Â\x83Ã\x83Â\x83Ã\x82Â\x83Ã\x83Â\x82Ã\x82Â\x82Ã\x83Â\x83Ã\x82Â\x82Ã\x83Â\x82Ã\x82Â© Spa Cuisine' else x)
zomato['name'] = zomato['name'].apply(lambda x: 'Cafe Down The Alley' if x == 'CafÃ\x83Â\x83Ã\x82Â\x83Ã\x83Â\x82Ã\x82Â\x83Ã\x83Â\x83Ã\x82Â\x82Ã\x83Â\x82Ã\x82Â© Down The Alley' else x)


# In[11]:


#Missing value search
number_of_missing_data = (zomato.isnull().sum()).sort_values(ascending=False)
number_of_missing_data = pd.DataFrame(number_of_missing_data, columns=['# of missing values'])                                                                    
percentage_of_missing_data = (zomato.isnull().sum()/zomato.shape[0]*100).sort_values(ascending=False)
percentage_of_missing_data = pd.DataFrame(percentage_of_missing_data, columns=['% of missing part'])
missing = pd.concat([number_of_missing_data,percentage_of_missing_data], axis=1) 

missing
       


# In[12]:


#Remove missing value containing rows - Remaining part = 23.259 rows
zomato = zomato.dropna(how='any')
zomato = zomato.reset_index(drop=True)


# In[13]:


#Search for duplicated rows
zomato.duplicated().value_counts()


# In[14]:


#Remove duplicated rows - Remaining part = 21.064 rows
zomato = zomato.drop_duplicates()


# In[15]:


#Removo rows whose number of votes is smaller than 50, because rate data of restaurants change by 0.1 interval
#Adding 1 more vote to a restaurant whose vote number is smaller than 50 may cause more than 0.1 difference on average rate
#Having more than 50 votes guarantees that the restaurants average rate will not change more than 0.1 by adding 1 more vote
#It means that restaurant's rate is settled and reliable 
#Remaining part = 19934 rows
zomato = zomato[zomato.votes > 49]
zomato = zomato.reset_index(drop=True)


# In[ ]:




