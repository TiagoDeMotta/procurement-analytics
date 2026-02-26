import pandas as pd
import os

# --- CONFIGURAÇÃO ---
arquivo_entrada = 'Relatorio_Compras_Validado.xlsx'

# Lista dos meses que faltam analisar (Agosto a Dezembro)
meses_para_auditar = {
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
}

print(f"--- INICIANDO GERAÇÃO DOS DOSSIÊS (AGO-DEZ) ---")

try:
    # 1. Carrega a base geral
    df = pd.read_excel(arquivo_entrada, sheet_name='Detalhado')

    # Conversões obrigatórias (Data e Dinheiro)
    df['Data_Formatada'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)

    # 2. LOOP AUTOMÁTICO PELOS MESES
    for mes_numero, mes_nome in meses_para_auditar.items():
        print(f"\nprocessando Mês {mes_numero} ({mes_nome})...")

        # Filtra o mês da vez
        df_mes = df[df['Data_Formatada'].dt.month == mes_numero].copy()

        if df_mes.empty:
            print(f"   > Aviso: Nenhuma nota encontrada para {mes_nome}.")
            continue

        # 3. IDENTIFICA DUPLICIDADES (Igual fizemos em Julho)
        colunas_chave = ['Fornecedor', 'Data', 'Valor']
        duplicadas = df_mes[df_mes.duplicated(subset=colunas_chave, keep=False)]

        # Marca a coluna de alerta
        df_mes['Suspeita_Duplicidade'] = df_mes.duplicated(subset=colunas_chave, keep=False).map(
            {True: 'SIM', False: ''})

        # Estatísticas rápidas
        qtd_duplicadas = len(duplicadas)
        total_gasto = df_mes['Valor'].sum()
        print(f"   > Total Notas: {len(df_mes)}")
        print(f"   > Total Gasto: R$ {total_gasto:,.2f}")
        if qtd_duplicadas > 0:
            print(f"   > ⚠️ ALERTA: {qtd_duplicadas} notas suspeitas de duplicidade marcadas com 'SIM'.")
        else:
            print(f"   > ✅ Nenhuma duplicidade óbvia encontrada.")

        # 4. SALVA O ARQUIVO INDIVIDUAL
        nome_arquivo = f"Dossie_Auditoria_{mes_numero:02d}_{mes_nome}.xlsx"

        # Seleciona e ordena colunas
        colunas_finais = ['Suspeita_Duplicidade', 'Data', 'Valor', 'Fornecedor', 'CNPJ', 'Arquivo']
        # Remove a coluna temporária de data formatada para não confundir no Excel
        df_export = df_mes[colunas_finais].sort_values(by=['Fornecedor', 'Data'])

        df_export.to_excel(nome_arquivo, index=False)
        print(f"   > 📂 Arquivo gerado: {nome_arquivo}")

    print("\n" + "=" * 50)
    print("✅ PROCESSO CONCLUÍDO!")
    print("Agora você tem 5 novos arquivos Excel na pasta.")
    print("Abra um por um, corrija os erros e salve com o mesmo nome.")
    print("=" * 50)

except FileNotFoundError:
    print(f"ERRO: Não encontrei o arquivo '{arquivo_entrada}'.")
except Exception as e:
    print(f"ERRO: {e}")