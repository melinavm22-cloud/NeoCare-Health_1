import logging
import sys
from datetime import datetime
from typing import Optional

def setup_logging():
    """Configurar logging estructurado para la aplicación"""
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log')
        ]
    )
    
    return logging.getLogger("neocare")

def log_auth_attempt(email: str, success: bool, ip: Optional[str] = None):
    """Registrar intentos de autenticación"""
    logger = logging.getLogger("neocare.auth")
    if success:
        logger.info(f"Login exitoso - Email: {email}, IP: {ip}")
    else:
        logger.warning(f"Login fallido - Email: {email}, IP: {ip}")

def log_resource_access(user_id: int, resource_type: str, resource_id: int, action: str):
    """Registrar acceso a recursos"""
    logger = logging.getLogger("neocare.access")
    logger.info(f"User {user_id} - {action} {resource_type} {resource_id}")

def log_error(error: Exception, context: str):
    """Registrar errores con contexto"""
    logger = logging.getLogger("neocare.error")
    logger.error(f"Error en {context}: {str(error)}", exc_info=True)
