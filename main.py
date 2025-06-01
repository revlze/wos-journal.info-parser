import logging
from wos_journal_parser.downloader import Downloader
from wos_journal_parser import logging_config 
from wos_journal_parser.html_parser import JournalHtmlParser
from wos_journal_parser.serializer import JournalSerializer

logger = logging.getLogger(__name__)

logger.info(f"Starting downloader")
with Downloader() as d:
  d.download()

parser = JournalHtmlParser()
journals = parser.parse_journals()

save = JournalSerializer()
save.save_journal_to_csv(journals=journals)