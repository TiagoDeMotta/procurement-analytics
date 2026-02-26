import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURAÇÃO ---
arquivo_entrada = 'Relatorio_Impostos_Detalhado.xlsx'

print("--- CLASSIFICANDO FORNECEDORES POR REGIME TRIBUTÁRIO ---")

try:
    # 1. Carrega o relatório de impostos
    df = pd.read_excel(arquivo_entrada)


    # Extrai o nome do fornecedor do nome do arquivo (limpeza básica)
    # Ex: "Rapido Garibaldi - NF..." -> "Rapido Garibaldi"
    def limpar_nome(nome_arq):
        # Tenta pegar o texto antes de "NF" ou "R$"
        nome = nome_arq.split('NF')[0].split('R$')[0].split('RS')[0]
        return nome.replace('_', ' ').strip()


    df['Fornecedor_Provavel'] = df['Arquivo'].apply(limpar_nome)


    # 2. Regra de Classificação
    def definir_perfil(row):
        imposto_total = row['Total_Impostos']
        valor_nota = row['Valor_Nota_Total']

        if valor_nota == 0: return "Erro Leitura"

        ratio = (imposto_total / valor_nota) * 100

        # Se tem destaque relevante (>10%), provavelmente é Indústria/Lucro Real
        if ratio > 10:
            return "Indústria/Lucro Real (Gera Crédito)"
        # Se tem destaque pequeno (entre 1% e 10%), provável Simples com permissão de crédito
        elif 1 <= ratio <= 10:
            return "Simples Nacional"
        # Se é zero ou quase zero
        else:
            return "Sem Destaque / Serviço"


    df['Perfil_Tributario'] = df.apply(definir_perfil, axis=1)

    # 3. Análise Agrupada
    analise = df.groupby('Perfil_Tributario').agg(
        Qtd_Notas=('Arquivo', 'count'),
        Valor_Total=('Valor_Nota_Total', 'sum'),
        Imposto_Total=('Total_Impostos', 'sum')
    ).sort_values(by='Valor_Total', ascending=False)

    # Calcula % de representatividade
    total_compras = analise['Valor_Total'].sum()
    analise['% do Spend'] = (analise['Valor_Total'] / total_compras) * 100

    print("\n" + "=" * 60)
    print("RAIO-X DA SUA CADEIA DE SUPRIMENTOS")
    print("=" * 60)
    print(analise[['Qtd_Notas', 'Valor_Total', '% do Spend']])
    print("-" * 60)

    # 4. Lista dos "Top Geradores de Crédito"
    # Quem são os fornecedores que mais devolveram dinheiro em imposto?
    top_creditos = df.groupby('Fornecedor_Provavel')[['Total_Impostos', 'Valor_Nota_Total']].sum()
    top_creditos['% Retorno'] = (top_creditos['Total_Impostos'] / top_creditos['Valor_Nota_Total']) * 100
    top_creditos = top_creditos.sort_values(by='Total_Impostos', ascending=False).head(5)

    print("\n💎 TOP 5 FORNECEDORES QUE MAIS GERAM CRÉDITO (BONS PARA LUCRO REAL):")
    for fornecedor, row in top_creditos.iterrows():
        print(f"   > {fornecedor[:30]:<30} | Gerou R$ {row['Total_Impostos']:<10,.2f} ({row['% Retorno']:.1f}%)")

    # 5. Gráfico
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 6))

    # Cores: Verde (Bom crédito), Amarelo (Médio), Cinza (Sem crédito)
    cores_map = {
        'Indústria/Lucro Real (Gera Crédito)': '#27AE60',
        'Simples Nacional': '#F1C40F',
        'Sem Destaque / Serviço': '#95A5A6',
        'Erro Leitura': '#E74C3C'
    }
    cores = [cores_map.get(i, '#333333') for i in analise.index]

    analise['Valor_Total'].plot(kind='barh', color=cores, ax=ax)
    ax.set_title('Perfil Tributário dos Fornecedores (Onde gastamos?)')
    ax.set_xlabel('Valor Total Comprado (R$)')
    ax.set_ylabel('')

    # Rótulos
    for i, v in enumerate(analise['Valor_Total']):
        ax.text(v, i, f' R$ {v:,.0f} ({analise["% do Spend"].iloc[i]:.1f}%)', va='center', fontweight='bold')

    plt.tight_layout()
    plt.show()

except FileNotFoundError:
    print("Erro: Arquivo 'Relatorio_Impostos_Detalhado.xlsx' não encontrado.")
    print("Rode o script anterior primeiro.")