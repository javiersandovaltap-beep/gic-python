# -- coding: utf-8 --

__all__ = ['Cliente', 'ClienteRegular', 'ClientePremium', 'ClienteCorporativo']


def __getattr__(name):
    if name == 'Cliente':
        from modelos.cliente_base import Cliente
        return Cliente
    elif name == 'ClienteRegular':
        from modelos.cliente_regular import ClienteRegular
        return ClienteRegular
    elif name == 'ClientePremium':
        from modelos.cliente_premium import ClientePremium
        return ClientePremium
    elif name == 'ClienteCorporativo':
        from modelos.cliente_corporativo import ClienteCorporativo
        return ClienteCorporativo
    raise AttributeError(f"module 'modelos' has no attribute '{name}'")
