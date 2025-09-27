import os
import yaml
import hashlib
import json
import croniter
import importlib
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

# Get logger
logger = logging.getLogger('configer.py')


class Config:
    def __init__(self, config_dict: Dict[str, Any]):
        # Explicitly set properties for the fields we care about
        self._schedule = config_dict.get('schedule')
        self._module = config_dict.get('module')
        self._text = config_dict.get('text')
        self._chat_id = config_dict.get('chat_id')
        
        # Generate hash-based id from content
        self._generate_hash_id()
    
    # Property getters (read-only)
    @property
    def schedule(self):
        """Returns a croniter object based on the schedule string"""
        return croniter.croniter(self._schedule, datetime.now())
    
    @property
    def module(self):
        """Returns an instance of the module class"""
        module_name = self._module
        module_path = f"lib.modules.{module_name}"
        logger.info(f"Module path: {module_path}")
        module = importlib.import_module(module_path)
        instance = getattr(module, module_name)()
        return instance
    
    @property
    def text(self) -> str:
        return self._text
    
    @property
    def chat_id(self) -> int:
        return self._chat_id
    
    @property
    def id(self) -> str:
        return self._id
    
    def _generate_hash_id(self):
        # Create a dictionary with only the elements we want to hash
        hash_elements = {
            'schedule': self._schedule,  # Use raw schedule string for hashing
            'module': self._module,      # Use raw module name for hashing
            'text': self._text,
            'chat_id': self._chat_id
        }
        
        # Convert to JSON string and hash it
        content_str = json.dumps(hash_elements, sort_keys=True)
        hash_obj = hashlib.md5(content_str.encode('utf-8'))
        
        # Set the id attribute to the hash
        self._id = hash_obj.hexdigest()


class Configer:
    _instance = None
    _config_path = "config.yml"
    _configs: Optional[List[Config]] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Configer, cls).__new__(cls)
            cls._configs = None
        return cls._instance
    
    @classmethod
    def Get(cls) -> List[Config]:
        instance = cls()
        instance._update_configs()
        return instance._configs
    
    def _update_configs(self) -> None:
        # Check if config file exists
        if not os.path.exists(self._config_path):
            raise FileNotFoundError(f"Configuration file not found: {self._config_path}")

        with open(self._config_path, 'r', encoding='utf-8') as file:
            config_data = yaml.safe_load(file)
            self._process_config_data(config_data)
    
    def _process_config_data(self, config_data: Dict[str, Any]) -> None:
        self._configs = []
        if 'broadcasts' in config_data and isinstance(config_data['broadcasts'], list):
            for broadcast_dict in config_data['broadcasts']:
                self._configs.append(Config(broadcast_dict))
