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