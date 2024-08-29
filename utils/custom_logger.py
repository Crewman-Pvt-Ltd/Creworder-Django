import logging
import os
def get_logger(fileName):
    logs_dir = os.path.join(os.path.dirname(__file__), '../logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    logger = logging.getLogger(fileName)
    
    if not logger.hasHandlers():
        file_handler = logging.FileHandler(os.path.join(logs_dir, f"{fileName}.log"))
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.setLevel(logging.DEBUG)
    
    return logger
