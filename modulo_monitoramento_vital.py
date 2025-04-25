import random
import time
import datetime
import sys
import winsound # Para alarme sonoro no Windows (requer instação se não padrão)
import os # Para alarme sonoro em Linux/Mac

# --- Constantes de Status ---
STATUS_NORMAL = "NORMAL"
STATUS_ATENCAO = "ATENÇÃO"
STATUS_CRITICO = "CRÍTICO"

# --- Tripulação (7 membros como na história) ---
TRIPULANTES_IDS = [f"Astronauta_{i+1:02d}" for i in range(7)] # Ex: Astronauta_01, ..., Astronauta_07

# --- Definição de Parâmetros, Unidades e Limites (Valores Exemplo) ---
# Chave: Nome do Parâmetro
# Valor: Dicionário com unidade, limites (normal, atencao_baixo, atencao_alto, critico_baixo, critico_alto),
#        e parâmetros para simulação (media, desvio_padrao)
PARAMETROS_MONITORADOS = {
    # Vitals (por tripulante)
    "Frequencia Cardiaca":    {"unidade": "BPM",      "limites": (60, 100, 50, 110, 40, 120), "sim": (75, 8)},
    "Pressao Sistolica":      {"unidade": "mmHg",     "limites": (90, 120, 85, 140, 80, 160), "sim": (110, 10)},
    "Pressao Diastolica":     {"unidade": "mmHg",     "limites": (60, 80,  55, 90,  50, 100), "sim": (70, 8)},
    "Temperatura Corporal":   {"unidade": "°C",       "limites": (36.1, 37.2, 35.5, 37.8, 35.0, 38.5), "sim": (36.8, 0.3)},
    "Taxa Respiratoria":      {"unidade": "resp/min", "limites": (12, 20, 10, 24, 8, 30),   "sim": (16, 2)},
    "SpO2":                   {"unidade": "%",        "limites": (95, 100, 90, 94.9, 0, 89.9), "sim": (98, 1)}, # Atenção/Crítico só abaixo de 95
    # Ambiente (ECLSS)
    "Pressao Cabine":         {"unidade": "psi",      "limites": (14.5, 14.9, 14.0, 15.1, 13.5, 15.5), "sim": (14.7, 0.1)},
    "Nivel O2":               {"unidade": "%",        "limites": (20.0, 21.5, 19.0, 22.5, 18.0, 23.5), "sim": (20.9, 0.2)},
    "Nivel CO2":              {"unidade": "ppm",      "limites": (400, 1000, 1001, 3000, 0, 5000),  "sim": (800, 200)}, # Atenção/Crítico só acima de 1000/3000
    "Temperatura Ar Cabine":  {"unidade": "°C",       "limites": (20, 24, 18, 26, 16, 28),   "sim": (22, 1)},
    "Umidade Relativa Cabine":{"unidade": "%",        "limites": (40, 60, 30, 70, 20, 80),   "sim": (50, 5)},
}

# Probabilidade de gerar um valor FORA da faixa normal na simulação
PROB_FALHA_SIMULADA = 0.03 # 3% de chance para cada parâmetro gerar leitura anômala

# --- Funções Auxiliares ---

def _simular_leitura_sensor(param_info):
    """Simula a leitura de um sensor com base na média e desvio padrão."""
    media, std_dev = param_info["sim"]
    # Simula leitura com distribuição normal (Gaussiana) para realismo
    valor = random.gauss(media, std_dev)

    # Introduz chance de erro simulado (Atenção ou Crítico)
    # Isso força o sistema a lidar com anomalias ocasionalmente
    if random.random() < PROB_FALHA_SIMULADA:
        # ... (lógica para gerar valor na faixa de Atenção ou Crítico) ...
        # Decide se será Atenção ou Crítico e gera valor na faixa correspondente
        if random.random() < 0.6: # 60% chance de ser Atenção, 40% Crítico
            faixa = "atencao"
            lim_norm_min, lim_norm_max, lim_att_min, lim_att_max, _, _ = param_info["limites"]
            # Gera valor entre limite critico e normal (abaixo ou acima)
            valor = random.uniform(lim_att_min, lim_norm_min) if random.random() < 0.5 else random.uniform(lim_norm_max, lim_att_max)
        else:
            faixa = "critico"
            _, _, lim_att_min, lim_att_max, lim_crit_min, lim_crit_max = param_info["limites"]
             # Gera valor fora do limite de atenção (abaixo ou acima)
            valor = random.uniform(lim_crit_min, lim_att_min) if random.random() < 0.5 else random.uniform(lim_att_max, lim_crit_max)

    # Arredondamento para deixar mais simples
    unidade = param_info["unidade"]
    if unidade in ["°C", "psi", "%"]: # Manter 1 casa decimal para estes
        return round(valor, 1)
    else: # BPM, mmHg, resp/min, ppm - arredondar para inteiro
        return round(valor)

def _verificar_status_parametro(valor, param_info):
    """Avalia o valor lido e retorna o status (NORMAL, ATENCAO, CRITICO)."""
    norm_min, norm_max, att_min, att_max, crit_min, crit_max = param_info["limites"]

    if norm_min <= valor <= norm_max:
        return STATUS_NORMAL
    # Verifica Crítico primeiro (mais importante)
    # Atenção especial para SpO2 e CO2 que só têm limite crítico/atenção em uma direção
    elif (param_info["unidade"] == "%" and param_info["sim"][0] > 90 and valor <= crit_max) or \
         (param_info["unidade"] == "ppm" and valor >= crit_max) or \
         (param_info["unidade"] not in ["%", "ppm"] and (valor <= crit_min or valor >= crit_max)):
         return STATUS_CRITICO
    # Verifica Atenção
    elif (param_info["unidade"] == "%" and param_info["sim"][0] > 90 and att_min <= valor <= att_max) or \
         (param_info["unidade"] == "ppm" and att_min <= valor <= att_max) or \
         (param_info["unidade"] not in ["%", "ppm"] and (att_min <= valor < norm_min or norm_max < valor <= att_max)):
        return STATUS_ATENCAO
    else:
        # Caso raro de cair fora de todas as faixas definidas (pode indicar erro nos limites)
        # Por segurança, classificar como ATENCAO
        # print(f"Debug: Valor {valor} {param_info['unidade']} fora das faixas definidas para {param_info['sim']}.")
        return STATUS_ATENCAO


def _disparar_alarme(mensagens_criticas):
    """Simula um alarme visual e sonoro (se configurado)."""
    timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    print("\n" + "!"*70)
    print(f"!!! ALARME CRÍTICO - SUPORTE DE VIDA / MÉDICO ({timestamp}) !!!")
    for msg in mensagens_criticas:
        print(f"  - {msg}")
    print("!"*70 + "\n")

    # Tentativa de alarme sonoro (opcional e dependente do sistema)
    try:
         if sys.platform == "win32":
             winsound.Beep(1000, 1500) # Frequência 1000Hz por 1.5 segundos
             time.sleep(0.5)
             winsound.Beep(1000, 1500)
         elif sys.platform == "darwin": # MacOS
             os.system('say "Alerta Crítico"') # Requer 'say' command
         else: # Linux
             os.system('spd-say "Alert Critical"') # Requer speech-dispatcher
             # Alternativa: os.system('beep -f 1000 -l 1500') # Requer 'beep' package
    except Exception as e:
          print(f"(Não foi possível disparar alarme sonoro: {e})")


# --- Funções Principais do Módulo ---

def monitorar_condicoes_atuais():
    """
    Executa uma única verificação completa das condições vitais e ambientais,
    retornando dicionários com os status detalhados e uma lista de alarmes.
    """
    status_vital_tripulantes = {}
    status_ambiente_cabine = {}
    alarmes_ativos = []
    status_geral_nave = STATUS_NORMAL # Começa normal, piora se algo for detectado

    # Monitorar Ambiente
    for nome_param, info_param in PARAMETROS_MONITORADOS.items():
        if info_param["unidade"] in ["psi", "%", "ppm", "°C"] and nome_param != "Temperatura Corporal":
            valor = _simular_leitura_sensor(info_param)
            status = _verificar_status_parametro(valor, info_param)
            status_ambiente_cabine[nome_param] = {"valor": valor, "status": status, "unidade": info_param["unidade"]}
            if status == STATUS_CRITICO:
                alarmes_ativos.append(f"Ambiente: {nome_param} {status} ({valor} {info_param['unidade']})")
                status_geral_nave = STATUS_CRITICO
            elif status == STATUS_ATENCAO and status_geral_nave == STATUS_NORMAL:
                status_geral_nave = STATUS_ATENCAO

    # Monitorar Tripulantes
    for tripulante_id in TRIPULANTES_IDS:
        status_tripulante = {}
        status_geral_tripulante = STATUS_NORMAL
        for nome_param, info_param in PARAMETROS_MONITORADOS.items():
             # Filtra apenas parâmetros vitais
             if info_param["unidade"] not in ["psi", "%", "ppm"] and nome_param != "Temperatura Ar Cabine" and nome_param != "Umidade Relativa Cabine":
                valor = _simular_leitura_sensor(info_param)
                status = _verificar_status_parametro(valor, info_param)
                status_tripulante[nome_param] = {"valor": valor, "status": status, "unidade": info_param["unidade"]}
                if status == STATUS_CRITICO:
                    alarmes_ativos.append(f"{tripulante_id}: {nome_param} {status} ({valor} {info_param['unidade']})")
                    status_geral_tripulante = STATUS_CRITICO
                    status_geral_nave = STATUS_CRITICO # Status crítico de um tripulante afeta a nave
                elif status == STATUS_ATENCAO and status_geral_tripulante == STATUS_NORMAL:
                    status_geral_tripulante = STATUS_ATENCAO
                    if status_geral_nave == STATUS_NORMAL: # Atenção de um tripulante eleva o status da nave para Atenção
                         status_geral_nave = STATUS_ATENCAO

        status_vital_tripulantes[tripulante_id] = {"status_geral": status_geral_tripulante, "detalhes": status_tripulante}


    # Dispara o alarme consolidado se houver algum CRÍTICO
    if any(a.endswith(f"{STATUS_CRITICO})") or f" {STATUS_CRITICO} (" in a for a in alarmes_ativos):
        _disparar_alarme(alarmes_ativos)

    return status_geral_nave, status_vital_tripulantes, status_ambiente_cabine, alarmes_ativos


def exibir_relatorio_monitoramento(status_nave, status_tripulantes, status_ambiente):
    """Exibe um relatório formatado das condições atuais."""
    timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    print(f"\n--- Relatório de Condições Vitais e Ambientais [{timestamp}] ---")
    print(f"STATUS GERAL DA NAVE: {status_nave}")

    print("\n-- Status Ambiental (ECLSS) --")
    for param, data in sorted(status_ambiente.items()):
        print(f"  {param:<25}: {data['valor']} {data['unidade']:<4} [{data['status']}]")

    print("\n-- Status Vital da Tripulação --")
    for tripulante, data_tripulante in sorted(status_tripulantes.items()):
        print(f"  {tripulante}: [{data_tripulante['status_geral']}]")
        # Mostra detalhes apenas se não for NORMAL ou se o status geral da nave não for normal
        if data_tripulante['status_geral'] != STATUS_NORMAL or status_nave != STATUS_NORMAL:
            for param, data in sorted(data_tripulante['detalhes'].items()):
                 if data['status'] != STATUS_NORMAL: # Mostra só o que saiu do normal
                    print(f"    - {param:<25}: {data['valor']} {data['unidade']:<4} [{data['status']}]")
    print("----------------------------------------------------------------")


def iniciar_monitoramento_periodico(intervalo_segundos=30):
    """Inicia o ciclo de monitoramento que roda periodicamente."""
    print(f"\n=== INICIANDO MONITORAMENTO PERIÓDICO (Intervalo: {intervalo_segundos}s) ===")
    print("Pressione Ctrl+C para encerrar o monitoramento.")
    try:
        while True:
            print(f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] Executando verificação...")
            status_n, status_t, status_a, alarmes = monitorar_condicoes_atuais()

            # Exibe o relatório completo apenas se houver Alerta ou Crítico,
            # caso contrário, só uma mensagem de status normal.
            if status_n != STATUS_NORMAL:
                exibir_relatorio_monitoramento(status_n, status_t, status_a)
            else:
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Status Geral: NORMAL. Condições nominais.")

            # Espera para o próximo ciclo
            print(f"Próxima verificação em {intervalo_segundos} segundos...")
            time.sleep(intervalo_segundos)

    except KeyboardInterrupt:
        print("\n\n=== MONITORAMENTO PERIÓDICO ENCERRADO PELO USUÁRIO ===")
    except Exception as e:
        print(f"\n\n!!! ERRO CRÍTICO NO LOOP DE MONITORAMENTO: {e} !!!")
        print("=== MONITORAMENTO ENCERRADO ===")

# --- Bloco de Execução Principal (para teste) ---
if __name__ == "__main__":
    # Inicia o monitoramento contínuo com intervalo de 20 segundos
    iniciar_monitoramento_periodico(intervalo_segundos=20)

    # Para executar apenas uma vez:
    # print("Executando verificação única...")
    # status_n, status_t, status_a, alarmes = monitorar_condicoes_atuais()
    # exibir_relatorio_monitoramento(status_n, status_t, status_a)
    # print("\nVerificação única concluída.")