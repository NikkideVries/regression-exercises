# imports list
import pandas as pd
import numpy as no
import env
import os


from sklearn.model_selection import train_test_split

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

def create_zillow_data():
    '''
    This function acquires zillow.csv it is available
    otherwise, it makes the SQL connection and uses the query provided
    to read in the dataframe from SQL.
    If they csv is not present, it will write one.
    '''
    filename = "zillow_2017.csv"

    if os.path.isfile(filename):

        return pd.read_csv(filename, index_col=0)
    else:
        # Create the url
        db = 'zillow'
        url = f'mysql+pymysql://{env.user}:{env.password}@{env.host}/{db}'
        
        sql_query = '''
            SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
            FROM properties_2017
            WHERE propertylandusetypeid = 261'''

        # Read the SQL query into a dataframe
        df = pd.read_sql(sql_query, url)

        # Write that dataframe to disk for later. Called "caching" the data for later.
        df.to_csv(filename)

        # Return the dataframe to the calling code
        return df

def prep_zillow(df):
    '''
    This function takes in a dataframe
    renames the columns and drops nulls values
    Additionally it changes datatypes for appropriate columns
    and renames fips to actual county names.
    Then returns a cleaned dataframe
    '''
    df = df.rename(columns = {'bedroomcnt':'bedrooms',
                     'bathroomcnt':'bathrooms',
                     'calculatedfinishedsquarefeet':'area',
                     'taxvaluedollarcnt':'taxvalue',
                     'fips':'county'})
    
    df = df.dropna()
    
    make_ints = ['bedrooms','area','taxvalue','yearbuilt']

    for col in make_ints:
        df[col] = df[col].astype(int)
        
    df.county = df.county.map({6037:'LA',6059:'Orange',6111:'Ventura'})
    
    return df

def split_zillow_data(df):
    '''
    This funciton will split the data frame into train, validate, and test
    '''
    
    train_validate, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train_validate, test_size=.3, random_state=123)
    
    return train, validate, test