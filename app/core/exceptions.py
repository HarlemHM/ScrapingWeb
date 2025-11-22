"""
Excepciones personalizadas de la aplicación
"""
from fastapi import HTTPException, status


class ScrapingWebException(Exception):
    """Excepción base de la aplicación"""
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class DatabaseException(ScrapingWebException):
    """Excepción de base de datos"""
    pass


class ScrapingException(ScrapingWebException):
    """Excepción durante scraping"""
    pass


class NLPException(ScrapingWebException):
    """Excepción durante procesamiento NLP"""
    pass


class ExportException(ScrapingWebException):
    """Excepción durante exportación"""
    pass


class NotFoundException(HTTPException):
    """Recurso no encontrado"""
    def __init__(self, resource: str, resource_id: str = None):
        detail = f"{resource} no encontrado"
        if resource_id:
            detail = f"{resource} con ID {resource_id} no encontrado"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class AlreadyExistsException(HTTPException):
    """Recurso ya existe"""
    def __init__(self, resource: str, identifier: str = None):
        detail = f"{resource} ya existe"
        if identifier:
            detail = f"{resource} con identificador '{identifier}' ya existe"
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class ValidationException(HTTPException):
    """Error de validación de datos"""
    def __init__(self, message: str, errors: dict = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": message, "errors": errors or {}}
        )


class UnauthorizedException(HTTPException):
    """No autorizado"""
    def __init__(self, message: str = "No autorizado"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


class ForbiddenException(HTTPException):
    """Prohibido - sin permisos"""
    def __init__(self, message: str = "No tiene permisos para esta operación"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)


class BadRequestException(HTTPException):
    """Petición inválida"""
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class ServiceUnavailableException(HTTPException):
    """Servicio no disponible"""
    def __init__(self, message: str = "Servicio temporalmente no disponible"):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=message)
