import logging
from datetime import datetime
from typing import Dict, Optional

# Get logger
logger = logging.getLogger('global_data.py')

class GlobalData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._last_runs = {}
        return cls._instance

    def get_last_run(self, broadcast_id: str) -> datetime:
        if broadcast_id not in self._last_runs:
            logger.info(f"No previous run for broadcast {broadcast_id}")
            self._last_runs[broadcast_id] = datetime.now()
        
        return self._last_runs[broadcast_id]

    def update_last_run(self, broadcast_id: str) -> None:
        run_time = datetime.now()
        
        self._last_runs[broadcast_id] = run_time
        logger.info(f"Updated last run for broadcast {broadcast_id} to {run_time}")
