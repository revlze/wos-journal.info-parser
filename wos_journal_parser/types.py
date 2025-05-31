from dataclasses import dataclass
from typing import Optional

@dataclass
class Journal:
  id_: Optional[str]
  title: Optional[str]
  issn: Optional[str]
  eissn: Optional[str]
  indexes: Optional[str]
  jif: Optional[str]
  details_url: Optional[str]
  
  missing_value = '-'
