import os
import threading
import subprocess

class GerenciadorTarefas(threading.Thread):
	def __init__(self):
		self.pid = os.getpid()
		self.lock = threading.Lock()
		threading.Thread.__init__(self)

	def run(self):
		while True:
			print('---------- GERENCIADOR DE TAREFAS ----------')
			print('[ 1 ] Fazer login\n[ 2 ] Cadastrar usuario\n[ 3 ] Sair')
			inp = input()
			if int(inp) == 1:
				nome_login = input('Digite seu nome: ')
				senha_login = input('Digite sua senha: ')

				self.lock.acquire()
				try:
					login = subprocess.run('./fazer_login.sh ' + str(nome_login) + ' ' + str(senha_login), text=True, capture_output=True, shell=True)
					if int(login.returncode) == 1:
						print("Login valido!")
					else:
						print("Login invalido!")
						continue
				finally:
					self.lock.release()

				finaliza_sessao = False
				while not finaliza_sessao:
					print('---------- Ola, {}! ----------'.format(nome_login))
					print('[ 1 ] Adicionar tarefa\n[ 2 ] Listar tarefas\n[ 3 ] Sair')
					inp = input()
					if int(inp) == 1:
						tarefa = input('Insira a tarefa: ')

						self.lock.acquire()
						try:
							f = open('tarefas.txt', 'a')
							f.write(str(tarefa) + '\n')
							f.close()
							print('Tarefa cadastrada com sucesso!')
							continue
						finally:
							self.lock.release()
							pass
					elif int(inp) == 2:
						self.lock.acquire()
						try:
							tarefas = subprocess.run('./buscar_tarefas.sh ', text=True, capture_output=True, shell=True)
							print(tarefas.stdout)
						finally:
							self.lock.release()
							pass
					else:
						finaliza_sessao = True

			elif int(inp) == 2:
				login_valido = False
				while not login_valido:
					self.lock.acquire()
					try:
						nome = input('Nome: ')
						senha = input('Digite a senha: ')
						senha_verifica = input('Digite novamente a senha: ')

						if not nome:
							print('Nome não pode ser vazio!')
						elif senha != senha_verifica:
							print('Senhas não são iguais!')
						else:
							f = open('usuarios.txt', 'a')
							f.write(str(nome) + '-' + str(senha) + '\n')
							f.close()
							print('Usuario cadastrado com sucesso!')
							login_valido = True
					finally:
						self.lock.release()
			else:
				os.system('kill -9 ' + str(self.pid))
				break

gerenciador = GerenciadorTarefas()
gerenciador.start()
