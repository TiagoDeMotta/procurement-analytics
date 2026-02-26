import os
import re
import pandas as pd
from pdfminer.high_level import extract_text

# --- CONFIGURAÇÃO ---
# Cole aqui o caminho da sua pasta de PDFs (use o r antes das aspas)
pasta_arquivos = r"C:\Users\LENOX PC\OneDrive\Documentos\NF PARA ANALISE  COM NOME DE FORNECEDORES"

arquivo_saida = 'Relatorio_Impostos_Detalhado.xlsx'

print(f"--- INICIANDO RAIO-X TRIBUTÁRIO EM: {pasta_arquivos} ---")


def extrair_valor_campo(texto, padroes):
    """
    Tenta encontrar um valor monetário após palavras-chave específicas.
    """
    for padrao in padroes:
        # Regex explica: Procure a palavra chave, aceite espaços/dois pontos, pegue numeros com ponto/virgula
        regex = padrao + r'[:\s]*R?\$?\s*([\d\.,]+)'
        busca = re.search(regex, texto, re.IGNORECASE)
        if busca:
            valor_txt = busca.group(1)
            # Limpa o valor (tira ponto de milhar, troca virgula por ponto)
            try:
                valor_limpo = valor_txt.replace('.', '').replace(',', '.')
                return float(valor_limpo)
            except:
                continue
    return 0.0


lista_dados = []

if not os.path.exists(pasta_arquivos):
    print("❌ ERRO: Pasta não encontrada.")
else:
    arquivos = [f for f in os.listdir(pasta_arquivos) if f.lower().endswith('.pdf')]
    total_arqs = len(arquivos)
    print(f"Encontrei {total_arqs} notas. Lendo impostos (isso pode demorar um pouco)...")

    for i, arquivo in enumerate(arquivos):
        caminho_completo = os.path.join(pasta_arquivos, arquivo)

        try:
            # Extrai o texto do PDF
            texto_pdf = extract_text(caminho_completo)

            # 1. VALOR TOTAL DA NOTA
            v_total = extrair_valor_campo(texto_pdf, ['VALOR TOTAL DA NOTA', 'VALOR TOTAL DO DOCUMENTO',
                                                      'VALOR LIQUIDO DA FATURA'])
            if v_total == 0:  # Tenta pegar do nome do arquivo se falhar no PDF
                busca_nome = re.search(r'(?:R\$|RS)\s*([\d\.,]+)', arquivo, re.IGNORECASE)
                if busca_nome:
                    v_total = float(busca_nome.group(1).replace('.', '').replace(',', '.'))

            # 2. IMPOSTOS ESPECÍFICOS (Padrão DANFE)
            v_icms = extrair_valor_campo(texto_pdf, ['VALOR DO ICMS', 'V.ICMS'])
            v_ipi = extrair_valor_campo(texto_pdf, ['VALOR DO IPI', 'V.IPI'])
            v_pis = extrair_valor_campo(texto_pdf, ['VALOR DO PIS', 'V.PIS'])
            v_cofins = extrair_valor_campo(texto_pdf, ['VALOR DA COFINS', 'V.COFINS'])

            # 3. VALOR APROXIMADO TRIBUTOS (Rodapé da nota - Lei da Transparência)
            v_aprox_trib = extrair_valor_campo(texto_pdf, ['VALOR APROXIMADO DOS TRIBUTOS', 'VAL. APROX. TRIBUTOS',
                                                           'TRIBUTOS TOTAIS INCIDENTES'])

            # Se não achou PIS/COFINS explícito, tenta estimar pelo Total Aprox se disponível
            # (Muitas notas escondem PIS/COFINS nas linhas dos itens)

            # Soma dos impostos destacados
            impostos_destacados = v_icms + v_ipi + v_pis + v_cofins

            # Definição do "Custo Imposto" para análise
            # Se a nota tiver o campo "Valor Aprox Tributos", usamos ele pois é mais completo
            # Se não, usamos a soma do que achamos
            total_impostos = max(impostos_destacados, v_aprox_trib)

            # Valor Real do Produto (O que sobra pro fornecedor)
            valor_produto_liquido = v_total - total_impostos
            if valor_produto_liquido < 0: valor_produto_liquido = 0  # Proteção

            lista_dados.append({
                'Arquivo': arquivo,
                'Valor_Nota_Total': v_total,
                'ICMS': v_icms,
                'IPI': v_ipi,
                'PIS': v_pis,
                'COFINS': v_cofins,
                'Total_Impostos': total_impostos,
                'Produto_Liquido': valor_produto_liquido,
                '%_Imposto': (total_impostos / v_total * 100) if v_total > 0 else 0
            })

            print(f"[{i + 1}/{total_arqs}] Lido: R$ {v_total:.2f} | Imposto: R$ {total_impostos:.2f}", end='\r')

        except Exception as e:
            continue

    print("\n\nConsolidando dados...")

    if lista_dados:
        df = pd.DataFrame(lista_dados)

        # --- ANÁLISE ESTATÍSTICA ---
        total_gasto = df['Valor_Nota_Total'].sum()
        total_imposto = df['Total_Impostos'].sum()
        total_produto = df['Produto_Liquido'].sum()

        print("=" * 50)
        print("RESUMO DA CARGA TRIBUTÁRIA")
        print("=" * 50)
        print(f"💰 VALOR TOTAL GASTO:     R$ {total_gasto:,.2f}")
        print(f"🏛️ VALOR PAGO EM IMPOSTOS: R$ {total_imposto:,.2f}  ({(total_imposto / total_gasto) * 100:.1f}%)")
        print(f"📦 VALOR REAL DOS PRODUTOS:R$ {total_produto:,.2f}")
        print("=" * 50)

        # Salva Excel
        df.to_excel(arquivo_saida, index=False)
        print(f"📂 Relatório detalhado salvo em: {arquivo_saida}")

        # --- GRÁFICO VISUAL ---
        import matplotlib.pyplot as plt

        plt.style.use('ggplot')

        fig, ax = plt.subplots(figsize=(10, 6))

        labels = ['Produto/Serviço Real', 'Impostos (Custo Brasil)']
        sizes = [total_produto, total_imposto]
        colors = ['#3498DB', '#E74C3C']  # Azul e Vermelho

        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
               explode=(0, 0.1), shadow=True, textprops={'fontsize': 14})

        ax.set_title(f'Para onde foi o dinheiro? (Total: R$ {total_gasto:,.0f})', fontsize=16)

        plt.tight_layout()
        plt.show()

    else:
        print("Nenhum dado extraído.")