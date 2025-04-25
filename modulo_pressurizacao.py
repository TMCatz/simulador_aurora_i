import time
import sys # Usado para forçar a atualização da saída no terminal (efeito visual)

# --- Constantes de Status ---
STATUS_OK = "OPERACIONAL"
STATUS_WARN = "ALERTA"
STATUS_CRIT = "CRÍTICO"


def simular_ciclo_pressurizacao(
    pressao_interna_psi=15.0,
    pressao_externa_psi=0.0,
    tempo_espera_zero_s=10.0, # Tempo em segundos para permanecer em 0 psi
    passo_psi=1.0,            # Quanto a pressão muda a cada passo
    intervalo_passo_s=0.5     # Tempo em segundos entre cada passo da simulação
):
    """
    Simula o ciclo completo de despressurização e repressurização
    de uma câmara de ar (airlock).

    Args:
        pressao_interna_psi (float): Pressão inicial e final dentro da câmara (em psi).
        pressao_externa_psi (float): Pressão alvo durante a despressurização (em psi).
        tempo_espera_zero_s (float): Duração em segundos para manter a pressão externa.
        passo_psi (float): A variação de pressão em cada etapa da simulação (em psi).
        intervalo_passo_s (float): O tempo de espera entre cada etapa (em segundos).

    Returns:
        bool: True se o ciclo completou normalmente, False se foi interrompido ou falhou.
    """

    print("\n--- MÓDULO DE CONTROLE DE PRESSÃO DA CÂMARA DE AR ---")
    print(f"Iniciando ciclo: {pressao_interna_psi:.1f} PSI -> {pressao_externa_psi:.1f} PSI -> {pressao_interna_psi:.1f} PSI")
    print("------------------------------------------------------")

    pressao_atual = pressao_interna_psi # Variável para rastrear pressão durante o ciclo

    try:
        # --- Fase 1: Despressurização ---
        print("\n[FASE 1] Iniciando despressurização...")
        while pressao_atual > pressao_externa_psi:
            # Calcula a próxima pressão, garantindo que não passe do alvo (0.0)
            pressao_proximo_passo = max(pressao_externa_psi, pressao_atual - passo_psi)

            # Exibe a pressão atual (usando \r para sobrescrever a linha anterior)
            # A linha abaixo é a que foi corrigida:
            print(f" Pressão: {pressao_atual:.1f} PSI... Despressurizando", end='\r') # <-- CORRIGIDO
            sys.stdout.flush() # Garante que a linha seja atualizada imediatamente no console

            # Pausa para simular o tempo do passo
            time.sleep(intervalo_passo_s)

            # Atualiza a pressão para o próximo passo
            pressao_atual = pressao_proximo_passo

        # Garante que a pressão final seja exatamente o alvo (0.0 psi) e limpa a linha
        pressao_atual = pressao_externa_psi
        # Os espaços no final limpam caracteres remanescentes de "Despressurizando"
        print(f" Pressão: {pressao_atual:.1f} PSI... Nível externo atingido.  ")
        print("[FASE 1] Despressurização concluída.")

        # --- Fase 2: Manutenção em Pressão Externa (Vácuo Simulado) ---
        print(f"\n[FASE 2] Mantendo pressão em {pressao_externa_psi:.1f} PSI por {tempo_espera_zero_s:.1f} segundos.")
        print("         (Simulando período de atividade externa ou interface com vácuo)")
        # Pausa para simular o tempo de espera
        time.sleep(tempo_espera_zero_s)
        print("[FASE 2] Tempo de manutenção concluído.")

        # --- Fase 3: Repressurização ---
        print("\n[FASE 3] Iniciando repressurização...")
        while pressao_atual < pressao_interna_psi:
             # Calcula a próxima pressão, garantindo que não passe do alvo interno (15.0)
            pressao_proximo_passo = min(pressao_interna_psi, pressao_atual + passo_psi)

             # Exibe a pressão atual (usando \r para sobrescrever a linha anterior)
            print(f" Pressão: {pressao_atual:.1f} PSI... Repressurizando ", end='\r') # Espaço extra opcional no fim
            sys.stdout.flush() # Garante que a linha seja atualizada imediatamente

            # Pausa para simular o tempo do passo
            time.sleep(intervalo_passo_s)

            # Atualiza a pressão para o próximo passo
            pressao_atual = pressao_proximo_passo

        # Garante que a pressão final seja exatamente o alvo interno (15.0 psi) e limpa a linha
        pressao_atual = pressao_interna_psi
        # Os espaços no final limpam caracteres remanescentes de "Repressurizando"
        print(f" Pressão: {pressao_atual:.1f} PSI... Nível interno atingido.   ")
        print("[FASE 3] Repressurização concluída.")

        print("\n--- CICLO DE PRESSURIZAÇÃO DA CÂMARA DE AR COMPLETO ---")
        return True # Indica que o ciclo terminou com sucesso

    except KeyboardInterrupt:
        # Captura interrupção pelo usuário (Ctrl+C)
        print("\n\n! ALERTA: Ciclo de pressurização interrompido manualmente pelo usuário!")
        print(f"  Última pressão registrada: {pressao_atual:.1f} PSI")
        return False # Indica que o ciclo foi interrompido

    except Exception as e:
        # Captura qualquer outro erro inesperado durante o ciclo
        print(f"\n\n! ERRO CRÍTICO no sistema de pressurização: {e}")
        print(f"  Última pressão registrada: {pressao_atual:.1f} PSI")
        return False # Indica que o ciclo falhou

# --- Bloco de Execução Principal (para teste autônomo do módulo) ---
# Este código só roda se você executar este arquivo diretamente (python modulo_pressurizacao.py)
if __name__ == "__main__":
    print("--- Testando o Módulo de Pressurização Independentemente ---")

    # Chama a função principal do módulo com parâmetros de exemplo
    sucesso_do_teste = simular_ciclo_pressurizacao(
        pressao_interna_psi=15.0,
        pressao_externa_psi=0.0,
        tempo_espera_zero_s=5.0,  # Espera 5 segundos em 0 PSI
        passo_psi=1.0,           # Varia 1 PSI por passo
        intervalo_passo_s=0.3    # 0.3 segundos entre cada passo
    )

    # Imprime uma mensagem final baseada no resultado do teste
    if sucesso_do_teste:
        print("\n[Teste] Operação da câmara de ar finalizada com sucesso no teste.")
    else:
        print("\n[Teste] Operação da câmara de ar finalizada com interrupção ou erro no teste.")