from os.path import join, basename, exists
import tabula
import calendar
import pandas as pd
import Utils.funcs
import Apoio.tickets
from datetime import datetime

# ===================================================================================================
# Processamento de notas de corretagens corretora "AGORA CORRETORA DE TITULOS E VALORES MOBILIARIOS S/A"
# ===================================================================================================
def agora(corretora,filename,item,log):
    
    #Extraindo os dados das operações na B3
    data = tabula.read_pdf(filename, pandas_options={'dtype': str}, guess=False, stream=True, multiple_tables=True, pages='all', encoding="utf-8", area=((40.556,452.264,58.415,580.249),(126.128,453.008,145.474,578.761),(208.723,35.568,472.878,581.737)))
    df = pd.concat(data,axis=0,ignore_index=True)
    df['Preço / Ajuste'] = df['Preço / Ajuste'].apply(Utils.funcs.sanitiza_moeda).astype('float') 
    df['Valor Operação / Ajuste'] = df['Valor Operação / Ajuste'].apply(Utils.funcs.sanitiza_moeda).astype('float')
    df['Quantidade'] = df['Quantidade'].apply(Utils.funcs.anitiza_moeda).astype('float')
    df['Nr.Nota'] = df['Nr.Nota'].apply(Utils.funcs.sanitiza_moeda).astype('float')
    df['Unnamed: 0'] = Utils.funcs.sanitiza_especificacao_titulo(df['Unnamed: 0'])
    df['Tipo mercado'] = Utils.funcs.sanitiza_especificacao_titulo(df['Tipo mercado'])
    df['Prazo'] = Utils.funcs.sanitiza_especificacao_titulo(df['Prazo'])
    df['Prazo'].fillna("", inplace=True)
    df['Especificação do título'] = df['Especificação do título'] + df['Unnamed: 0']
    df['Obs. (*)'] = Utils.funcs.sanitiza_observacao(df['Obs. (*)'])
    if 'Unnamed: 1' in df.columns:
        df['Unnamed: 1'] = df['Unnamed: 1'].apply(Utils.funcs.sanitiza_moeda).astype('float')
    if 'Unnamed: 2' in df.columns:
        df['Unnamed: 2'] = df['Unnamed: 2'].apply(Utils.funcs.sanitiza_moeda).astype('float')
    if 'Unnamed: 3' in df.columns:
        df['Unnamed: 3'] = df['Unnamed: 3'].apply(Utils.funcs.sanitiza_moeda).astype('float')
    
    #Extraindo os dados das taxas e impostos
    data = tabula.read_pdf(filename, pandas_options={'dtype': str}, guess=False, stream=True, multiple_tables=True, pages='all', encoding="utf-8", area=((40.556,452.264,58.415,580.249),(472.131,35.568,667.086,566.855)))
    df_gastos = pd.concat(data,axis=0,ignore_index=True)
    df_gastos['Nr.Nota'] = df_gastos['Nr.Nota'].apply(Utils.funcs.sanitiza_moeda).astype('float')
    if 'Unnamed: 0' in df_gastos.columns:
        df_gastos['Unnamed: 0'] = df_gastos['Unnamed: 0'].apply(Utils.funcs.sanitiza_moeda).astype('float')
        df_gastos['Unnamed: 0'].fillna(0, inplace=True)
    if 'Unnamed: 1' in df_gastos.columns:
        df_gastos['Unnamed: 1'] = df_gastos['Unnamed: 1'].apply(Utils.funcs.sanitiza_moeda).astype('float')
        df_gastos['Unnamed: 1'].fillna(0, inplace=True)
    if 'Unnamed: 2' in df_gastos.columns:
        df_gastos['Unnamed: 2'] = df_gastos['Unnamed: 2'].apply(Utils.funcs.sanitiza_moeda).astype('float')
        df_gastos['Unnamed: 2'].fillna(0, inplace=True)
    lista = list(df_gastos[df_gastos['Resumo dos Negócios'].str.contains("Valor das operações",na=False)].index)
    note_taxa = []
    
    #Obtem o número da conta na corretora
    conta = tabula.read_pdf(filename, pandas_options={'dtype': str}, guess=False, stream=True, multiple_tables=True, pages='1', encoding="utf-8", area=(144.727,455.017,164.818,539.845))
    conta = pd.concat(conta,axis=0,ignore_index=True)
    conta = conta['Unnamed: 0'].iloc[0].strip().lstrip('0')
    conta = conta.split(' -')[0] + conta.split(' -')[1]
    
    #Verifica se a Nota de Corretagem já foi processada anteriormente
    cpf = str(df['C.P.F./C.N.P.J./C.V.M./C.O.B.'][1])
    nome = conta + '_' + df_gastos['Data pregão'][0][6:10] + '_' + df_gastos['Data pregão'][0][3:5] + '.xlsx'
    current_path = './Resultado/'
    folder_prefix = str(df['C.P.F./C.N.P.J./C.V.M./C.O.B.'][1] + '/' +corretora + '/' + df_gastos['Data pregão'][0][6:10])
    folder_path = join(current_path, folder_prefix)
    if exists(folder_path+'/'+nome):
        log.append(Utils.funcs.verifica_nota_corretagem(folder_path,nome,item))
        Utils.funcs.log_processamento(current_path,cpf,log)
        return()
    
    for current_row in lista:
        nota = df_gastos['Nr.Nota'].iloc[current_row-8]
        data = datetime.strptime(df_gastos['Data pregão'].iloc[current_row-8], '%d/%m/%Y').date()
        total = df_gastos['Unnamed: 0'].iloc[current_row]
        vendas = df_gastos['Unnamed: 0'].iloc[current_row-6]
        if df_gastos['Unnamed: 2'].iloc[current_row-6] > 0:
            liquidacao = df_gastos['Unnamed: 2'].iloc[current_row-5]
            registro = df_gastos['Unnamed: 2'].iloc[current_row-4]
            emolumentos = df_gastos['Unnamed: 2'].iloc[current_row+1]
            corretagem = df_gastos['Unnamed: 2'].iloc[current_row+4] 
            imposto = df_gastos['Unnamed: 2'].iloc[current_row+6]
            irrf = df_gastos['Unnamed: 2'].iloc[current_row+7]
            basecalculo = str(df_gastos['Unnamed: 1'].iloc[current_row+7])
            if basecalculo != "nan":
                basecalculo = float(basecalculo.split("R$")[0])
            else:
                basecalculo = "0"
            outros = df_gastos['Unnamed: 2'].iloc[current_row+8]
            ir_daytrade = str(df_gastos['Resumo dos Negócios'].iloc[current_row+7])
            if ir_daytrade != "nan":
                ir_daytrade = ir_daytrade.split("Projeção R$ ")[1]
            else:
                ir_daytrade = "0"
            ir_daytrade = float(ir_daytrade.replace('.','').replace(',','.'))               
        else:
            liquidacao = df_gastos['Unnamed: 1'].iloc[current_row-5]
            registro = df_gastos['Unnamed: 1'].iloc[current_row-4]
            emolumentos = df_gastos['Unnamed: 1'].iloc[current_row+1]
            corretagem = df_gastos['Unnamed: 1'].iloc[current_row+4]
            imposto = df_gastos['Unnamed: 1'].iloc[current_row+6]
            irrf = 0
            basecalculo = 0
            outros = df_gastos['Unnamed: 1'].iloc[current_row+7]
            ir_daytrade = str(df_gastos['Resumo dos Negócios'].iloc[current_row+6])
            if ir_daytrade != "nan":
                ir_daytrade = ir_daytrade.split("Projeção R$ ")[1]
            else:
                ir_daytrade = "0"
            ir_daytrade = float(ir_daytrade.replace('.','').replace(',','.'))
        row_data = [nota,data,total,vendas,liquidacao,registro,emolumentos,corretagem,imposto,outros,emolumentos+liquidacao+registro,corretagem+imposto+outros,irrf,ir_daytrade,basecalculo]                                        
        note_taxa.append(row_data)
    cols = ['Nota','Data','Total','Vendas','Liquidação','Registro','Emolumentos','Corretagem','Imposto','Outros','Custos_Fin','Custos_Op','IRRF','IR_DT','BaseCalculo']
    taxas_df = pd.DataFrame(data=note_taxa, columns=cols)
    taxas_df = taxas_df.drop_duplicates(subset='Nota', keep='last', ignore_index=True)
     
    cont_notas = len(taxas_df['Nota'])
    if cont_notas > 1:
        log.append('Serão processadas ' + str(cont_notas) + ' notas de corretagens do mercado à vista.\n')
    else:
        log.append('Será processada ' + str(cont_notas) + ' nota de corretagem do mercado à vista.\n')
    
    #Incluir aqui a etapa para obter lista de linhas de cada operação
    operacoes = list(df[df['Negociação'].str.contains("BOVESPA",na=False)].index)
    note_data = []
    numero_nota = 0
    cpf = ''
    nome = ''
    ano = ''
    mes = ''
    temp = ''
    for current_row in operacoes:
        cell_value = df['Nr.Nota'].iloc[current_row-2]
        if cell_value > 0:
            numero_nota = df['Nr.Nota'].iloc[current_row-2]
            data = df['Data pregão'].iloc[current_row-2]
            if ano == '':
                cpf = df['C.P.F./C.N.P.J./C.V.M./C.O.B.'].iloc[current_row-1]
                nome = conta + '_' + data[6:10] + '_' + data[3:5] + '.xlsx'
                ano = data[6:10]
                mes = data[3:5]

            if mes == '':
                mes = data[3:5]

            data = datetime.strptime(df['Data pregão'].iloc[current_row-2], '%d/%m/%Y').date()

        #Tipo de operação (Compra ou Venda)
        c_v = df['C/V'].iloc[current_row].strip()
    
        #Nome do ativo no pregão
        stock_title = df['Especificação do título'].iloc[current_row].strip()

        operacao = df['Obs. (*)'].iloc[current_row]
        if operacao == "D":
            operacao = "DayTrade"
        else:
            operacao = "Normal"
        
        #Tipo de Mercado operado
        if df['Tipo mercado'].iloc[current_row] == "VISTA":
            mercado = "VISTA"
        elif df['Tipo mercado'].iloc[current_row] == "OPCAO DE COMPRA":
            mercado = "CALL"
        elif df['Tipo mercado'].iloc[current_row] == "OPCAO DE VENDA":
            mercado = "PUT"
        elif df['Tipo mercado'].iloc[current_row] == "EXERC OPC VENDA":
            mercado = "EXERC PUT"
        elif df['Tipo mercado'].iloc[current_row] == "EXERC OPC COMPRA":
            mercado = "EXERC CALL"
        else:
            mercado = df['Tipo mercado'].iloc[current_row]
        
        #Prazo de Vencimento da Opção
        if df['Prazo'].iloc[current_row] != "":            
            monthRange = calendar.monthrange(2000 + int(df['Prazo'].iloc[current_row][3:]),int(df['Prazo'].iloc[current_row][0:2]))
            prazo = str(monthRange[1]) +'/' + str(int(df['Prazo'].iloc[current_row][0:2])) + '/' +str(2000 + int(df['Prazo'].iloc[current_row][3:]))
            prazo = datetime.strptime(prazo, '%d/%m/%Y').date()
        elif df['Prazo'].iloc[current_row] != "" and df['Tipo mercado'].iloc[current_row] in "TERMOTermotermo":
            prazo = int(df['Prazo'].iloc[current_row])
        else:
            prazo = ""
        
        #Exercicio de opção de compra/venda
        if df['Tipo mercado'].iloc[current_row].split(" ")[0] == "EXERC":
            exercicio = df['Especificação do título'].iloc[current_row]
            exercicio = exercicio[:-1]
        else:
            exercicio = ""
        
        #Quantidade operada de cada ativo por nota de corretagem
        quantidade = Utils.funcs.quantidade_operada(df['Quantidade'].iloc[current_row],df['Unnamed: 0'].iloc[current_row] if 'Unnamed: 0' in df.columns else 0,df['Unnamed: 1'].iloc[current_row] if 'Unnamed: 1' in df.columns else 0,df['Unnamed: 2'].iloc[current_row] if 'Unnamed: 2' in df.columns else 0)
        
        #Valor total de cada operação por nota de corretagem
        valor_total = Utils.funcs.valor_total_ativo(df['Valor Operação / Ajuste'].iloc[current_row],df['Unnamed: 2'].iloc[current_row] if 'Unnamed: 2' in df.columns else 0 ,df['Unnamed: 1'].iloc[current_row] if 'Unnamed: 1' in df.columns else 0)
 
        # Preço unitário da operação de cada ativo por nota de corretagem
        preco_unitario = valor_total / quantidade
    
        #Dividindo os custos e o IRRF por operação
        custo_financeiro,irrf_operacao = Utils.funcs.custos_por_operacao(taxas_df,numero_nota,c_v,valor_total,operacao)
        
        #Susbstitui o nome do papel no pregão pelo seu respectivo código na B3 no padrão "XXXX3"
        stock_title,log_nome_pregao = Utils.funcs.nome_pregao(Apoio.tickets.acoes, stock_title, data)
        if log_nome_pregao != temp:
            temp = log_nome_pregao
            log.append(log_nome_pregao)
                   
        #Calculando o preço médio de cada operação
        pm = Utils.funcs.preco_medio(c_v,valor_total,custo_financeiro,quantidade)
        
        row_data = [corretora, cpf, numero_nota, data, c_v, stock_title, operacao, preco_unitario, quantidade, valor_total, custo_financeiro, pm, irrf_operacao,mercado,prazo,exercicio]
        note_data.append(row_data)
    cols = ['Corretora','CPF', 'Nota', 'Data', 'C/V', 'Papel', 'Operacao','Preço', 'Quantidade', 'Total', 'Custos_Fin', 'PM', 'IRRF','Mercado','Prazo','Exercicio']
    note_df = pd.DataFrame(data=note_data, columns=cols)
    
    #Agrupar os dados de preço e quantidade por cada ativo comprado/vendido em cada nota de corretagem
    grouped = Utils.funcs.agrupar(note_df)
    grouped = grouped[cols]
    
    # Seleção de papel isento de IR (IRRF e IRPF). Apenas uma operação (um papel) está sendo analisada por NC       
    note_data,log_isencao = Utils.funcs.isencao_imposto_renda(taxas_df,grouped,note_data)
    log.append(log_isencao)
    
    cols = ['Corretora','CPF', 'Nota', 'Data', 'C/V', 'Papel', 'Operacao','Preço', 'Quantidade', 'Total', 'Custos_Fin', 'PM', 'IRRF','Mercado','Prazo','Exercicio']
    note_df = pd.DataFrame(data=note_data, columns=cols)
    
    # Refaz o agrupamento para atulizar os dados de preço e quantidade com a correção de compra/venda a maior no DayTrade
    grouped = Utils.funcs.agrupar(note_df)
    grouped = grouped[cols]
    
    # Agrupa as operações por tipo de operação (Normal ou Daytrade)
    try:
        normal_df,daytrade_df,result = Utils.funcs.agrupar_operacoes(grouped,cols)
        # Insere o valor do IR para as operações de Daytrade"
        note_data,taxas_df,log_daytrade_ir = Utils.funcs.daytrade_ir(result,taxas_df,note_data,grouped)
        log.append(log_daytrade_ir)
        cols = ['Corretora','CPF', 'Nota', 'Data', 'C/V', 'Papel', 'Operacao','Preço', 'Quantidade', 'Total', 'Custos_Fin', 'PM', 'IRRF','Mercado','Prazo','Exercicio']
        note_df = pd.DataFrame(data=note_data, columns=cols)
        # Refaz o agrupamento para atualizar os dados de preço e quantidade por cada ativo comprado/vendido 
        grouped = Utils.funcs.agrupar(note_df)
        grouped = grouped[cols]
    except ValueError:
        Utils.funcs.agrupar_operacoes(grouped,cols)
        #normal_df,daytrade_df = agrupar_operacoes(grouped,cols)
       
    # Acrescentando os custos operacionais (Corretagem, Imposto e Outros)
    grouped = Utils.funcs.custos_operacionais(grouped,taxas_df)
    
    # Obtendo o valor correto do preço unitário de cada operação 
    grouped['Preço'] = grouped['Total'] / grouped['Quantidade']
    
    # Obtendo o valor correto do preço médio de cada operação
    grouped['PM'] = Utils.funcs.preco_medio_correcao(grouped)
    
    # Inseri o número da conta na corretora
    grouped.insert(2,"Conta",int(conta),True)
    taxas_df.insert(0,"Conta",int(conta),True)
    
    # Agrupa as operações por tipo de trade com correção de compra/venda a maior no DayTrade 
    normal_df,daytrade_df = Utils.funcs.agrupar_operacoes_correcao(grouped,cols)
    cols = ['Corretora','CPF','Conta','Nota', 'Data', 'C/V', 'Papel','Mercado','Preço', 'Quantidade', 'Total', 'Custos_Fin', 'PM', 'IRRF','Prazo','Exercicio']
    if normal_df.empty == False:
        normal_df = normal_df[cols]
    if daytrade_df.empty == False:
        daytrade_df = daytrade_df[cols]  
    
    # Cria o caminho completo de pastas/subpasta para salvar o resultado do processamento
    current_path = './Resultado/'
    folder_prefix = cpf+'/'+corretora+'/'+ano
    folder_path = join(current_path, folder_prefix)
    log_move_resultado,pagebmf = Utils.funcs.move_resultado(folder_path,cpf,nome,item,pagebmf=0)
    log.append(log_move_resultado)
    
    # Disponibiliza os dados coletados em um arquivo .xlsx separado por mês
    Utils.funcs.arquivo_separado(folder_path,nome,note_df,normal_df,daytrade_df,taxas_df)
    
    # Disponibiliza todos os dados coletados de todos os arquivos processados em um único arquivo
    Utils.funcs.arquivo_unico(current_path,cpf,note_df,normal_df,daytrade_df,taxas_df)

    # Cria o caminho completo de pastas/subpastas para mover os arquivos já processados.
    log_move_saida = Utils.funcs.move_saida(cpf,corretora,ano,mes,item)
    log.append(log_move_saida)

    # Cria um arquivo de LOG para armazenar os dados do processamento
    log.append('Todas as Notas de Corretagem contidadas no arquivo "'+basename(item)+'" foram processadas com sucesso.\n')
    Utils.funcs.log_processamento(current_path,cpf,log)