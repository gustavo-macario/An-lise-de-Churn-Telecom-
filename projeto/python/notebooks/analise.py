# %%
import pandas as pd

# %%
df = pd.read_csv('../data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
df.head()


# %%
# 2.1 Perfil de quem cancelou x quem ficou
# Comparar média, mediana e desvio padrão de MonthlyCharges e tenure entre os dois grupos de Churn.
# Os grupos se comportam de forma diferente? Em algum deles a média se afasta muito da mediana?
# R: Sim, existe uma diferença relevante entre os grupos. Quem cancelou tem uma média de permanência de aproximadamente 18 meses, contra 38 meses de quem continua. Também dá para perceber uma diferença maior entre média e mediana no grupo que cancelou, principalmente no tenure, com quase 8 meses de diferença, indicando uma possível assimetria nos dados.
estats = df.copy()
estats = estats.groupby('Churn').agg(
    media_charges=('MonthlyCharges', 'mean'),
    mediana_charges=('MonthlyCharges', 'median'),
    dp_charges=('MonthlyCharges', 'std'),
    media_tenure=('tenure', 'mean'),
    mediana_tenure=('tenure', 'median'),
    dp_tenure=('tenure', 'std')
)
estats


# %%
# 2.2 Valores extremos nas cobranças
# Aplicar o método do IQR em MonthlyCharges e TotalCharges para procurar outliers.
# Se aparecerem, são mais prováveis de ser erro de cadastro ou cliente legítimo (muito tempo de casa, plano caro)?
# R: Aplicando o método do IQR com os limites de 1,5 × IQR, não foram encontrados outliers em MonthlyCharges nem em TotalCharges. Portanto, não há valores extremos nessas variáveis que precisem ser investigados como possíveis erros de cadastro.
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

q1 = df[['MonthlyCharges','TotalCharges']].quantile(0.25)
q3 = df[['MonthlyCharges', 'TotalCharges']].quantile(0.75)

iqr = q3 - q1

limite_inferior = q1 - 1.5 * iqr
limite_superior = q3 + 1.5 * iqr

outliers = (
    (df['MonthlyCharges'] < limite_inferior['MonthlyCharges']) |
    (df['MonthlyCharges'] > limite_superior['MonthlyCharges']) |
    (df['TotalCharges'] < limite_inferior['TotalCharges']) |
    (df['TotalCharges'] > limite_superior['TotalCharges'])
)

df[outliers]


# %%
# 2.3 Relação do churn com tempo de casa e mensalidade
# Transformar Churn em 0/1 e calcular a correlação dele com tenure e MonthlyCharges.
# O que o sinal e a força de cada correlação indicam sobre quem cancela?
# R: O tempo de permanência (tenure) é o fator com maior relação com o cancelamento. Por ter correlação negativa moderada (-0,35), os clientes mais antigos tendem a cancelar menos. Já o valor cobrado mensalmente (MonthlyCharges) possui uma correlação positiva fraca (0,19), indicando que mensalidades mais altas apresentam uma leve tendência a aumentar o churn.
cor = df.copy()
cor['Churn'] = cor['Churn'].map({'No':0, 'Yes':1})

cor = cor[['Churn', 'MonthlyCharges', 'tenure']].corr()[['Churn']]
cor


# %%
# 2.4 Grupo de maior risco
# Isolar os clientes com contrato mensal, até 12 meses de casa e sem suporte técnico.
# Qual a taxa de churn desse grupo comparada à da base inteira, e a diferença justifica uma ação de retenção direcionada?
# R: O grupo de risco (contrato mensal, até 12 meses de casa e sem suporte técnico) tem 1363 clientes, e 61% deles cancelaram, contra 26,5% da base total de 7043 clientes. É mais que o dobro da taxa geral, então vale uma ação de retenção focada nesse perfil. Esse resultado mostra que a combinação dos três fatores concentra muito cancelamento, mas ainda não dá pra dizer quanto disso vem só da falta de suporte, porque ele é um dos filtros do grupo.
seg = df.copy()
seg = seg[(seg['Contract'] == 'Month-to-month') & (seg['tenure'] <= 12) & (seg['TechSupport'] == 'No')].copy()
seg['Churn'] = seg['Churn'].map({'No': 0, 'Yes': 1})
taxa_seg = seg['Churn'].mean() * 100.0
df['Churn_bin'] = df['Churn'].map({'No': 0, 'Yes': 1})
taxa_geral = df['Churn_bin'].mean() * 100.0
print(taxa_seg, taxa_geral)


# %%
# 2.5 Conferência por outro caminho
# Refazer em SQL o cálculo do grupo de risco da 2.4 e comparar com o resultado do Pandas.
# R: Refiz a segmentação de risco (contrato mensal, até 12 meses de casa e sem suporte técnico) no MySQL. O resultado foi igual ao do Pandas: 1363 clientes no grupo, com taxa de churn de 61%, contra 26,5% da base total.
# select 
# count(*) as qtde_clientes,
# round(100.0 * avg((case when Churn = 'Yes' then 1 else 0 end)), 2) as seg_taxa,
# (select round(100.0 * avg((case when Churn = 'Yes' then 1 else 0 end)), 2) from clientes) as taxa_total
# from clientes c
# where c.Contract = 'Month-to-month' and c.tenure <= 12 and c.TechSupport = 'No'


# %%
# 2.6 Resumos para o Excel
# Calcular a taxa de churn e a quantidade de clientes por tipo de contrato, forma de pagamento e faixa de tempo de casa.
# Exportar os três resumos e a base limpa em CSV, para montar a tabela dinâmica e os gráficos no Excel.
df['faixa_tenure'] = pd.cut(
    df['tenure'],
    bins=[0, 12, 24, 72],
    labels=['0-12 meses', '13-24 meses', '25+ meses'],
    include_lowest=True
)
csv_taxas = df.groupby('PaymentMethod').agg(
    taxa=('Churn_bin', 'mean'),
    qtde_clientes=('Churn_bin', 'count')
).reset_index()
csv_taxas['taxa'] = round(csv_taxas['taxa'] * 100.0, 2)


csv_taxas_tenure = df.groupby('faixa_tenure', observed=True).agg(
    taxa=('Churn_bin', 'mean'),
    qtde_clientes=('Churn_bin', 'count')
).reset_index()
csv_taxas_tenure['taxa'] = round(csv_taxas_tenure['taxa'] * 100.0, 2)
csv_taxas_tenure


csv_taxas_contract = df.groupby('Contract').agg(
    taxa=('Churn_bin', 'mean'),
    qtde_clientes=('Churn_bin', 'count')
).reset_index()
csv_taxas_contract['taxa'] = round(csv_taxas_contract['taxa'] * 100.0, 2)


# %%
# Exportação dos arquivos
csv_taxas.to_csv('../data/resumo_pagamento.csv', index=False)
csv_taxas_tenure.to_csv('../data/resumo_tenure.csv', index=False)
csv_taxas_contract.to_csv('../data/resumo_contrato.csv', index=False)
df.to_csv('../data/clientes_limpo.csv', index=False)