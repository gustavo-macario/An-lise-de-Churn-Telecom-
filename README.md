# Análise de Churn em Telecom

Projeto de estudo onde analisei uma base de clientes de uma empresa de telecom para entender quem cancela o serviço e por quê. Usei MySQL para limpar e explorar os dados, Python (Pandas) para a parte estatística e Excel para montar a tabela dinâmica e os gráficos.

## Sobre os dados

Base Telco Customer Churn (Kaggle), com 7043 clientes. Cada linha é um cliente, com informações como tipo de contrato, tempo de casa (tenure), forma de pagamento, valor da mensalidade e se ele cancelou ou não (Churn).

## O que eu quis responder

* Qual a taxa geral de churn?
* Quem cancela mais, clientes novos ou antigos?
* O tipo de contrato e a forma de pagamento mudam o churn?
* Existe um grupo de clientes com risco bem maior que o resto?

## Ferramentas

* MySQL Workbench (limpeza e consultas)
* Python com Pandas, rodando no VS Code
* Excel (tabela dinâmica e gráficos)

## Como o projeto foi feito

**1. SQL:** conferi a qualidade dos dados e calculei a taxa de churn geral e por grupo. Na coluna TotalCharges tinha 11 linhas com valor vazio (todas de clientes com tenure 0), então tratei isso antes de analisar.

**2. Python:** calculei média, mediana e desvio padrão por grupo, procurei outliers com IQR (não encontrei), testei a correlação do churn com tempo de casa e mensalidade e montei uma segmentação de risco. Também refiz essa segmentação em SQL para conferir se os resultados batiam, e bateram. No fim exportei resumos em CSV para usar no Excel.

**3. Excel:** montei tabelas dinâmicas e três gráficos (churn por contrato, por tempo de casa e por forma de pagamento), além de uma aba de resumo com as conclusões.

## O que eu encontrei

* A taxa geral de churn é de 26,5%.
* O contrato mensal cancela 43%, o anual 11% e o de 2 anos 3%.
* Quem tem de 0 a 12 meses de casa cancela 47%, contra 14% de quem tem mais de 25 meses.
* Quem paga com cheque eletrônico cancela 45%, bem acima das outras formas de pagamento (entre 15% e 19%).
* O grupo de maior risco (contrato mensal, até 12 meses de casa e sem suporte técnico) tem 1363 clientes e 61% de churn, mais que o dobro da média.

