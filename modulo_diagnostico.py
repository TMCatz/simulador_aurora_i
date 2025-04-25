import random
import time
import sys

# --- Constantes de Status ---
# Usar constantes torna o código mais legível e fácil de manter
STATUS_OPERACIONAL = "OPERACIONAL"
STATUS_ALERTA = "ALERTA"
STATUS_CRITICO = "CRÍTICO"
STATUS_VERIFICANDO = "VERIFICANDO..."
STATUS_DESCONHECIDO = "DESCONHECIDO"

# --- Definição dos Subsistemas da Espaçonave ---
# Lista expandida para maior realismo
SUBSISTEMAS_PARA_VERIFICAR = [
    # Propulsão
    "Propulsor Principal (Motor Nuclear Térmico)",
    "Propulsores RCS (Controle de Atitude e Manobras)",
    "Tanques de Propelente",
    # Estrutura e Mecanismos
    "Integridade Estrutural (Casco)",
    "Escotilhas e Selos",
    "Trem de Pouso (se aplicável à fase)",
    "Braço Robótico (se houver)",
    # Energia
    "Geração de Energia (Reator/Painéis Solares)",
    "Baterias Principais",
    "Distribuição de Energia (Linhas e Conversores)",
    # Suporte à Vida (ECLSS)
    "Controle Atmosférico (O2/CO2/Umidade)",
    "Sistema de Gerenciamento de Água",
    "Controle de Temperatura Interna",
    "Monitoramento de Pressão da Cabine",
    # Comunicações
    "Antena de Alto Ganho (Comunicação Terra)",
    "Antena de Baixo Ganho (Backup/Proximidade)",
    "Sistema de Comunicação Interna (Intercom)",
    # Navegação, Guiagem e Controle (GNC)
    "Computador Principal de Voo",
    "Computador de Voo de Backup",
    "Sensores de Navegação (Estelar, Solar, IMU)",
    "Algoritmos de Guiagem e Controle",
    # Sistemas Térmicos
    "Sistema de Controle Térmico Externo (Radiadores)",
    "Sistema de Controle Térmico Interno (Loops de Fluido)",
    # Outros
    "Computadores de Bordo e Rede de Dados",
    "Sistema de Detecção e Supressão de Incêndio",
    "Proteção Contra Radiação Cósmica",
    "Sistema de Gerenciamento de Resíduos"
]

# --- Simulação de Verificação ---

def _simular_verificacao_subsistema(nome_subsistema):
    """
    Simula a verificação de um único subsistema, retornando um status aleatório
    com probabilidades definidas.
    """
    # Probabilidades: Mais chance de estar OK, menos de Crítico
    prob_operacional = 0.85  # 85%
    prob_alerta = 0.10       # 10%
    prob_critico = 0.05      # 5%

    # Sorteia um número entre 0 e 1
    resultado_random = random.random()

    # Simula um pequeno atraso para a verificação
    time.sleep(random.uniform(0.1, 0.3))

    # Determina o status com base no sorteio e probabilidades
    if resultado_random < prob_operacional:
        return STATUS_OPERACIONAL
    elif resultado_random < prob_operacional + prob_alerta:
        return STATUS_ALERTA
    else:
        return STATUS_CRITICO

# --- Funções Principais do Módulo ---

def executar_diagnostico_completo():
    """
    Executa a verificação de todos os subsistemas listados e
    retorna o painel de controle (dicionário) com os status.
    """
    print("\n--- INICIANDO DIAGNÓSTICO GERAL DA AURORA I ---")
    painel_controle_status = {}
    tempo_inicio = time.time()

    for i, subsistema in enumerate(SUBSISTEMAS_PARA_VERIFICAR):
        # Mostra o progresso
        progresso = f"[{i+1}/{len(SUBSISTEMAS_PARA_VERIFICAR)}]"
        print(f"{progresso} Verificando: {subsistema} ...", end=" ")
        sys.stdout.flush() # Força a escrita no terminal

        status_atual = _simular_verificacao_subsistema(subsistema)
        painel_controle_status[subsistema] = status_atual

        # Limpa a parte do "..." e escreve o status final na mesma linha
        print(f"\r{progresso} Verificado : {subsistema} - Status: {status_atual}{' '*10}") # Espaços limpam a linha

    tempo_fim = time.time()
    duracao = tempo_fim - tempo_inicio
    print("-------------------------------------------------")
    print(f"Diagnóstico Completo Concluído em {duracao:.2f} segundos.")
    print("-------------------------------------------------")

    return painel_controle_status

def exibir_painel_controle(painel_status):
    """
    Exibe de forma organizada o status de cada subsistema no painel de controle.
    """
    print("\n--- PAINEL DE CONTROLE DE STATUS DA ESPAÇONAVE ---")
    if not painel_status:
        print("Nenhum dado de diagnóstico disponível.")
        return

    # Agrupa sistemas por status para melhor visualização
    sistemas_por_status = {
        STATUS_CRITICO: [],
        STATUS_ALERTA: [],
        STATUS_OPERACIONAL: [],
        STATUS_DESCONHECIDO: []
    }

    max_len_nome = 0
    for subsistema, status in painel_status.items():
        if status in sistemas_por_status:
            sistemas_por_status[status].append(subsistema)
        else:
            # Caso algum status inesperado apareça
            sistemas_por_status[STATUS_DESCONHECIDO].append(subsistema)
        if len(subsistema) > max_len_nome:
             max_len_nome = len(subsistema)

    # Define um indicador visual simples
    indicadores = {
        STATUS_CRITICO: "[ X ]",
        STATUS_ALERTA:  "[ ! ]",
        STATUS_OPERACIONAL: "[ OK ]",
        STATUS_DESCONHECIDO:"[ ? ]"
    }

    print("\n--- STATUS CRÍTICO (Ação Imediata!) ---")
    if sistemas_por_status[STATUS_CRITICO]:
        for item in sorted(sistemas_por_status[STATUS_CRITICO]):
             print(f"{indicadores[STATUS_CRITICO]} {item:<{max_len_nome}} : {STATUS_CRITICO}")
    else:
        print("Nenhum sistema em estado crítico.")

    print("\n--- STATUS DE ALERTA (Monitorar/Manutenção) ---")
    if sistemas_por_status[STATUS_ALERTA]:
        for item in sorted(sistemas_por_status[STATUS_ALERTA]):
            print(f"{indicadores[STATUS_ALERTA]} {item:<{max_len_nome}} : {STATUS_ALERTA}")
    else:
        print("Nenhum sistema em alerta.")

    print("\n--- STATUS OPERACIONAL ---")
    if sistemas_por_status[STATUS_OPERACIONAL]:
        for item in sorted(sistemas_por_status[STATUS_OPERACIONAL]):
            print(f"{indicadores[STATUS_OPERACIONAL]} {item:<{max_len_nome}} : {STATUS_OPERACIONAL}")
    else:
        print("Nenhum sistema operacional reportado (verificar diagnóstico).")

    if sistemas_por_status[STATUS_DESCONHECIDO]:
         print("\n--- STATUS DESCONHECIDO ---")
         for item in sorted(sistemas_por_status[STATUS_DESCONHECIDO]):
             print(f"{indicadores[STATUS_DESCONHECIDO]} {item:<{max_len_nome}} : {STATUS_DESCONHECIDO}")

    print("-------------------------------------------------")

# --- Bloco de Execução Principal (para teste) ---
if __name__ == "__main__":
    try:
        # Executa o diagnóstico
        painel_atualizado = executar_diagnostico_completo()

        # Exibe os resultados
        exibir_painel_controle(painel_atualizado)

        # Exemplo de como acessar um status específico depois, se necessário:
        # status_propulsor = painel_atualizado.get("Propulsor Principal (Motor Nuclear Térmico)", STATUS_DESCONHECIDO)
        # print(f"\nStatus verificado do Propulsor Principal: {status_propulsor}")

    except KeyboardInterrupt:
        print("\n\nDiagnóstico interrompido pelo usuário.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado durante o diagnóstico: {e}")