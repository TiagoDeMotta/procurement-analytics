import matplotlib.pyplot as plt
import pandas as pd

# --- DADOS REAIS EXTRAÍDOS DA SUA AUDITORIA ---
# Valores aproximados baseados nos logs anteriores
gasto_atual_semestre = 411163.79  # Total auditado
gasto_frete_atual = 13221.28  # Total frete rastreado
volume_sem_credito = 204342.71  # Volume comprado de empresas Simples/Serviço

# --- METAS DO PLANO ESTRATÉGICO ---
# 1. Negociação com Fornecedores "Sem Crédito" (Meta: 5% de desconto)
economia_negociacao = volume_sem_credito * 0.05

# 2. Otimização Logística (Meta: 15% no frete + Migração FOB->CIF)
economia_frete = gasto_frete_atual * 0.15 + 1500  # (+1500 estimado de conversão para CIF)

# 3. Consolidação Operacional (Redução de Custo de Processo)
# Estima-se R$ 30,00 de custo admin por pedido (tempo, sistema, financeiro)
# Meta: Reduzir de 287 notas para 215 (25% a menos)
qtd_notas_atual = 287
qtd_notas_meta = 215
economia_operacional = (qtd_notas_atual - qtd_notas_meta) * 30

# Cálculo do Novo Cenário
total_economia = economia_negociacao + economia_frete + economia_operacional
gasto_projetado = gasto_atual_semestre - total_economia

# --- PREPARAÇÃO DO GRÁFICO WATERFALL ---
# Define os passos da escada
steps = [
    gasto_atual_semestre,
    -economia_negociacao,
    -economia_frete,
    -economia_operacional,
    gasto_projetado
]

labels = [
    'Cenário Atual\n(Semestre)',
    'Negociação\nFornecedores',
    'Otimização\nLogística',
    'Eficácia\nOperacional',
    'Cenário Meta\n2026'
]

# Configuração do Gráfico
plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(12, 7))

# Criação das Barras Flutuantes
# A lógica é: A barra começa onde a anterior terminou
running_total = 0
for i, (val, label) in enumerate(zip(steps, labels)):
    if i == 0 or i == len(steps) - 1:
        color = '#2C3E50'  # Azul Escuro (Início e Fim)
        bottom = 0
        height = val
    else:
        color = '#27AE60'  # Verde (Economia/Ganho)
        height = val
        bottom = running_total  # Começa do topo da anterior

    ax.bar(label, height, bottom=bottom, color=color, edgecolor='black', width=0.6)

    # Atualiza o total corrente (menos para o último passo que é o resultado)
    if i == 0:
        running_total = val
    elif i < len(steps) - 1:
        running_total += val

    # Texto com o Valor
    # Se for economia, coloca o sinal de menos
    if i > 0 and i < len(steps) - 1:
        texto = f"- R$ {abs(val):,.0f}"
        pos_y = bottom + (val / 2)  # Centraliza na barra de queda
    else:
        texto = f"R$ {val:,.0f}"
        pos_y = val + 5000  # Coloca em cima da barra

    ax.text(i, pos_y, texto, ha='center', va='center', fontweight='bold', fontsize=11, color='black')

# Linhas de conexão (para ficar bonito estilo consultoria)
ax.plot([0, 1], [steps[0], steps[0]], color='gray', linestyle='--')
ax.plot([1, 2], [steps[0] + steps[1], steps[0] + steps[1]], color='gray', linestyle='--')
ax.plot([2, 3], [steps[0] + steps[1] + steps[2], steps[0] + steps[1] + steps[2]], color='gray', linestyle='--')

# Títulos
ax.set_title('Plano "Eficácia 2026": Projeção de Economia Semestral', fontsize=16, fontweight='bold')
ax.set_ylabel('Custo Total (R$)', fontsize=12)

# Adiciona o Resumo no canto
texto_resumo = (
    f"💰 ECONOMIA TOTAL PROJETADA: R$ {total_economia:,.2f}\n"
    f"📉 REDUÇÃO DE CUSTO: {((total_economia / gasto_atual_semestre) * 100):.1f}%\n"
    f"📦 MENOS {qtd_notas_atual - qtd_notas_meta} NOTAS FISCAIS"
)
plt.text(0.75, 0.85, texto_resumo, transform=ax.transAxes,
         bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'), fontsize=11)

plt.tight_layout()
print("Mostrando o Gráfico do Plano de Metas...")
plt.show()
