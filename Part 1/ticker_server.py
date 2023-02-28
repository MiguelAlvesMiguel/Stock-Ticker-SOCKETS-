#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_server.py
Grupo:
Números de aluno:
"""

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
2. O resource_pool a estrutura que gere o conjunto das ações.
3. O resource  a estrutura que representa cada uma das ações disponíveis no servidor.
Cada servidor deverá instanciar M recursos, sendo que cada recurso deverá ser inicializado aleatoriamente. 
Isto é, com Nome e Valor gerados aleatoriamente. Nome deverá ser uma string com 7 carateres. Valor deverá 
ser um número real entre 100 e 200. Símbolo deverá ser uma string com 3 carateres iguais aos 3 primeiros 
carateres de Nome.
A lista de subscritores de cada ação deverá começar vazia.

"""

# Zona para fazer importação


###############################################################################
class resource:
    def __init__(self, resource_id):
        pass # Remover esta linha e fazer implementação da função
    def subscribe(self, client_id, time_limit):
        pass # Remover esta linha e fazer implementação da função
    def unsubscribe (self, client_id):
        pass # Remover esta linha e fazer implementação da função
    def status(self, client_id):
        pass # Remover esta linha e fazer implementação da função

    def __repr__(self):
        output = ""
        # R <resource_id> <list of subscribers>
        return output
class resource_pool:
    """
    Abstrai um conjunto de recursos. Implementa métodos para: adicionar um 
    recurso; remover um recurso; obter um recurso; obter a lista de recursos; 
    obter a lista de subscritores de um recurso; adicionar um subscritor a um 
    recurso; remover um subscritor de um recurso; obter o número de subscritores 
    de um recurso; obter o número de subscritores de todos os recursos; 
    obter o número de recursos.
    """
    def __init__(self, max_resources, max_subscribers, max_subscriptions):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        self.max_resources = max_resources
        self.max_subscribers = max_subscribers
        self.max_subscriptions = max_subscriptions
        self.resources = []
        self.subscribers = []
        self.subscriptions = []
    
    def add_resource(self, resource):
        """
        Adiciona um recurso à lista de recursos.
        """
        self.resources.append(resource)

    def remove_resource(self, resource):
        """
        Remove um recurso da lista de recursos.
        """
        self.resources.remove(resource)
    
    def get_resource(self, resource_name):
        """
        Retorna um recurso da lista de recursos.
        """
        for resource in self.resources:
            if resource.name == resource_name:
                return resource
        return None
    
    def get_resources(self):
        """
        Retorna a lista de recursos.
        """
        return self.resources
    
    def get_subscribers(self, resource_name):
        """
        Retorna a lista de subscritores de um recurso.
        """
        for resource in self.resources:
            if resource.name == resource_name:
                return resource.subscribers
        return None
    
    def add_subscriber(self, resource_name, subscriber):
        """
        Adiciona um subscritor a um recurso.
        """
        for resource in self.resources:
            if resource.name == resource_name:
                resource.subscribers.append(subscriber)


    def remove_subscriber(self, resource_name, subscriber):
        """
        Remove um subscritor de um recurso.
        """
        for resource in self.resources:
            if resource.name == resource_name:
                resource.subscribers.remove(subscriber)

    def get_subscriber_count(self, resource_name):
        """
        Retorna o número de subscritores de um recurso.
        """
        for resource in self.resources:
            if resource.name == resource_name:
                return len(resource.subscribers)
        return None
    
    def get_subscriber_count_all(self):
        """
        Retorna o número de subscritores de todos os recursos.
        """
        count = 0
        for resource in self.resources:
            count += len(resource.subscribers)
        return count
    
    def get_resource_count(self):
        """
        Retorna o número de recursos.
        """
        return len(self.resources)
    
    def get_subscriptions(self):
        """
        Retorna a lista de subscrições.
        """
        return self.subscriptions
    
    
    