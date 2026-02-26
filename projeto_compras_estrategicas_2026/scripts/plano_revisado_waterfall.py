import matplotlib.pyplot as plt

# --- DADOS EXATOS DA SUA IMAGEM ---
total_semestre = 411163.00
economia_materiais = 12397.00
economia_frete = 1983.00
ganho_financeiro_rh = 3000.00

total_economia = economia_materiais + economia_frete + ganho_financeiro_rh
novo_custo = total_semestre - total_economia

# --- GRÁFICO ---
plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(12, 7))

# Estrutura de dados
steps = [total_semestre, -economia_materiais, -economia_frete, -ganho_financeiro_rh, novo_custo]
labels = [
    'Custo Atual',
    'Negociação\nMateriais',
    'Otimização\nFrete',
    'Ganho Finan.\n(Caixa)',
    'Meta 2026'
]

running_total = 0
for i, (val, label) in enumerate(zip(steps, labels)):
    # Cores: Azul para as colunas totais, Verde para as economias
    color = '#1F3A52' if i in [0, 4] else '#27AE60'

    # Lógica da cascata
    if i == 0:
        height = val
        bottom = 0
        running_total = val
    elif i == 4:
        height = val
        bottom = 0
    else:
        height = abs(val)  # A barra desenha para cima...
        bottom = running_total - abs(val)  # ...mas começa mais baixo
        running_total -= abs(val)

        # Desenha a barra
    ax.bar(label, height, bottom=bottom, color=color, edgecolor='white', width=0.5, linewidth=2)

    # Texto com o valor
    texto = f"- R$ {abs(val):,.0f}" if (i > 0 and i < 4) else f"R$ {val:,.0f}"

    # Posicionamento do texto
    if i in [0, 4]:
        pos_y = val + 1500  # Em cima da barra principal
        ax.text(i, pos_y, texto, ha='center', fontweight='bold', fontsize=12, color='black')
    else:
        pos_y = bottom + (height / 2)  # No meio da barra verde
        ax.text(i, pos_y, texto, ha='center', va='center', fontweight='bold', fontsize=11, color='white')

# --- O PULO DO GATO: O ZOOM NO EIXO Y ---
# Cortamos a parte de baixo (vazia) para focar na mudança
limite_inferior = novo_custo - 10000
limite_superior = total_semestre + 8000
ax.set_ylim(limite_inferior, limite_superior)

# Linhas de conexão
ax.plot([0, 1], [total_semestre, total_semestre], color='gray', linestyle='--', alpha=0.5)
ax.plot([1, 2], [total_semestre - economia_materiais, total_semestre - economia_materiais], color='gray',
        linestyle='--', alpha=0.5)
ax.plot([2, 3],
        [total_semestre - economia_materiais - economia_frete, total_semestre - economia_materiais - economia_frete],
        color='gray', linestyle='--', alpha=0.5)

# Limpa o eixo Y para não poluir
ax.get_yaxis().set_visible(False)

# Títulos
ax.set_title('Plano Estratégico 2026: Economia Projetada (Semestre)', fontsize=16, fontweight='bold', pad=20)

# Resumo em destaque
texto_resumo = f"ECONOMIA TOTAL: R$ {total_economia:,.0f}"
plt.text(0.5, 0.90, texto_resumo, transform=ax.transAxes, ha='center',
         bbox=dict(facecolor='#27AE60', alpha=0.9, edgecolor='white', boxstyle='round,pad=0.5'),
         fontsize=14, fontweight='bold', color='white')

plt.tight_layout()
plt.show()
