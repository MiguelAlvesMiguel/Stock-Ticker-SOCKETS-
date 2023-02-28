#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_client.py
Grupo:
Números de aluno:
"""
# Zona para fazer imports

import socket as socket
import argparse as argparse
import sys as sys 

"""
Client for the Stock Market Ticker
=================================
VISÃO GERAL
2 Visão Geral
O primeiro projeto visa concretizar um Ticker do mercado de ações utilizando o modelo cliente-servidor (uma 
ação é um título patrimonial correspondente a uma parcela do capital social de uma empresa). Um Ticker do 
mercado de ações permite aos utilizadores subscreverem informação sobre ações específicas e receberem
atualizações continuamente ao longo do tempo. O projeto utilizará a arquitetura cliente-servidor, em que os 
utilizadores usam o cliente para subscreverem informação sobre as ações e o servidor envia continuamente 
aos clientes a informação sobre as ações subscritas. O servidor a implementar neste projeto possui os últimos 
dados das ações e transmite as atualizações para todos os clientes que subscreveram a informação sobre essas 
ações.
Cada cliente pode (1) subscrever ou (2) cancelar a subscrição de múltiplas ações. Quando uma subscrição é 
feita, ela terá uma duração definida em segundos. A partir do momento da subscrição e durante esse período, 
o servidor deverá transmitir a informação mais recente da ação em questão ao cliente, uma vez por segundo.
Após o período definido, a inscrição será cancelada e as informações deixarão de ser enviadas.
O cliente pode ainda solicitar um vasto leque de informações ao servidor, nomeadamente informações do 
cliente: (3) saber se está subscrito ou não a uma determinada ação, (4) a lista de ações que ele tem atualmente 
subscritas e (5) quantas outras ações ainda pode subscrever. Tem também a possibilidade de pedir informação 
fonte: www.quoteinspector.com/
FCUL LTI Aplicações Distribuídas 2022/2023
Projeto 1
mais genérica, nomeadamente: (6) o número atual de subscritores de uma dada ação, e (7) a listagem completa 
do estado de cada uma das ações do servidor.
----------------------------------------------------------------------------------------------------------------

CLIENTE
Conceitos: 

Ação - também designada por recurso no contexto do projeto – é no essencial uma estrutura de dados e uma
lista de funcionalidades intrínsecas. Cada recurso é caracterizado:
• pelo ID único (número natural), 
• pela SIMBOLO (string de 3 carateres) 
• pela NOME (string de 7 carateres) 
• pelo VALOR (número real).

Um recurso deverá implementar funcionalidades como: 
• ser subscrito,
• anular a subscrição, 
• retornar se um cliente em particular é subscritor, e
• retornar o número total de subscritores.
Cliente – programa que aceita comandos de texto do Utilizador para que este possa fazer uso das 7
funcionalidades acima referidas, e que envia esses comandos ao programa servidor.
Servidor – programa gestor dos recursos (ações) que responde aos pedidos dos clientes.

Regras:
• Uma ação pode ser subscrita por múltiplos clientes simultaneamente até a um máximo de N clientes -
limite fixado pelo servidor. A estrutura de dados de cada ação deverá ir anotando a lista dos clientes
subscritores para garantir este limite. Assim sendo, um cliente ao tentar subscrever a uma ação já 
subscrita por outros N clientes terá o seu pedido negado.
• Por outro lado, um cliente está restrito a subscrever até ao máximo de K ações simultaneamente - limite 
fixado pelo servidor. Assim sendo, quando o cliente tenta subscrever a ação K+1, o servidor deverá 
negar esse pedido. O servidor deverá ser capaz de contar quantas ações tem subscritas um dado cliente.
• Uma ação é sempre subscrita por um tempo de concessão decidido pelo cliente. O servidor deverá 
automaticamente anular a subscrição de um cliente findo esse tempo
----------------------------------------------------------------------------------------------------------------
O programa deverá receber os seguintes parâmetros pela linha de comandos, pela ordem apresentada:
1. o ID único do cliente
2. o IP ou hostname do servidor
3. o porto TCP onde o servidor recebe pedidos de ligação
----------------------------------------------------------------------------------------------------------------
Desta forma, um exemplo de inicialização do cliente é o seguinte:
$ python3 ticker_client.py 1 localhost 9999
*Validar o comando fornecido: O cliente será responsável por verificar se o comando do utilizador é válido e 
se não possui gralhas na sintaxe especificada.
• Caso o comando não exista ou possua gralhas, o cliente apresentará o resultado “UNKNOWNCOMMAND”. 
• Caso faltem argumentos, o cliente apresentará o resultado “MISSING-ARGUMENTS

"""


#ALL COMMANDS THAT THE CLIENT CAN SEND TO THE SERVER (static)
COMMANDS = ["SUBSCR", "CANCEL", "STATUS", "INFO", "STATIS"]

# Programa principal

class server_connection:
    """
    Abstrai uma ligação a um servidor TCP. Implementa métodos para: estabelecer 
    a ligação; envio de um comando e receção da resposta; terminar a ligação.
    """

    def __init__(self, address, port):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        server_connection.address = address
        server_connection.port = port
        server_connection.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a TCP socket

    def connect(self):
        """
        Estabelece a ligação ao servidor especificado na inicialização.
        """
        #Connect to the server without using the sock_utils library
        self.sock.connect((server_connection.address, server_connection.port))

    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação, e retorna
        a resposta recebida pela mesma socket.
        """
        
        self.sock.sendall(data.encode()) #Encode the data to bytes and send it to the server because the server is expecting bytes
        response = self.sock.recv(1024)
        self.sock.close()
        return response.decode()
    
    def close(self):
        """
        Termina a ligação ao servidor.
        """
        self.sock.close()

def validate_command(command):
    """
    Valida o comando fornecido pelo utilizador. 

    SUBSCR <ID do recurso> <limite de tempo>
    CANCEL <ID do recurso>
    STATUS <ID do recurso>
    INFOS M OR INFOS K  
    STATIS L <ID do recurso> OR STATIS ALL
    """
    #Split the command into a list
    command = command.split()
    noArguments=0
    #Check if the command is valid
    if command[0] not in COMMANDS:
        print("UNKNOWN-COMMAND")
        return False
    #Check if the command is SUBSCRIBE
    elif command[0] == "SUBSCR":
        noArguments=3
    else:
        nArguments=2
    if len(command) != noArguments:
        print("MISSING-ARGUMENTS")
        return False
    

        
    

def main():
    """
    Função principal do programa cliente.

    1- Pedir ao utilizador um comando, através da prompt “comando > ”
    2- Ler uma string do utilizador no standard input
    3- Validar o comando fornecido*
    4- Caso o comando pressuponha um pedido ao servidor:
    a. Ligar ao servidor;
    b. Enviar para o servidor o comando respetivo através de uma string com um formato de 
    mensagem específico;
    c. Receber a string de resposta do servidor;
    d. Apresentar a resposta recebida;
    e. Terminar a ligação com o servidor;
    5- Caso o comando seja para processamento local, executá-lo;
    6- Voltar a 1.
    """

    # 1- Pedir ao utilizador um comando, através da prompt “comando > ”
    
    # 2- Ler uma string do utilizador no standard input
    while True:
       command =  input("comando > ")
       if validate_command(command.strip()):# 3- Validar o comando fornecido*
           break
        
    # 4- Caso o comando pressuponha um pedido ao servidor:
    # a. Ligar ao servidor;
    server_connection.connect()
    # b. Enviar para o servidor o comando respetivo através de uma string com um formato de mensagem específico;
    command_args = command.split()
    command = command_args[0]
    if command == "SUBSCR":
        stock_id = command_args[1]
        time_limit = command_args[2]
        message = "SUBSCR " + str(stock_id) + " " + str(time_limit) + " " + str(args.client_id)
    elif command == "CANCEL":
        

        

    # 


        
 
    
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Stock Market Ticker Client")
    parser.add_argument("client_id", help="Client ID", type=int)
    parser.add_argument("server_address", help="Server address")
    parser.add_argument("server_port", help="Server port", type=int)
   
    args = parser.parse_args()
    
    main()
    



    