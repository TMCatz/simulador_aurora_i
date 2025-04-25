# Simulador Aurora I 🚀

## Descrição

Simulador em Python dos módulos de software essenciais para a espaçonave fictícia Aurora I (missão para Marte), incluindo painel de comando, diagnóstico, suporte de vida, câmara de ar e menu de controle. Desenvolvido como um projeto de design de software aplicado à engenharia.

Este projeto simula, de forma conceitual, as interações e funcionalidades básicas que seriam necessárias para monitorar e controlar uma missão interplanetária.

## Funcionalidades Implementadas ✨

* **Menu Principal Interativo:** Interface central (`main.py`) para acessar todos os subsistemas simulados.
* **Limpeza de Tela:** Limpeza automática do console para melhor visualização entre menus e módulos.
* **Controle da Câmara de Ar (`modulo_pressurizacao.py`):**
    * Simulação do ciclo completo de despressurização (15->0 psi) e repressurização (0->15 psi).
    * Feedback visual da progressão da pressão.
* **Diagnóstico de Sistemas (`modulo_diagnostico.py`):**
    * Verificação simulada de múltiplos subsistemas da nave (Propulsão, Energia, Suporte Vital, etc.).
    * Atribuição aleatória de status: `OPERACIONAL`, `ALERTA`, `CRÍTICO` (com maior probabilidade para operacional).
    * Exibição de um painel de controle formatado com o status de cada sistema.
* **Monitoramento Vital e Ambiental (`modulo_monitoramento_vital.py`):**
    * Monitoramento contínuo (baseado em intervalos) de sinais vitais simulados para 7 tripulantes (Freq. Cardíaca, Pressão, Temp, SpO2, etc.).
    * Monitoramento contínuo de parâmetros ambientais da cabine (Pressão, O2, CO2, Temp, Umidade).
    * Geração de dados pseudo-realistas com flutuações (distribuição Gaussiana).
    * Classificação de status: `NORMAL`, `ATENÇÃO`, `CRÍTICO` baseado em limites pré-definidos.
    * Disparo de alarme visual no console para condições críticas.
* **Painel de Comando de Voo (`modulo_painel_comando.py`):**
    * Interface interativa para controle e monitoramento da viagem.
    * Acompanhamento de:
        * Nível de Combustível (UAC e Percentual) com **gauge visual `[###---]`**.
        * Distância Restante até Marte.
        * Velocidade Atual.
        * **Progresso da Viagem** com **gauge visual `[>>>...]`**.
        * **ETA (Tempo Estimado de Chegada)** calculado em dias/horas.
    * Controle de Velocidade:
        * Permite definir a velocidade desejada.
        * Limite de velocidade ajustável (Normal e **Modo Eco**).
        * Custo de combustível simulado para manobras (Delta-V).
    * **Modo Econômico (`eco on`/`off`)**: Modo de baixo consumo com velocidade limitada.
    * Simulação de Tempo Acelerada: Cada passo simula várias horas de voo (`HORAS_SIMULADAS_POR_INTERVALO`).
    * Consumo de Combustível Operacional: Simulado a cada passo (com taxas diferentes para modo Normal/Eco).
    * **Comando `impulso N`**: Permite executar N passos de simulação de uma vez para acelerar a viagem.
    * **Eventos Aleatórios**: Chance de ocorrerem eventos (micrometeoritos, falhas menores, tempestades solares) durante a simulação.
    * **Pausa em Eventos**: A simulação (especialmente durante `impulso`) pausa automaticamente se um evento ocorrer, exibindo a mensagem e esperando confirmação do usuário (Enter).

## Tecnologias Utilizadas 🛠️

* **Python 3:** Linguagem principal de desenvolvimento.
* **Biblioteca Padrão do Python:** Módulos como `time`, `sys`, `math`, `random`, `datetime`, `os` (este último opcional, dependendo da implementação de `limpar_tela`). Nenhuma biblioteca externa é necessária por padrão (a menos que `readchar` tivesse sido usada).

## Estrutura do Projeto 📂
