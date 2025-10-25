import os
from pathlib import Path
import yaml
import configparser

class ProjectConfigs:
    """
    Class containing methods relating to project configurations allowing user to determine \n
    root directory; obtain various project configs/settings; and read/write to yaml. 
    
    Instantiate with: \n
        project=ProjectConfigs() \n

    Available methods:
          .root_dir() \n
          .configs_from_yaml(dir='configs', filename='settings.yaml') \n 
          .print_global_configs() \n
          .yaml_to_dict(filename) \n
          .dict_to_yaml(data_dict, filename, append=False)
    """

    
    def root_dir(self):
        path = Path().absolute()
        markers = ['data', 'src', 'notebooks', '.git', 'configs', 'scripts']
        
        while path != path.parent:
            if any((path / marker).exists() for marker in markers):
                return path
            path = path.parent
        return None


    def configs_from_yaml(self, dir='configs', filename='settings.yaml'):
        return self.yaml_to_dict(self.root_dir() / dir / filename)


    def print_global_configs(self):
        project_dir = self.root_dir()
        global_configs = self.configs_from_yaml()
        for k,v in global_configs.items():
            print(f'{k} <- {v}')

            if isinstance(v, dict):
                for k2,v2 in v.items():
                    print(f'  {k2} <- {v2}')
                    if k2.endswith('_dir'):     
                        print(f'     contains:{[f for f in os.listdir(project_dir / v2) if not f.startswith(".")]}')

            print('\n')

    def yaml_to_dict(self,filename):
        """
        Reads a YAML file and returns data in form of dictionary.
        """
        try:
            with open(filename, "r") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return {}
        
 
    def dict_to_yaml(self,data_dict, filename, append=False):
        """
        Takes a data_dict and writes data out to filename.yaml
        """

        with open(filename, 'a' if append else 'w') as f:

            if append:
                print(f'appending to {filename}...')
            else:
                print(f'writing to {filename}...')

            for k,v in data_dict.items():
                if isinstance(v, list):
                    f.write(f'{k}:\n')
                    for item in v:
                        f.write(f'  - {item}\n')
                    f.write('\n')
                
                if isinstance(v,dict):
                    f.write(f'{k}:\n')
                    for col,attrbutes in v.items():
                        f.write(f'  {col}: {attrbutes}\n')
                    f.write('\n')



    def load_credentials(self, credentials_json):
        creds = credentials_json
        result = {}

        for key, path in creds.items():

            credential_files = [f for f in os.listdir(path) if f.startswith('credentials')]
            
            for file in credential_files:
                parser = configparser.ConfigParser()
                file_path = f'{path}/{file}'

                try:
                    parser.read(file_path)

                    if not parser.sections():
                         raise ValueError(f"No sections found in credential file: {file_path}")

                    section_data = {section: dict(parser[section]) for section in parser.sections()}

                    if key=='other':
                        file_key = file.split('_')[1]

                    else:
                        file_key = key

                    result[file_key] = section_data

                except FileNotFoundError:
                    raise FileNotFoundError(f"Credential file for {key} not found at: {path}")
                
                except Exception as e:
                    raise ValueError(f"Error parsing credentials for {key} from {path}: {e}")

        return result
    

    def set_env_from_creds(self, verbose=True):
        configs = self.configs_from_yaml()
        credentials = self.load_credentials(configs['credentials'])

        skipped = []

        for k,v in credentials.items():
            for k2,v2 in v.items():
                
                if k not in ['aws'] and k2=='default' and isinstance(v2.get('api_key'), str):
                    os.environ[f'{k.upper()}_API_KEY'] = v2.get('api_key')
                    if verbose:
                        print(f'set environment variable for default: {k.upper()}_API_KEY')

                else:
                    skipped.append(f'{k}[{k2}]')
                                   
        if verbose:
            print('skipping:')
            print(skipped) #('\n'.join(skipped))  