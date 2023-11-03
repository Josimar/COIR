import pandas as pd

#filds  = ['Taxa de liquidação' , 'Taxa de Registro' , 'Total CBLC' , 'Taxa de termo/opções','Taxa ANA' , 'Emolumentos' , 'Taxa Operacional' , 'Taxa de Custódia' , 'Outros']
#cods  = {'ON' : '3' , 'PN' : '4' , 'PNA' : '5' , 'PNB' : '6' , 'PNC' : '7' , 'UNT' : '11'}
#Tipo mercado (OPCAO DE COMPRA|OPCAO DE VENDA|EXERC OPC VENDA|VISTA|FRACIONARIO|TERMO)

# ===================================================================================================
# Arquivo CSV contendo o nome dos papeis no pregão da B3
# ATENÇÃO: Para cada NOVO papel, incluir o nome correto no PREGÃO e o CÓDIGO correspondente na B3
# ===================================================================================================
# acoes = pd.read_csv('./Apoio/acoes.csv')

# ===================================================================================================
# Códigos dos ativos á vista da Bolsa de valores brasileira
# {'ON' : '3' , 'PN' : '4' , 'PNA' : '5' , 'PNB' : '6' , 'PNC' : '7' , 'UNT' : '11'}
# ===================================================================================================
codigos  = { 'ON' : '3' , 'PN' : '4' , 'PNA' : '5' , 'PNB' : '6' , 'PNC' : '7' , 'UNT' : '11' }

# ===================================================================================================
# Há duas possibilidades de implementação. Buscando em um arquivo csv ou incorporando essas informações
# no próprio script python, conforme implementado a seguir. 
# Analisar qual a melhor abordagem.
# ===================================================================================================
''' Atualizado em 21/09/2023'''
acoes = pd.DataFrame(data=(
    ['3M','MMMC34'],
    ),
    columns=['TICKET','CODIGO'])

# ===================================================================================================
# Arquivo contendo o nome dos ativos que compoem o índice Bovespa
# ===================================================================================================
''' Atualizado em 31/01/2023'''
opcoes = pd.DataFrame(data=(
    ['ABEV','ABEV3'],
    ['ALPA','ALPA4'],
    ['ALSO','ALSO3'],
    ['ARZZ','ARZZ3'],
    ['ASAI','ASAI3'],
    ['AZUL','AZUL4'],
    ['B3SA','B3SA3'],
    ['BBAS','BBAS3'],
    ['BBDC','BBDC3'],
    ['BBDC','BBDC4'],
    ['BBSE','BBSE3'],
    ['BEEF','BEEF3'],
    ['BHIA','BHIA3'],
    ['BPAC','BPAC11'],
    ['BPAN','BPAN4'],
    ['BRAP','BRAP4'],
    ['BRFS','BRFS3'],
    ['BRKM','BRKM5'],
    ['CASH','CASH3'],
    ['CCRO','CCRO3'],
    ['CIEL','CIEL3'],
    ['CMIG','CMIG4'],
    ['CMIN','CMIN3'],
    ['COGN','COGN3'],
    ['CPFE','CPFE3'],
    ['CPLE','CPLE6'],
    ['CRFB','CRFB3'],
    ['CSAN','CSAN3'],
    ['CSNA','CSNA3'],
    ['CVCB','CVCB3'],
    ['CYRE','CYRE3'],
    ['DXCO','DXCO3'],
    ['ECOR','ECOR3'],
    ['EGIE','EGIE3'],
    ['ELET','ELET3'],
    ['ELET','ELET6'],
    ['EMBR','EMBR3'],
    ['ENBR','ENBR3'],
    ['ENEV','ENEV3'],
    ['ENGI','ENGI11'],
    ['EQTL','EQTL3'],
    ['EZTC','EZTC3'],
    ['FLRY','FLRY3'],
    ['GGBR','GGBR4'],
    ['GOAU','GOAU4'],
    ['GOLL','GOLL4'],
    ['HAPV','HAPV3'],
    ['HYPE','HYPE3'],
    ['IGTI','IGTI11'],
    ['ITSA','ITSA4'],
    ['ITUB','ITUB4'],
    ['JBSS','JBSS3'],
    ['KLBN','KLBN11'],
    ['LREN','LREN3'],
    ['LWSA','LWSA3'],
    ['MGLU','MGLU3'],
    ['MRFG','MRFG3'],
    ['MRVE','MRVE3'],
    ['MULT','MULT3'],
    ['NTCO','NTCO3'],
    ['PCAR','PCAR3'],
    ['PETR','PETR3'],
    ['PETR','PETR4'],
    ['PETZ','PETZ3'],
    ['PRIO','PRIO3'],
    ['PSSA','PSSA3'],
    ['QUAL','QUAL3'],
    ['RADL','RADL3'],
    ['RAIL','RAIL3'],
    ['RAIZ','RAIZ4'],
    ['RDOR','RDOR3'],
    ['RENT','RENT3'],
    ['RRRP','RRRP3'],
    ['SANB','SANB11'],
    ['SBSP','SBSP3'],
    ['SLCE','SLCE3'],
    ['SMTO','SMTO3'],
    ['SOMA','SOMA3'],
    ['SUZB','SUZB3'],
    ['TAEE','TAEE11'],
    ['TASA','TASA4'],
    ['TIMS','TIMS3'],
    ['TOTS','TOTS3'],
    ['UGPA','UGPA3'],
    ['USIM','USIM5'],
    ['VALE','VALE3'],
    ['VBBR','VBBR3'],
    ['VIIA','VIIA3'],
    ['VIVT','VIVT3'],
    ['WEGE','WEGE3'],
    ['YDUQ','YDUQ3']
    ),
    columns=['TICKET','CODIGO'])

# ===================================================================================================
# Arquivo contendo o nome das principais Corretoras B3
# ATENÇÃO: Para NOVA corretora incluir o nome completo e o código no arquivo /Apoio/Corretoras.csv
# ===================================================================================================
#corretoras_cadastradas = pd.read_csv('./Apoio/Corretoras.csv')

# ===================================================================================================
# Há duas possibilidades de implementação. Buscando em um arquivo csv ou incorporando essas informações
# no próprio script python, conforme implementado a seguir. Analisar qual a melhor aboradagem.
# ===================================================================================================
''' Atualizado em 31/01/2022'''
corretoras_cadastradas = pd.DataFrame(data=(
    ['3','XP INVESTIMENTOS CCTVM S/A','XP'],
    ['386','RICO INVESTIMENTOS - GRUPO XP','RICO'],
    ['90','EASYNVEST - TITULO CV S.A.','EASYNVEST'],
    ['308','CLEAR CORRETORA - GRUPO XP','CLEAR'],
    ['85','BTG PACTUAL CTVM S.A.','BTG'],
    ['72','BRADESCO S/A CTVM','BRADESCO'],
    ['39','AGORA CTVM S/A','AGORA'],
    ['39','AGORA CORRETORA DE TITULOS E VALORES MOBILIARIOS S/A','AGORA'],
    ['3701','ORAMA DTVM S.A.','ORAMA'],
    ['735','ICAP DO BRASIL CTVM LTDA','ICAP'],
    ['120','GENIAL INSTITUCIONAL CCTVM S.A','GENIAL'],
    ['173','GENIAL INVESTIMENTOS CVM S.A.','GENIAL'],
    ['93','NOVA FUTURA CTVM LTDA','NOVA FUTURA'],
    ['107','TERRA INVESTIMENTOS DTVM LTDA','TERRA'],
    ['6003','C6 CTVM LTDA','C6'],
    ['1982','MODAL DTVM LTDA','MODAL'],
    ['683','BANCO MODAL','MODAL'],
    ['4090','TORO CTVM LTDA.','TORO'],
    ['1099','INTER DTVM LTDA','INTER'],
    ['15','GUIDE INVESTIMENTOS S.A. CV','GUIDE'],
    ['114','ITAU CV S/A','ITAU'],
    ['820','BB BANCO DE INVESTIMENTO S/A','BB'],
    ['713','BB GESTAO DE RECURSOS DTVM S/A','BB'],
    ['147','ATIVA INVESTIMENTOS S.A. CTCV','ATIVA'],
    ['1618','IDEAL CTVM SA','IDEAL'],
    ['172','BANRISUL S/A CVMC','BANRISUL'],
    ['442','BANCO OURINVEST','OURINVEST'],
    ['359','BANCO DAYCOVAL','DAYCOVAL'],
    ['1116','BANCO CITIBANK','CITIBANK'],
    ['251','BANCO BNP PARIBAS BRASIL S/A','BNP'],
    ['4','ALFA CCVM S.A.','ALFA'],
    ['979','ADVALOR DTVM LTDA','ADVALOR'],
    ['226','AMARIL FRANKLIN CTV LTDA.','AMARIL'],
    ['4002','BANCO ANDBANK (BRASIL) S.A.','ANDBANK'],
    ['3112','BANESTES DTVM S/A','BANESTES'],
    ['2197','BCO FIBRA','FIBRA'],
    ['122','BGC LIQUIDEZ DTVM','BGC'],
    ['18','BOCOM BBM CCVM S/A','BOCOM'],
    ['4015','BS2 DTVM S/A','BS2'],
    ['1570','CAIXA ECONOMICA FEDERAL','CEF'],
    ['77','CITIGROUP GMB CCTVM S.A.','CITIGROUP'],
    ['88','CM CAPITAL MARKETS CCTVM LTDA','CM CAPITAL'],
    ['234','CODEPE CV E CAMBIO S/A','CODEPE'],
    ['74','COINVALORES CCVM LTDA.','COINVALORES'],
    ['186','CORRETORA GERAL DE VC LTDA','GERAL'],
    ['45','CREDIT SUISSE BRASIL S.A. CTVM','CREDIT SUISSE'],
    ['133','DIBRAN DTVM LTDA','DIBRAN'],
    ['711','DILLON S.A. DTVM','DILLON'],
    ['174','ELITE CCVM LTDA.','ELITE'],
    ['131','FATOR S.A. CV','FATOR'],
    ['238','GOLDMAN SACHS DO BRASIL CTVM','GOLDMAN'],
    ['115','H.COMMCOR DTVM LTDA','H.COMMCOR'],
    ['41','ING CCT S/A','ING'],
    ['1130','INTL FCSTONE DTVM LTDA.','INTL'],
    ['16','J. P. MORGAN CCVM S.A.','J. P. MORGAN'],
    ['33','LEROSA S.A. CVC','LEROSA'],
    ['2640','LLA DTVM LTDA','LLA'],
    ['1','MAGLIANO S.A. CCVM','MAGLIANO'],
    ['83','MAXIMA S/A CTVM','MAXIMA'],
    ['106','MERC. DO BRASIL COR. S.A. CTVM','MERC.'],
    ['13','MERRILL LYNCH S/A CTVM','MERRILL'],
    ['262','MIRAE ASSET WEALTH MANAGEMENT','MIRAE'],
    ['40','MORGAN STANLEY CTVM S/A','MORGAN'],
    ['181','MUNDINVEST S.A. CCVM','MUNDINVEST'],
    ['23','NECTON INVESTIMENTOS S.A. CVMC','NECTON'],
    ['63','NOVINVEST CVM LTDA.','NOVINVEST'],
    ['2379','ORLA DTVM S/A','ORLA'],
    ['1106','OURINVEST DTVM S.A.','Ourinvest'],
    ['129','PLANNER CV S.A','PLANNER'],
    ['2492','POSITIVA CTVM S/A','POSITIVA'],
    ['1089','RB CAPITAL INVESTIMENTOS DTVM','RB CAPITAL'],
    ['92','RENASCENCA DTVM LTDA.','RENASCENCA'],
    ['3371','RIO BRAVO INVEST S.A. DTVM','RIO BRAVO'],
    ['3762','RJI CTVM LTDA','RJI'],
    ['59','SAFRA CVC LTDA.','SAFRA'],
    ['27','SANTANDER CCVM S/A','SANTANDER'],
    ['2570','SANTANDER SECURITIES SERVICES','SANTANDER'],
    ['191','SENSO CCVM S.A.','SENSO'],
    ['187','SITA SCCVM S.A.','SITA'],
    ['110','SLW CVC LTDA.','SLW'],
    ['58','SOCOPA SC PAULISTA S.A.','SOCOPA'],
    ['177','SOLIDUS S/A CCVM','SOLIDUS'],
    ['127','TULLETT PREBON','TULLETT'],
    ['8','UBS BRASIL CCTVM S/A','UBS'],
    ['37','UM INVESTIMENTOS S.A. CTVM','UM INVESTIMENTOS'],
    ['29','UNILETRA CCTVM S.A.','UNILETRA'],
    ['21','VOTORANTIM ASSET MANAG. DTVM','VOTORANTIM']
    ),
    columns=['Codigo','Corretora','Nome'])