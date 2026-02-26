import os
import re
import pandas as pd

# --- CONFIGURAÇÃO ---
# Caminho da sua pasta (com o r antes para o Windows aceitar)
pasta_arquivos = r"C:\Users\LENOX PC\OneDrive\Documentos\NF PARA ANALISE  COM NOME DE FORNECEDORES"

# Lista de Transportadoras para caçar
alvos = {
    'GARIBALDI': ['GARIBALDI', 'RAPIDO GARIBALDI'],
    'JAMEF': ['JAMEF'],
    'BRASPRESS': ['BRASPRES', 'BRASPRESS'],
    'LOG 100': ['LOG 100', 'LOG100', 'LOG-100'],
    'RODONAVES': ['RODONAVES', 'RTE'],
    'TRANS WELLS': ['TRANS WELLS', 'TRANSWELLS', 'TRANS-WELLS']
}

print(f"--- INICIANDO CAÇA AOS VALORES DE FRETE (VERSÃO FLEXÍVEL) ---")
print(f"Pasta: {pasta_arquivos}\n")

lista_fretes = []

if not os.path.exists(pasta_arquivos):
    print("❌ ERRO: Pasta não encontrada! Verifique o caminho.")
else:
    arquivos = [f for f in os.listdir(pasta_arquivos) if f.lower().endswith('.pdf')]

    for arquivo in arquivos:
        # 1. IDENTIFICA A TRANSPORTADORA
        transportadora_detectada = None
        nome_upper = arquivo.upper()

        for grupo, termos in alvos.items():
            if any(termo in nome_upper for termo in termos):
                transportadora_detectada = grupo
                break

        # Se achou uma transportadora, procura o valor
        if transportadora_detectada:
            # 2. PROCURA O VALOR (AGORA ACEITA "R$" E "RS")
            # A regex abaixo diz: Procure R$ OU RS, seguido de espaço opcional e números
            busca_valor = re.search(r'(?:R\$|RS)\s*([\d\.,]+)', arquivo, re.IGNORECASE)

            valor_final = 0.0

            if busca_valor:
                valor_texto = busca_valor.group(1)
                # Limpa o número (Tira ponto de milhar, troca vírgula por ponto)
                # Ex: 1.200,50 -> 1200.50
                valor_limpo = valor_texto.replace('.', '').replace(',', '.')
                try:
                    valor_final = float(valor_limpo)
                except:
                    valor_final = 0.0

            # Adiciona na lista
            lista_fretes.append({
                'Transportadora': transportadora_detectada,
                'Valor': valor_final,
                'Arquivo': arquivo
            })

    # --- RELATÓRIO FINAL ---
    if lista_fretes:
        df = pd.DataFrame(lista_fretes)

        # Tabela Dinâmica (Soma por Transportadora)
        resumo = df.groupby('Transportadora')['Valor'].sum().sort_values(ascending=False).reset_index()

        print("=" * 60)
        print("RESUMO DE GASTOS COM FRETE (ATUALIZADO)")
        print("=" * 60)
        print(f"{'TRANSPORTADORA':<20} | {'TOTAL (R$)':<15} | {'QTD NOTAS'}")
        print("-" * 60)

        for _, row in resumo.iterrows():
            qtd = len(df[df['Transportadora'] == row['Transportadora']])
            print(f"{row['Transportadora']:<20} | R$ {row['Valor']:<12,.2f} | {qtd}")

        print("-" * 60)
        total_geral = resumo['Valor'].sum()
        print(f"{'TOTAL GERAL':<20} | R$ {total_geral:<12,.2f}")
        print("=" * 60)

        # Verifica se ainda sobrou alguém zerado
        zerados = df[df['Valor'] == 0]
        if not zerados.empty:
            print("\n⚠️ AINDA ZERADOS (Verifique se digitou o valor no nome):")
            for _, row in zerados.iterrows():
                print(f"   > {row['Arquivo']}")
        else:
            print("\n✅ SUCESSO! Todos os valores foram lidos.")

        # Salva Excel para conferência
        df.to_excel("Relatorio_Fretes_Nomes_Final.xlsx", index=False)
        print(f"\n📂 Detalhes salvos em: Relatorio_Fretes_Nomes_Final.xlsx")

    else:
        print("Nenhuma nota dessas transportadoras foi encontrada na pasta.")