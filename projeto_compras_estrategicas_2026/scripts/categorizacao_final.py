import pandas as pd
import os

# --- CONFIGURAÇÃO ---
arquivo_entrada = 'Base_Consolidada_Final.xlsx'  # Usa a base que unificou os nomes
arquivo_saida = 'Base_Categorizada_2026.xlsx'

print("--- INICIANDO CATEGORIZAÇÃO ESTRATÉGICA ---")

try:
    df = pd.read_excel(arquivo_entrada)


    # 1. Definição das Regras
    def definir_categoria(row):
        fornecedor = str(row['Fornecedor_Tratado']).upper()

        # Regra 1: Alimentação (RH)
        if 'EXPLOSÃO' in fornecedor or 'IZABELA' in fornecedor or 'RESTAURANTE' in fornecedor:
            return 'ALIMENTAÇÃO (RH)'

        # Regra 2: Logística
        transportadoras = ['GARIBALDI', 'JAMEF', 'RODONAVES', 'BRASPRESS', 'LOG', 'TRANS WELLS', 'TRANSPORTE']
        if any(t in fornecedor for t in transportadoras):
            return 'LOGÍSTICA'

        # Regra 3: O resto é Material/Serviço (Core Business)
        return 'MATERIAIS E INSUMOS'


    # 2. Aplica a categorização
    df['Categoria'] = df.apply(definir_categoria, axis=1)

    # 3. Análise dos Grupos
    resumo = df.groupby('Categoria').agg(
        Valor_Total=('Valor_Nota_Total', 'sum'),
        Qtd_Notas=('Arquivo', 'count'),
        Imposto_Recuperavel=('Total_Impostos', 'sum')
    ).sort_values(by='Valor_Total', ascending=False)

    # Calcula %
    total_geral = resumo['Valor_Total'].sum()
    resumo['% do Budget'] = (resumo['Valor_Total'] / total_geral) * 100

    print("\n" + "=" * 60)
    print("NOVO PERFIL DE GASTOS (PÓS-SANEAMENTO)")
    print("=" * 60)
    print(resumo)
    print("-" * 60)

    # 4. Salva o arquivo final
    df.to_excel(arquivo_saida, index=False)
    print(f"\n📂 Base Categorizada salva: {arquivo_saida}")
    print("Agora sabemos exatamente onde atacar!")

except FileNotFoundError:
    print(f"ERRO: Não encontrei '{arquivo_entrada}'. Rode o script de unificação primeiro.")
