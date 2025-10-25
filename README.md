## gsd

### Overview
#### A python package of utilities to help Get Sh*t Done

### Installation
inclue in ```requirements.txt``` as
```
git+https://github.com/someuser/mypackage.git 
#or
git+https://github.com/someuser/mypackage.git@v0.1.0
```
then:

```bash
pip install -r requirements.txt
```

or ```pip install``` from github via:

```bash
pip install git+https://github.com/essans/gsd.git

#or

pip install git+https://github.com/essans/gsd.git@v0.1.0

#or

pip install git+https://github.com/essans/gsd.git@<commit-hash>
```

or ```git clone https://github.com/essans/gsd.git``` to local and install via:

```bash
git tag # to see available tagged versions
git checkout v0.1.0 #for example

pip install .
#or
pip install git+file://Users<user_name>/code_dir/gsd@v.0.1.0
```

<br>

## Usage
```py
from gsd import *
```
or
```py
from gsd import ProjectConfig, Timer, gsdIO, gsdUtil
```

### Structure

<br>


## Features
- [ProjectConfigs](#ProjectConfigs)
- [gsdIO](#gsdIO)
- [gsdUtil](#gsdUtil)
- [Timer](#Timer)


---
<br>

## ProjectConfigs

#### `class ProjectConfigs:`

Class in the `project.py` module containing methods relating to project configurations allowing user to determine root directory; obtain various project configs/settings; and read/write to yaml. 

Instantiate with:
```py
project=ProjectConfigs()
```

Available methods:
```py
project.root_dir() 
       .configs_from_yaml(dir='configs', filename='settings.yaml') 
       .print_global_configs() 
       .yaml_to_dict(filename) 
       .dict_to_yaml(data_dict, filename, append=False) 
```

eg:
```py
project=ProjectConfigs()

root_dir = project.root_dir()
configs = project.configs_from_yaml() #assuming file is in default location based on cookiecutter template

project.print_global_configs() #shows defaults and shows dir content for any config label ending in '_dir'

project.set_envs_from_creds(verbose=False`) #sets any env variables based on credentials info in project config yaml

```

eg 
```yaml
#settings.yaml

project_name: "project_name"

input_data:
  raw_dir: "data/raw/"
  processed_dir: "data/processed/"
  
outputs:
  outputs_dir: "outputs/"
  logs_dir: "outputs/logs/"

credentials:
  aws_credentials: "/USERS/<user_name>/.aws/credentials"
```

Then input data path can be set programatically via supplied project config info:
```py
data_dir = project_dir / configs['input_data']['raw_dir']

```

<br>

#### `yaml_to_dict(full_path)`

eg for pulling out specific information from project and user configs based on above example yaml

```py
project=ProjectConfigs()
configs = project.configs_from_yaml()

aws_credentials_dict = project.yaml_to_dict(configs['credentials']['aws_credentials'])
```
<br>

#### `load_credentials(credentials_json, aws_profile='default)`

Used to extract and load credentials

```py
project=ProjectConfigs()
configs = project.configs_from_yaml()

credentials = project.load_credentials(configs['credentials'], aws_profile='default')


---
<br>



## gsdIO

gsdIO: Functions to handles files, directories, input/output operations.

Available functions:
```
- create_dir(..): creates new directory
- join_csv(..): join multiple csv files as they are read into memory
```
<br>

#### `create_dir(full_path)`
```py
gsdIO.create_dir('/USERS/<user_name>/dir')

# creates new dir if needed based on full_path.
```
<br>

#### `join_csv(path, file_list=None, wildcard='', return_as='df')`

```py
#read and join all files in provided path.  Return a dataframe
gsdIO.join_csv('/USERS/<user_name>/dir', file_list=None, wildcard='', return_as='df')

#read and join all files in provided path containing "_prod.csv" string pattern. Return a dataframe
gsdIO.join_csv('/USERS/<user_name>/dir', file_list=None, wildcard='_prod.csv', return_as='df')

#read and join the provided list of files.  Return as a py dictionary.
gsdIO.join_csv('/USERS/<user_name>/dir', 
               file_list=['/USERS/<user_name>/dir/filename1.csv',
                          '/USERS/<user_name>/dir/filename2.csv'
                         ],
               wildcard=None, return_as='df')

```


<br>

<br>

## gsdUtil
Various gsd functions:
- gsdUtil.snake2camel(snake_str)
- gsdUtil.col_to_str(df, colname, fill_na=False)
- gsdUtil.col_cast(dataframe, colname, cast_as, fill_na=False)
- gsdUtil.rename_col(df, current_colname, desired_colname)
- gsdUtil.print_vars(str_pattern, match_criteria='contains', local_scope=None)
- gsdUtil.pd_format(maxRows=50, maxCols=20, displayWidth=250)
- gsdUtil.merge2(df1, df2, left_on, right_on, how, cast_keys_as, fill_NA_keys=False)

#### `gsdUtil.snake2camel(snake_str)`
```py
gsdUtil.snake2camel("my_string")

# outputs "myString"
```

#### `col_to_str(df, colname, fill_na=False)`

Force formating (in place) of dataframe column to be of type string

```py
col_to_str(data_df, '<col_name', fill_na=False) #set fill_na=True to handle and NAs first
```

<br>

#### `col_cast(dataframe, [colnames], cast_as, fill_na=False)`
Force format / recast columns (in place) to specified format with fine-grain control of NAs

```py
col_cast(data_df,'<col_name>', 'int32', fill_na=-1)

col_cast(data_df,['<col_name>','ticker'], 'str', fill_na='NA')

col_cast(data_df,['<col_name>'], 'boolean', fill_na='pd.NA')

col_cast(data_df,'<col_name>', 'float64', fill_na='pd.NA')

col_cast(data_df,'<col_name>', 'str', fill_na='NA')


```

<br>

#### `rename_col(df, current_colname, desired_colname)`

Convenience function for inplace renaming of a single df column

<br>

#### `print_vars(str_pattern, match_criteria='contains', local_scope=None)`

Helper function for printing variables from memory.

eg:
```py
print_vars('_prod') #print all variable names and their values when variable name contains '_prod'

print_vars('_prod', 'endswith') # where variable name ends with '_prod'
```

Current default implemention of function is for local_scope variables, but local scope can be set with `local_scope` input parameter

-----
<br>

#### `pd_format(maxRows=50, maxCols=20, maxColWidth=50, displayWidth=250)`

Convenience function for adjust common pandas dataframe view settings

<br>

#### `merge2(df1, df2, left_on, right_on, how, cast_keys_as, fill_NA_keys=False)`

Convenience function to minimize steps needed to merge two dataframes with different key columns formts.

eg:
```py
merge2(df1, df2, left_on='<col_name_1>', right_on='<col_name_2>',how='left', cast_keys_as='str', fill_NA_keys='N/A')
```

<br>

## Timer

Class and methods for setting and tracking timers.  eg. for ligh-weight logging / de-bugging

eg.
```py

from gsd import Timer

timer=Timer()

timer.start(message='')

timer.elapsed(message='', periodicity='s') # 's' to display in for seconds, 'm' for minutes

timer.end(periodicity='s')

timer.get_timestamp(format="YYYY-MM-DD_HHMMSS") #alternative provide valid python strf datetime format (eg: "%Y-%m-%d_%H%M%S")
```

<br>



### Notes:
```
git tag -a v0.1.2.post2 -m "new version"
git push origin v0.1.2.post2
```
