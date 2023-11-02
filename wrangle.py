# imports list
import pandas as pd
import numpy as no
import env
import os


#-----------------------------------------------------------------#
#Aquire functions:

# get connection url 
def get_db_url(db, user = env.user, host = env.host, password = env.password):
    '''
    This function will take in a databse and set enviromental credentials and
    return a datbase connection link. 
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

# create new data: 
def new_zillow_data():
    '''
    This function will use a set sql query and return a zillow data frame based on the 
    exercise II in the ds.codeup.com regression: acquistion and prep request
    '''
    
    sql_query = '''
                select 
                    propertylandusetypeid,
                    propertylandusedesc,
                    bedroomcnt,
                    bathroomcnt,
                    calculatedfinishedsquarefeet,
                    taxvaluedollarcnt,
                    yearbuilt,
                    taxamount,
                    fips
                from properties_2017
                Left join propertylandusetype as pt
                    Using (propertylandusetypeid)
                where pt.propertylandusedesc like 'Single%%'
                '''
    df = pd.read_sql(sql_query, get_db_url('zillow'))
    
    return df

# make data into a csv 
def get_zillow_data():
    '''
    This function reads in data from a codeup database, writes the data to a csv file if a 
    local file does not exist, and returns a df
    '''
    
    if os.path.isfile('zillow.csv'):
        
        #if csv file exists, read in data from csv file 
        df = pd.read_csv('zillow.csv', index_col = 0)
        
    else:
        
        # read fresh data from db into a dataframe
        df = new_zillow_data()
        
        #write dataframe to a csv file
        df.to_csv('zillow.csv')
    
    return df




#-----------------------------------------------------------------#
# Data prepation functions: 