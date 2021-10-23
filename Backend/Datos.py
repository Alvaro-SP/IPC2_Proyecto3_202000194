from datetime import date as Date


class datos:
    def __init__(self,valido,Codigo_completo, date, referencia, nit_emisor, nit_receptor, valor, iva, total, referencia_duplicada, nit_emisor_invalid, nit_receptor_invalid, iva_error, total_error):
        self.valido = valido
        self.Codigo_completo = Codigo_completo
        self.date = date
        self.referencia = referencia
        self.nit_emisor = nit_emisor
        self.nit_receptor = nit_receptor
        self.valor = valor
        self.iva = iva
        self.total = total
        #errores
        self.referencia_duplicada = referencia_duplicada
        self.nit_emisor_invalid = nit_emisor_invalid
        self.nit_receptor_invalid = nit_receptor_invalid
        self.iva_error = iva_error
        self.total_error = total_error
        

    # def __init__(self, date: Date, facturas_recibidas: int, facturas_sinerror: int, emisores_facturas: int, receptores_facturas: int):
    #     self.date: Date = date
    #     self.facturas_recibidas: int = facturas_recibidas
    #     self.facturas_sinerror: int = facturas_sinerror
    #     self.emisores_facturas: int = emisores_facturas
    #     self.receptores_facturas: int = receptores_facturas
    #     self.list_error_emisor: list = []
    #     self.list_error_receptor: list = []
    #     self.list_error_iva: list = []
    #     self.list_error_total: list = []
    #     self.list_error_referencia: list = []

    # def agregar_error_factura(self, user: str):
    #     self.list_affected_users.append(user)
