# 📊 Procurement Analytics & Inteligência Fiscal (Python)

## 🎯 Sobre o Projeto
Este projeto foi desenvolvido para transformar o setor de Compras de um centro de custos operacional em um **gerador de lucro estratégico**. Utilizando Python, automatizamos a leitura de dezenas de Notas Fiscais (PDFs) para extrair inteligência de dados, auditar impostos e desenhar o **Plano Estratégico de Suprimentos 2026**.

**Autor:** Tiago Motta (Analista de Compras & Estudante de Data Science)

## 💡 Principais Entregas e Resultados

1. **Auditoria Tributária (Data Mining em PDFs):** - Script que lê as NFs e calcula a "Eficiência Fiscal" de cada fornecedor (Lucro Real vs. Simples Nacional).
   - Identificação de **~50% do Spend** alocado em empresas que não geravam crédito tributário, permitindo a renegociação de preços com base no Custo Total de Aquisição (TCO).

2. **Saneamento e Categorização de Spend:**
   - Algoritmo que limpa nomes de fornecedores duplicados (ex: Razão Social vs. Nome Fantasia) e categoriza os gastos automaticamente em `Matérias-Primas`, `Logística` e `Alimentação (RH)`.

3. **Dashboards Executivos (Matplotlib/Pandas):**
   - **Matriz Estratégica:** Gráfico de dispersão (Scatter Plot) cruzando o Volume de Compras vs. Retorno de Crédito Tributário.
   - **Combo Chart Semestral:** Relação entre o valor gasto (Estratégia) e a quantidade de notas emitidas (Carga Operacional).
   - **Gráfico Waterfall (Cascata):** Projeção visual da redução de custos do plano estratégico.

4. **Automação de Compliance Fiscal:**
   - Geração de um Guia HTML/PDF com a matriz "De -> Para" de **CFOPs**, isolando os riscos de Substituição Tributária (ST) no sistema ERP Omie.

## 🛠️ Tecnologias Utilizadas
* **Python 3.10+**
* **Pandas** (Tratamento, unificação e agrupamento de dados)
* **Matplotlib** (Visualização de dados executiva e storytelling)
* **pdfminer.six** (Extração de texto bruto de faturas em PDF)
* **Regex (re)** (Identificação de padrões monetários e CFOPs)

## 📂 Estrutura dos Scripts
* `extrator_impostos.py`: Minera os PDFs caçando os campos ICMS, IPI, PIS, COFINS e Tributos Aproximados.
* `matriz_estrategica.py`: Plota a eficiência fiscal para identificar fornecedores "Estrelas" vs. "Alvos de Negociação".
* `plano_revisado_waterfall.py`: Projeta as metas de saving (Logística, Negociação e Financeiro) em gráfico de cascata.
* `gerador_pdf_cfop.py`: Gera o manual de boas práticas de entrada de notas via HTML automatizado.

---
*Nota: Por motivos de compliance e segurança da informação, os arquivos contendo dados financeiros reais (PDFs e Excel) não constam neste repositório público.*
## 📈 Resultados Visuais e Dashboards Executivos

Abaixo estão os recortes dos painéis gerados via Python (Matplotlib/Pandas), cruzando a carga operacional do setor de compras com a eficiência tributária.

### 1. Matriz Estratégica: Volume vs. Eficiência Fiscal
*Identificação visual do quadrante de fornecedores "Estrelas" (Alto volume e Alto crédito) contra os "Alvos de Negociação" (Alto volume e Zero crédito, foco primário de redução de custos).*
![Matriz de Eficiência Fiscal](img/matriz_estrategica.png)

### 2. Projeção de Saving Semestral (Waterfall)
*Impacto direto no fluxo de caixa da empresa após a renegociação de preços baseada no Custo Total de Aquisição (TCO), descontando perdas tributárias.*
![Gráfico Waterfall](img/waterfall_saving.png)

### 3. Curva A de Suprimentos (Top 10 Fornecedores)
*Mapeamento do Spend Analysis detalhando onde o capital da empresa está concentrado.*
![Top 10 Gastos](img/top10_gastos.png)

### 4. Esforço Operacional vs. Gasto Real
*Comparativo entre o volume de notas fiscais processadas (custo de tempo/homem) e o volume financeiro real das operações.*
![Volume vs Operacional](img/volume_vs_operacional.png)

---

## 📞 Contato & Perfil
Este projeto faz parte do meu portfólio prático de **Data Science aplicado a Negócios**. Se você busca um profissional capaz de extrair inteligência de dados brutos para gerar lucro e otimização de processos corporativos, vamos conversar!

* **Analista:** Tiago Motta
* **Localização:** Duque de Caxias, RJ
* **E-mail:** tiago-moda-senac@hotmail.com
* **LinkedIn:** https://www.linkedin.com/in/demotta/
* 