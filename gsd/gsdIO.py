"""
gsdIO: Functions to handles files, directories, input/output operations.

- create_dir: creates new directory
- join_csv: join multiple csv files as they are read into memory

See each function for corresponding docstring
"""




import os
import s3fs
import pandas as pd


def create_dir(full_path):
    """create a new path where if it doesn't already exist"""
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        print('created directory ' + full_path)
    else:
        print('path already exists: ' + full_path)



def join_csv(path, file_list=None, wildcard='',return_as='df'):
    
    """
    join multiple csv files:
        
    > join_csv(path, file_list=None, wildcard='', return_as='df')

    - supply file_list or read all from path as default
    - provide wildcard to filter filename for import(eg '_2024_01').  Default is no filtering
    - return_as 'df' (default) or 'dict'

    """

    dict_store = {} 
    
    if file_list is None:
        dir_contents = os.listdir(path)
        filenames = [f for f in  dir_contents if os.path.isfile(path / f)] 

    else:
        filenames = file_list
    
    filenames = [f for f in filenames if wildcard in f]
    
    for file in filenames:
        _this_file = pd.read_csv(path / file, low_memory=False)
        _this_file['source_file'] = file
        dict_store[file] = _this_file

        print('>>> ' + file, _this_file.shape)

        
    if return_as == 'dict':
        return dict_store
    
    else:
        return pd.concat(dict_store).reset_index(drop=True)
    
