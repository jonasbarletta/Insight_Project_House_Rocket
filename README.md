# Projeto House Rocket
O Projeto House Rocket é um projeto do tipo Insights fictício que busca analisar as melhores oportunidades de compras de imóveis para a empresa House Rocket (também fictícia). 

Esse projeto é uma proposta do Curso: Python do ZERO ao DS, da Comunidade DS. O conjunto de dados utilizados está disponível em [Kaggle](https://www.kaggle.com/datasets/harlfoxem/housesalesprediction). 


## 1.	Questões de Negócio
A empresa House Rocket trabalha com o seguinte modelo de negócio: comprar imóveis a preços baixos e revendê-los a um preço maior. 
### 1.1.	Problemática
A equipe de negócios da empresa está com dificuldade de encontrar as melhores oportunidades de compra de imóveis. A principal dificuldade relatada por eles é a grande quantidade de dados e como filtrá-los para encontrar os melhores imóveis para compra.
### 1.2.	Objetivo
Indicar os melhores imóveis para compra, com uma sugestão de margem de lucro.

## 2.	Premissas de negócio
Os atributos do conjunto de dados são:
| Atributos |	Descrição |
| --------- | --------- |
| id | Identificador |
| date |Data que o imóvel foi colocado à venda |
| price	| Preço do imóvel |
| bedrooms	| Quantidade de quartos |
| bathrooms |	Quantidade de banheiros |
| sqft_living	| Pés quadrados construídos |
| sqft_lot |	Pés quadrados do terreno |
| floors	| Quantidade de andares |
| waterfront	| Se é de frente para a água: Sim (1) ou Não (0) |
| view |	Índice de 0 – 4 com relação a vista do imóvel |
| condition	| Índice de 1 – 5 com relação as condições que se encontram a casa |
| grade |	Nota de 1 – 13 com relação a qualidade dos materiais e mão de obra utilizada na construção |
| sqft_above	| Pés quadrados construídos sem considerar o porão |
| sqft_basement |	Pés quadrados do porão |
| yr_built	| Ano que começou a construção |
| yr_renovated	| Ano da última reforma. Zero (0) indica que não foi reformada |
| zipcode | Código ZIP do imóvel |
| lat	| Latitude |
| long | Longitude |
| sqft_living15	| Média dos pés quadrados construídos dos 15 imóveis mais próximos |
| sqft_lot15 |	Média dos pés quadrados do terreno dos 15 imóveis mais próximos |

- Não entraremos em detalhes sobre as quantidades não inteiras de quartos, andares e banheiros.
- Para o atributo ‘conditions’ consideraremos que 1 e 2 são imóveis em condições ruins, ou seja, imóveis que exigiriam reforma. Já 3, 4 e 5 condições boas, que não exigiriam reforma.

Para a limpeza dos dados:

- Desconsideraremos um dos imóveis que possui um número muito elevado de quartos (33) com relação ao seu tamanho.
- Alguns imóveis possuem o mesmo Id, estes foram imóveis que estavam a venda em determinada data e posteriormente foram colocados a venda novamente. Então, mantivemos apenas os imóveis com a data do anúncio de venda mais recente.

## 3.	Planejamento da solução

### 3.1.	Produto final
- Entregar cinco Insights dos dados;
- Fazer recomendações de compras de imóveis;
- Dashboard interativo completo, com mapas, tabelas e gráficos.

### 3.2.	Ferramentas
- Python 3.10
- PyCharm
- Jupyter Notebook
- Github
- Streamlit
- Heroku

## 4.	Insights dos dados
Com análises realizadas, investiguei quatro hipóteses que geraram insights interessantes:

H1: Imóveis com vista para a água possuem o preço por pé quadrado construído 30% superior, na média.

Hipótese verdadeira. O preço por pé quadrado construído das casas que possuem vista para água é 37%, na média, maior.

H2: Imóveis com data de construção maior que 1975 são 20% mais caros, na média.

Hipótese falsa. O preço é, na média, 13% superior. Porém é importante notar que se considerarmos os imóveis que foram reformados depois de 1975, a diferença passa para 20%.

H3: Por região, imóveis que sofreram reforma possuem, na média, o preço 30% superior com relação aos que não foram reformados.

Hipótese falsa. Na média, os preços dos imóveis, por região, que foram reformados são 17% maiores do que os que não foram. Porém, em algumas regiões esse percentual pode variar de 75% a 135%.

H4: Os valores dos imóveis com data no verão são na média 0% superior do que os com data no inverno.

Hipótese falsa. O preço dos imóveis anunciados no verão são 7,5% superior quando comparados com os anunciados no inverno. Porém, em algumas localidades, essa porcentagem pode subir para quase 20%.


## 5.	Resultados

### 5.1. Resultados financeiros

Nessa primeira etapa, na busca por grandes oportunidades de compras de imóveis, focamos em imóveis que tenham:

- o preço pelo menos 10% abaixo da mediana dos preços de sua localidade;
- a condição superior, ou igual, a média das condições dos imóveis da sua localidade;
- a área do terreno superior, ou igual, a média das áreas dos terrenos dos 15 imóveis mais próximos;
- a área construída superior, ou igual, a média das áreas construídas dos 15 imóveis mais próximos.

Satisfazendo todos esses critérios, foram selecionados 882 imóveis. Considerando uma margem de lucro de 30%, o faturamento esperado na venda de todos esses imóveis seria de U$108,3 milhões.

### 5.2. Dashboard

Construímos um dashboard completo com filtros interativos para que o CEO da empresa possa analisar os imóveis com diferentes perspectivas. Esse dashboard pode ser acessado de qualquer localidade com acesso a internet: [Dashboard](https://dashboard-house-rocket-project.herokuapp.com/)

## 6.	Conclusões
Após uma análise bastante criteriosa dos imóveis foi possível encontrar imóveis com qualidade superior com relação aos imóveis mais próximos e com o preço bem abaixo do mercado. 

Além disso, os insights apresentados para o time de negócio podem ser grande contribuição para selecionar outros imóveis que também possam ser grandes oportunidades, além de possibilitar um novo modelo de negócio para a empresa.

## 7.	Próximos passos
Como mencionado anteriormente, os insights analisados abriram portas para duas grandes possibilidades de negócio:
- comprar imóveis no inverno e esperar para vendê-los no verão, podendo assim incorporar uma taxa de lucro maior que 30%.
- analisar as possibilidades de expandir a empresa com um novo modelo de negócio: compra de imóveis em condições ruins, para reforma-los e vende-los.
- acrescentar mais funcionalidades no dashboard.

## 8. Referências
[1] HARLFOXEM. Kaggle - House Sales in King County, USA. https://www.kaggle.com/datasets/harlfoxem/housesalesprediction. Último acesso: 07/05/2022

[2] LOPES, Meigarom. Curso de Python do ZERO ao DS - Comunidade DS. https://www.youtube.com/watch?v=1xXK_z9M6yk&list=PLZlkyCIi8bMprZgBsFopRQMG_Kj1IA1WG&index=1. Último acesso: 07/05/2022

[3] GeoDa Data and Lab. https://geodacenter.github.io/data-and-lab//KingCounty-HouseSales2015/. Último acesso: 07/05/2022



