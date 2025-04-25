# -----------------------------------------------------------------------------
# Módulo Principal de Controle da Espaçonave Aurora I
# -----------------------------------------------------------------------------
# Este script serve como o menu principal para acessar os diversos
# subsistemas de software da nave.
#
# Certifique-se de que os seguintes arquivos estejam na mesma pasta que main.py:
# - modulo_pressurizacao.py
# - modulo_diagnostico.py
# - modulo_monitoramento_vital.py
# - modulo_painel_comando.py
# -----------------------------------------------------------------------------

try:  # Importar os módulos dos subsistemas da espaçonave
    import modulo_pressurizacao
    import modulo_diagnostico
    import modulo_monitoramento_vital
    import modulo_painel_comando
except ImportError as e:
    print(f"!!! ERRO CRÍTICO DE INICIALIZAÇÃO !!!")
    print(f"Não foi possível encontrar um dos módulos necessários: {e}")
    print("Verifique se todos os arquivos .py estão no mesmo diretório que 'main.py'.")
    print("O sistema não pode continuar.")
    exit() # Encerra o programa se um módulo essencial faltar

# Importar bibliotecas padrão necessárias
import sys
import os # Necessário se usar a alternativa os.system
import time
import datetime # Para exibir data/hora

def limpar_tela():
    """Limpa a tela do terminal usando códigos ANSI (preferencial)
       ou comandos do sistema operacional."""
    # Método preferido (ANSI) - Funciona na maioria dos terminais modernos
    print("\033[H\033[J", end="")
    sys.stdout.flush() # Garante que a limpeza seja efetiva imediatamente

    # Alternativa usando comandos do SO (menos chique, mas funciona caso necessário)
    # if sys.platform.startswith('win'):
    #     os.system('cls')
    # else:
    #     os.system('clear')

# --- Funções do Menu Principal ---

def exibir_menu_principal():
    """Exibe as opções do menu de navegação principal da espaçonave."""
    print("\n" + "="*50)
    print("=== MENU PRINCIPAL - ESPAÇONAVE AURORA I ===")
    print("="*50)
    print("Selecione o sistema que deseja acessar:")
    print("  1. Controle de Pressão da Câmara de Ar")
    print("  2. Diagnóstico Geral dos Sistemas da Nave")
    print("  3. Monitoramento Vital e Ambiental (Contínuo)")
    print("  4. Painel de Comandos de Voo")
    print("-" * 50)
    print("  0. Encerrar Sistema de Controle Principal")
    print("=" * 50)

def processar_escolha_menu(escolha):
    """
    Processa a escolha do usuário, chamando a função correspondente
    do módulo apropriado. Retorna False se o usuário escolher sair ('0'),
    True caso contrário para continuar exibindo o menu.
    """
    pausar_antes_de_retornar = True # Controla se pede "Pressione Enter"

    if escolha == '1':
        limpar_tela()
        # Função de limpar a tela
        print("\n>>> Acessando Módulo [1]: Controle de Pressão da Câmara de Ar...")
        # Chama a função principal do módulo de pressurização
        sucesso = modulo_pressurizacao.simular_ciclo_pressurizacao()
        if sucesso:
            print("\n[INFO] Ciclo de pressurização concluído.")
        else:
            print("\n[ALERTA] Ciclo de pressurização não foi concluído (interrompido ou erro).")

    elif escolha == '2':
        limpar_tela()
        # Função de limpar a tela
        print("\n>>> Acessando Módulo [2]: Diagnóstico Geral da Espaçonave...")
        # Chama as funções do módulo de diagnóstico
        painel_status_atual = modulo_diagnostico.executar_diagnostico_completo()
        modulo_diagnostico.exibir_painel_controle(painel_status_atual)
        print("\n[INFO] Diagnóstico finalizado.")

    elif escolha == '3':
        limpar_tela()
        # Função de limpar a tela
        print("\n>>> Acessando Módulo [3]: Monitoramento Vital e Ambiental...")
        print("   Este módulo executa verificações contínuas.")
        print("   Para retornar ao Menu Principal, interrompa o monitoramento")
        print("   pressionando [Ctrl] + [C] quando solicitado ou a qualquer momento.")
        input("\n   Pressione Enter para iniciar o monitoramento...")
        # Chama a função de monitoramento contínuo (que tem seu próprio loop)
        modulo_monitoramento_vital.iniciar_monitoramento_periodico(intervalo_segundos=20) # Intervalo de 20s
        print("\n[INFO] Monitoramento contínuo encerrado. Retornando ao Menu Principal.")
        pausar_antes_de_retornar = False # O módulo já lidou com a saída

    elif escolha == '4':
        limpar_tela()
        # Função de limpar a tela
        print("\n>>> Acessando Módulo [4]: Painel de Comandos de Voo...")
        print("   Este módulo possui sua própria interface interativa.")
        print("   Digite 'sair' dentro do Painel de Comandos para retornar ao Menu Principal.")
        input("\n   Pressione Enter para acessar o Painel de Comandos...")

        # --- CORREÇÃO AQUI ---
        # 1. Crie uma instância (objeto) da classe PainelComandosNave
        painel_nave = modulo_painel_comando.PainelComandosNave()
        # 2. Chame o método iniciar_interface() A PARTIR do objeto criado
        painel_nave.iniciar_interface()
        # --- FIM DA CORREÇÃO ---

        print("\n[INFO] Painel de Comandos encerrado. Retornando ao Menu Principal.")
        pausar_antes_de_retornar = False # Módulo já lidou com a saída

    # ... (resto do código: opção '0', 'else', etc.) ...

    elif escolha == '0':
        print("\n>>> Comando [0]: Encerrar Sistema Principal...")
        confirmar = input("   Tem certeza que deseja encerrar o sistema principal? (s/N): ").strip().lower()
        if confirmar == 's':
            print("\nEncerrando o Sistema de Controle Principal da Aurora I. Até a próxima, Engenheiro-Chefe!")
            return False # Sinaliza para sair do loop principal do menu
        else:
            print("   Encerramento cancelado.")
            pausar_antes_de_retornar = False # Não precisa pausar

    else:
        print(f"\n[ERRO] Opção '{escolha}' inválida. Por favor, escolha um número do menu.")
        pausar_antes_de_retornar = False # Não precisa pausar para erro de opção

    # Pausa para o usuário ler a saída dos módulos 1 e 2 antes de voltar ao menu
    if pausar_antes_de_retornar:
         print("-" * 30) # Separador visual
         input("Pressione Enter para retornar ao Menu Principal...")

    return True # Sinaliza para continuar no loop principal do menu (exceto se escolheu '0' e confirmou)

# --- Função Principal de Execução ---

def iniciar_sistema_controle():
    """Inicia e mantém o loop do menu de navegação principal."""
    timestamp_inicio = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    print("*"*60)
    print("      Sistema de Controle Principal da Espaçonave AURORA I")
    print("                          ATIVADO")
    print(f"                      {timestamp_inicio}")
    print("*"*60)

    continuar_executando = True
    while continuar_executando:
        limpar_tela() # Aqui está uma das edições após os testes para limpar o log
        exibir_menu_principal()
        try:
            # Captura a escolha do usuário
            escolha_usuario = input("Digite o número da opção desejada: ").strip()
            # Processa a escolha e decide se continua no menu
            continuar_executando = processar_escolha_menu(escolha_usuario)

        except KeyboardInterrupt: # Permite sair do menu principal com Ctrl+C
            print("\n\n[ALERTA] Interrupção manual (Ctrl+C) detectada no Menu Principal.")
            confirmar_saida = input("   Deseja realmente encerrar o sistema? (s/N): ").strip().lower()
            if confirmar_saida == 's':
                 print("Encerrando sistema por solicitação manual...")
                 continuar_executando = False
            else:
                 print("Retornando ao menu.")
        except Exception as e: # Captura outros erros inesperados no laço principal
             print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
             print(f"  ERRO INESPERADO NO SISTEMA PRINCIPAL: {e}")
             print("  Recomenda-se reiniciar o sistema.")
             print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
             # Em um sistema real, logaria o erro detalhado e talvez tentasse um modo seguro.
             # Aqui, vamos encerrar por segurança após um erro grave.
             print("Encerrando o sistema devido a erro inesperado.")
             time.sleep(2) # Pausa para ler o erro
             continuar_executando = False


    print("\n" + "*" * 60)
    print("      Sistema de Controle Principal da Espaçonave AURORA I")
    print("                         DESATIVADO")
    print(f"                      {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    print("*" * 60)

# --- Ponto de Entrada do Programa ---
# Garante que o código principal só rode quando o script é executado diretamente
if __name__ == "__main__":
    iniciar_sistema_controle()