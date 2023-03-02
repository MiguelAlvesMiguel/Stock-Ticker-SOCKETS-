#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_server.py
Grupo:
Números de aluno:
"""
import random
import socket as socket
import argparse as argparse
import string
import sys as sys
import time 
"""
Server for the Stock Market Ticker
=================================
Server for the Stock Market Ticker. It receives a connection from a client and receives a word from it and prints it.
Send the word "hello" to the server and it will respond with "world".~


Programa Servidor
O programa Servidor será implementado em Python3 no ficheiro ticker_server.py fornecido.
O seu ciclo de operações é o seguinte:
1. Esperar um pedido de ligação;
2. Mostrar no ecrã informação sobre a ligação (IP/hostname e porto de origem do cliente);
3. Verificar se existem recursos cujo tempo de subscrição tenha expirado, e remover essas subscrições;
4. Receber uma mensagem com um pedido;
5. Processar esse pedido;
6. Responder ao cliente;
7. Fechar a ligação.
O servidor deverá receber os seguintes parâmetros pela linha de comandos, pela ordem apresentada:
1. IP ou hostname onde o servidor fornecerá os recursos;
2. Porto TCP onde escutará por pedidos de ligação;
3. Número de ações/recursos que serão geridos pelo servidor (M);
4. Número máximo de ações por cliente (K);
5. Número máximo de subscritores por ação (N).
FCUL LTI Aplicações Distribuídas 2022/2023
Projeto 1
Desta forma, um exemplo de inicialização do servidor é o seguinte:
$ python3 ticker_server.py localhost 9999 4 3 100
O servidor deverá ser composto por 3 classes, tal como representado na Figura 1, nomeadamente:
1. O ticker_server gere as ligações por sockets com o cliente,
2. O stock _pool a estrutura que gere o conjunto das ações.
3. O stock  a estrutura que representa cada uma das ações disponíveis no servidor.
Cada servidor deverá instanciar M recursos, sendo que cada recurso deverá ser inicializado aleatoriamente. 
Isto é, com Nome e Valor gerados aleatoriamente. Nome deverá ser uma string com 7 carateres. Valor deverá 
ser um número real entre 100 e 200. Símbolo deverá ser uma string com 3 carateres iguais aos 3 primeiros 
carateres de Nome.
A lista de subscritores de cada ação deverá começar vazia.

"""
# Zona para fazer importação
###############################################################################
class stock :
    def __init__(self, stock_id):
        self.stock_id = stock_id
        # Gerar aleatoriamente uma string com 7 carateres
        self.name= ''.join(random.choice(string.ascii_uppercase) for _ in range(7))
        self.symbol = self.name[:3]
        self.subscribers = []
        self.value = random.randint(100,200)


    def subscribe(self, client_id, time_limit): #se é o server que gera tudo porque é que o time_limit é passado como argumento?
        self.subscribers.append(client_id)
        #after time_limit seconds, remove client_id from subscribers

    def unsubscribe (self, client_id):
        self.subscribers.remove(client_id)
    def status(self, client_id):
        pass # Remover esta linha e fazer implementação da função
    
    
    def __repr__(self):
        return "R " + str(self.stock_id) + " " + str(self.subscribers) 
        
class stock_pool:
    """
    Abstrai um conjunto de recursos.
    """
    def __init__(self, M,K, N):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        self.max_stocks = M
        self.max_stocks_per_client = K
        self.max_subscriptions_per_stock = N
        self.subscriptions_per_client = {} #subscriptions_per_client é um dicionário que tem como chave o id do cliente e como valor uma lista com os ids dos stocks que o cliente subscreveu e o tempo limite de subscrição
        #por examplo: {1: [(2, 10), (1, 20)], 2: [(2, 10), (3, 20)]}
        self.stocks = [stock(stock_number) for stock_number in range(M)]

    def clear_expired_subs(self):
        pass # Remover esta linha e fazer implementação da função
    def subscribe(self, resource_id, client_id, time_limit):
        #verificar se o stock existe e se o cliente já não subscreveu o stock
        """
        Em geral, se o recurso existir, o servidor deverá registar o pedido, e retornar OK.
    
   
    • 
    • Se o recurso já tiver ativas N subscrições, o servidor deverá retornar NOK.
        """
        #Se o recurso não existir, o servidor deverá retornar UNKNOWN-RESOURCE
        if resource_id not in range(self.max_stocks):
            return "UNKNOWN-RESOURCE"
        
        #verificar que o número de stocks que o cliente subscreveu não ficaria maior que o máximo permitido
        if client_id not in self.subscriptions_per_client.keys():# evitar bug
            if len(self.subscriptions_per_client[client_id])+1 > self.max_stocks_per_client:
                return "NOK"
        
         #verificar que o número de subscritores do stock não ficaria maior que o máximo permitido
        if self.stocks[resource_id].get_number_of_subscribers()+1 > self.max_subscriptions_per_stock:
            return "NOK"


        #Se o pedido for para um recurso já subscrito pelo cliente, o novo Deadline deverá ser atualizado, 
        # e retornar OK.
        if client_id in self.subscriptions_per_client.keys():
            #verificar se o cliente já subscreveu o stock
            if resource_id in [stock[0] for stock in self.subscriptions_per_client[client_id]]:
                #atualizar o tempo limite de subscrição 
                for stock in self.subscriptions_per_client[client_id]:
                    if stock[0] == resource_id:
                        stock[1] = time_limit
                return "OK"
            else:
                self.add_subscriber(resource_id, client_id, time_limit)
                return "OK"
        
    def unsubscribe (self, resource_id, client_id):
        pass # Remover esta linha e fazer implementação da função
    def status(self, resource_id, client_id):
        pass # Remover esta linha e fazer implementação da função
    def infos(self, option, client_id):
        pass # Remover esta linha e fazer implementação da função
    def statis(self, option, resource_id):
        pass # Remover esta linha e fazer implementação da função
    def __repr__(self):
        output = ""
        # Acrescentar no output uma linha por cada recurso
        return output
    """
     Implementa métodos para: adicionar um 
    recurso; remover um recurso; obter um recurso; obter a lista de recursos; 
    obter a lista de subscritores de um recurso; adicionar um subscritor a um 
    recurso; remover um subscritor de um recurso; obter o número de subscritores 
    de um recurso; obter o número de subscritores de todos os recursos; 
    obter o número de recursos.
    """
    def add_stock(self, stock):
        #verificar se o stock já existe e se o número de stocks não excede o máximo permitido
        if stock not in self.stocks and len(self.stocks) < self.max_stocks:
            self.stocks.append(stock)
    def remove_stock(self, stock_id):
        #remover o stock com o id stock_id
        self.stocks.remove(stock_id)

    def get_stock(self, stock_id):
        #retornar o stock com o id stock_id
        return self.stocks[stock_id]
    def get_stocks(self):
        return self.stocks
    def get_subscribers(self, stock_id):
        return self.stocks[stock_id].subscribers
    def add_subscriber(self, stock_id, client_id,time_limit):
        #verificar se o cliente já não subscreveu o stock e se o número de subscrições do cliente não excede o máximo permitido e se o número de subscrições do stock não excede o máximo permitido em vários if's separados
        self.stocks[stock_id].subscribers.append(client_id)
        self.subscriptions_per_client[client_id].append((stock_id, time()+time_limit))

        
    def remove_subscriber(self, stock_id, client_id):
        #verificar se o cliente subscreveu o stock e se o cliente existe em vários if's separados
        if client_id in self.subscriptions_per_client.keys():
            if stock_id in self.subscriptions_per_client[client_id]:
                self.stocks[stock_id].subscribers.remove(client_id)
                self.subscriptions_per_client[client_id].remove(stock_id)
                
    def get_subscribers_count(self, stock_id):
        return len(self.stocks[stock_id].subscribers)
    def get_total_subscribers_count(self):
        total_subscribers = 0
        for stock in self.stocks:
            total_subscribers += len(stock.subscribers)
        return total_subscribers
    def get_stocks_count(self):
        return len(self.stocks)
###############################################################################



def main():
    # Ler argumentos da linha de comandos
    # Criar instância de stock _pool
    # Criar M recursos e adicionar à stock _pool
    # Criar socket TCP/IP
    # Associar socket à porta
    # Escutar por novas ligações
    # Processar pedidos de ligação
    # Fechar socket
    pass

if __name__ == "__main__":
    """
    O servidor deverá receber os seguintes parâmetros pela linha de comandos, pela ordem apresentada:
    1. IP ou hostname onde o servidor fornecerá os recursos;
    2. Porto TCP onde escutará por pedidos de ligação;
    3. Número de ações/recursos que serão geridos pelo servidor (M);
    4. Número máximo de ações por cliente (K);
    5. Número máximo de subscritores por ação (N).
    FCUL LTI Aplicações Distribuídas 2022/2023
    Projeto 1
    Desta forma, um exemplo de inicialização do servidor é o seguinte:
    $ python3 ticker_server.py localhost 9999 4 3 100
    """
    #use argparse
    parser = argparse.ArgumentParser(description='Ticker Server')
    parser.add_argument('host', type=str, help='IP or hostname where the server will provide the stocks')
    parser.add_argument('port', type=int, help='TCP port where the server will listen for connection requests')
    parser.add_argument('stocks', type=int, help='Number of stocks that will be managed by the server')
    parser.add_argument('max_stocks', type=int, help='Maximum number of stocks per client')
    parser.add_argument('max_subscribers', type=int, help='Maximum number of subscribers per stock ')
    args = parser.parse_args()

    main()

    