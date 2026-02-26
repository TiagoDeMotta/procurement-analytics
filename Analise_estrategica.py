import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- CONFIGURAÇÃO ---
arquivo_entrada = 'Relatorio_Compras_Validado.xlsx'


def formata_reais(x, pos):
    return f'R$ {x * 1e-3:,.0f}k'


try:
    print("Carregando dados e processando datas...")
    df = pd.read_excel(arquivo_entrada, sheet_name='Detalhado')

    # 1. LIMPEZA E CONVERSÃO
    # Garante que Valor é número
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)

    # CONVERTE A DATA (O Pulo do Gato)
    # dayfirst=True avisa que no Brasil usamos Dia/Mes/Ano
    df['Data_Formatada'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')

    # Remove linhas onde a data não foi identificada
    df = df.dropna(subset=['Data_Formatada'])

    # Filtra apenas o ano de 2025 (caso tenha entrado algo de 2024 ou 2026 errado)
    df = df[df['Data_Formatada'].dt.year == 2025]

    # Cria uma coluna só com "Ano-Mês" para agrupar (Ex: 2025-08)
    df['Mes_Ano'] = df['Data_Formatada'].dt.to_period('M')

    # ==========================================================
    # 2. AGRUPAMENTO POR MÊS
    # ==========================================================
    # Queremos duas coisas: Soma do Valor e Contagem de Notas
    timeline = df.groupby('Mes_Ano').agg(
        Total_Gasto=('Valor', 'sum'),
        Qtd_Notas=('Valor', 'count')
    )

    # ==========================================================
    # 3. O GRÁFICO DUPLO (BARRAS + LINHA)
    # ==========================================================
    # Estilo profissional
    plt.style.use('ggplot')

    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Eixo 1 (Esquerda): Barras de Dinheiro
    cor_barra = '#3498DB'  # Azul
    # O index (Mes_Ano) precisa virar string para o gráfico entender
    x_labels = timeline.index.astype(str)

    ax1.bar(x_labels, timeline['Total_Gasto'], color=cor_barra, alpha=0.7, label='Valor Gasto (R$)')
    ax1.set_ylabel('Valor Total (R$)', color=cor_barra, fontsize=12, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=cor_barra)
    ax1.set_title('Evolução Mensal: Gasto vs. Quantidade de Notas (2025)', fontsize=14)

    # Coloca os valores em R$ em cima das barras
    for i, v in enumerate(timeline['Total_Gasto']):
        ax1.text(i, v, f'R$ {v:,.0f}', ha='center', va='bottom', fontsize=9, color='black')

    # Eixo 2 (Direita): Linha de Quantidade
    ax2 = ax1.twinx()  # Cria um eixo gêmeo compartilhando o mesmo X
    cor_linha = '#E74C3C'  # Vermelho

    ax2.plot(x_labels, timeline['Qtd_Notas'], color=cor_linha, marker='o', linewidth=3, label='Qtd. Notas')
    ax2.set_ylabel('Quantidade de Notas (Und)', color=cor_linha, fontsize=12, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=cor_linha)

    # Coloca os números das bolinhas da linha
    for i, v in enumerate(timeline['Qtd_Notas']):
        ax2.text(i, v, f'{v}', ha='center', va='bottom', fontsize=10, fontweight='bold', color=cor_linha,
                 backgroundcolor='white')

    # Ajustes finais
    plt.grid(visible=False)  # Limpa o fundo para não confundir
    print("Gerando gráfico de evolução mensal...")
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Erro ao processar datas: {e}")
    print("DICA: Verifique se a coluna 'Data' no Excel está no formato dd/mm/aaaa")