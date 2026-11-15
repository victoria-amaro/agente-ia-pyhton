"""Errores estables que ocultan detalles internos del proveedor."""


class ErrorAgentes(Exception):
    """Error base visible para la aplicación."""


class ConfiguracionIncompleta(ErrorAgentes):
    """Falta una variable necesaria para ejecutar el modelo."""


class LimiteTemporal(ErrorAgentes):
    """La API rechazó la llamada por cuota o frecuencia."""


class ServicioNoDisponible(ErrorAgentes):
    """La API no está disponible o no se puede alcanzar."""


class RespuestaVacia(ErrorAgentes):
    """El agente finalizó sin producir texto utilizable."""


class ProveedorNoAdmitido(ErrorAgentes):
    """El proveedor configurado no está implementado."""


class ErrorDeArchivo(ErrorAgentes):
    """No fue posible guardar un archivo de salida."""

