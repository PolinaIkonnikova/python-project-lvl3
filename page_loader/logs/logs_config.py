import logging
import os, sys


log_path = os.path.join(os.getcwd(), 'page_loader/logs/logs.log')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(log_path, 'a')])

logger = logging.getLogger(__name__)

err_logger = logging.getLogger(__name__)
err_logger.setLevel(logging.WARNING)
handler = logging.StreamHandler(stream=sys.stderr)
err_logger.addHandler(handler)

