import logging


def set_logger(tag: str):
    # Configuração do logger  
    logger = logging.getLogger(tag)  
    logger.setLevel(logging.DEBUG)  # Define o nível de log para DEBUG  
    
    # Adiciona um manipulador que imprime os logs no console  
    console_handler = logging.StreamHandler()  
    console_handler.setLevel(logging.DEBUG)  # Também define o nível do manipulador para DEBUG  
    
    # Define um formato de mensagem para os logs  
    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')  
    console_handler.setFormatter(formatter)  
    
    # Adiciona o manipulador ao logger  
    logger.addHandler(console_handler)
    return logger