import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Preparação dos Dados (Baseado na nossa análise anterior)
data = {
    'Item': [
        'RODA 150 X 75 GR 60', 'RODA 150 X 75 GR 80', 'DISCO CORTE 115 BNA12',
        'DISCO FLAP 115 X 22', 'MINICONTOUR GR 60', 'MINICONTOUR GR 80',
        'GEL DECAPANTE', 'DISCO CORTE TURBINOX', 'FL SCOTH BRITE 225 X 275'
    ],
    'Var_Perc': [-12.66, -10.48, -8.14, -9.80, -8.99, -7.53, -0.92, -28.89, 1.92],
    'Savings_6M': [156.34, 116.57, 66.86, 42.86, 12.00, 1.50, 1.11, 0.00, -4.29]
}

df = pd.DataFrame(data)
total_savings = df['Savings_6M'].sum()

# 2. Configuração Visual Estilo "Modern Dashboard"
sns.set_theme(style="white")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), gridspec_kw={'width_ratios': [1.2, 1]})
fig.patch.set_facecolor('#f8f9fa')

# Título Centralizado com Destaque
fig.suptitle(f'PROJEÇÃO DE SAVINGS - PRÓXIMOS 6 MESES\nTotal Acumulado: R$ {total_savings:,.2f}',
             fontsize=22, fontweight='bold', color='#1a3a5a', y=0.96)

# --- GRÁFICO 1: SAVINGS ACUMULADO (R$) ---
df_savings = df[df['Savings_6M'] > 0].sort_values('Savings_6M', ascending=True)
colors = sns.color_palette("Greens_d", len(df_savings))

bars1 = ax1.barh(df_savings['Item'], df_savings['Savings_6M'], color=colors, height=0.7)
ax1.set_title('Economia Real Projetada (R$)', fontsize=15, pad=15, fontweight='semibold')
ax1.set_xlabel('Valor em Reais (R$)', fontsize=12, color='#444')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Adicionar labels de valor nas barras
for bar in bars1:
    width = bar.get_width()
    ax1.text(width + 2, bar.get_y() + bar.get_height()/2, f'R$ {width:,.2f}',
             va='center', fontweight='bold', color='#2e7d32')

# --- GRÁFICO 2: PERFORMANCE DE DESCONTO (%) ---
# Focamos nos descontos obtidos (valores negativos da variação)
df_disc = df[df['Var_Perc'] < 0].copy()
df_disc['Desconto'] = df_disc['Var_Perc'] * -1
df_disc = df_disc.sort_values('Desconto', ascending=True)

bars2 = ax2.barh(df_disc['Item'], df_disc['Desconto'], color='#3498db', height=0.7)
ax2.set_title('% de Redução por Item', fontsize=15, pad=15, fontweight='semibold')
ax2.set_xlabel('Percentual de Desconto (%)', fontsize=12, color='#444')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Adicionar labels de porcentagem
for bar in bars2:
    width = bar.get_width()
    ax2.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'{width:.1f}%',
             va='center', fontweight='bold', color='#1565c0')

# Ajustes finais de layout
plt.tight_layout(rect=[0, 0.03, 1, 0.92])
plt.show()
