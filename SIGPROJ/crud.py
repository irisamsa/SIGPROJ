 # -*- coding: utf-8 -*-

from easygui import multenterbox, msgbox, passwordbox, choicebox, buttonbox, textbox
from peewee import *

#=======================================================================
# BANCO DE DADOS
#=======================================================================

from peewee import Expression # the building block for expressions

OP_MOD = 'mod'
OP_REGEXP = 'regexp'

def mod(lhs, rhs):
    return Expression(lhs, OP_MOD, rhs)

def regexp(lhs, rhs):
    return Expression(lhs, OP_REGEXP, rhs)

SqliteDatabase.register_ops({OP_MOD: '%', OP_REGEXP: 'REGEXP'})

db = SqliteDatabase('sgpp.db', threadlocals=True)

#=======================================================================
# TABELAS
#=======================================================================

class MPesquisador(Model):
    nome = CharField()
    telefone = CharField()
    endereco = CharField()
    email = CharField()
    curriculo = CharField()

    class Meta: 
		database = db

class MBolsista(Model):
    nome = CharField()
    telefone = CharField()
    endereco = CharField()
    email = CharField()
    curriculo = CharField()

    class Meta: 
		database = db

class MProjeto(Model):
	titulo = CharField()
	coordenador = CharField()
	resumo = CharField()
	keywords = CharField()
	inicio = CharField()
	final = CharField()

	class Meta: 
		database = db
		
class MEdital(Model):
	titulo = CharField()
	ano = CharField()

	class Meta:
		database = db

class MPublicacao(Model):
	referencia = CharField()
	tipo = CharField()
	ano = CharField()

	class Meta:
		database = db
	
class MGrupo(Model):
	nome = CharField()

	class Meta:
		database = db
	
class MParticipante(Model):
	projeto = CharField()
	participante = CharField()
		
	class Meta:
		database = db
	

#=======================================================================
# FUNCOES AUXILIARES
#=======================================================================
import unicodedata

def remover_acentos(s):
	if isinstance(s, unicode):
		return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c)  != 'Mn'))
	else:
		return s
     
def array_to_ascii(lista):
	for i in range(len(lista)):
		lista[0] = remover_acentos(lista[0])
	return lista

#=======================================================================
# FUNCOES DO SISTEMA
#=======================================================================
title = "SISTEMA DE GESTAO DE PROJETOS DE PESQUISA (SIGPROJ)"

def login():

	msg = "Entre com a senha para acesso."
	for i in range(3):
		senha = passwordbox(msg, title, default='', image=None, root=None)
		if senha == "pesquisa@2015": return True
		else: 
			msgbox(msg="Senha Incorreta! Tente novamente.", title=title, ok_button='Continuar', image=None, root=None)
	return False


#=======================================================================
# Edital
#=======================================================================

def cadastrar_edital():
	title = "Edital - Cadastrar"
	msg = "Entre com os dados do edital."
	fieldNames = ["Titulo: ", "Ano: "]
	fieldValues = []
	fieldValues = multenterbox(msg, title, fieldNames)
	
	while 1:
		if fieldValues ==  None: break
		errmsg = ""
		for i in range(len(fieldNames)):
			if fieldValues[i].strip() == "":
				errmsg = errmsg + ('"%" e um campo requisido. \n\n' % fieldNames[i])
			if errmsg == "": break #no problems found
			fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
			
		if fieldValues == None:
			return
		else:
			#Tira acentos
			fieldValues = array_to_ascii(fieldValues)
			
			#Converte para maiśuculo o título do edital
			fieldValues[0] = fieldValues[0].upper()
			edital = MEdital.create(titulo = fieldValues[0], ano = fieldValues[1])
			edital.save()
			msgbox(" Edital:  " + fieldValues[0] + "cadastrado com sucesso", title = title, ok_button ='Continuar', image= None, root = None)
		return
			
def editar_edital():
	editais = [x.titulo for x in MEdital.select().order_by(MEdital.titulo)]
	
	msg ="Selecione um edital para editar."
	title = "Edital - Editar"
	edital = choicebox(msg, title, editais)
	
	if edital == None: return
	
	edital = MEdital.get(MEdital.titulo == edital)
	
	msg ="Entre com as alteracoes."
	fieldNames = ["Titulo: ","Ano: "]
	fieldValues = [edital.titulo, edital.ano]
	
	fieldValues = multenterbox(msg, title, fieldNames, fieldValues)
	
	if fieldValues == None: return
	
	#Tira acentos
	fieldValues = array_to_ascii(fieldValues)
		
	#Converte para Maiúsculo o Nome do Pesquisador
	fieldValues[0] = fieldValues[0].upper()
	
	edital.titulo = fieldValues[0]
	edital.ano = fieldValues[1]
	edital.save()
	msgbox(msg="Edital: " + fieldValues[0] + " atualizado(a) com sucesso!", title=title, ok_button='Continuar', image=None, root=None)

	return

#=======================================================================
# Pesquisador
#=======================================================================
def cadastrar_pesquisador():
	title = "Cadastrar Pesquisador"
	msg = "Entre com os dados do(a) pesquisador(a)."
	fieldNames = ["Nome Completo: ","Telefone: ","Endereco: ","E-mail: ", "Mini-CV: "]
	fieldValues = []
	fieldValues = multenterbox(msg, title, fieldNames)
	
	while 1:
		if fieldValues == None: break
		errmsg = ""
		for i in range(len(fieldNames)):
		  if fieldValues[i].strip() == "":
			errmsg = errmsg + ('"%s" e um campo requisido.\n\n' % fieldNames[i])
		if errmsg == "": break # no problems found
		fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
	
	if fieldValues == None: 
		return
	else:
		#Tira acentos
		fieldValues = array_to_ascii(fieldValues)
		
		#Converte para Maiúsculo o Nome do Pesquisador
		fieldValues[0] = fieldValues[0].upper()
		
		pesquisador = MPesquisador.create(nome=fieldValues[0], telefone=fieldValues[1], endereco=fieldValues[2], email=fieldValues[3], curriculo=fieldValues[4])
		pesquisador.save()
		msgbox(msg="Pesquisador(a): " + fieldValues[0] + " cadastrado(a) com sucesso!", title=title, ok_button='Continuar', image=None, root=None)
	return

def editar_pesquisador():
	pesquisadores = [x.nome for x in MPesquisador.select().order_by(MPesquisador.nome)]
	
	msg ="Selecione um(a) pesquisador(a) para editar."
	title = "Pesquisador - Editar"
	pesquisador = choicebox(msg, title, pesquisadores)
	
	if pesquisador == None: return
	
	pesquisador = MPesquisador.get(MPesquisador.nome == pesquisador)
	
	msg ="Entre com as alteracoes."
	fieldNames = ["Nome Completo: ","Telefone: ","Endereco: ","E-mail: ", "Mini-CV: "]
	fieldValues = [pesquisador.nome, pesquisador.telefone, pesquisador.endereco, pesquisador.email, pesquisador.curriculo]
	
	fieldValues = multenterbox(msg, title, fieldNames, fieldValues)
	
	if fieldValues == None: return
	
	#Tira acentos
	fieldValues = array_to_ascii(fieldValues)
		
	#Converte para Maiúsculo o Nome do Pesquisador
	fieldValues[0] = fieldValues[0].upper()
	
	pesquisador.nome = fieldValues[0]
	pesquisador.telefone = fieldValues[1]
	pesquisador.endereco = fieldValues[2]
	pesquisador.email = fieldValues[3]
	pesquisador.curriculo = fieldValues[4]
	pesquisador.save()
	msgbox(msg="Pesquisador(a): " + fieldValues[0] + " atualizado(a) com sucesso!", title=title, ok_button='Continuar', image=None, root=None)

	return

#=======================================================================
# Bolsista
#=======================================================================
def cadastrar_bolsista():
	title = "Cadastrar Bolsista"
	msg = "Entre com os dados do(a) Bolsista: "
	fieldNames = ["Nome Completo: ","Telefone: ","Endereco: ","E-mail: ", "Mini-CV: "]
	fieldValues = []
	fieldValues = multenterbox(msg, title, fieldNames)
	
	while 1:
		if fieldValues == None: break
		errmsg = ""
		for i in range(len(fieldNames)):
		  if fieldValues[i].strip() == "":
			errmsg = errmsg + ('"%s" e um campo requisido.\n\n' % fieldNames[i])
		if errmsg == "": break # no problems found
		fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
	
	if fieldValues == None: 
		return
	else:
		#Tira acentos
		fieldValues = array_to_ascii(fieldValues)
		
		#Converte para Maiúsculo o Nome do Pesquisador
		fieldValues[0] = fieldValues[0].upper()
		
		bolsista = MBolsista.create(nome=fieldValues[0], telefone=fieldValues[1], endereco=fieldValues[2], email=fieldValues[3], curriculo=fieldValues[4])
		bolsista.save()
		msgbox(msg="Bolsista: " + fieldValues[0] + " cadastrado(a) com sucesso!", title=title, ok_button='Continuar', image=None, root=None)
	return

def editar_bolsista():
	bolsistas = [x.nome for x in MBolsista.select().order_by(MBolsista.nome)]
	
	msg ="Selecione um(a) bolsista para editar."
	title = "Bolsista - Editar"
	bolsista = choicebox(msg, title, bolsistas)
	
	if bolsista == None: return
	
	bolsista = MBolsista.get(MBolsista.nome == bolsista)
	
	msg ="Entre com as alteracoes."
	fieldNames = ["Nome Completo: ","Telefone: ","Endereco: ","E-mail: ", "Mini-CV: "]
	fieldValues = [bolsista.nome, bolsista.telefone, bolsista.endereco, bolsista.email, bolsista.curriculo]
	
	fieldValues = multenterbox(msg, title, fieldNames, fieldValues)
	
	if fieldValues == None: return
	
	#Tira acentos
	fieldValues = array_to_ascii(fieldValues)
		
	#Converte para Maiúsculo o Nome do Pesquisador
	fieldValues[0] = fieldValues[0].upper()
	
	bolsista.nome = fieldValues[0]
	bolsista.telefone = fieldValues[1]
	bolsista.endereco = fieldValues[2]
	bolsista.email = fieldValues[3]
	bolsista.curriculo = fieldValues[4]
	bolsista.save()
	msgbox(msg="Bolsista: " + fieldValues[0] + " atualizado(a) com sucesso!", title=title, ok_button='Continuar', image=None, root=None)

	return
#=======================================================================
# GRUPO
#=======================================================================

def cadastrar_grupo():
	title = "Cadastrar Grupo"
	msg = "Entre com os dados do grupo: "
	fieldNames = ["Nome: "]
	fieldValues = []
	fieldValues = multenterbox(msg, title, fieldNames)
	
	while 1:
		if fieldValues == None: break
		errmsg = ""
		for i in range(len(fieldNames)):
		  if fieldValues[i].strip() == "":
			errmsg = errmsg + ('"%s" e um campo requisido.\n\n' % fieldNames[i])
		if errmsg == "": break # no problems found
		fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
	
	if fieldValues == None: 
		return
	else:
		#Tira acentos
		fieldValues = array_to_ascii(fieldValues)
		
		#Converte para Maiúsculo o Nome do Pesquisador
		fieldValues[0] = fieldValues[0].upper()
		
		grupo = MGrupo.create(nome=fieldValues[0])
		grupo.save()
		msgbox(msg="Grupo: " + fieldValues[0] + " cadastrado(a) com sucesso!", title=title, ok_button='Continuar', image=None, root=None)
	return
	
def editar_grupo():
	
	grupos = [x.nome for x in MGrupo.select().order_by(MGrupo.nome)]
	
	msg ="Selecione um grupo para editar."
	title = "Grupo - Editar"
	grupo = choicebox(msg, title, grupos)
	
	if grupo == None: return
	
	grupo = MBolsista.get(MBolsista.nome == bolsista)
	
	msg ="Entre com as alteracoes."
	fieldNames = ["Nome: "]
	fieldValues = [grupo.nome]
	
	fieldValues = multenterbox(msg, title, fieldNames, fieldValues)
	
	if fieldValues == None: return
	
	#Tira acentos
	fieldValues = array_to_ascii(fieldValues)
		
	#Converte para Maiúsculo o Nome do Grupo
	fieldValues[0] = fieldValues[0].upper()
	
	grupo.nome = fieldValues[0]
	grupo.save()
	msgbox(msg="Grupo: " + fieldValues[0] + " atualizado(a) com sucesso!", title=title, ok_button='Continuar', image=None, root=None)

	return
	
def adicionar_participante_grupo():
	title = "Grupo - Adicionar Participante"
	
	# Pergunta se o participante eh Pesquisador ou Bolsista
	msg = "Selecione o tipo de Participante: "
	choices = ["Pesquisador","Bolsista","Cancelar"]
	reply = buttonbox(msg, title, choices=choices)
	
	if reply == "Pesquisador":
		
		pesquisadores = [x.nome for x in MPesquisador.select().order_by(MPesquisador.nome)]
		
		msg = "Selecione um(a) Pesquisador(a) para adicionar como Parcipante ao grupo:"
		
		pesquisador = choicebox(msg, title, pesquisadores)
	
		if pesquisador == None: return
		
		grupos = [x.nome for x in MGrupo.select().order_by(MGrupo.nome)]
		
		msg ="Selecione o grupo para adicionar o(a) Pesquisador(a) como participante:"
		title = "Grupo - Adicionar Participante"
		grupo = choicebox(msg, title, grupos)
		
		if grupo == None: return
		
		participante = MParticipante.create(grupo=grupo, participante=pesquisador)
		participante.save()
		
		msgbox(msg="O(A) Pesquisador(a): " + pesquisador + " agora participa no grupo: " + grupo + ".", title=title, ok_button='Continuar', image=None, root=None)
	
	if reply == "Bolsista":
		
		bolsistas = [x.nome for x in MBolsista.select().order_by(MBolsista.nome)]
		
		msg = "Selecione um(a) Bolsista para adicionar como parcipante do grupo:"
		
		bolsista = choicebox(msg, title, bolsistas)
	
		if bolsista == None: return
		
		grupos = [x.nome for x in MGrupo.select().order_by(MGrupo.nome)]
		
		msg ="Selecione o grupo para adicionar o(a) Bolsista como participante:"
		title = "Grupo - Adicionar Participante"
		grupo = choicebox(msg, title, grupos)
		
		if projeto == None: return
		
		participante = MParticipante.create(grupo=grupo, participante=bolsista)
		participante.save()
		
		msgbox(msg="O(A) Bolsista: " + bolsista + " agora participa no grupo: " + grupo + ".", title=title, ok_button='Continuar', image=None, root=None)
	
	if reply == "Cancelar": return
		
	return 
def remover_participante_grupo():
	
	title = "Grupo - Remover Participante"
	
	grupos = [x.nome for x in MGrupo.select().order_by(MGrupo.nome)]
	
	msg ="Selecione o grupo para remover participante:"
	
	grupo = choicebox(msg, title, grupos)
	
	if grupo == None: return
		
	participantes = [x.participante for x in MParticipante.select().where(MParticipante.grupo == grupo).order_by(MParticipante.participante)]
	
	msg = "Selecione o(a) participante a ser removido do grupo:"
	
	participante = choicebox(msg, title, participantes)
	
	if participante == None: return
	
	participante = MParticipante.get(MParticipante.participante == participante)
	
	print participante 
	
	participante.delete_instance()

	msgbox(msg=participante.participante + " nao mais participa do " + grupo + ".", title=title, ok_button='Continuar', image=None, root=None)

	
	return	
	
#=======================================================================
# Projeto
#=======================================================================
def cadastrar_projeto():
	
	# SEMELHANTE A LINHA ABAIXO.
	#pesquisadores = []
	#for x in MPesquisador.select().order_by(MPesquisador.nome):
	#	pesquisadores.append(x.nome)
	
	pesquisadores = [x.nome for x in MPesquisador.select().order_by(MPesquisador.nome)]
	
	msg ="Selecione o(a) Coordenador(a) do Projeto."
	title = "Cadastro de Projeto"
	coordenador = choicebox(msg, title, pesquisadores)

	if coordenador == None: return

	msg = "Entre com os dados do Projeto: "
	fieldNames = ["Titulo: ","Resumo: ","Palavras-chave: ", "Ano de Início: ", "Ano de Término: "]
	fieldValues = []
	fieldValues = multenterbox(msg, title, fieldNames)
	
	while 1:
		if fieldValues == None: break
		errmsg = ""
		for i in range(len(fieldNames)):
		  if fieldValues[i].strip() == "":
			errmsg = errmsg + ('"%s" e um campo requisido.\n\n' % fieldNames[i])
		if errmsg == "": break # no problems found
		fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
	
	if fieldValues == None: 
		return
	else:
		#Tira acentos
		fieldValues = array_to_ascii(fieldValues)
		
		#Converte para Maiúsculo o Titulo do Projeto
		fieldValues[0] = fieldValues[0].upper()
		
		projeto = MProjeto.create(titulo=fieldValues[0], coordenador=coordenador, resumo=fieldValues[1], keywords=fieldValues[2], inicio=fieldValues[3], final=fieldValues[4])
		projeto.save()
		msgbox(msg="Projeto: " + fieldValues[0] + " cadastrado com sucesso!", title=title, ok_button='Continuar', image=None, root=None)
	return


def editar_projeto():
	projetos = [x.titulo for x in MProjeto.select().order_by(MProjeto.titulo)]
	
	msg ="Selecione um projeto para editar."
	title = "Projeto - Editar"
	projeto = choicebox(msg, title, projetos)
	
	if projeto == None: return
	
	projeto = MProjeto.get(MProjeto.titulo == projeto)
	
	msg ="Entre com as alteracoes."
	fieldNames = ["Titulo: ","Coordenador: ", "Resumo: ", "Palavras-chave: ", "Ano de Início: ", "Ano de Término: "]
	fieldValues = [projeto.titulo, projeto.coordenador, projeto.resumo, projeto.keywords, projeto.inicio, projeto.final]
	
	fieldValues = multenterbox(msg, title, fieldNames, fieldValues)
	
	if fieldValues == None: return 
	
	#Tira acentos
	fieldValues = array_to_ascii(fieldValues)
		
	#Converte para Maiúsculo o Nome do Pesquisador
	fieldValues[0] = fieldValues[0].upper()
	
	projeto.titulo = fieldValues[0]
	projeto.coordenador = fieldValues[1]
	projeto.resumo = fieldValues[2]
	projeto.keywords = fieldValues[3]
	projeto.inicio = fieldValues[4]
	projeto.final = fieldValues[5]
	projeto.save()
	msgbox(msg="Projeto: " + fieldValues[0] + " atualizado com sucesso!", title=title, ok_button='Continuar', image=None, root=None)

	return
#=======================================================================
# Participante
#=======================================================================
def adicionar_participante():
	title = "Projeto - Adicionar Participante"
	
	# Pergunta se o participante eh Pesquisador ou Bolsista
	msg = "Selecione o tipo de Participante: "
	choices = ["Pesquisador","Bolsista","Cancelar"]
	reply = buttonbox(msg, title, choices=choices)
	
	if reply == "Pesquisador":
		
		pesquisadores = [x.nome for x in MPesquisador.select().order_by(MPesquisador.nome)]
		
		msg = "Selecione um(a) Pesquisador(a) para adicionar como Parcipante ao projeto:"
		
		pesquisador = choicebox(msg, title, pesquisadores)
	
		if pesquisador == None: return
		
		projetos = [x.titulo for x in MProjeto.select().order_by(MProjeto.titulo)]
		
		msg ="Selecione o projeto para adicionar o(a) Pesquisador(a) como participante:"
		title = "Projeto - Adicionar Participante"
		projeto = choicebox(msg, title, projetos)
		
		if projeto == None: return
		
		participante = MParticipante.create(projeto=projeto, participante=pesquisador)
		participante.save()
		
		msgbox(msg="O(A) Pesquisador(a): " + pesquisador + " agora participa no projeto: " + projeto + ".", title=title, ok_button='Continuar', image=None, root=None)
	
	if reply == "Bolsista":
		
		bolsistas = [x.nome for x in MBolsista.select().order_by(MBolsista.nome)]
		
		msg = "Selecione um(a) Bolsista para adicionar como parcipante ao projeto:"
		
		bolsista = choicebox(msg, title, bolsistas)
	
		if bolsista == None: return
		
		projetos = [x.titulo for x in MProjeto.select().order_by(MProjeto.titulo)]
		
		msg ="Selecione o projeto para adicionar o(a) Bolsista como participante:"
		title = "Projeto - Adicionar Participante"
		projeto = choicebox(msg, title, projetos)
		
		if projeto == None: return
		
		participante = MParticipante.create(projeto=projeto, participante=bolsista)
		participante.save()
		
		msgbox(msg="O(A) Bolsista: " + bolsista + " agora participa no projeto: " + projeto + ".", title=title, ok_button='Continuar', image=None, root=None)
	
	if reply == "Cancelar": return
		
	return 

def remover_participante():
	
	title = "Projeto - Remover Participante"
	
	projetos = [x.titulo for x in MProjeto.select().order_by(MProjeto.titulo)]
	
	msg ="Selecione o projeto para remover participante:"
	
	projeto = choicebox(msg, title, projetos)
	
	if projeto == None: return
		
	participantes = [x.participante for x in MParticipante.select().where(MParticipante.projeto == projeto).order_by(MParticipante.participante)]
	
	msg = "Selecione o(a) participante a ser removido do projeto:"
	
	participante = choicebox(msg, title, participantes)
	
	if participante == None: return
	
	participante = MParticipante.get(MParticipante.participante == participante)
	
	print participante 
	
	participante.delete_instance()

	msgbox(msg=participante.participante + " nao mais participa do " + projeto + ".", title=title, ok_button='Continuar', image=None, root=None)

	
	return	

#=======================================================================
# Publicacao
#=======================================================================
	
def cadastrar_publicacao():
	pass
def editar_publicacao():
	pass

#=======================================================================
# Relatorios
#=======================================================================
def relatorio_projeto():
	projetos = [x.titulo for x in MProjeto.select().order_by(MProjeto.titulo)]
	
	msg ="Selecione o projeto para gerar o relatório."
	title = "Relatório - Projeto"
	projeto = choicebox(msg, title, projetos)
	
	if projeto == None: return
	
	projeto = MProjeto.get(MProjeto.titulo == projeto)
	
	relatorio = "Titulo: " + projeto.titulo + "\n\n"
	relatorio += "Coordenador: " + projeto.coordenador + "\n\n"
	relatorio += "Resumo: " + projeto.resumo + "\n\n"
	relatorio += "Palavras-chave: " + projeto.keywords + "\n\n"	
	
	participantes = [x.participante for x in MParticipante.select().where(MParticipante.projeto == projeto.titulo).order_by(MParticipante.participante)]
	
	if participantes:
		relatorio += "Participantes: \n"
		for i in participantes: 
			relatorio +=  i + "\n"
		relatorio += "\n\n"	
	
	textbox("Relatório de Projeto", "Relatorio - Projeto", (relatorio))
	
	return
	

def menu():
	question="Selecione a opcao desejada: "
	choices = [
	"Edital - Cadastrar",
	"Edital - Editar",
	"Pesquisador - Cadastrar", 
	"Pesquisador - Editar",
	"Bolsista - Cadastrar",
	"Bolsista - Editar", 
	"Grupo de Pesquisa - Cadastrar",
	"Grupo de Pesquisa - Editar",
	"Grupo de Pesquisa - Adicionar Participante",
	"Grupo de Pesquisa - Remover Participante",
	"Projeto - Cadastrar", 
	"Projeto - Editar", 
	"Projeto - Adicionar Participante", 
	"Projeto - Remover Participante",
	"Publicacao - Cadastrar",
	"Publicacao - Editar",
	"Relatorio - Pesquisador",
	"Relatorio - Pesquisadores", 
	"Relatorio - Projeto", 
	"Relatorio - Projetos",
	"Configuracoes", 
	"Sair do Sistema"]
	
	while 1: 
		opcao = choicebox(question, title, choices);
		print opcao
		
		if opcao == "Edital - Cadastrar":
			cadastrar_edital()
		
		if opcao == "Edital - Editar":
			editar_edital()
			pass
		
		if opcao == "Pesquisador - Cadastrar":
			cadastrar_pesquisador()
		
		if opcao == "Pesquisador - Editar":
			editar_pesquisador()
		
		if opcao == "Bolsista - Cadastrar":
			cadastrar_bolsista()
		
		if opcao == "Bolsista - Editar":
			editar_bolsista()

		if opcao == "Grupo de Pesquisa - Cadastrar":
			cadastrar_grupo()
			pass
			
		if opcao == "Grupo de Pesquisa - Editar":
			editar_grupo()
			pass
		
		if opcao == "Grupo de Pesquisa - Adicionar Participante":
			adicionar_participante_grupo()
			pass
						
		if opcao == "Grupo de Pesquisa - Remover Participante":
			remover_participante_grupo()
			pass

		if opcao == "Projeto - Cadastrar":
			cadastrar_projeto()
			
		if opcao == "Projeto - Editar":
			editar_projeto()
		
		if opcao == "Projeto - Adicionar Participante":
			adicionar_participante()
						
		if opcao == "Projeto - Remover Participante":
			remover_participante()
		
		if opcao == "Publicacao - Cadastrar":
			cadastrar_publicacao()
			
		
		if opcao == "Publicacao - Editar":
			editar_pesquisador()
		
	
	# =======================================================	
	# Os relatorios nao serao implementados agora
	# Daqui para baixo, nao e necessario implementar.
	# =======================================================
		
		if opcao == "Relatorio - Pesquisador":
			pass
		
		if opcao == "Relatorio - Pesquisadores":
			pass
			
		if opcao == "Relatorio - Projeto":
			relatorio_projeto()
		
		if opcao == "Relatorio - Projetos":
			pass
		
		if opcao == "Configuracoes":
			pass
			
		if opcao == None or opcao == "Sair do Sistema":
			return
	
def tela_inicial():
	image = "ifce.jpeg"
	msg = "SISTEMA DE GESTAO DE PROJETOS DE PESQUISA\n\nTecle 'enter' para continuar."
	choices = ["Continuar..."]
	reply = buttonbox(msg, image=image, choices=choices)

if __name__ == "__main__":
	#=======================================================================
	# Sempre que modificar alguma tabela do banco: 
	# 1. Apagar o arquivo "sgpp.db"
	# 2. Descomentar as linhas abaixo, para criar o banco de dados novamente
	# OBS: Depois que o banco de dados (sgpp.db) for criado, as linhas abaixo devem ser comentadas novamente. 
	#MPesquisador.create_table()
	#MProjeto.create_table()
	#MParticipante.create_table()
	#MBolsista.create_table()
	#MEdital.create_table()
	#MPublicacao.create_table()
	#MGrupo.create_table()
	#=======================================================================
	
	menu()
	
	#=======================================================================
	# Descomentar as linhas abaixo, e comentar a linha acima, 
	# 	caso queira uma tela de login
	# OBS: Esta tosco!
	#=======================================================================
	
	#tela_inicial()
	#if login() == True:
	#	menu()
	#else:
	#	exit

