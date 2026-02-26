import pandas as pd
import os

# --- CONFIGURAÇÃO: LISTA DE ARQUIVOS AUDITADOS ---
# Coloque aqui o nome exato dos 6 arquivos que ela salvou
arquivos_para_juntar = [
    'Dossie_Auditoria_Julho.xlsx',  # Ajuste o nome se necessário
    'Dossie_Auditoria_08_Agosto.xlsx',
    'Dossie_Auditoria_09_Setembro.xlsx',
    'Dossie_Auditoria_10_Outubro.xlsx',
    'Dossie_Auditoria_11_Novembro.xlsx',
    'Dossie_Auditoria_12_Dezembro.xlsx'
]

arquivo_saida = 'BASE_MESTRA_2025_AUDITADA.xlsx'

print("--- INICIANDO CONSOLIDAÇÃO FINAL (O GRAND FINALE) ---")

lista_dfs = []
total_geral_auditorias = 0

try:
    # 1. LOOP PARA LER CADA MÊS
    for arquivo in arquivos_para_juntar:
        if os.path.exists(arquivo):
            print(f"Lendo: {arquivo}...")

            # Lê o Excel
            df_temp = pd.read_excel(arquivo)

            # Limpeza preventiva (garante que números são números)
            df_temp['Valor'] = pd.to_numeric(df_temp['Valor'], errors='coerce').fillna(0)

            # Soma o valor desse mês para conferência
            total_mes = df_temp['Valor'].sum()
            total_geral_auditorias += total_mes
            print(f"   > Registros: {len(df_temp)} | Total: R$ {total_mes:,.2f}")

            lista_dfs.append(df_temp)
        else:
            print(f"❌ ERRO CRÍTICO: Não encontrei o arquivo '{arquivo}'.")
            print("   Verifique se o nome está certo ou se ele está na mesma pasta do script.")

    # 2. JUNTAR TUDO (MERGE)
    if lista_dfs:
        print("\nUnindo os arquivos...")
        df_final = pd.concat(lista_dfs, ignore_index=True)

        # 3. TRATAMENTO FINAL NA BASE MESTRA
        # Garante data certa
        df_final['Data_Formatada'] = pd.to_datetime(df_final['Data'], dayfirst=True, errors='coerce')

        # Ordena por Data
        df_final = df_final.sort_values(by='Data_Formatada')

        # 4. SALVAR
        # Seleciona as colunas essenciais
        colunas_finais = ['Data', 'Fornecedor', 'CNPJ', 'Valor', 'Arquivo', 'Suspeita_Duplicidade']
        # (Usa colunas que existirem, caso ela tenha deletado alguma)
        colunas_validas = [c for c in colunas_finais if c in df_final.columns]

        df_final[colunas_validas].to_excel(arquivo_saida, index=False)

        print("\n" + "=" * 50)
        print("✅ SUCESSO! BASE MESTRA CRIADA.")
        print(f"📂 Arquivo gerado: {arquivo_saida}")
        print("-" * 50)
        print(f"💰 VALOR TOTAL DO SEMESTRE: R$ {df_final['Valor'].sum():,.2f}")
        print(f"📄 TOTAL DE NOTAS: {len(df_final)}")
        print("=" * 50)

    else:
        print("Nenhum arquivo foi carregado. Verifique os nomes na lista.")

except Exception as e:
    print(f"Ocorreu um erro: {e}")
