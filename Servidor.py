#!/usr/bin/python
# encoding: utf-8
# python version: 3.3
# filename: servidor.py
# author: igor

import socket

class Mestre:
	listaPortasClientes = []
	soma = fatia = numeroProcessar = numeroEscravos = 0
	udp = None
	servidor = None

	def inicializar(self):
		self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		self.servidor = ('localhost', 4573)

		self.udp.bind(self.servidor)

	def fechar(self):
		self.udp.close()

	def esperaEscravos(self):
		i=0;
		while i < int(self.numeroEscravos):
			msg, enderecoCliente = self.udp.recvfrom(1024)
			print ('Cliente ', str(msg.decode('utf-8')) ,' conectado !')
			self.listaPortasClientes.append(enderecoCliente)
			i = i + 1

	def distribuifatias(self):
		i = 0
		numeroMinimo = 0
		numeroMaximo = self.fatia

		while i < int(self.numeroEscravos): # envia primeira processamento a todos
			self.udp.sendto (bytes(str(numeroMinimo).encode('utf-8')), self.listaPortasClientes[i])
			self.udp.sendto (bytes(str(numeroMaximo).encode('utf-8')), self.listaPortasClientes[i])
			numeroMinimo = numeroMaximo + 1
			numeroMaximo = numeroMaximo + self.fatia
			
			i = i + 1;
		# Agora balanceia a carga
		self.soma = 0
		while numeroMinimo < int(self.numeroProcessar):  ## enquanto houver fatias disponiveis
			self.somaAux, enderecoCliente = self.udp.recvfrom(1024) # recebe o somatorio e o endereco do cliente
			self.soma += int(self.somaAux.decode('utf-8')) # soma no total
			self.udp.sendto (bytes(str(numeroMinimo).encode('utf-8')), enderecoCliente) # envia mais carga para o cliente
			self.udp.sendto (bytes(str(numeroMaximo).encode('utf-8')), enderecoCliente)
			numeroMinimo = numeroMaximo + 1
			numeroMaximo = numeroMaximo + self.fatia;
			
			if numeroMaximo > int(self.numeroProcessar):
				numeroMaximo = int(self.numeroProcessar)
		i = 0
		# soma a parte dos que ficaram por ultimo processando
		msg = 'fecha'
		while i < int(self.numeroEscravos):
			self.somaAux, enderecoCliente = self.udp.recvfrom(1024)
			self.soma += int(self.somaAux.decode('utf-8'))
			i = i + 1
			self.udp.sendto(bytes(msg.encode('utf-8')),enderecoCliente)
			self.udp.sendto(bytes(msg.encode('utf-8')),enderecoCliente)

	def calculafatias(self):
		if int(self.numeroEscravos) % 2 == 0: # se for par a quantidade de escravos
			self.fatia = int(int(self.numeroProcessar) / (int(self.numeroEscravos) * 4)) # multiplica a qtd de servidores por 4
		else:
			self.fatia = int(int( int(self.numeroProcessar)) / ((int(self.numeroEscravos)+1) * 4)) # soma + 1 e multiplica, para dรก sempre PAR o pedaco

if __name__ == '__main__':

	mestre = Mestre()

	mestre.inicializar()

	print ('\n==================================\n')
	print ('\nBalanceamento de Carga - Servidor\n')

	print ('Digite o numero de clientes: ')
	mestre.numeroEscravos = input()

	print ('\nAguardando clientes...')

	mestre.esperaEscravos()

	while int(mestre.numeroProcessar) < int(mestre.numeroEscravos):
		print ('\nNumero para processar: ')
		mestre.numeroProcessar = input()

	mestre.calculafatias()

	mestre.distribuifatias()

	print ('\nprocessando...\n')

	print ('\nsomatorio: ',mestre.soma)
	print ('\n==================================\n')

	mestre.fechar()
