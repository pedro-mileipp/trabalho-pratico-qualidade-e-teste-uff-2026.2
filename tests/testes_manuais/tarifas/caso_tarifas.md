# Caso de Teste Manual — Consulta de Tarifas

> Documento de caso de teste manual da funcionalidade de consulta de tarifas do Banco Digital.

## 1. Identificação

| Campo | Valor |
|---|---|
| Funcionalidade | Tarifas — Consulta de tarifa mensal (`/tarifas`) |
| Executor | Vinicius Sales Felinto |
| Data de execução | 19/09/2026 |
| Ambiente | Windows · Chrome · `DATABASE=/tmp/tarifas_teste.db` |
| Build testado | commit `main` |
| Técnica aplicada | Partição de equivalência + análise de valor-limite (BVA) |

## 2. Pré-condições e preparação

1. `uv sync --all-extras`
2. Subir a aplicação com banco fora do workspace:
   ```bash
   DATABASE=/tmp/tarifas_teste.db uv run flask --app app:create_app run
   ```
3. Criar conta em `http://127.0.0.1:5000/registro`:
   - Nome: `Teste Tarifas`
   - E-mail: `tarifas@teste.com`
   - Senha: `senha123`
4. Fazer login e acessar `/tarifas`.

### Dados de teste

O formulário de tarifas possui os seguintes campos de entrada:

| Campo | Tipo | Valores |
|---|---|---|
| Tipo de conta | Select | `corrente`, `poupanca`, `premium` |
| Saldo (R$) | Numérico (decimal) | Mínimo 0 na interface; step 0,01 |
| Transações no mês | Numérico (inteiro) | Mínimo 0 |
| Pacote de serviços | Checkbox | marcado / desmarcado |

#### Constantes de referência (regra de negócio)

| Constante | Valor |
|---|---|
| Tarifa base corrente | R$ 30,00 |
| Tarifa base poupança | R$ 0,00 |
| Tarifa base premium | R$ 50,00 |
| Faixa de isenção — Corrente | saldo ≥ R$ 5.000,00 |
| Faixa de isenção — Premium | saldo ≥ R$ 50.000,00 |
| Transações gratuitas | 10 |
| Tarifa por transação excedente | R$ 2,50 |

## 3. Casos de teste

Os 15 casos abaixo foram selecionados para maximizar a cobertura dos ramos acessíveis pela interface. A seleção combina os cenários propostos pelo testador com cenários de fronteira (BVA) e interação entre variáveis adicionados pela IA.

| ID | Cenário | Origem | Pré-condição | Passos | Dados de entrada | Resultado esperado | Resultado obtido | Status | Evidência |
|---|---|---|---|---|---|---|---|---|---|
| CT-01 | Corrente, valores zerados, sem pacote | Proposto pelo testador | Logado em `/tarifas` | 1) Selecionar Corrente; 2) saldo `0`; 3) transações `0`; 4) sem pacote; 5) Calcular | tipo `corrente`, saldo `0,00`, transações `0`, pacote desmarcado | Tarifa mensal: R$ 30,00 | <!-- preencher --> | <!-- PASS/FAIL --> | `evidencias/ct01.png` |
| CT-02 | Poupança, valores zerados, sem pacote | Proposto pelo testador | Logado em `/tarifas` | 1) Selecionar Poupança; 2) saldo `0`; 3) transações `0`; 4) sem pacote; 5) Calcular | tipo `poupanca`, saldo `0,00`, transações `0`, pacote desmarcado | Tarifa mensal: R$ 0,00 | <!-- preencher --> | <!-- PASS/FAIL --> | `evidencias/ct02.png` |
| CT-03 | Premium, valores zerados, sem pacote | Proposto pelo testador | Logado em `/tarifas` | 1) Selecionar Premium; 2) saldo `0`; 3) transações `0`; 4) sem pacote; 5) Calcular | tipo `premium`, saldo `0,00`, transações `0`, pacote desmarcado | Tarifa mensal: R$ 50,00 | <!-- preencher --> | <!-- PASS/FAIL --> | `evidencias/ct03.png` |
| CT-04 | Corrente, saldo 1 centavo abaixo da isenção (BVA) | Proposto pelo testador + BVA pela IA | Logado em `/tarifas` | 1) Selecionar Corrente; 2) saldo `4999.99`; 3) transações `0`; 4) sem pacote; 5) Calcular | tipo `corrente`, saldo `4.999,99`, transações `0`, pacote desmarcado | Tarifa mensal: R$ 30,00 | <!-- preencher --> | <!-- PASS/FAIL --> | `evidencias/ct04.png` |
| CT-05 | Corrente, saldo exatamente na fronteira de isenção (BVA) | Proposto pelo testador + BVA pela IA | Logado em `/tarifas` | 1) Selecionar Corrente; 2) saldo `5000`; 3) transações `0`; 4) sem pacote; 5) Calcular | tipo `corrente`, saldo `5.000,00`, transações `0`, pacote desmarcado | Tarifa mensal: R$ 0,00 | <!-- preencher --> | <!-- PASS/FAIL --> | `evidencias/ct05.png` |
| CT-06 | Premium, saldo 1 centavo abaixo da isenção (BVA) | Proposto pelo testador + BVA pela IA | Logado em `/tarifas` | 1) Selecionar Premium; 2) saldo `49999.99`; 3) transações `0`; 4) sem pacote; 5) Calcular | tipo `premium`, saldo `49.999,99`, transações `0`, pacote desmarcado | Tarifa mensal: R$ 50,00 | <!-- preencher --> | <!-- PASS/FAIL --> | `evidencias/ct06.png` |
| CT-07 | Premium, saldo exatamente na fronteira de isenção (BVA) | Proposto pelo testador + BVA pela IA | Logado em `/tarifas` | 1) Selecionar Premium; 2) saldo `50000`; 3) transações `0`; 4) sem pacote; 5) Calcular | tipo `premium`, saldo `50.000,00`, transações `0`, pacote desmarcado | Tarifa mensal: R$ 0,00 | <!-- preencher --> | <!-- PASS/FAIL --> | `evidencias/ct07.png` |
| CT-08 | Corrente, 10 transações — exatamente na cota (BVA) | Proposto pelo testador + BVA pela IA | Logado em `/tarifas` | 1) Selecionar Corrente; 2) saldo `0`; 3) transações `10`; 4) sem pacote; 5) Calcular | tipo `corrente`, saldo `0,00`, transações `10`, pacote desmarcado | Tarifa mensal: R$ 30,00 | <!-- preencher --> | <!-- PASS/FAIL --> | `evidencias/ct08.png` |
| CT-09 | Corrente, 11 transações — primeira excedente (BVA) | Proposto pelo testador + BVA pela IA | Logado em `/tarifas` | 1) Selecionar Corrente; 2) saldo `0`; 3) transações `11`; 4) sem pacote; 5) Calcular | tipo `corrente`, saldo `0,00`, transações `11`, pacote desmarcado | Tarifa mensal: R$ 32,50 (30 + 1×2,50) | <!-- preencher --> | <!-- PASS/FAIL --> | `evidencias/ct09.png` |
| CT-10 | Poupança, saldo zero, 20 transações | Proposto pelo testador | Logado em `/tarifas` | 1) Selecionar Poupança; 2) saldo `0`; 3) transações `20`; 4) sem pacote; 5) Calcular | tipo `poupanca`, saldo `0,00`, transações `20`, pacote desmarcado | Tarifa mensal: R$ 0,00 (poupança é sempre isenta) | <!-- preencher --> | <!-- PASS/FAIL --> | `evidencias/ct10.png` |
| CT-11 | Premium com pacote e saldo na isenção (isenção total) | Adicionado pela IA | Logado em `/tarifas` | 1) Selecionar Premium; 2) saldo `50000`; 3) transações `0`; 4) com pacote; 5) Calcular | tipo `premium`, saldo `50.000,00`, transações `0`, pacote marcado | Tarifa mensal: R$ 0,00 | <!-- preencher --> | <!-- PASS/FAIL --> | `evidencias/ct11.png` |
| CT-12 | Corrente com pacote e saldo alto — desconto 50% | Adicionado pela IA | Logado em `/tarifas` | 1) Selecionar Corrente; 2) saldo `5000`; 3) transações `0`; 4) com pacote; 5) Calcular | tipo `corrente`, saldo `5.000,00`, transações `0`, pacote marcado | Tarifa mensal: R$ 15,00 (30×0,5) | <!-- preencher --> | <!-- PASS/FAIL --> | `evidencias/ct12.png` |
| CT-13 | Premium com pacote e saldo baixo — desconto 30% | Proposto pelo testador | Logado em `/tarifas` | 1) Selecionar Premium; 2) saldo `3.000`; 3) transações `0`; 4) com pacote; 5) Calcular | tipo `premium`, saldo `3.000,00`, transações `0`, pacote marcado | Tarifa mensal: R$ 35,00 (50×0,7) | <!-- preencher --> | <!-- PASS/FAIL --> | `evidencias/ct13.png` |
| CT-14 | Corrente com pacote e 20 transações (pacote ignora extras) | Adicionado pela IA | Logado em `/tarifas` | 1) Selecionar Corrente; 2) saldo `0`; 3) transações `20`; 4) com pacote; 5) Calcular | tipo `corrente`, saldo `0,00`, transações `20`, pacote marcado | Tarifa mensal: R$ 30,00 (pacote não cobra extras) | <!-- preencher --> | <!-- PASS/FAIL --> | `evidencias/ct14.png` |
| CT-15 | Corrente isenta por saldo com transações excedentes | Adicionado pela IA | Logado em `/tarifas` | 1) Selecionar Corrente; 2) saldo `5000`; 3) transações `15`; 4) sem pacote; 5) Calcular | tipo `corrente`, saldo `5.000,00`, transações `15`, pacote desmarcado | Tarifa mensal: R$ 12,50 (base=0 + 5×2,50) | <!-- preencher --> | <!-- PASS/FAIL --> | `evidencias/ct15.png` |

## 4. Defeitos e observações

<!-- Preencher após execução dos testes -->

### Limitações da interface

| Limitação | Descrição | Impacto |
|---|---|---|
| Antiguidade não exposta | O campo `antiguidade_meses` existe no domínio (desconto de 50% com pacote para ≥24 meses e de 20% sem pacote para ≥36 meses), mas **não é exposto** no formulário web. A rota sempre envia `0`. | Ramos de desconto por antiguidade não são testáveis via interface |
| Saldo negativo bloqueado | O formulário tem `min="0"`, mas o domínio cobra taxa adicional de R$ 6,00 para saldo negativo | Ramo de saldo negativo não é testável via interface |
| Limpeza de formulario | o formulario é limpo a cada preenchimento, sem nenhum aviso para o usuario|

> **Nota:** os cenários de antiguidade e saldo negativo devem ser cobertos por testes unitários diretamente na classe `TarifaBancaria`, não por testes manuais pela interface.

## 5. Conclusão

- Total de **15 casos** selecionados, cobrindo todos os ramos acessíveis pela interface web do método `tarifa_mensal` (CC = 12). Os 4 ramos restantes (antiguidade e saldo negativo) estão documentados como limitações da interface.
- As técnicas de **Partição de Equivalência** e **Análise de Valor-Limite (BVA)** foram aplicadas sobre as faixas de isenção de saldo (R$ 5.000 e R$ 50.000) e sobre a cota de transações gratuitas (10).
- Os 15 casos cobrem: os 3 tipos de conta, BVA nas duas fronteiras de isenção por saldo (corrente e premium), BVA na cota de transações gratuitas, com e sem pacote, descontos diferenciados por pacote (50% e 30%), pacote ignorando transações extras, e interação entre isenção por saldo e transações excedentes.
