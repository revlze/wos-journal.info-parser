import csv
import logging

from pathlib import Path
from typing import List

from wos_journal_parser import logging_config
from .types import Journal

class JournalSerializer:
  
  logger = logging.getLogger(__name__)
  def __init__(self, data_path = 'data/'):
    self.data_path = Path(data_path)
    self.files_dir = None
    self.create_processed_dir()
    
  def create_processed_dir(self):
    self.files_dir = self.data_path / 'processed'
    self.files_dir.mkdir(exist_ok=True, parents=True)
    
  def save_journal_to_csv(self, journals: List[Journal], filename: str = "journals.csv"):
    file_path = self.files_dir / filename
    
    fieldnames = [field for field in Journal.__dataclass_fields__]
    
    with open(file_path, 'w', encoding='utf-8') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      for journal in journals:
        writer.writerow(journal.__dict__)
    self.logger.info(f"Saved {len(journals)} journals into {file_path}!")