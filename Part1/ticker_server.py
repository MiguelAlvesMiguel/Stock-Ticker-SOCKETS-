#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_client.py
Grupo:19
Números de aluno:
Henrique Venâncio-58618
Miguel Miguel-58628
"""
import random
import socket as s
import argparse as argparse
import string
import sys as sys
import time 
"""
Server for the resource Market Ticker
=================================
Server for the resource Market Ticker. It receives a connection from a client and receives a word from it and prints it.
"""
class resource :
    def __init__(self, resource_id):
        self.resource_id = resource_id
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
        #Ver se o resource existe
        if self.resource_id not in range(self.max_resources):
            return "UNKNOWN-RESOURCE"
        #Ver se o cliente está subscrito
        if client_id in self.subscribers:
            return "SUBSCRIBED"
        else:
            return "UNSUBSCRIBED"
        
    def __repr__(self):
        """
        Devolve uma string com a informação de um recurso.
        Cada linha é composta por texto com os seguintes campos (separados por espaços): 
        1. A letra R para indicar um recurso;
        2. O ID do recurso;
        3. O número atual de subscritores desse recurso;
        4. A lista de clientes subscritos (ordenada crescentemente pelo cliente-ID). Não apresentar nada,
        se não houver clientes subscritos.
        """
        if len(self.subscribers) == 0:
            return f"R {self.resource_id} {len(self.subscribers)}"
        else:
            return f"R {self.resource_id} {len(self.subscribers)} {self.subscribers}"

class resource_pool:
    """
    Abstrai um conjunto de recursos.
    """
    def __init__(self, M,K,N):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        self.max_resources = M
        self.max_resources_per_client = K
        self.max_subscribers_per_resource = N
        self.subscriptions_per_client = {} #subscriptions_per_client é um dicionário que tem como chave o id do cliente e como valor uma lista com os ids dos resources que o cliente subscreveu e o tempo limite de subscrição
        #por examplo: {1: [(2, time()+10), (3, time()+10)], 2: [(1, time()+10)]}
        self.resources = [resource(resource_number) for resource_number in range(M)]

    def clear_expired_subs(self):
        for client_id in self.subscriptions_per_client.keys():
            for resource in self.subscriptions_per_client[client_id]:
                if time() > resource[1]:
                    self.unsubscribe(resource[0], client_id)

    def subscribe(self, resource_id, client_id, time_limit):
        #Se o recurso não existir, o servidor deverá retornar UNKNOWN-RESOURCE
        if resource_id not in range(self.max_resources):
            return "UNKNOWN-RESOURCE"
        
        #verificar que o número de resources que o cliente subscreveu não ficaria maior que o máximo permitido
        if client_id not in self.subscriptions_per_client.keys():# evitar bug
            if len(self.subscriptions_per_client[client_id])+1 > self.max_resources_per_client:
                return "NOK"
        
         #verificar que o número de subscritores do resource não ficaria maior que o máximo permitido
        if self.resources[resource_id].get_number_of_subscribers()+1 > self.max_subscribers_per_resource:
            return "NOK"

        #Se o pedido for para um recurso já subscrito pelo cliente, o novo Deadline deverá ser atualizado, 
        # e retornar OK.
        if client_id in self.subscriptions_per_client.keys():
            #verificar se o cliente já subscreveu o resource
            if resource_id in [resource[0] for resource in self.subscriptions_per_client[client_id]]:
                #atualizar o tempo limite de subscrição 
                for resource in self.subscriptions_per_client[client_id]:
                    if resource[0] == resource_id:
                        resource[1] = time()+time_limit
                return "OK"
            else:
                self.add_subscriber(resource_id, client_id, time_limit)
                return "OK"
        
    def unsubscribe (self, resource_id, client_id): #CANCEL
        """
        O comando CANCEL <recurso ID> remove uma subscrição ativa numa determinada ação/recurso para o 
        cliente que está a enviar o pedido. 
        • Em geral, se o recurso existir e estiver subscrito pelo cliente, o servidor deverá registar o pedido, e 
        retornar OK.
        • Se o recurso não existir, o servidor deverá retornar UNKNOWN-RESOURCE.
        • Se o pedido for para um recurso não subscrito pelo cliente, o servidor deverá retornar NOK.
        """
        #Se o recurso não existir, o servidor deverá retornar UNKNOWN-RESOURCE
        if resource_id not in range(self.max_resources):
            return "UNKNOWN-RESOURCE"
        
        #Se o pedido for para um recurso não subscrito pelo cliente, o servidor deverá retornar NOK.
        if client_id not in self.subscriptions_per_client.keys():
            return "NOK"
        else:
            if resource_id not in [resource[0] for resource in self.subscriptions_per_client[client_id]]:
                return "NOK"
            else:
                self.remove_subscriber(resource_id, client_id)
                return "OK"
    def status(self, resource_id, client_id):
        """
        O comando STATUS <recurso ID> retorna o estado de subscrição de um determinado recurso para o cliente que está a enviar o pedido. 
        • Em geral, se o recurso existir, o servidor deverá retornar o estado de subscrição do recurso para o cliente.
        • Se o recurso não existir, o servidor deverá retornar UNKNOWN-RESOURCE.
        """
        #Se o recurso não existir, o servidor deverá retornar UNKNOWN-RESOURCE
        if resource_id not in range(self.max_resources):
            return "UNKNOWN-RESOURCE" 
        else:
            return self.resources[resource_id].status(client_id)
        
    def infos(self, option, client_id):
        """
        O comando INFOS tem duas variantes, é utilizado para obter informações sobre o cliente no servidor. 
        • INFOS M – deverá retornar o <lista de recursos-ID subscritos pelo cliente> 
        • INFOS K – deverá retornar o <número total de ações a que o cliente ainda pode subscrever> 
        """
        if option == "M":
            # Se o cliente não tiver subscrito nenhum resource, retornar "EMPTY"
            if client_id not in self.subscriptions_per_client.keys():
                return "EMPTY"
            #Extração dos ids dos resources que o cliente subscreveu
            return [resource[0] for resource in self.subscriptions_per_client[client_id]]

        elif option == "K":
            return self.max_resources_per_client - len(self.subscriptions_per_client[client_id])
        
    def statis(self, option, resource_id):
        """
        O comando STATIS é utilizado para obter informação genérica do servidor.
        • STATIS L <recurso ID> – deverá retornar o número de subscritores do recurso em questão.
        • STATIS ALL – é utilizado para obter uma visão geral do estado do serviço de gestão de ações e seus 
        subscritores. O servidor deverá retornar uma string formada por uma linha por cada recurso no 
        servidor. Cada linha é composta por texto com os seguintes campos (separados por espaços): 
        1. A letra R para indicar um recurso;
        2. O ID do recurso;
        3. O número atual de subscritores desse recurso;
        4. A lista de clientes subscritos (ordenada crescentemente pelo cliente-ID). Não apresentar nada,
        se não houver clientes subscritos.

        Um exemplo de resultado do comando num servidor com M=4 recursos pode ser o seguinte: 
        R 1 5 1 2 3 4 5
        R 2 0
        R 3 3 3 4 5
        R 4 3 1 2 3
        """
        #• STATIS L <recurso ID> – deverá retornar o número de subscritores do recurso em questão.
        if option == 'L':
            #N sei se isto é preciso
            if resource_id not in range(self.max_resources):
                return "UNKNOWN-RESOURCE"
            else:
                return self.resources[resource_id].get_number_of_subscribers()
        else:
            #• STATIS ALL – é utilizado para obter uma visão geral do estado do serviço de gestão de ações e seus 
            #subscritores. O servidor deverá retornar uma string formada por uma linha por cada recurso no 
            #servidor. Cada linha é composta por texto com os seguintes campos (separados por espaços): 
            #1. A letra R para indicar um recurso;
            #2. O ID do recurso;
            #3. O número atual de subscritores desse recurso;
            #4. A lista de clientes subscritos (ordenada crescentemente pelo cliente-ID). Não apresentar nada,
            #se não houver clientes subscritos.
            output = ""
            for resource in self.resources:
                output += resource.__repr__()
            return output




        
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
    def add_resource(self, resource):
        #verificar se o resource já existe e se o número de resources não excede o máximo permitido
        if resource not in self.resources and len(self.resources) < self.max_resources:
            self.resources.append(resource)
    def remove_resource(self, resource_id):
        #remover o resource com o id resource_id
        self.resources.remove(resource_id)

    def get_resource(self, resource_id):
        #retornar o resource com o id resource_id
        return self.resources[resource_id]
    def get_resources(self):
        return self.resources
    def get_subscribers(self, resource_id):
        return self.resources[resource_id].subscribers
    def add_subscriber(self, resource_id, client_id,time_limit):
        #verificar se o cliente já não subscreveu o resource e se o número de subscrições do cliente não excede o máximo permitido e se o número de subscrições do resource não excede o máximo permitido em vários if's separados
        self.resources[resource_id].subscribers.append(client_id)
        self.subscriptions_per_client[client_id].append((resource_id, time()+time_limit))

    def remove_subscriber(self, resource_id, client_id):
        #verificar se o cliente subscreveu o resource e se o cliente existe em vários if's separados
        if client_id in self.subscriptions_per_client.keys():
            if resource_id in self.subscriptions_per_client[client_id]:
                self.resources[resource_id].subscribers.remove(client_id)
                self.subscriptions_per_client[client_id].remove(resource_id)
                
    def get_subscribers_count(self, resource_id):
        return len(self.resources[resource_id].subscribers)
    def get_total_subscribers_count(self):
        total_subscribers = 0
        for resource in self.resources:
            total_subscribers += len(resource.subscribers)
        return total_subscribers
    def get_resources_count(self):
        return len(self.resources)
###############################################################################

class client_connection:
    """
    Abstracts a connection to a TCP client. Implements methods for: establishing 
    the connection; receving a message; sending a message; closing the connection.
    """

    def __init__(self, host, port):
        """
        Initializes the class with parameters for future operation.
        """
        self.host = host
        self.port = int(port)
        self.sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)

    def listen(self,queue_size):
        """
        Função que cria um socket TCP e estabelece a ligação ao servidor especificado
        nos parâmetros.
        Parâmetros:
        host - endereço IP do servidor
        port - número de porta do servidor
        Retorna:
        socket - socket TCP ligado ao servidor
        Excepções:
        socket.error - se ocorrer algum erro na criação do socket ou na ligação
        """
        self.sock.bind((self.host, int(self.port)))
        self.sock.listen(queue_size)


    def receive_all(self,socket, length):
        """
        Função que recebe uma quantidade de dados específica de uma socket.
        Parâmetros:
        socket - socket TCP ligada ao servidor
        length - quantidade de dados a receber
        Retorna:
        data - dados recebidos
        Excepções:
        socket.error - se ocorrer algum erro na recepção dos dados
        """

        data = b''
        while len(data) < length:
            data += socket.recv(length - len(data))
    
        return data
    
    def accept(self):
        """
        Accepts a connection from a client.
        """
        print("socket:",self.sock)
        print("self.adress:",self.host+"self.port:",self.port)
        self.sock, (self.host, self.port) = self.sock.accept()# What this line does?
        print("ACCEPTED")
        print("socket:",self.sock)
        print("self.adress:",self.address+"self.port:",self.port)
        
    def send(self, message):
        """
        Sends a message to the client.
        """
        self.sock.send(message.encode())
    
    def close(self):
        """
        Closes the connection to the client.
        """
        self.sock.close()
    
    def __repr__(self):
        """
        Returns a string representation of the class.
        """
        return "Client connection to {}:{}.".format(self.address, self.port)
    
    def __str__(self):
        """
        Returns a string representation of the class.
        """
        return self.__repr__()
    
###############################################################################
#ALL COMMANDS THAT THE CLIENT CAN SEND TO THE SERVER (static)
COMMANDS = ["SUBSCR", "CANCEL", "STATUS", "INFO", "STATIS","SLEEP", "EXIT"]
def processCommand(command,pool): #The command is already validated
    """
    Função que processa um comando recebido do cliente.
    Parâmetros:
    command - comando a processar (o última palavra do command é o clientID caso seja necessário)
    Retorna:
    A resposta a enviar ao cliente
    """
    command = command.split() #split the command into a list
    if command[0] == "SUBSCR":
        return pool.subscribe(command[1],command[2],int(command[3]))
    if command[0] == "CANCEL":
        return pool.unsubscribe(command[1],command[2])
    if command[0] == "STATUS":
        return pool.get_subscribers_count(command[1])
        
def main():

    """
    Ciclo de operações é o seguinte:
    1. Esperar um pedido de ligação;
    2. Mostrar no ecrã informação sobre a ligação (IP/hostname e porto de origem do cliente);
    3. Verificar se existem recursos cujo tempo de subscrição tenha expirado, e remover essas subscrições;
    4. Receber uma mensagem com um pedido;
    5. Processar esse pedido;
    6. Responder ao cliente;
    7. Fechar a ligação.
    """
    # Criar instância de resource_pool usando a classe acima
    pool = resource_pool(args.max_resources,args.max_subscriptions_per_client, args.max_subscribers_per_resource)

    # get the hostname
    host = s.gethostname()
    port = 5000  # initiate port no above 1024

    #ISTO SE CALHAR È DENTRO DO LOOP
    server_socket = s.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    """
    1. Esperar um pedido de ligação;
    2. Mostrar no ecrã informação sobre a ligação (IP/hostname e porto de origem do cliente);
    3. Verificar se existem recursos cujo tempo de subscrição tenha expirado, e remover essas subscrições;
    4. Receber uma mensagem com um pedido;
    5. Processar esse pedido;
    6. Responder ao cliente;
    7. Fechar a ligação.
    """
    while True:
        # configure how many client the server can listen simultaneously
        server_socket.listen(10)
        conn, address = server_socket.accept()  # accept new connection #conn is a socket object
        print("Connection from: " + str(address), "to port: " + str(port))
        # receive data stream. it won't accept data packet greater than 1024 bytes
        #Verificar se existem recursos cujo tempo de subscrição tenha expirado, e remover essas subscrições;
        pool.clear_expired_subs()
        received = conn.recv(1024).decode()
        if not received:
            # if data is not received break
            break
        print("from connected user: " + str(received))
        print("Processing message...")
        response=processCommand(received.split()[0],pool)
        #send OK to client
        conn.sendall(response.encode())
        #close connection
        conn.close()

    #connection = client_connection(args.host, args.port)
    ##waiting for connection
    #connection.listen(1)
    ##receive message
    ##if connected to client then receive message
    ##receive if connected to client
    ## if message is valid then process message
    ## if message is invalid then send error message
    ## if message is exit then close connection
    ## if message is sleep then sleep for 5 seconds
    ## code:
    #while True:
    #    client, address = connection.accept()
    #    print("Connected to client: {}".format(address))
    #    #receive message
    #    message = client.recv(1024).decode()
    #    print("Received message: {}".format(message))
    #    #process message



    #process message (assume that the message is valid)
    
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
    parser.add_argument('host', type=str, help='IP or hostname where the server will provide the resources')
    parser.add_argument('port', type=int, help='TCP port where the server will listen for connection requests')
    parser.add_argument('max_resources', type=int, help='Number of resources that will be managed by the server')
    parser.add_argument('max_subscriptions_per_client', type=int, help='Maximum number of resources per client')
    parser.add_argument('max_subscribers_per_resource', type=int, help='Maximum number of subscribers per resource ')
    args = parser.parse_args()

    main()

    