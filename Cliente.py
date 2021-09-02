#!/usr/bin/python
# encoding: utf-8
# python version: 3.3
# filename: cliente.py
# author: igor

import socket
import random

if __name__ == '__main__':

	print ('\n==================================\n')
	print ('\nBalanceamento de Carga - Cliente\n')

	nome = random.randint(1, 10)

	udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	servidor = ('localhost', 4573)

	msg = str(nome)
	#msg.encode('utf-8')
	udp.sendto (bytes(msg.encode('utf-8')), servidor)

	print ('Pronto para processar !')

	i = 0
	while 1:
		minimo, enderecoServidor = udp.recvfrom(1024) # recebe informacoes do servidor
		maximo, enderecoServidor = udp.recvfrom(1024)
		if str(minimo.decode('utf-8')) == 'fecha': # se nao houver mais informacoes sai do laco
			break
		i = i + 1
		minimo = int(minimo.decode('utf-8'))
		maximo = int(maximo.decode('utf-8'))
		soma = 0;
		print ('\nCliente ', nome, 'processando... ', i, 'vez.\n')
		while minimo <= maximo:
			soma = soma + minimo
			minimo = minimo + 1
		udp.sendto(bytes(str(soma).encode('utf-8')), servidor) # envia somatorio para servidor
	udp.close() # encerra a conexao
