import pandas as pd
import os

# --- CONFIGURAÇÃO ---
# O robô vai tentar usar a base unificada (que juntou a Izabela com a Explosão de Sabores).
# Se não achar, ele usa a base de impostos anterior.
arquivo_entrada = 'Base_Consolidada_Final.xlsx'
if not os.path.exists(arquivo_entrada):
    arquivo_entrada = 'Relatorio_Impostos_Detalhado.xlsx'

print(f"--- GERANDO LISTA DE ALVOS PARA NEGOCIAÇÃO 2026 ---")
print(f"Lendo base de dados: {arquivo_entrada}\n")

try:
    df = pd.read_excel(arquivo_entrada)

    # 1. Garante que temos a coluna com o nome limpo do fornecedor
    if 'Fornecedor_Tratado' not in df.columns:
        df['Fornecedor_Tratado'] = df['Arquivo'].apply(lambda x: x.split('NF')[0].split('R$')[0].split('RS')[0].replace('_', ' ').strip())

    # 2. O FILTRO CIRÚRGICO: Pega apenas as notas onde o imposto destacado foi ZERO
    df_sem_imposto = df[df['Total_Impostos'] == 0].copy()

    # 3. Agrupamento e Soma
    resumo = df_sem_imposto.groupby('Fornecedor_Tratado').agg(
        Qtd_Notas=('Arquivo', 'count'),
        Valor_Total=('Valor_Nota_Total', 'sum')
    ).reset_index()

    # 4. Ordenação (Do maior Gasto para o menor)
    resumo = resumo.sort_values(by='Valor_Total', ascending=False)

    # Remove fornecedores com valor zero (caso haja alguma nota zerada perdida)
    resumo = resumo[resumo['Valor_Total'] > 0]

    # Cálculos Totais
    total_gasto = resumo['Valor_Total'].sum()
    total_notas = resumo['Qtd_Notas'].sum()
    total_empresas = len(resumo)

    # 5. EXIBIÇÃO DO RELATÓRIO NO CONSOLE
    print("="*75)
    print("🚨 RELATÓRIO: EMPRESAS COM 0% DE RETORNO TRIBUTÁRIO (CUSTO CHEIO) 🚨")
    print("="*75)
    print(f"{'EMPRESA (FORNECEDOR)':<40} | {'NFs':<5} | {'MONTANTE GASTO (R$)'}")
    print("-" * 75)

    for index, row in resumo.iterrows():
        # Limita o nome a 38 caracteres para a tabela ficar perfeitamente alinhada
        nome = str(row['Fornecedor_Tratado'])[:38]
        qtd = row['Qtd_Notas']
        valor = row['Valor_Total']
        print(f"{nome:<40} | {qtd:<5} | R$ {valor:,.2f}")

    print("="*75)
    print(f"RESUMO GERAL DO SEMESTRE:")
    print(f"> Total de Empresas sem crédito: {total_empresas}")
    print(f"> Total de Notas Fiscais processadas: {total_notas}")
    print(f"> MONTANTE TOTAL (DINHEIRO PRESO): R$ {total_gasto:,.2f}")
    print("="*75)

    # 6. Salva em um Excel limpo para você imprimir
    arquivo_saida = 'Lista_Alvos_Negociacao_2026.xlsx'
    resumo.to_excel(arquivo_saida, index=False)
    print(f"\n📂 Arquivo Excel gerado com sucesso: {arquivo_saida}")
    print("Dica: Imprima este Excel e leve para a reunião de Diretoria.")

except FileNotFoundError:
    print(f"❌ ERRO: O arquivo '{arquivo_entrada}' não foi encontrado.")
    print("Verifique se o script está na mesma pasta dos arquivos Excel.")
except Exception as e:
    print(f"❌ ERRO INESPERADO: {e}")
