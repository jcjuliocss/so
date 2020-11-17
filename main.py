import os
import threading

class GerenciadorTarefas(threading.Thread):
	def __init__(self):
		self.pid = os.getpid()
		self.lock = threading.Lock()
		threading.Thread.__init__(self)

	def run(self):
		while True:
			print('[ 1 ] Fazer login\n[ 2 ] Cadastrar usuario\n[ 3 ] Sair')
			inp = input()
			if int(inp) == 1:
				nome_login = input('Digite seu nome: ')
				senha_login = input('Digite sua senha: ')

				self.lock.acquire()
				try:
					f = open('usuarios.txt', 'r')
					usuarios = f.readlines()
					f.close()
					if [nome_login, senha_login] in [usuario.replace('\n', '').split('-') for usuario in usuarios]:
						print("Login valido!")
					else:
						print("Login invalido!")
						continue
				finally:
					self.lock.release()
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