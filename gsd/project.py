"""
Various gsd functions:
    - gsdUtil.snake2camel(snake_str)
    - gsdUtil.col_to_str(df, colname, fill_na=False)
    - gsdUtil.col_cast(dataframe, colname, cast_as, fill_na=False)
    - gsdUtil.rename_col(df, current_colname, desired_colname)
    - gsdUtil.pd_format(maxRows=50, maxCols=20, displayWidth=250)

"""

import os
import pandas as pd
import datetime as dt


def snake_to_camel(snake_str):
    """convert from snake_case to camelCase"""
    components = snake_str.split('_') 
    return components[0] + ''.join(x.capitalize() for x in components[1:])


def col_to_str(df, colname, fill_na=False):
    """
    force formating of column to string.  fill_na=True to handle NA's first.
    """
    if fill_na:
        df[colname] = df[colname].fillna(fill_na).apply(int)
    df[colname] = df[colname].apply(str)



def col_cast(dataframe, colname_list, cast_as, fill_na=False):
    """
    Cast a list of dataFrame columns to a specified type and handle missing values.
      eg: cast_as =  'int32', 'float64', 'str', 'boolean', 
      eg: fill_na = -1, 'pd.NA', 'NA', '<any_str>' 
    """
    
    if not isinstance(colname_list, list):
        colname_list = [colname_list]
        #raise KeyError(f"colnames must be a list -even a list of one [colname]")

    for col in colname_list:
    
        if col not in dataframe.columns:
            print(f"column '{col}' does not exist in the dataframe -skipping")
            continue
        
        if fill_na == 'pd.NA':
           fill_na = pd.NA

        if fill_na is not False:
            dataframe[col] = dataframe[col].fillna(fill_na)

        if cast_as == 'str':
            if dataframe[col].dtype == 'float64':  # Convert floats with .0 to int before converting to str
                dataframe[col] = dataframe[col].astype('Int64').astype(str)
            else:
                dataframe[col] = dataframe[col].astype(str)

        if cast_as in['int','int64']:
            dataframe[col] = dataframe[col].astype(object).astype('Int64')
        
        else:
            try:
                dataframe[col] = dataframe[col].astype(object).astype(cast_as)            
            except ValueError as e:
                raise ValueError(f"Error casting column '{col}' to {cast_as}: {e}")
            


def rename_col(df, current_colname, desired_colname):
    """
    Convenience function to change column name
    """
    df.rename(columns={current_colname:desired_colname}, inplace=True)



def print_vars(str_pattern, match_criteria = 'contains', local_scope = None):
    """
    Helper function to print variables from locals() memory.

    Supported match_criteria "contains", "startswith", "ends with"
     
       eg: print_vars('_prod', 'contains') prints all variable names containing '_prod' and their values
    """

    if local_scope is None:
        scope= globals()
    else:
        scope = local_scope

    if match_criteria == "contains":
        vars = {name: value for name, value in scope.items() if str_pattern in name}
    
    elif match_criteria == "startswith":
        vars = {name: value for name, value in scope.items() if name.startswith(str_pattern)}

    elif match_criteria == 'endswith':
        vars = {name: value for name, value in scope.items() if name.endswith(str_pattern)}

    else:
        vars = False
    
    if vars:
        for k,v in vars.items():
            print(k,':',v)
    else:
        print("match_criteria must be 'contains', 'startswith', or 'endswith'")


def pd_format(maxRows=50, maxCols=20, maxColWidth=50, displayWidth=250):
    """
    Convenience function for setting dataframe defaults
    """

    pd.set_option('display.max_rows', maxRows) #pd.get_option("display.max_rows")
    pd.set_option('display.max_columns', maxCols)
    pd.set_option('display.max_colwidth', maxColWidth)
    pd.set_option('display.width', displayWidth)


def merge2(df1, df2, left_on, right_on, how, cast_keys_as, fill_NA_keys=False):
    """
    Helper function which re-casts the format of the chosen keys to
    be the same prior to passing into pandas merge function"""

    col_cast(df1, [left_on], cast_as=cast_keys_as, fill_na=fill_NA_keys)
    col_cast(df2, [right_on], cast_as=cast_keys_as, fill_na=fill_NA_keys)

    return pd.merge(df1, df2, left_on=left_on, right_on=right_on, how=how)



def date_list(st_date,en_date):
    """ 
    generate sequential list of dates between st and en 
    formatted as yyyy-mm-dd
    """
    if len(st_date)==10:
        st_yy = int(st_date[0:4])
        st_mm = int(st_date[5:7])
        st_dd = int(st_date[8:10])

    else:
        st_yy = int(st_date[0:4])
        st_mm = int(st_date[4:6])
        st_dd = int(st_date[6:8])
    
    st_dt = dt.date(st_yy,st_mm,st_dd)
        
    if len(en_date)==10:
        en_yy = int(en_date[0:4])
        en_mm = int(en_date[5:7])
        en_dd = int(en_date[8:10])  

    else:
        en_yy = int(en_date[0:4])
        en_mm = int(en_date[4:6])
        en_dd = int(en_date[6:8])  
    
    en_dt = dt.date(en_yy,en_mm,en_dd)
    
    datedif = en_dt - st_dt
    
    date_list = []
    
    for i in range(datedif.days+1):
        dateincr = st_dt+dt.timedelta(days=i)
        date_list.append(dt.datetime.strftime(dateincr,"%Y%m%d"))
    
    return date_list


