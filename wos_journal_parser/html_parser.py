import logging
import re
from pathlib import Path
from bs4 import BeautifulSoup
from typing import List, Optional
from wos_journal_parser import logging_config

from .types import Journal

class JournalHtmlParser:
  logger = logging.getLogger(__name__)
  
  def __init__(self, data_path = 'data/'):
    self.data_path = Path('data/')
    self.files_dir = self.data_path / 'raw'
    
  def parse_journals(self) -> List[Journal]:
    journals = []
    html_files = sorted(self.files_dir.glob("page_*.html"), key=lambda f: int(f.stem.split('_')[1]))
    for file in html_files:
      self.logger.info(f"Reading {file.name}...")
      with open(file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
      
      for row in soup.find_all("div", class_="row px-5 py-5"):
        titles = row.find_all("div", class_="title")
        contents = row.find_all("div", class_="content")
        title_map = {t.get_text(strip=True): i for i, t in enumerate(titles)}
        
        def get_content(key) -> Optional[str]:
          idx = title_map.get(key)
          return contents[idx].get_text(strip=True) if idx is not None else None
        
        details_link = row.find("a", string=re.compile(r"More Details\s*"))
        details_url = details_link.get("href") if details_link else Journal.missing_value
        
        journal = Journal(
          id_=get_content("ID:"),
          title=get_content("Journal Title:"),
          issn=get_content("ISSN:"),
          eissn=get_content("eISSN:"),
          indexes=get_content("WoS Core Citation Indexes:"),
          jif=get_content("Journal Impact Factor (JIF):"),
          details_url=details_url,
        )
        journals.append(journal)
    return journals