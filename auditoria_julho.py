import pandas as pd
import os

# --- CONFIGURAÇÃO ---
arquivo_entrada = 'Relatorio_Compras_Validado.xlsx'
arquivo_saida = 'Dossie_Auditoria_Julho.xlsx'
mes_alvo = 7  # Julho

try:
    print(f"--- INICIANDO AUDITORIA DO MÊS {mes_alvo:02d} ---")

    # 1. Carrega os dados
    df = pd.read_excel(arquivo_entrada, sheet_name='Detalhado')

    # Converte coluna de datas para o formato que o Python entende
    df['Data_Formatada'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')

    # Converte valor para garantir que é número
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)

    # 2. FILTRO: SOMENTE MÊS 07
    df_julho = df[df['Data_Formatada'].dt.month == mes_alvo].copy()

    if df_julho.empty:
        print(f"❌ Nenhuma nota encontrada para o mês {mes_alvo}.")
    else:
        total_julho = df_julho['Valor'].sum()
        qtd_julho = len(df_julho)

        print(f"\n📊 RESUMO DE JULHO:")
        print(f"   > Total de Notas: {qtd_julho}")
        print(f"   > Valor Total: R$ {total_julho:,.2f}")

        # 3. CAÇA ÀS DUPLICIDADES (O PULO DO GATO)
        # Verifica se existem linhas com MESMO Fornecedor, MESMA Data e MESMO Valor
        colunas_chave = ['Fornecedor', 'Data', 'Valor']

        # duplicated(keep=False) marca TODAS as ocorrências (a original e a cópia)
        duplicadas = df_julho[df_julho.duplicated(subset=colunas_chave, keep=False)]

        print(f"\n🔍 ANÁLISE DE DUPLICIDADE:")
        if not duplicadas.empty:
            print(f"⚠️ ATENÇÃO: Encontrei {len(duplicadas)} registros suspeitos de duplicidade!")
            print("   (Isso acontece quando Fornecedor + Data + Valor são idênticos)")
            print("-" * 50)

            # Mostra na tela as duplicadas para conferência rápida
            for i, row in duplicadas.iterrows():
                print(
                    f"   🚩 R$ {row['Valor']:<10} | {row['Data']} | {row['Fornecedor'][:30]}... | Arq: {row['Arquivo']}")

            # Marca no Excel quem é duplicado para facilitar a vida dela
            df_julho['Suspeita_Duplicidade'] = df_julho.duplicated(subset=colunas_chave, keep=False).map(
                {True: 'SIM', False: ''})

        else:
            print("✅ Nenhuma duplicidade óbvia encontrada (Fornecedor+Data+Valor iguais).")
            df_julho['Suspeita_Duplicidade'] = ''

        # 4. RECORRÊNCIA NO MÊS
        recorrencia = df_julho['Fornecedor'].value_counts().head(5)
        print(f"\n🔄 FORNECEDORES MAIS RECORRENTES EM JULHO:")
        for nome, qtd in recorrencia.items():
            print(f"   > {nome}: {qtd} notas")

        # 5. SALVAR O DOSSIÊ
        # Organiza as colunas para ficar fácil de ler
        colunas_finais = ['Suspeita_Duplicidade', 'Data', 'Valor', 'Fornecedor', 'CNPJ', 'Arquivo']
        df_export = df_julho[colunas_finais].sort_values(by=['Fornecedor', 'Data'])

        df_export.to_excel(arquivo_saida, index=False)

        print("\n" + "=" * 50)
        print(f"📂 ARQUIVO GERADO: {arquivo_saida}")
        print("Abra este Excel. As linhas marcadas com 'SIM' na coluna A são as duplicadas.")
        print("=" * 50)

except FileNotFoundError:
    print("Erro: Arquivo original não encontrado. Rode o 'analisador' primeiro.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")