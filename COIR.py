# -*- coding: utf-8 -*-
#
# ===== PYTHON 3 ======
#
# ===================================================================================================
# Script para extração e exportação dos dados contidos nas Notas de Corretagem no padrão SINACOR
# Os dados extraídos são inseridos em planilhas excel
# O atual scritp foi testado nas corretoras BTG, XP, Rico e Agora
# Para outras corretoras favor enviar notas de corretagem para implementação
# ------
# Para dúvidas e sugestões entrar em contato pelo e-mail: marcelo.pcf@gmail.com
# Última atualização em 25/10/2023
# ===================================================================================================
import Utils.funcs
from os.path import isfile, join, basename, exists
import sys
import re
from datetime import datetime
from icecream import ic

# Corretoras
import Corretoras.btg
import Corretoras.agora
import Corretoras.toro
import Corretoras.btg_bmf
import Corretoras.xp_rico_clear
import Corretoras.xp_rico_clear_bmf
import Corretoras.unknown

# ====================================================================================================
# MELHORIAS FUTURAS NO SCRIPT - Analisar a criação de VARIÁVEIS GLOBAIS nessa área.
# ====================================================================================================
# Colcar aqui as futuras melhorias

#Docstrings
"""
 - docstrings - 
- ajuda a detalhar as funcionalidades de cada função
logo abaixo da declação da função
def teste():
    -> O que a função faz
    :param X: é isso
    :param y: faz isso
    Função criada por marcelo.pcf@gmail.com
help(teste)
""" 

# ====================================================================================================
# Verifica se está rodando versão correta do Python
# ====================================================================================================
if sys.version_info <= (3, 0):
    sys.stdout.write("Versao do intepretador python (" + str(platform.python_version()) + ") inadequada.\n")
    sys.stdout.write("Este programa requer Python 3 (preferencialmente Python 3.9.2 ou superior).\n")
    sys.exit(1)

# ===================================================================================================
# Carga de módulos opcionais
# ===================================================================================================
def instalar_modulo(modulo):
    # Comando para instalar módulos
    import subprocess
    comando = sys.executable + " -m" + " pip" + " install " + modulo
    print("-"*100)
    print("- O módulo", modulo,"não vem embutido na instalação do python e necessita de instalação específica.")
    print("- Instalando módulo opcional: ", modulo, "Aguarde....")
    subprocess.call([sys.executable, "-m", "pip", "install", modulo])
    if modulo == 'tabula-py':
        modulo = 'tabula'
    try:
        __import__(modulo)
    except ImportError as e:
        print("- Erro: Instalação de Módulo adicional", modulo, "falhou: " + str(e))
        print("- Para efetar uma instalação manual, conecte este computador na internet e utilize o comando abaixo")
        print(comando)
        input("- Digite <ENTER> para prosseguir")
        sys.exit(1)
    return comando

# ===================================================================================================
# Lista de modulos opcionais
# ATENÇÃO: PARA CADA MÓDULO NOVO, INCLUIR AS DUAS LINHAS, com a definição da váriavel modulo e o import
# ===================================================================================================
modulo = ''   
try:
    modulo='pandas'
    import  pandas
except ImportError as e:
    print("-"*100)
    print(str(e))
    comando=instalar_modulo(modulo)
    
try:
    modulo='openpyxl'
    import  openpyxl
except ImportError as e:
    print("-"*100)
    print(str(e))
    comando=instalar_modulo(modulo)
    
try:
    modulo='xlwings'
    import  xlwings
except ImportError as e:
    print("-"*100)
    print(str(e))
    comando=instalar_modulo(modulo)
    
try:
    modulo='tabula-py'
    import tabula
except ImportError as e:
    print("-"*100)
    print(str(e))
    comando=instalar_modulo(modulo)

### Por enquanto não são necessários
# Talvez precise mais tarde
#
#try:
#    modulo='shutil' - Já importado
#    import  shutil
#except ImportError as e:
#    print("-"*100)
#    print(str(e))
#    comando=instalar_modulo(modulo)
#
#try:
#    modulo='et-xmlfile'
#    import  et-xmlfile
#except ImportError as e:
#    print("-"*100)
#    print(str(e))
#    comando=instalar_modulo(modulo)
#
# try:
#     modulo='cryptography'
#     import cryptography
# except ImportError as e:
#     print("-"*100)
#     print(str(e))
#     comando=instalar_modulo(modulo)
#
# try:
#     modulo='python-dateutil'
#     import python-dateutil
# except ImportError as e:
#     print("-"*100)
#     print(str(e))
#     comando=instalar_modulo(modulo)
# try:
#     modulo='scipy'
#     import  scipy
# except ImportError as e:
#     print("-"*100)
#     print(str(e))
#     comando=instalar_modulo(modulo)
#
# try:
#     modulo='numpy'
#     import  numpy
# except ImportError as e:
#     print("-"*100)
#     print(str(e))
#     comando=instalar_modulo(modulo)
#
# try:
#     modulo='sklearn'
#     import  sklearn
# except ImportError as e:
#     print("-"*100)
#     print(str(e))
#     comando=instalar_modulo(modulo)

#Simula um erro de instalção de módulo
#try:
#    modulo='xxxxxxx'
#    import  xxxxxxx
#except ImportError as e:
#    print("-"*100)
#    print(str(e))
#    comando=instalar_modulo(modulo)

# ===================================================================================================
# Modulos necessários para execução correta do script de extração de dados das Notas de Corretagem
# ATENÇÃO: Esses modulos serão instalados automaticamente, 
#          caso não estejam instalados na primeira execução do script.
# ===================================================================================================
from tabula import read_pdf 
import pandas as pd

# unicode box drawing characteres
'''
┌ ┐
└ ┘
─
│
┴
├ ┤
┬
╷
'┼'
'''

# ===================================================================================================
# Padrão de leitura dos arquivos PDF's contendo as Notas de Corretagem no padrão SINANCOR
# ===================================================================================================
#col1str = {'dtype': str}
col1str = {'header': None}
kwargs = {
        'multiple_tables':False,
        'encoding': 'utf-8',
        'pandas_options': col1str,
        'stream':True,
        'guess':False
}

#rxcountpages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE|re.DOTALL)
#def count_pages(filename):
#    data = file(filename,"rb").read()
#    return len(rxcountpages.findall(data))
#

# ===================================================================================================
#                  Módulo principal - SISTEMA DE CONTROLE DE OPERAÇÕES E IRPF
#    Leitura, análise, extração, formatação e conversão das Notas de Corretagem no padrão SINANCOR
# ---------------------------------------------------------------------------------------------------
# Controle de arquivos que não foram processados durante a execução do script
# São arquivos que permanecerão na pasta ./Entrada após a execução do script
# ===================================================================================================
def extracao_nota_corretagem(path_origem='./Entrada/', ext='pdf'):
    from os import listdir
    resposta = ''
    for item in [join(path_origem, f) for f in listdir(path_origem) if isfile(join(path_origem, f)) and f.endswith(ext)]:
        filename = item
        log = []

        #Validação de notas de corretagem no padrão Sinacor
        try:        
            validacao = tabula.read_pdf(filename, pandas_options={'header': None}, guess=False, stream=True, multiple_tables=False, pages='1', silent=True, encoding="utf-8", area=(1.116,0.372,68.797,447.366)) #- BTG
            df_validacao = pd.concat(validacao,axis=1,ignore_index=True)
            df_validacao = pd.DataFrame({'NotaCorretagem': df_validacao[0].unique()})
            cell_value = df_validacao['NotaCorretagem'].iloc[0]
            # conta_value = df_validacao['NotaCorretagem'].iloc[1]
            conta_value = ""
            #ic(validacao, df_validacao, cell_value, conta_value)
            if cell_value == 'NOTA DE NEGOCIAÇÃO' or cell_value == 'NOTA DE CORRETAGEM' or (conta_value == "Conta: 947437"):
                print('processando o arquivo:',basename(item))
                log.append(datetime.today().strftime('%d/%m/%Y %H:%M:%S') + ' - Processando o arquivo "' + basename(item) + '"\n')
            else:
                Utils.funcs.print_atencao()
                print('\033[0;3340mO arquivo {} NÃO é uma NOTA de Corretagem no Padrão Sinacor {}\033[m'.format(basename(item).upper(), '\n'))
                continue
        except ValueError:
            Utils.funcs.print_atencao()
            print('\033[0;3340mO arquivo {} NÃO é uma NOTA de Corretagem no Padrão Sinacor {}\033[m'.format(basename(item).upper(), '\n'))
            continue

        #Validação de Corretoras cadastradas e implementadas, e corretoras não validadas
        corretora = tabula.read_pdf(filename, pandas_options={'dtype': str}, guess=False, stream=True, multiple_tables=True, pages='all', encoding="utf-8", area=(2.603,26.609,214.572,561.903))#BTG
        df_corretora = pd.concat(corretora,axis=0,ignore_index=True)
        corretora = tabula.read_pdf(filename, pages='1', **kwargs, area=(2.603,26.609,214.572,561.903))
        
        try:
            if (conta_value == "Conta: 947437"): # testando Corretora Toro, é muito diferente das outras
                Corretoras.toro.toro("Toro",filename,item,log, 'all')
            else:    
                control,corretora,cell_value = Utils.funcs.valida_corretora(corretora)
                if control == 0:
                    print('Corretora',cell_value, 'não implementada','\n')
                    continue
                elif corretora in 'XPxpRICOricoCLEARclear' and control == 1:
                    lista_acoes = list(df_corretora[df_corretora['NOTA DE NEGOCIAÇÃO'].str.contains(cell_value,na=False)].index)
                    lista_bmf = list(df_corretora[df_corretora['Unnamed: 0'].str.contains(cell_value,na=False)].index)
                    n1 = len(lista_acoes)
                    n2 = len(lista_bmf)
                    if n2 >= 1:
                        page_acoes = ('1'+'-'+str(n1))
                        page_bmf = (str(int(n1+1))+'-'+str(int(n1+n2)))
                        Corretoras.xp_rico_clear.xp_rico_clear(corretora,filename,item,log,page_acoes,page_bmf,control)
                    else:
                        Corretoras.xp_rico_clear.xp_rico_clear(corretora,filename,item,log,'all')
                elif corretora in 'XPxpRICOricoCLEARclear' and control == 2:
                    Corretoras.xp_rico_clear_bmf.xp_rico_clear_bmf(corretora,filename,item,log,'all',control=2)
                elif corretora in 'AGORAagora' and control == 1:
                    Corretoras.agora.agora(corretora,filename,item,log)
                elif corretora in 'BTGbtg' and control == 1:
                    Corretoras.btg.btg(corretora,filename,item,log,'all',control=1)
                elif corretora in 'BTGbtg' and control == 2:
                    Corretoras.btg_bmf.btg_bmf(corretora,filename,item,log,'all',control=2)
                elif corretora in 'TOROTorotoro' and control == 1:
                    Corretoras.toro.toro(corretora,filename,item,log,'all',control=1)
                elif control == 1:
                    print()
                    print(f'A corretora {corretora} ainda não foi validada.')
                    print('Não há notas de corretagens suficientes para testá-la e implementá-la.')
                    print('Todavia, será extraída com uma rotina de teste.')
                    print('Dessa forma, Erros e inconsistência podem ocorrer durante o processamento.')
                    print('-=' * 50)
                    print()
                    if resposta == '':
                        while resposta not in 'SsNn':
                            resposta = str(input('Deseja realmente continuar [S/N]: '))
                    if resposta in 'Ss':
                        Corretoras.unknown.corretora_nao_validada(corretora, filename,item,log)
                    else:
                        continue
        except ValueError as e:
            print(e)
            print('ValueError - Corretora ',cell_value, 'ocorreu erro durante o processamento das notas de corretagens','\n')
            continue

# ===================================================================================================
# Mensagem de alerta para os aplicativos abertos do excel              
# O sistema continuará após a confirmação do uauário
# ===================================================================================================
def principal():
    print()
    print('-=' * 50)
    print(f'{"SISTEMA DE CONTROLE DE OPERAÇÕES E IRPF - COIR":^100}')
    print(f'{"Leitura, Análise, Extração, Formatação e Conversão das Notas de Corretagem no padrão SINACOR":^100}')
    print('-=' * 50)
    print()
    excel_fechado = ' '
    Utils.funcs.print_atencao()
    print('Feche todos os documentos do Excel antes de iniciar o processamento das Notas de Corretagens.')
    print('Isso evitará erros e inconsistênica durante o processamento.\n')
    while excel_fechado not in 'SsNn':
        excel_fechado = str(input('O programa Excel está fechado [S/N]? ')).upper().strip()[0]
    if excel_fechado in 'Ss':
        print()
        print('-=' * 50)
        print('Iniciando o processamento das Notas de Corretagens...\n\n')
        extracao_nota_corretagem()

if __name__ == '__main__':
    principal()

print('-=' * 50)    
print('Fim do processamento!','\n')
input('Pressione qualquer tecla para concluir.\n')