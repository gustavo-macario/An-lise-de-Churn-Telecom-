-- 1.1 - Qualidade dos dados

-- Verificando a existência de linhas duplicadas com base no customerID.
-- Nenhuma duplicata foi encontrada.
WITH checagem AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY customerID
               ORDER BY customerID
           ) AS rn
    FROM clientes
)
SELECT *
FROM checagem
WHERE rn > 1;


-- Verificando valores nulos nas principais colunas.
-- Nenhum valor nulo foi encontrado nas colunas verificadas.
SELECT
    SUM(CASE WHEN gender IS NULL THEN 1 ELSE 0 END) AS nulos_gender,
    SUM(CASE WHEN tenure IS NULL THEN 1 ELSE 0 END) AS nulos_tenure,
    SUM(CASE WHEN PaymentMethod IS NULL THEN 1 ELSE 0 END) AS nulos_paymentmethod,
    SUM(CASE WHEN MonthlyCharges IS NULL THEN 1 ELSE 0 END) AS nulos_monthlycharges
FROM clientes;


-- Verificando valores vazios em TotalCharges.
-- Foram encontradas 11 linhas com valores vazios. Todas apresentam
-- tenure = 0 e Churn = 'No', indicando que são clientes recentes
-- que ainda não acumularam cobranças totais.
SELECT *
FROM clientes
WHERE TRIM(TotalCharges) = '';


-- Conferindo a distribuição de Churn entre os clientes com TotalCharges vazio.
-- O resultado confirma que todos esses clientes possuem Churn = 'No'.
SELECT Churn, COUNT(*)
FROM clientes
WHERE TRIM(TotalCharges) = ''
GROUP BY Churn;


-- Substituindo os valores vazios de TotalCharges por 0.
UPDATE clientes
SET TotalCharges = 0
WHERE TRIM(TotalCharges) = '';


-- Convertendo TotalCharges de VARCHAR para DECIMAL(10,2)
-- para permitir operações e cálculos numéricos.
ALTER TABLE clientes
MODIFY COLUMN TotalCharges DECIMAL(10,2);


-- 1.2 — Perguntas de negócio em SQL

-- Qual é a taxa geral de churn (% de clientes que cancelaram)?
-- R: A taxa geral de churn ficou em 26,54%. Isso significa que aproximadamente 1 a cada 4 clientes acabou cancelando o serviço.
select
round((sum(case when churn = 'Yes' then 1 else 0 end) / count(*)) * 100.0, 2) as taxa_churn
from clientes;

-- A taxa de churn varia por tipo de contrato (mês a mês, 1 ano, 2 anos)? Qual contrato retém mais?
-- R: Sim, a diferença é bem grande. O contrato mensal tem o maior churn, com 43%, enquanto o contrato de 2 anos fica em apenas 3%. Na prática, quanto maior o tempo de contrato, menor tende a ser o número de cancelamentos.
select Contract,
round((sum(case when churn = 'Yes' then 1 else 0 end) / count(*)) * 100.0, 2) as taxa_churn
from clientes
group by Contract;

-- Churn varia por forma de pagamento? Alguma forma de pagamento concentra mais cancelamento?
-- R: Sim. O 'Electronic check' se destaca bastante, com 45% de churn, enquanto as outras formas de pagamento ficam bem mais próximas umas das outras.
select PaymentMethod,
round((sum(case when churn = 'Yes' then 1 else 0 end) / count(*)) * 100.0, 2) as taxa_churn
from clientes
group by PaymentMethod;

-- Clientes com internet fibra óptica cancelam mais ou menos que DSL? E os sem internet?
-- R: Os clientes de fibra óptica cancelam bem mais que os de DSL, 42% contra 19%. A fibra também tem um preço médio maior, R$41,89 contra R$18,96 da DSL, então o preço pode ter alguma relação com essa diferença. Já quem não possui internet tem o menor churn, com 7%.
select InternetService,
round((sum(case when churn = 'Yes' then 1 else 0 end) / count(*)) * 100.0, 2) as taxa_churn
from clientes
group by InternetService;

-- Existe diferença de churn entre quem tem suporte técnico contratado e quem não tem?
-- R: Sim, a diferença é bem clara. Entre os clientes que possuem suporte técnico, o churn é de 15%, enquanto entre os que não possuem chega a 42%. Isso indica que o suporte pode estar ajudando na retenção dos clientes.
select TechSupport,
round((sum(case when churn = 'Yes' then 1 else 0 end) / count(*)) * 100.0, 2) as taxa_churn
from clientes
group by TechSupport;

-- Qual é o tempo médio de permanência (tenure) de quem cancela vs. de quem fica?
-- R: Quem continua como cliente fica, em média, 38 meses, enquanto quem cancela fica cerca de 18 meses. Ou seja, existe uma diferença bem grande no tempo de permanência entre os dois grupos.
select Churn,
avg(tenure) as dias_media
from clientes
group by Churn;


select 
count(*) as qtde_clientes,
round(100.0 * avg((case when Churn = 'Yes' then 1 else 0 end)), 2) as seg_taxa,
(select round(100.0 * avg((case when Churn = 'Yes' then 1 else 0 end)), 2) from clientes) as taxa_total
from clientes c
where c.Contract = 'Month-to-month' and c.tenure <= 12 and c.TechSupport = 'No'


