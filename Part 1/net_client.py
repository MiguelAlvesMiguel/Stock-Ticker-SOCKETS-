# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - net_client.py
Grupo: 
Números de aluno:
"""

"""
Stock Market Ticker
===================

"""

# zona para fazer importação



# definição da classe server_connection 

class server_connection:
    """
    Abstrai uma ligação a um servidor TCP. Implementa métodos para: estabelecer 
    a ligação; envio de um comando e receção da resposta; terminar a ligação.
    """
    def __init__(self, address, port):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        pass # Remover esta linha e fazer implementação da função
        
    def connect(self):
        """
        Estabelece a ligação ao servidor especificado na inicialização.
        """
        pass # Remover esta linha e fazer implementação da função

    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação, e retorna
        a resposta recebida pela mesma socket.
        """
        pass # Remover esta linha e fazer implementação da função
    
    def close(self):
        """
        Termina a ligação ao servidor.
        """
        pass # Remover esta linha e fazer implementação da função
