import time
import sys
import math
import random
import datetime # Importado para uso no _adicionar_log

# --- Constantes da Simulação e da Nave ---
DISTANCIA_INICIAL_MARTE_KM = 225_000_000
VELOCIDADE_MAX_COMANDO_KMH = 80_000    # Limite normal
VELOCIDADE_INICIAL_KMH = 15_000

# Capacidade e Consumo (UAC)
CAPACIDADE_TOTAL_UAC = 100_000.0       # Capacidade total de combustível (UAC)
# Fator de custo para MUDAR velocidade (manobra) - Mantido baixo para permitir ajustes frequentes
FATOR_CUSTO_MANOBRA_UAC = 0.005        # Custo para mudar velocidade

# --- Consumo HORÁRIO --- Aqui foi feita uma escolha de consumo fixo ou proporcional
# (Proporcional: Consumo proporcional à velocidade, Fixo: Consumo fixo por hora)
# Alt 1: Proporcional (Fator baixo)
CONSUMO_FIXO_POR_HORA_UAC = None
FATOR_CONSUMO_HORARIO_UAC = 0.0005
# Alt 2: Fixo (Simples) Consumo FIXO por hora - Simplifica cálculo, valor baixo para longa duração
# FATOR_CONSUMO_HORARIO_UAC = None
# CONSUMO_FIXO_POR_HORA_UAC = 10.0

# --- Constantes MODO ECO ---
VELOCIDADE_MAX_ECO_KMH = 10_000
# Consumo Eco (Escolha UMA alternativa, correspondente à acima)
# Ambas são auto-explicativas, mas a primeira é par um valor mais baixo e a segunda é valor fixo
# (Proporcional: Consumo proporcional à velocidade, Fixo: Consumo fixo por hora)
# Alt 1 Eco: Proporcional (Mais baixo)
CONSUMO_FIXO_POR_HORA_ECO_UAC = None
FATOR_CONSUMO_HORARIO_ECO_UAC = 0.0001
# Alt 2 Eco: Fixo (Mais baixo)
# FATOR_CONSUMO_HORARIO_ECO_UAC = None
# CONSUMO_FIXO_POR_HORA_ECO_UAC = 2.0

# --- Constantes EVENTOS ALEATÓRIOS ---
PROBABILIDADE_EVENTO_POR_PASSO = 0.07 # 7% de chance de evento por passo
# (Aumentar para 0.10 ou mais para testes de eventos)

# --- Controle da Simulação de Tempo ---
INTERVALO_REAL_S = 5 # Intervalo real entre simulações (em segundos)
# (Aumentar para 10s ou mais para testes de eventos)
HORAS_SIMULADAS_POR_INTERVALO = 240 # 10 dias (240h) por intervalo de 5s
# (Aumentar para 1 dia ou mais para testes de eventos)

# --- Constantes Visuais ---
LARGURA_GAUGE = 20
# Largura do gauge de combustível e progresso (em caracteres)

# --- Classe Principal ---
class PainelComandosNave:
    """Gerencia o estado e as interações do painel de comandos da espaçonave."""

    def __init__(self):
        self.combustivel_uac = float(CAPACIDADE_TOTAL_UAC)
        self.distancia_marte_km = float(DISTANCIA_INICIAL_MARTE_KM)
        self.velocidade_atual_kmh = float(VELOCIDADE_INICIAL_KMH)
        self.em_viagem = True
        self.log_eventos = []
        self.modo_eco_ativo = False

    def _adicionar_log(self, mensagem):
        timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S") # Formato: dd/mm/aa HH:MM:SS
        # Adiciona o timestamp à mensagem e armazena no log
        log_completo = f"[{timestamp}] {mensagem}"
        self.log_eventos.append(log_completo)
        print(f"LOG: {mensagem}") # Mostra apenas a mensagem no console para brevidade

    def get_combustivel_percentual(self):
        return max(0.0, min(100.0, (self.combustivel_uac / CAPACIDADE_TOTAL_UAC) * 100.0)) # Retorna percentual de combustível

    def exibir_status_painel(self):
        print("\n" + "=" * 55)
        print("========= PAINEL DE COMANDOS - AURORA I =========")
        print("=" * 55)

        # Gauge de Combustível
        # Calcula proporção preenchida da barra baseado no percentual
        percentual_comb = self.get_combustivel_percentual() # Percentual de combustível
        preenchido_comb = int(percentual_comb / 100 * LARGURA_GAUGE) # Preenchido do gauge
        # ... (criação do gauge) ...
        vazio_comb = LARGURA_GAUGE - preenchido_comb
        gauge_comb = f"[{'#' * preenchido_comb}{'-' * vazio_comb}]"
        print(f" Combustível {gauge_comb} : {percentual_comb:.2f}% ({int(self.combustivel_uac):,} UAC)")

        # Gauge de Progresso
        if DISTANCIA_INICIAL_MARTE_KM > 0:
            progresso_pct = max(0.0, min(100.0, ((DISTANCIA_INICIAL_MARTE_KM - self.distancia_marte_km) / DISTANCIA_INICIAL_MARTE_KM) * 100.0))
        else:
            progresso_pct = 100.0 if self.distancia_marte_km <= 0 else 0.0
        preenchido_dist = int(progresso_pct / 100 * LARGURA_GAUGE)
        vazio_dist = LARGURA_GAUGE - preenchido_dist
        gauge_dist = f"[{'>' * preenchido_dist}{'.' * vazio_dist}]"
        print(f" Progresso   {gauge_dist} : {progresso_pct:.1f}% ({int(DISTANCIA_INICIAL_MARTE_KM - self.distancia_marte_km):,} / {int(DISTANCIA_INICIAL_MARTE_KM):,} km)")
        # Distância até Marte (em km)
        print(f" Velocidade Atual           : {int(self.velocidade_atual_kmh):,} km/h")
        print(f" Distância até Marte        : {int(self.distancia_marte_km):,} km")

        # ETA (Estimativa de Tempo de Chegada)
        # Calcula o tempo estimado de chegada (ETA) em dias e horas
        eta_str = "N/A (parado ou chegou)"
        # Só calcula ETA se houver velocidade e distância restante
        if self.velocidade_atual_kmh > 0 and self.distancia_marte_km > 0:
            tempo_horas = self.distancia_marte_km / self.velocidade_atual_kmh
            # Converte total de horas em dias e horas restantes
            dias = int(tempo_horas // 24)
            horas_restantes = int(tempo_horas % 24)
            eta_str = f"{dias} dias, {horas_restantes} horas"
        print(f" ETA (Estimativa)           : {eta_str}")

        # Modo Eco
        # Exibe o status do modo econômico e o limite de velocidade se ativo
        status_eco = "ATIVADO" if self.modo_eco_ativo else "DESATIVADO"
        limite_eco_str = f"(Max: {int(VELOCIDADE_MAX_ECO_KMH):,} km/h)" if self.modo_eco_ativo else ""
        print(f" Modo Econômico             : {status_eco} {limite_eco_str}")

        status_viagem = "EM CURSO" if self.em_viagem else "CONCLUÍDA / INTERROMPIDA"
        print(f" Status da Viagem           : {status_viagem}")
        if self.combustivel_uac <= 0 and self.distancia_marte_km > 0:
             print(" !!! ALERTA: SEM COMBUSTÍVEL !!!")
        print("="*55)

    def tentar_definir_velocidade(self, entrada_usuario): #"""Tenta definir a velocidade desejada."""
        """Tenta definir a velocidade desejada. Retorna True se sucesso, False se falha."""
        if not self.em_viagem:
            self._adicionar_log("Comando ignorado: Viagem não ativa.")
            return False # Retorna False para indicar falha

        try:
            velocidade_desejada = float(entrada_usuario)
        except ValueError:
            if entrada_usuario.strip():
                 self._adicionar_log(f"Erro: Velocidade '{entrada_usuario}' inválida.")
            return False

        limite_atual = VELOCIDADE_MAX_ECO_KMH if self.modo_eco_ativo else VELOCIDADE_MAX_COMANDO_KMH
        velocidade_ajustada = False
        # Se a velocidade desejada é negativa, retorna erro
        if velocidade_desejada < 0:
            self._adicionar_log("Erro: Velocidade não pode ser negativa.")
            return False
        if velocidade_desejada > limite_atual:
            # Informa e ajusta para o limite máximo permitido no modo atual
            self._adicionar_log(f"Alerta: Velocidade solicitada ({int(velocidade_desejada):,} km/h) excede limite atual ({int(limite_atual):,} km/h). Ajustando.")
            velocidade_desejada = limite_atual
            velocidade_ajustada = True
        # --- Calcular custo da manobra (Delta-V) ---
        # Custo é proporcional à diferença entre velocidade atual e desejada
        delta_v = abs(velocidade_desejada - self.velocidade_atual_kmh)
        custo_manobra = delta_v * FATOR_CUSTO_MANOBRA_UAC

        if delta_v == 0 and not velocidade_ajustada:
            return True # Já na velocidade correta
        # Se a velocidade desejada é igual à atual, não faz nada
        if self.combustivel_uac >= custo_manobra:
            self.combustivel_uac -= custo_manobra
            self._adicionar_log(f"Manobra: Velocidade {'ajustada para' if velocidade_ajustada else 'alterada para'} {int(velocidade_desejada):,} km/h. Custo: {custo_manobra:.2f} UAC.")
            self.velocidade_atual_kmh = velocidade_desejada
            return True # Manobra bem sucedida 
        else:
            self._adicionar_log(f"Falha Manobra: Combustível insuficiente. Necessário: {custo_manobra:.2f} UAC.")
            return False # Manobra falhou por falta de combustível

    def _processar_eventos_aleatorios(self):
        """Verifica e processa eventos aleatórios. Retorna a msg do evento ou None."""
        evento_msg = None
        # Verifica se deve tentar um evento (só se estiver em viagem)
        if self.em_viagem and random.random() < PROBABILIDADE_EVENTO_POR_PASSO:
            tipo_evento = random.choice(['micrometeorito', 'falha_menor', 'tempestade_solar'])

            if tipo_evento == 'micrometeorito':
                perda_comb = random.uniform(50, 250)
                comb_anterior = self.combustivel_uac
                self.combustivel_uac = max(0.0, self.combustivel_uac - perda_comb)
                perda_real = comb_anterior - self.combustivel_uac
                evento_msg = f"EVENTO: Impacto de micrometeorito! Perda de {perda_real:.2f} UAC."
            elif tipo_evento == 'falha_menor':
                 sistemas_exemplo = ["Sensor Navegação", "Bomba Refrigerante", "Regulador Tensão", "Antena Baixo Ganho", "Filtro CO2", "Interface Diagnóstico"]
                 sistema_afetado = random.choice(sistemas_exemplo)
                 evento_msg = f"EVENTO: Anomalia menor: {sistema_afetado}. Recomenda-se diagnóstico."
            elif tipo_evento == 'tempestade_solar':
                 evento_msg = "EVENTO: Tempestade solar! Monitore comunicações e radiação."

            if evento_msg:
                self._adicionar_log(evento_msg) # Loga o evento ocorrido

        return evento_msg # Retorna a mensagem para quem chamou decidir se pausa

    def simular_passagem_tempo(self, horas_a_simular):
        """Simula voo, consumo, distância e eventos. Retorna msg de evento, se houver."""
        if not self.em_viagem: return None
        if self.combustivel_uac <= 0 and self.velocidade_atual_kmh <= 0: return None # Já parado sem combustível

        # Verifica se acabou o combustível ANTES de calcular consumo/distância
        if self.combustivel_uac <= 0:
            if self.velocidade_atual_kmh > 0: # Estava se movendo, mas agora para
                self._adicionar_log("Combustível esgotado. Nave à deriva.")
                self.velocidade_atual_kmh = 0
            return None # Não consome nem se move mais

        # 1. Consumo Operacional
        consumo_neste_passo = 0
        fator_consumo_usado = 0
        if self.modo_eco_ativo:
            # Lógica de consumo ECO (usar a alternativa configurada - Fixa ou Proporcional)
            # ... (cálculo usando constantes _ECO_) ...
            if CONSUMO_FIXO_POR_HORA_ECO_UAC is not None: consumo_neste_passo = CONSUMO_FIXO_POR_HORA_ECO_UAC * horas_a_simular
            elif FATOR_CONSUMO_HORARIO_ECO_UAC is not None: consumo_neste_passo = self.velocidade_atual_kmh * FATOR_CONSUMO_HORARIO_ECO_UAC * horas_a_simular
        else:
            # Lógica de consumo Normal (usar a alternativa configurada - Fixa ou Proporcional)
            # ... (cálculo usando constantes normais) ...
             if CONSUMO_FIXO_POR_HORA_UAC is not None: consumo_neste_passo = CONSUMO_FIXO_POR_HORA_UAC * horas_a_simular
             elif FATOR_CONSUMO_HORARIO_UAC is not None: consumo_neste_passo = self.velocidade_atual_kmh * FATOR_CONSUMO_HORARIO_UAC * horas_a_simular

        combustivel_anterior = self.combustivel_uac
        self.combustivel_uac = max(0.0, self.combustivel_uac - consumo_neste_passo) # Garante que combustível não fique negativo
        consumo_real = combustivel_anterior - self.combustivel_uac

        # 2. Atualização da Distância
        distancia_percorrida = self.velocidade_atual_kmh * horas_a_simular
        distancia_anterior = self.distancia_marte_km
        self.distancia_marte_km = max(0.0, self.distancia_marte_km - distancia_percorrida)

        # Log do passo (opcional, pode poluir muito o log)
        # print(f"\n... Simulando {horas_a_simular}h ... D: {int(distancia_percorrida):,}km | C: {consumo_real:.2f} UAC")

        # 3. Processar Eventos Aleatórios
        # Chama a função que pode ou não disparar um evento e retorna a mensagem
        mensagem_evento = self._processar_eventos_aleatorios() # Captura a mensagem

        # 4. Verificar Chegada
        # Verifica se cruzou o "marco zero" de distância neste passo
        if self.distancia_marte_km <= 0 and distancia_anterior > 0: # Só loga na chegada
            # ... (lógica de chegada) ...
            self._adicionar_log("***** CHEGADA EM MARTE CONFIRMADA! *****")
            self.velocidade_atual_kmh = 0
            self.em_viagem = False # Finaliza a viagem

        # Retorna a mensagem do evento para o loop principal decidir sobre a pausa
        return mensagem_evento # Retorna o evento que ocorreu neste passo

    def _pausar_por_evento(self, mensagem_evento):
        """Função auxiliar para padronizar a pausa por evento."""
        if mensagem_evento:
            print("\n" + "+" * 35)
            print("    !!! ATENÇÃO: EVENTO !!!")
            print(f"    {mensagem_evento}")
            print("+" * 35)
            input("    Pressione Enter para continuar...")
            return True # Indica que houve pausa
        return False # Indica que não houve pausa


    def iniciar_interface(self):
        """Inicia o loop principal da interface do painel de comandos."""
        self._adicionar_log("Painel de Comandos Ativado.")
        try:
            while self.em_viagem:
                # ... (exibe status) ...
                # ... (prompt de entrada) ...
                self.exibir_status_painel()

                # --- Processamento de Entrada e Simulação ---
                print(f"\nPróxima atualização em {INTERVALO_REAL_S}s. Simulando {HORAS_SIMULADAS_POR_INTERVALO}h.")
                prompt = f"Comandos: [Velocidade], 'impulso N', 'eco on/off', 'sair': "
                entrada = input(prompt).strip().lower()

                executou_impulso = False
                mensagem_evento_passo = None

                if entrada == 'sair':
                    self._adicionar_log("Comando 'sair' recebido.")
                    self.em_viagem = False; break

                elif entrada == 'eco on':
                    if not self.modo_eco_ativo:
                        self.modo_eco_ativo = True; self._adicionar_log("Modo Econômico ATIVADO.")
                        if self.velocidade_atual_kmh > VELOCIDADE_MAX_ECO_KMH:
                             self._adicionar_log(f"Reduzindo velocidade para limite Eco...")
                             self.tentar_definir_velocidade(str(VELOCIDADE_MAX_ECO_KMH))
                    else: self._adicionar_log("Modo Econômico já ativado.")
                    if self.em_viagem: mensagem_evento_passo = self.simular_passagem_tempo(HORAS_SIMULADAS_POR_INTERVALO)

                elif entrada == 'eco off':
                    if self.modo_eco_ativo: self.modo_eco_ativo = False; self._adicionar_log("Modo Econômico DESATIVADO.")
                    else: self._adicionar_log("Modo Econômico já desativado.")
                    if self.em_viagem: mensagem_evento_passo = self.simular_passagem_tempo(HORAS_SIMULADAS_POR_INTERVALO)
                
                # --- Processamento de Comando: Impulso ---
                elif entrada.startswith('impulso '):
                    # ... (parsing de N) ...
                    # Verifica se o comando é 'impulso N' e tenta extrair o número de passos
                    # Se não for, ignora e continua
                    partes = entrada.split()
                    if len(partes) == 2:
                        try:
                            num_passos = int(partes[1])
                            if num_passos > 0:
                                executou_impulso = True
                                print(f"\n>>> Iniciando Impulso de {num_passos} passo(s)...")
                                passos_completos = 0
                                for i in range(num_passos):
                                # Verifica condições de parada ANTES de simular o passo i
                                # ... (if not self.em_viagem or self.combustivel_uac <= 0: break) ...
                                    if not self.em_viagem: print(f"\n... Impulso interrompido no passo {i+1}: Fim da viagem."); break
                                    # Simula passo e captura possível evento
                                    mensagem_evento_impulso = self.simular_passagem_tempo(HORAS_SIMULADAS_POR_INTERVALO)
                                    passos_completos += 1
                                    print('.', end='', flush=True)
                                    # PAUSA se evento ocorreu neste passo do impulso
                                    if self._pausar_por_evento(mensagem_evento_impulso):
                                        # ... (lógica de pausa e retomada) ...
                                        print("... Retomando impulso ...") # Mensagem de continuação
                                        # Verifica se a viagem terminou APÓS o passo simulado
                                        # ... (if not self.em_viagem: break) ...
                                    # --- Fim do Loop Interno do Impulso ---
                                # --- Fim Processamento Impulso ---

                                    if not self.em_viagem: break # Sai se simular_passagem_tempo encerrou a viagem
                                print(f"\n>>> Impulso concluído após {passos_completos} passo(s).")
                            else: self._adicionar_log("Erro: Número de passos para 'impulso' deve ser > 0.")
                        except ValueError: self._adicionar_log(f"Erro: Valor inválido para N em 'impulso N'.")
                    else: self._adicionar_log("Erro: Comando 'impulso N' inválido.")

                # --- Processamento Comando: Velocidade ou Vazio (Passo Único) ---
                elif entrada: # Tenta definir velocidade
                # ... (chama tentar_definir_velocidade) ...
                # Simula passo único após tentativa
                    if self.tentar_definir_velocidade(entrada): # Se a manobra foi ok (ou não necessária)
                        if self.em_viagem: mensagem_evento_passo = self.simular_passagem_tempo(HORAS_SIMULADAS_POR_INTERVALO)
                    # else: não simula tempo se a manobra falhou por falta de combustível

                else: # Entrada vazia, apenas simula um passo
                    if self.em_viagem: mensagem_evento_passo = self.simular_passagem_tempo(HORAS_SIMULADAS_POR_INTERVALO)

                # --- Pausa por Evento (Passo Único) ---
                # Pausa por evento ocorrido em passo único (fora do impulso)
                houve_pausa_evento = self._pausar_por_evento(mensagem_evento_passo)

                # --- Pausa Temporizada Normal ---
                # Pausa real só se ainda em viagem, não executou impulso e não pausou por evento
                if self.em_viagem and not executou_impulso and not houve_pausa_evento:
                    time.sleep(INTERVALO_REAL_S)

    # --- Fim do Loop Principal ---

        except KeyboardInterrupt: self._adicionar_log("Interrupção manual (Ctrl+C)."); self.em_viagem = False
        except Exception as e: self._adicionar_log(f"ERRO INESPERADO: {e}"); self.em_viagem = False
        finally:
            print("\n" + "=" * 55)
            print("=========== PAINEL DE COMANDOS DESATIVADO ===========")
            self.exibir_status_painel()
            print("=" * 55)


# --- Bloco de Execução Principal (para teste autônomo) ---
if __name__ == "__main__":
     print("--- Testando Módulo Painel de Comandos Independentemente ---")
     # Exemplo: Forçar consumo fixo para teste
     FATOR_CONSUMO_HORARIO_UAC = None
     CONSUMO_FIXO_POR_HORA_UAC = 10.0
     FATOR_CONSUMO_HORARIO_ECO_UAC = None
     CONSUMO_FIXO_POR_HORA_ECO_UAC = 2.0
     print(f"INFO: Testando com consumo FIXO (Normal={CONSUMO_FIXO_POR_HORA_UAC} UAC/h, Eco={CONSUMO_FIXO_POR_HORA_ECO_UAC} UAC/h)")

     painel_teste = PainelComandosNave()
     painel_teste.iniciar_interface()