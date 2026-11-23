# 📌 Plano de Teste — Banco Digital

> Plano de Teste das **Entregas 1 e 2** do trabalho prático de Qualidade e Teste (UFF 2026.2).

---

## 📝 Registro de Mudanças

| Versão | Data | Autor | Descrição |
|------|--------|----------|--------|
| 1.0 | 21/09/2026 | Alexandre Colmenero | Criação do Plano de Teste com base nos testes executados na Entrega 1 |
| 1.1 | 23/09/2026 | Alexandre Colmenero | Atualização para refletir o estado atual dos testes (fix do `test_credito`, tarifas manual preenchida, resultados da suíte) |
| 1.2 | 11/11/2026 | Pedro Mileipp | Entrega 2: seção 6 com o `DecisorCredito` (técnicas funcionais e cobertura estrutural, issue #42); #35 reclassificado como erro de teste |
| 1.3 | 11/11/2026 | Pedro Mileipp | Entrega 2: testes de sistema com Selenium — Crédito/RF06 (issue #60) e base compartilhada dos testes de sistema (seção 6.2) |
| 1.4 | 11/11/2026 | Pedro Mileipp | Entrega 2: requisito não funcional de segurança da autenticação — RNF06 (issue #61, seção 6.3) |
| 1.5 | 12/11/2026 | Pedro Mileipp | Entrega 2: mutação do `DecisorCredito` (issue #47) na seção 6.1 |
| 1.6 | 18/11/2026 | Pedro Mileipp | Entrega 2: correções do Sonar na funcionalidade de crédito (issue #52) na seção 6.1 |
| 1.7 | 20/11/2026 | Gabrielle Rosa | Entrega 2: correção do bug de desconto de IR no mês 12 em `CalculadoraJuros` (issue #20) na seção 6.4 |
| 1.8 | 20/11/2026 | Gabrielle Rosa | Entrega 2: testes unitários com mock do repositório para `AuthService` e `TransacaoService` (issue #53) na seção 6.5 |
| 1.9 | 20/11/2026 | Gabrielle Rosa | Entrega 2: ampliação dos testes unitários e cobertura estrutural todas-arestas (100%) de `CalculadoraJuros` (issue #39) na seção 6.4 |
| 1.10 | 20/11/2026 | Gabrielle Rosa | Entrega 2: teste de mutação de `CalculadoraJuros` com `mutmut` (escore 87,25%, issue #44) na seção 6.4 |
| 1.11 | 20/11/2026 | Gabrielle Rosa | Entrega 2: testes de sistema com Selenium — Autenticação/RF01 e RF02 (issue #57) na seção 6.2 |
| 1.12 | 22/11/2026 | Vinicius Sales Felinto | Entrega 2: testes de sistema com Selenium — Empréstimo/RF05 (issue #59) nas seções 6.2 e 6.6 |
| 1.13 | 22/11/2026 | Vinicius Sales Felinto | Entrega 2: testes de integração das rotas Flask com test_client (seção 6.7) |
| 1.14 | 22/11/2026 | Vinicius Sales Felinto | Entrega 2: teste de mutação de `SimuladorEmprestimo` com `mutmut` (escore 99,34%, issue #46) na seção 6.6 |
| 1.14 | 22/11/2026 | Daniel Izu | Entrega 2: ampliação dos testes unitários e cobertura estrutural todas-arestas (100%) de `TarifaBancaria` (issue #40), defeitos #77 e #78, na seção 6.8; antiguidade passa a ser coberta por testes unitários (seção 1.1.2) |
| 1.15 | 22/11/2026 | Daniel Izu | Entrega 2: teste de mutação de `TarifaBancaria` com `mutmut` (escore 94,3%; 100% descontando equivalentes, issue #45) na seção 6.8 |
| 1.16 | 22/11/2026 | Vinicius Sales Felinto | Entrega 2: correções do Sonar na funcionalidade de empréstimo (issue #51) na seção 6.6 |
| 1.16 | 22/11/2026 | Gabrielle Rosa | Entrega 2: inspeção estática SonarQube em `CalculadoraJuros` — 0 apontamentos e evidência pós-correção (issue #49) nas seções 6.4 e registro de mudanças |
| 1.17 | 22/11/2026 | Daniel Izu | Entrega 2: correção dos apontamentos do Sonar em `TarifaBancaria` e `tarifas.html` (7 → 0) e do defeito #77 (issue #50) na seção 6.8 |
| 1.18 | 22/11/2026 | Daniel Izu | Entrega 2: testes de integração serviços ↔ repositório, sem mocks, no `SqliteRepositorio` e no `MemoriaRepositorio` (issue #54) na seção 6.9 |
| 1.19 | 22/11/2026 | Alexandre Colmenero | Entrega 2: atualização global do plano (escopo, estado atual, ferramentas e critérios) e planejamento dos testes de `TransacaoPix` — issues #38, #43, #48 e #56 — na seção 6.10 |
| 1.20 | 22/11/2026 | Alexandre Colmenero | Entrega 2: ampliação dos testes unitários de `TransacaoPix` para 104 casos e cobertura estrutural todas-arestas (100%, issue #38) na seção 6.10.2 |
| 1.21 | 22/11/2026 | Alexandre Colmenero | Entrega 2: teste de mutação de `TransacaoPix` com `mutmut` (escore 97,3%; 100% descontando 4 equivalentes, issue #43) na seção 6.10.3 |
| 1.22 | 22/11/2026 | Daniel Izu | Entrega 2: testes de sistema com Selenium — Tarifas/RF04 (issue #58) na seção 6.2; defeito #78 confirmado na interface |
| 1.22 | 22/11/2026 | Alexandre Colmenero | Entrega 2: correções do Sonar na funcionalidade PIX (7 → 0 apontamentos, issue #48) na seção 6.10.4 |
| 1.23 | 22/11/2026 | Alexandre Colmenero | Entrega 2: testes de sistema com Selenium — PIX/RF03 (issue #56) nas seções 6.2 e 6.10.5 |
| 1.24 | 22/11/2026 | Daniel Izu | Entrega 2: avaliação ISO/IEC 25010:2023 das 9 características, com escala e evidências (issue #62), em `docs/relatorios/iso25010.md` |
| 1.25 | 22/11/2026 | Daniel Izu | Entrega 2: correção do defeito #78 (meia tarifa do pacote sobre a tarifa do próprio tipo de conta: premium 25,00), decisão do grupo; 4 `xfail` viram regressão e 1 caso novo da corrente; mutação de `TarifaBancaria` 92,3%; estado atual e seções 6.2 e 6.8 |

> Nota: as versões 1.14, 1.16 e 1.22 aparecem duplicadas por registros simultâneos de integrantes; a numeração histórica foi preservada porque o AI-LOG e os prompts a citam.

---

## 📖 1. Introdução

O presente Plano de Teste tem como finalidade descrever as estratégias, processos e métodos utilizados para assegurar a qualidade do sistema **Banco Digital**.

O principal objetivo é verificar se as funcionalidades implementadas atendem aos requisitos definidos, além de garantir uma experiência de uso confiável e adequada ao público alvo.

Para isso, foram adotadas abordagens de **testes unitários** e **testes manuais**, contemplando funcionalidades como autenticação de usuários, transferência PIX, consulta de tarifas, simulação de empréstimo e análise de crédito. O processo de verificação e validação foi conduzido de forma iterativa, possibilitando a identificação antecipada de falhas e a evolução contínua do sistema ao longo da Entrega 1.

Na **Entrega 2**, o processo foi ampliado com **testes de integração**, **testes de sistema automatizados (Selenium)**, **cobertura estrutural (todas-arestas)**, **teste de mutação (mutmut)** e **inspeção estática (SonarQube)**, além do requisito não funcional de segurança (RNF06). As seções 6.1 a 6.9 registram os resultados por classe e funcionalidade; o planejamento e os resultados de `TransacaoPix` ficam na seção 6.10.

---

## 🎯 1.1. Escopo

### ✅ 1.1.1 No Escopo

| Nome do Módulo | Papéis Aplicáveis | Descrição |
| :--- | :---: | :--- |
| Autenticação (Registro/Login/Logout) | Cliente | O Cliente pode se cadastrar, autenticar e encerrar a sessão no sistema |
| Transferência PIX | Cliente | O Cliente pode transferir valores via PIX usando chaves de CPF, e-mail, telefone ou aleatória |
| Consulta de Tarifas | Cliente | O Cliente pode consultar a tarifa mensal por tipo de conta, saldo, transações e pacote de serviços |
| Simulação de Empréstimo | Cliente | O Cliente pode simular empréstimo com amortização Price ou SAC |
| Análise de Crédito | Cliente | O Cliente pode consultar a análise de crédito (aprovação, negação ou aprovação parcial) |
| Cálculo de Juros | — | Regras de juros compostos, mora e aportes — domínio puro, sem interface web, testado no nível de unidade |

### Requisitos Funcionais no Escopo

| Requisito | Descrição |
|----------|-----------|
| RF01 – Autenticação de usuários | Validar login, logout e acesso às rotas protegidas |
| RF02 – Cadastro de usuários | Testar criação e validação de contas (e-mail, senha mínima de 6 caracteres) |
| RF03 – Transferência PIX | Validar chaves, valor, limites por horário e saldo |
| RF04 – Consulta de tarifas | Validar a tarifa mensal por tipo de conta, saldo, transações e pacote |
| RF05 – Simulação de empréstimo | Validar simulações Price/SAC e as regras de valor mínimo, prazo e renda |
| RF06 – Análise de crédito | Validar aprovação, negação e aprovação parcial por score e renda |
| RF07 – Regras de negócio | Testar a lógica pura das classes de domínio (CC ≥ 10) |

### Requisitos Não Funcionais no Escopo

| Requisito | Descrição |
|----------|-----------|
| RNF01 – Usabilidade | Verificar facilidade de uso da interface e clareza das mensagens de erro |
| RNF02 – Confiabilidade | Garantir funcionamento correto das regras de negócio |
| RNF03 – Integridade dos dados | Validar consistência de saldo e extrato após transferências |
| RNF04 – Manutenibilidade | Validar o código por meio de testes unitários e medição de complexidade ciclomática (radon) |
| RNF05 – Compatibilidade | Testes em Python 3.12 gerenciado por uv |
| RNF06 – Segurança (autenticação) | Bloqueio de acesso às rotas sem sessão (`login_required`), logout, armazenamento da senha e mensagens de erro do login. Sem caso de teste dedicado na Entrega 1; testes automatizados na Entrega 2 (seção 6.3) |

---

### ❌ 1.1.2 Fora do Escopo

Esses recursos não foram testados porque não estão expostos na interface ou não fazem parte do escopo da Entrega 1.

### Requisitos Funcionais Fora do Escopo

| Requisito | Justificativa |
|----------|----------------|
| Chargeback de PIX pela interface | Não exposto na UI na Entrega 1 (regra de domínio, coberta por testes unitários) |
| Antiguidade e saldo negativo de tarifas | Campos não expostos no formulário web; saldo negativo e antiguidade cobertos por testes unitários (antiguidade na Entrega 2, issue #40) |
| Integrações com sistemas externos | Não fazem parte da versão atual |

### Requisitos Não Funcionais Fora do Escopo

| Requisito | Justificativa |
|----------|----------------|
| Testes de carga em larga escala | Não previstos nesta fase |
| Testes de segurança avançados | Fora do escopo acadêmico do projeto |
| Testes de desempenho em larga escala | Não aplicável nesta entrega |
| Testes de banco de dados em alto volume | Não contemplados |

---

## 🧪 1.2. Objetivos de Qualidade

Os testes têm como objetivo garantir que as principais funcionalidades do sistema operem corretamente, atendendo aos requisitos definidos e proporcionando uma experiência confiável ao usuário.

Nos testes funcionais (manuais), buscou-se validar operações como **autenticação de usuários**, **transferência PIX**, **consulta de tarifas**, **simulação de empréstimo** e **análise de crédito**.

Nos testes unitários, o foco foi verificar o funcionamento correto das classes de domínio, incluindo a **validação de chaves PIX**, o **cálculo de juros**, a **tarifa bancária**, a **simulação de empréstimo** e a **decisão de crédito**, além de revelar defeitos presentes no código, reportados como issues.

Além disso, os testes visam garantir a integridade dos dados, o tratamento de entradas inválidas e a estabilidade do sistema durante sua execução.

## 👥 1.3. Papéis e Responsabilidades

| Papel | Responsável |
|------|-------------|
| Plano de Teste | Alexandre Colmenero |
| Testes unitários | Todos |
| Testes manuais | Todos |
| Gestão de casos no TestLink | Gabrielle Rosa e Pedro Mileipp |
| Organização do GitHub (milestones e issues) | Alexandre Colmenero |
| Slides da apresentação | Daniel Izu |

### Testes da Entrega 1 — responsáveis por issue

#### Testes unitários

| Teste unitário | Classe | Issue | Responsável |
|----------------|--------|-------|-------------|
| `tests/unit/test_pix.py` | `TransacaoPix` | [#3](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/3) | Alexandre Colmenero |
| `tests/unit/test_juros.py` | `CalculadoraJuros` | [#4](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/4) | Gabrielle Rosa |
| `tests/unit/test_tarifas.py` | `TarifaBancaria` | [#5](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/5) | Daniel Izu |
| `tests/unit/test_emprestimo.py` | `SimuladorEmprestimo` | [#6](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/6) | Vinicius Sales Felinto |
| `tests/unit/test_credito.py` | `DecisorCredito` | [#7](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/7) | Pedro Mileipp |

#### Casos de teste manuais

| Caso manual | Funcionalidade | Issue | Responsável |
|-------------|----------------|-------|-------------|
| `tests/testes_manuais/pix/` | PIX | [#8](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/8) | Alexandre Colmenero |
| `tests/testes_manuais/auth/` | Auth | [#9](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/9) | Gabrielle Rosa |
| `tests/testes_manuais/tarifas/` | Tarifas | [#10](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/10) | Vinicius Sales Felinto |
| `tests/testes_manuais/emprestimo/` | Empréstimo | [#11](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/11) | Daniel Izu |
| `tests/testes_manuais/credito/` | Crédito | [#12](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/12) | Pedro Mileipp |

> Issues do projeto: [GitHub Issues](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues).

---

### 📊 1.4. Estado Atual dos Testes (23/09/2026)

#### Testes unitários

| Teste unitário | Classe | Casos | Resultado |
|----------------|--------|-------|-----------|
| `tests/unit/test_pix.py` | `TransacaoPix` | 68 | 66 pass · 2 fail |
| `tests/unit/test_credito.py` | `DecisorCredito` | 60 | 55 pass · 5 fail |
| `tests/unit/test_juros.py` | `CalculadoraJuros` | 36 | 35 pass · 1 fail |
| `tests/unit/test_emprestimo.py` | `SimuladorEmprestimo` | 40 | 40 pass |
| `tests/unit/test_tarifas.py` | `TarifaBancaria` | 44 | 44 pass |
| **Total** | | **248** | **240 pass · 8 fail** |

> As falhas identificadas são registradas e tratadas como issues de defeito no GitHub.

#### Casos de teste manuais

| Funcionalidade | Casos | Resultado |
|----------------|-------|-----------|
| PIX | 4 | 3 aprovados · 1 falha |
| Auth | 10 | 10 aprovados |
| Tarifas | 15 | 15 aprovados |
| Empréstimo | 5 | 5 aprovados |
| Crédito | 10 | 10 aprovados |

#### Estado atual (22/11/2026)

| Suíte | Casos | Resultado |
|-------|-------|-----------|
| Unitária (`tests/unit/`) | 548 | 548 pass |
| Integração (`tests/integration/`) | 84 | 84 pass |
| Sistema (`tests/system/`) | 56 | 56 pass |
| Requisitos não funcionais (`tests/rnf/`) | 22 | 22 pass |
| **Total** | **710** | **710 pass** |

Unitários por classe de domínio:

| Classe | Casos | Resultado |
|--------|-------|-----------|
| `TransacaoPix` | 111 | 111 pass |
| `DecisorCredito` | 96 | 96 pass |
| `CalculadoraJuros` | 68 | 68 pass |
| `SimuladorEmprestimo` | 125 | 125 pass |
| `TarifaBancaria` | 132 | 132 pass |
| `AuthService` e `TransacaoService` | 16 | 16 pass |

> A suíte completa ficou verde em 22/11/2026, após a correção dos bugs de PIX #16 e #17 (commit `e7881bd`, PR #89). Os 4 `xfail` que documentavam o defeito #78 (Tarifas) viraram testes de regressão com a correção da #78, e foi acrescentada a regressão da corrente: a suíte tem 710 testes, todos passando.

---

## 🔬 2. Metodologia de Teste

### 🔄 2.1 Fases de Teste

No projeto foram conduzidas as seguintes fases de teste na Entrega 1:

- **Teste de Unidade:** classes puras de `app/dominio/` testadas com **pytest**, aplicando partição de equivalência, análise de valor-limite, tabela de decisão e teste de laços. Suíte em `tests/unit/` (1 arquivo por classe).
- **Teste de Sistema (manual):** casos executados na interface do Flask em `tests/testes_manuais/` (PIX, Auth, Tarifas, Empréstimo e Crédito), com evidências por caso.
- **Gestão de casos:** casos manuais registrados no TestLink, com relatório do caso Auth exportado em PDF ([Auth — Relatório TestLink](https://drive.google.com/file/d/14yShZiduI8gixsV5wCQqA70DH2TV4SN4/view?usp=sharing)).

Na **Entrega 2**, além das fases acima:

- **Teste de integração:** rotas HTTP com `test_client` (#55) e serviços ↔ repositório sem mocks (#54), em `tests/integration/`.
- **Cobertura estrutural (todas-arestas):** ≥ 80% nas 5 classes de domínio, com `pytest-cov` e `branch = True`.
- **Teste de mutação:** escore ≥ 80% nas mesmas classes, com `mutmut`.
- **Teste de sistema automatizado:** Selenium + Chrome headless em `tests/system/` (uma pasta por funcionalidade).
- **Requisito não funcional:** segurança da autenticação (RNF06) em `tests/rnf/seguranca/`.
- **Inspeção estática:** SonarQube local (Docker), perfil *Sonar way comprehensive*, com registro "antes" e "depois".

---

### ⛔ 2.2 Critérios de Suspensão e Retomada

A execução dos testes poderá ser suspensa caso sejam identificadas falhas críticas que impeçam o funcionamento das principais funcionalidades do sistema, ou quando uma alta taxa de falhas comprometer a continuidade dos testes.

Os testes serão retomados após a correção dos problemas identificados, garantindo que o sistema esteja novamente em condições adequadas para execução dos testes.

---

### ✅ 2.3 Completude do Teste

Os testes foram considerados concluídos quando:

- 100% dos casos de teste planejados foram executados
- Os resultados dos testes foram devidamente registrados
- As falhas identificadas foram documentadas em issues
- As principais funcionalidades do sistema foram avaliadas

Na Entrega 2, acrescentam-se:

- Cobertura estrutural ≥ 80% (todas-arestas) nas 5 classes de domínio;
- Escore de mutação ≥ 80% nas mesmas classes;
- Testes de sistema automatizados executados e verdes;
- Apontamentos do Sonar resolvidos ou justificados, com print antes/depois.

---

## 📅 2.4. Atividades do projeto, estimativas e cronograma

| Atividade | Início | Fim |
|----------|--------|------|
| Planejamento dos testes | 15/09/2026 | 16/09/2026 |
| Testes unitários por integrante | 16/09/2026 | 21/09/2026 |
| Casos de teste manuais | 16/09/2026 | 20/09/2026 |
| Gestão de casos no TestLink | 20/09/2026 | 20/09/2026 |
| Plano de Teste | 21/09/2026 | 23/09/2026 |
| Consolidação dos resultados e entrega | 23/09/2026 | 23/09/2026 |

---

## 📦 3. Entregáveis de Teste

Os entregáveis de teste são fornecidos conforme abaixo.

#### Antes da fase de teste

- Plano de Teste.
- Issues da Entrega 1 (planejamento das atividades).
- Casos de teste manuais projetados.

#### Durante o teste

- Dados de teste (contas, chaves PIX, valores de fronteira).
- Evidências (screenshots) por caso de teste manual.
- Resultados de execução dos testes unitários e manuais.
- Registro de uso de IA (`docs/ai/AI-LOG.md`).

#### Após o término dos ciclos de teste

- Casos manuais preenchidos em `tests/testes_manuais/`.
- Testes unitários em `tests/unit/`.
- Relatório do TestLink (PDF — caso Auth): [Auth — Relatório TestLink](https://drive.google.com/file/d/14yShZiduI8gixsV5wCQqA70DH2TV4SN4/view?usp=sharing).
- Issues de defeito abertas no GitHub (bugs encontrados pelos testes):
  - [#16](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/16) — e-mail com dois `@` aceito como válido (PIX). **Corrigida na Entrega 2:** `_validar_email` passou a exigir exatamente um `@` (commit `e7881bd`, PR #89)
  - [#17](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/17) — chave bloqueada ignora regra de valor no chargeback (PIX). **Corrigida na Entrega 2:** chargeback de chave bloqueada passou a devolver `False` (commit `e7881bd`, PR #89)
  - [#20](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/20) — desconto de IR não aplicado no mês 12 (Juros). **Corrigida na Entrega 2:** ajustado o laço em `CalculadoraJuros.montante_com_aportes` para `range(1, meses + 1)`
  - [#35](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/35) — limite máximo não aplicado para score ≥ 850 (Crédito). **Fechada na Entrega 2:** o defeito estava nas expectativas dos testes, não no código; corrigido na issue [#42](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/42)

---

## 🖥️ 4. Necessidades de Recursos e Ambiente

### 🧰 4.1 Ferramentas de Teste

| No. | Recursos | Descrição |
| :--- | :---: | :--- |
| 1 | pytest | Framework utilizado para a criação e execução dos testes unitários |
| 2 | uv | Gerenciador de pacotes e ambiente (Python 3.12) |
| 3 | ruff / radon | Lint estático e medição de complexidade ciclomática |
| 4 | TestLink | Gestão de casos de teste manuais |
| 5 | GitHub Issues | Reporte de bugs e acompanhamento das atividades |
| 6 | Google Chrome | Navegador usado na execução dos testes manuais |
| 7 | Selenium WebDriver | Automação dos testes de sistema (Chrome headless) |
| 8 | mutmut | Teste de mutação sobre as classes de domínio |
| 9 | pytest-cov / coverage.py | Cobertura estrutural (todas-arestas) |
| 10 | SonarQube (Docker) | Inspeção estática do código |

### 💻 4.2 Ambiente de Teste

Para a execução do sistema e realização dos testes, é necessário dispor de um ambiente compatível com as tecnologias utilizadas no desenvolvimento do projeto.

**Requisitos de Software:**

- Sistema operacional macOS, Linux ou Windows
- Python **3.12** gerenciado por **uv**
- Navegador Google Chrome (headless nos testes de sistema, via Selenium Manager)
- Banco de dados **SQLite** (arquivo em `/tmp` no ambiente de teste, fora do workspace)
- Servidor de desenvolvimento **Flask**
- Docker para o SonarQube local

---

## 📚 5. Termos e Acrônimos

| Termo | Significado |
|------|-------------|
| PIX | Transferência instantânea de valores |
| PE | Partição de Equivalência |
| AVL / BVA | Análise de Valor Limite (Boundary Value Analysis) |
| CC | Complexidade Ciclomática |
| RF | Requisito Funcional |
| RNF | Requisito não Funcional |
| SQLite | Banco de dados local embarcado |
| pytest | Framework para testes unitários em Python |
| TestLink | Ferramenta de gestão de casos de teste |
| Flask | Microframework web do projeto |
| TD | Tabela de Decisão |
| Selenium | Framework de automação dos testes de sistema |
| mutmut | Ferramenta de teste de mutação |
| SonarQube | Plataforma de inspeção estática de código |
| Cobertura de arestas | Critério estrutural que exige a passagem por todos os desvios |

---

## 🚀 6. Entrega 2 — Resultados

> Cada integrante documenta a subseção da sua classe ao concluir as issues da Entrega 2; pendente: relatório consolidado do Sonar (#63). A avaliação ISO 25010 (#62) está em [`docs/relatorios/iso25010.md`](relatorios/iso25010.md). O detalhamento (comandos, saídas e casos) fica em [`docs/relatorios/cobertura_mutacao.md`](relatorios/cobertura_mutacao.md).

### 6.1 `DecisorCredito` — Pedro Mileipp

| Item | Issue | Situação | Resultado |
|---|---|---|---|
| Unitários + cobertura estrutural (todas-arestas) | [#42](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/42) | Concluído | 90 casos, todos passando; **100%** de cobertura de arestas (antes: 93%) |
| Teste de sistema (Selenium) — Crédito, RF06 | [#60](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/60) | Concluído | 13 cenários automatizados, todos passando (ver seção 6.2) |
| Requisito não funcional — segurança da autenticação, RNF06 | [#61](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/61) | Concluído | 22 testes, todos passando; 5 riscos documentados (ver seção 6.3) |
| Mutação (escore ≥ 80%) | [#47](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/47) | Concluído | 184 mutantes, 179 mortos: **97,3%** (100% descontando 5 equivalentes justificados); +6 casos de valor-limite (96 no total) |
| Correções do Sonar | [#52](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/52) | Concluído | `DecisorCredito` sem apontamentos (0 → 0); os 4 apontamentos da tela de crédito (`credito.html`) foram corrigidos (4 → 0). Projeto: 40 → 36 apontamentos. Detalhes na seção 6.1 de [`docs/relatorios/inspecao_sonar.md`](relatorios/inspecao_sonar.md) |

**Técnicas aplicadas** (identificadas pelo prefixo do id de cada caso em `tests/unit/test_credito.py`):

- **Partição de equivalência (`pe_`)**: um caso por tipo de evento do histórico, faixas de score e renda inválida.
- **Análise de valor-limite (`vl_`)**: piso e teto do score (0 e 1000), fronteiras entre faixas (299/300, 499/500, 699/700, 849/850) e teto de limite de cada faixa (logo abaixo, no teto e logo acima).
- **Tabela de decisão (`td_`)**: as 6 regras de `decidir` e as combinações em que mais de uma regra se aplica.
- **Teste de laços (`laco_`)**: 0, 1, 2, 3 e 100 iterações sobre o histórico, incluindo o clamp aplicado no meio do laço.
- **Baseada em defeitos (mutação, mutmut)**: dos 6 mutantes sobreviventes da primeira execução, 5 são equivalentes (justificados no relatório) e 1 revelou uma fronteira não testada (score exatamente 1001), coberta por novos casos `vl_` com passo 1. Detalhes e evidências em [`docs/relatorios/cobertura_mutacao.md`](relatorios/cobertura_mutacao.md).

**Defeitos e decisões:**

- [#35](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/35) fechado: as 5 falhas eram expectativas erradas nos testes, corrigidas na #42.
- **Decisão de projeto:** a tabela de decisão mostrou que, quando mais de uma regra se aplica (ex.: score baixo e valor inválido), `decidir()` informa o motivo da regra avaliada primeiro (score → limite → valor). Como a especificação não define essa precedência, a ordem atual foi mantida e documentada. Os casos `td_r1_precedencia_*` e `td_r2_precedencia_*` fixam esse comportamento.

### 6.2 Testes de sistema (Selenium)

**Ferramentas:** Selenium WebDriver 4 com Google Chrome em modo headless (driver resolvido pelo Selenium Manager) e pytest.

**Situação em 22/11/2026:** 56 testes de sistema passando — Crédito (13), Auth (12), Empréstimo (6), Tarifas (19) e PIX (6). O `xfail` do defeito #78 virou teste de regressão com a correção.

**Base compartilhada** (`tests/system/conftest.py`), para todos os testes de sistema:

| Fixture | O que faz |
|---|---|
| `servidor` | Sobe a aplicação Flask real numa thread, em porta livre, com banco SQLite temporário criado do zero a cada execução |
| `navegador` | Chrome headless reaproveitado na sessão, com cookies apagados antes de cada teste; salva screenshot e HTML em `<funcionalidade>/falhas/` quando um teste falha |
| `cliente_logado` | Cadastra um cliente com e-mail único pela tela `/registro` (que já abre a sessão), deixando cada teste independente dos demais |
| `evidencia` | Registra o screenshot de uma etapa do teste (ex.: formulário preenchido antes do envio) quando `EVIDENCIAS=1` |

Cada funcionalidade tem a sua pasta em `tests/system/` (ex.: `tests/system/credito/`), com o arquivo de testes, o page object e as evidências. O page object concentra os seletores da tela: se ela mudar, só ele é ajustado. Com `EVIDENCIAS=1`, os screenshots das etapas registradas e da tela final de cada teste são salvos em `<funcionalidade>/evidencias/`, numerados na ordem em que acontecem.

#### Crédito (RF06) — Pedro Mileipp, issue [#60](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/60)

Pasta: `tests/system/credito/` (testes em `test_credito_sistema.py`, page object em `pagina_credito.py`). Os cenários automatizam o caso manual da Entrega 1 (`tests/testes_manuais/credito/caso_credito.md`) com os mesmos ids, e acrescentam duas fronteiras. Sem histórico na tela, o score é sempre 500 e o limite é `min(renda, 10000)`.

| Id | Cenário | Entrada (renda / valor) | Resultado esperado |
|---|---|---|---|
| CT-01 | Aprovado dentro do limite | 10000 / 5000 | aprovado · limite R$ 10000.00 |
| CT-02 | Aprovado exatamente no limite | 10000 / 10000 | aprovado |
| CT-03 | Parcial entre o limite e 1,5× | 10000 / 12000 | parcial |
| CT-04 | Negado acima de 1,5× | 10000 / 20000 | negado · `acima_limite` |
| CT-05 | Negado com valor zero | 10000 / 0 | negado · `valor_invalido` |
| CT-06 | Valor negativo barrado pelo formulário | 10000 / -500 | validação HTML5 impede o envio |
| CT-07 | Negado com renda zero | 0 / 5000 | negado · `sem_limite` · limite R$ 0.00 |
| CT-08 | Renda negativa barrada pelo formulário | -1000 / 5000 | validação HTML5 impede o envio |
| CT-09 | Parcial exatamente em 1,5× | 10000 / 15000 | parcial |
| CT-10 | Parcial logo abaixo de 1,5× | 10000 / 14999.99 | parcial |
| CT-11 (novo) | Negado logo acima de 1,5× | 10000 / 15000.01 | negado · `acima_limite` |
| CT-12 (novo) | Limite no teto da faixa de score 500 | 20000 / 10000 | aprovado · limite R$ 10000.00 |
| — | Acesso à tela sem login | — | redireciona para `/login` |

**Resultado (11/11/2026):** 13 cenários, todos passando (`uv run pytest tests/system -v`), em execuções seguidas com o mesmo resultado. Evidências em `tests/system/credito/evidencias/`: para cada cenário, um print do formulário preenchido antes do envio (`__1_formulario_preenchido`) e um da tela final com o resultado (`__2_final`).

#### Autenticação (RF01/RF02) — Gabrielle Rosa, issue [#57](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/57)

Pasta: `tests/system/auth/` (testes em `test_auth_sistema.py`, page object em `pagina_auth.py`). Os cenários automatizam os casos manuais de autenticação (`tests/testes_manuais/auth/caso_auth.md`) e acrescentam o bloqueio de acesso sem sessão às rotas protegidas (`/` e `/credito`).

| Id | Cenário | Entrada | Resultado esperado |
|---|---|---|---|
| CT-01 | Login com usuário inexistente | E-mail inexistente · senha `123456` | Bloqueia acesso em `/login` e exibe `E-mail ou senha inválidos.` |
| CT-02 | Cadastro válido e redirecionamento para dashboard | Nome `Gabrielle Rosa` · e-mail único · senha `senha123` | Cria conta, inicia sessão e redireciona para `/` |
| CT-03 | Encerrar sessão (Logout) | Cliente autenticado acessando `/logout` | Encerra sessão e redireciona para `/login` |
| CT-04 | Reautenticação após logout | E-mail recém-cadastrado · senha `senha123` | Concede acesso e redireciona para `/` |
| CT-05 | Login com senha incorreta | E-mail cadastrado · senha `senhaERRADA` | Bloqueia acesso em `/login` e exibe `E-mail ou senha inválidos.` |
| CT-06 | Tentativa de cadastro com e-mail duplicado | E-mail já cadastrado · senha `senha123` | Permanece em `/registro` e exibe `Este e-mail já está cadastrado.` |
| CT-07 | Cadastro com e-mail sem `@` | E-mail sem `@` · senha `senha123` | Validação HTML5 (`typeMismatch`) impede envio em `/registro` |
| CT-08 | Cadastro com e-mail sem domínio | E-mail terminado em `@` · senha `senha123` | Validação HTML5 (`typeMismatch`) impede envio em `/registro` |
| CT-09 | Cadastro com senha curta (< 6 caracteres) | E-mail único · senha `12345` | Permanece em `/registro` e exibe `Dados inválidos. Verifique os campos.` |
| CT-10 | Cadastro com campos obrigatórios vazios | Nome vazio · e-mail único · senha `senha123` | Validação HTML5 (`valueMissing`) impede envio em `/registro` |
| — | Acesso a rotas protegidas sem autenticação (`/`, `/credito`) | Sem sessão ativa | Redireciona para `/login` |

**Resultado (20/11/2026):** 12 cenários de autenticação (25 testes no total da suíte `tests/system`), todos passando (`.venv/bin/pytest tests/system -q`), em execuções seguidas com o mesmo resultado. Cada teste utiliza e-mails únicos e cookies limpos entre execuções, garantindo independência total; evidências geradas em `tests/system/auth/evidencias/` com `EVIDENCIAS=1` (screenshots numerados das etapas registradas e da tela final).

#### Empréstimo (RF05) — Vinicius Sales Felinto, issue [#59](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/59)

Pasta: `tests/system/emprestimo/` (testes em `test_emprestimo_sistema.py`, page object em `pagina_emprestimo.py`). Os cenários automatizam os casos manuais de empréstimo (`tests/testes_manuais/emprestimo/caso_emprestimo.md`) e acrescentam a validação de rota protegida sem autenticação (`/emprestimo` redirecionando para `/login`).

| Id | Cenário | Entrada (principal / meses / renda / sistema) | Resultado esperado |
|---|---|---|---|
| TC-01 | Simulação válida com Tabela Price | 1000 / 12 / 5000 / Price | Aprovado · 1ª parcela R$ 100.46 · Total R$ 1205.52 · 12 parcelas |
| TC-02 | Simulação válida com Tabela SAC | 1000 / 12 / 5000 / SAC | Aprovado · 1ª parcela R$ 113.33 · Total R$ 1194.96 · 12 parcelas |
| TC-03 | Recusa por valor solicitado abaixo do mínimo (R$ 100,00) | 50 / 12 / 5000 / Price | Não aprovado · `valor_abaixo_minimo` |
| TC-04 | Prazo abaixo do mínimo permitido (2 meses) | 1000 / 1 / 5000 / Price | Validação HTML5 (`min="2"` / `rangeUnderflow`) impede o envio na interface |
| TC-05 | Recusa por principal acima do teto de renda (15% para renda < 2000) | 200 / 2 / 1000 / Price | Não aprovado · `acima_teto` |
| — | Acesso à tela de empréstimo sem login | — | Redireciona para `/login` |

**Resultado (22/11/2026):** 6 cenários de empréstimo (31 testes no total da suíte `tests/system`), todos passando (`uv run pytest tests/system -q`), em execuções repetidas obtendo o mesmo resultado verde (49.36s e 53.05s). Cada teste utiliza um cliente com e-mail único cadastrado via fixture `cliente_logado`, garantindo independência total e banco SQLite limpo por sessão; evidências geradas em `tests/system/emprestimo/evidencias/` com `EVIDENCIAS=1` (screenshots numerados do formulário preenchido, resultado e tela final).

#### Tarifas (RF04) — Daniel Izu, issue [#58](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/58)

Pasta: `tests/system/tarifas/` (testes em `test_tarifas_sistema.py`, page object em `pagina_tarifas.py`). Os cenários automatizam os 15 casos manuais de tarifas (`tests/testes_manuais/tarifas/caso_tarifas.md`) com os mesmos ids e acrescentam as recusas do formulário, o acesso sem login e um caso do defeito [#78](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/78). A tela chama `TarifaBancaria(TarifasBase()).tarifa_mensal(tipo, saldo, pacote, transacoes)`: a antiguidade não é exposta, e o formulário não aceita valores negativos. Para os seletores, o template `tarifas.html` recebeu só `id="pacote"` (checkbox) e `id="tarifa-resultado"` (parágrafo do resultado); o `conftest.py` compartilhado não foi alterado.

| Id | Cenário | Entrada (tipo / saldo / transações / pacote) | Resultado esperado |
|---|---|---|---|
| CT-01 | Corrente, valores zerados | corrente / 0 / 0 / não | R$ 30.00 |
| CT-02 | Poupança, valores zerados | poupança / 0 / 0 / não | R$ 0.00 |
| CT-03 | Premium, valores zerados | premium / 0 / 0 / não | R$ 50.00 |
| CT-04 | Corrente 1 centavo abaixo da isenção | corrente / 4999.99 / 0 / não | R$ 30.00 |
| CT-05 | Corrente na fronteira da isenção | corrente / 5000 / 0 / não | R$ 0.00 |
| CT-06 | Premium 1 centavo abaixo da isenção | premium / 49999.99 / 0 / não | R$ 50.00 |
| CT-07 | Premium na fronteira da isenção | premium / 50000 / 0 / não | R$ 0.00 |
| CT-08 | Corrente, 10 transações (na cota) | corrente / 0 / 10 / não | R$ 30.00 |
| CT-09 | Corrente, 11 transações (primeira excedente) | corrente / 0 / 11 / não | R$ 32.50 |
| CT-10 | Poupança, 20 transações | poupança / 0 / 20 / não | R$ 0.00 |
| CT-11 | Premium com pacote e saldo na isenção | premium / 50000 / 0 / sim | R$ 0.00 |
| CT-12 | Corrente com pacote, desconto de 50% | corrente / 5000 / 0 / sim | R$ 15.00 |
| CT-13 | Premium com pacote, desconto de 30% | premium / 3000 / 0 / sim | R$ 35.00 |
| CT-14 | Corrente com pacote ignora transações extras | corrente / 0 / 20 / sim | R$ 30.00 |
| CT-15 | Corrente isenta com transações excedentes | corrente / 5000 / 15 / não | R$ 12.50 |
| — | Saldo negativo barrado pelo formulário | corrente / -100 / 0 / não | validação HTML5 (`min="0"` / `rangeUnderflow`) impede o envio |
| — | Transações negativas barradas pelo formulário | corrente / 0 / -1 / não | validação HTML5 (`min="0"` / `rangeUnderflow`) impede o envio |
| — | Acesso à tela sem login | — | redireciona para `/login` |
| — | Regressão do defeito #78: premium com pacote e saldo entre 5000 e 50000 | premium / 6000 / 0 / sim | R$ 25.00 (antes da correção, a tela mostrava R$ 15.00) |

**Resultado (22/11/2026):** 19 cenários: **18 passando e 1 `xfail`** (#78). Suíte `tests/system`: **49 passed, 1 xfailed** (antes: 31 passed). Execução isolada (`-k ct09`) também passa. Evidências em `tests/system/tarifas/evidencias/` com `EVIDENCIAS=1` (37 prints): para cada cenário, o formulário preenchido antes do envio (`__1_formulario_preenchido`) e a tela final com o resultado (`__2_final`). Como a tela limpa o formulário a cada envio (limitação registrada no caso manual), o print final mostra o resultado com o formulário de volta aos valores padrão. A gravação de evidência em falha foi verificada quebrando de propósito o esperado do CT-09: `falhas/` recebeu o screenshot e o HTML, e o esperado foi restaurado.

**Defeito #78 confirmado na interface e corrigido:** o valor de 15,00 foi verificado no Chrome (`--runxfail`: `assert 15.0 == 25.0`) e na validação manual do responsável. O grupo decidiu que é defeito no código: a meia tarifa do pacote é 50% da tarifa do próprio tipo de conta (premium 25,00). A correção foi feita na [#78](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/78); o teste deixou de ser `xfail`, virou regressão, e os 19 cenários de tarifas passam. O print do caso corrigido (R$ 25.00) está em `tests/system/tarifas/evidencias/test_defeito_78_pacote_premium_meia_tarifa__2_final.png`. Os testes foram gerados com IA; a solução inicial (`850f87d`) e a revisada (`afe29fa`) estão na sessão 24 do [AI-LOG](ai/AI-LOG.md).

#### PIX (RF03) — Alexandre Colmenero, issue [#56](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/56)

Pasta: `tests/system/pix/` (testes em `test_pix_sistema.py`, page object em `pagina_pix.py`). Os cenários automatizam os casos manuais de PIX (`tests/testes_manuais/pix/caso_pix.md`) e acrescentam a regressão do defeito #16, a validação HTML5 do valor e a guarda de autenticação. O saldo inicial é definido direto no SQLite temporário pela fixture `definir_saldo_sistema` (a interface não tem depósito), e os cenários usam valores válidos nas duas janelas de horário para não depender do relógio da máquina.

| Id | Cenário | Entrada (chave / tipo / valor / saldo) | Resultado esperado |
|---|---|---|---|
| TC-01 | PIX aprovado com CPF válido | `529.982.247-25` / cpf / 100,00 / 1000,00 | Redireciona ao dashboard com "Transferência realizada com sucesso.", saldo R$ 900,00 e extrato `PIX cpf -100.00` |
| TC-02 | Recusa por chave inválida | `123.456.789-00` / cpf / 50,00 / 1000,00 | "Chave PIX inválida." em `/pix`; saldo intacto (R$ 1000,00), extrato vazio |
| TC-03 | Recusa por saldo insuficiente | `529.982.247-25` / cpf / 500,00 / 100,00 | "Saldo insuficiente." em `/pix`; saldo intacto (R$ 100,00), extrato vazio |
| TC-04 (regressão #16) | E-mail com dois `@` recusado | `a@b@c.com` / email / 25,00 / 1000,00 | "Chave PIX inválida." em `/pix`; saldo intacto, extrato vazio |
| TC-05 | Valor zero barrado pelo formulário | 0 / cpf / — / 1000,00 | Validação HTML5 (`min="0.01"` / `rangeUnderflow`) impede o envio, sem flash |
| — | Acesso à tela de PIX sem login | — | Redireciona para `/login` |

**Resultado (22/11/2026):** 6 cenários, todos passando (`uv run pytest tests/system/pix -q`), em execuções repetidas com o mesmo resultado verde. A suíte completa de sistema fica em **55 passed, 1 xfailed** (`uv run pytest tests/system -q`, executada duas vezes: 40.40s e 43.11s). Cada teste usa um cliente com e-mail único e saldo definido pela fixture, garantindo independência e banco SQLite limpo por sessão; evidências geradas em `tests/system/pix/evidencias/` com `EVIDENCIAS=1` (formulário preenchido, dashboard após o PIX e tela final de cada cenário). Detalhes do planejamento na seção 6.10.

### 6.3 Requisito não funcional — segurança da autenticação (RNF06)

Pedro Mileipp, issue [#61](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/61). Relatório completo em [`docs/relatorios/rnf_seguranca.md`](relatorios/rnf_seguranca.md).

**Ferramenta:** cliente de testes do Flask (`app.test_client()`) com pytest: requisições HTTP reais às rotas, sem navegador, e banco SQLite temporário por teste (fixtures em `tests/rnf/conftest.py`). Arquivo: `tests/rnf/seguranca/test_seguranca_autenticacao.py`.

| Verificação | Casos | Resultado |
|---|---|---|
| Rotas protegidas exigem login (GET e POST), sem gravar nada no banco | 11 | ✅ |
| Depois do logout, as rotas protegidas não mostram dados do cliente | 6 | ✅ |
| Senha gravada como hash `pbkdf2:sha256`, com salt por cliente | 2 | ✅ |
| Mensagem de erro do login não revela se o e-mail existe | 2 | ✅ |
| Cookie de sessão `HttpOnly` | 1 | ✅ |

**Resultado (11/11/2026):** 22 testes, todos passando (`uv run pytest tests/rnf/seguranca -v`).

**Riscos identificados** (fora dos critérios da issue; detalhes e recomendações no relatório): R1 — o botão Voltar após o logout mostra o painel do cache do navegador; R2 — um cookie de sessão copiado antes do logout continua válido; R3 — `SECRET_KEY` com valor padrão fixo no código; R4 — o cadastro revela se o e-mail já existe; R5 — cookie de sessão sem `Secure`/`SameSite`. O relatório também traz a avaliação da característica Segurança da ISO/IEC 25010:2023 para a issue #62.


### 6.4 `CalculadoraJuros` — Gabrielle Rosa

| Item | Issue | Situação | Resultado |
|---|---|---|---|
| Correção de defeito (desconto de IR no mês 12) | [#20](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/20) | Concluído | Laço ajustado para `range(1, meses + 1)` em `montante_com_aportes`; 36 casos passando em `tests/unit/test_juros.py` em 20/11/2026 (evidências antes/depois em `docs/relatorios/evidencias/bug/`) |
| Unitários ampliados + cobertura estrutural (todas-arestas) | [#39](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/39) | Concluído | 68 casos passando em 20/11/2026 (`0.40s`); **100.00%** de cobertura de linhas e ramos (`67` statements, `0` missed, `36` branches, `0` partial) com `pe_`, `vl_`, `td_` e `laco_`[cite: 7] |
| Mutação (escore ≥ 80%) | [#44](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/44) | Concluído | 149 mutantes gerados, 130 mortos e 19 sobreviventes em 20/11/2026: **87,25%** de escore (meta ≥ 80% atingida); evidência em [`docs/relatorios/evidencias/mutacao/juros-mutacao.txt`](relatorios/evidencias/mutacao/juros-mutacao.txt) |
| Inspeção estática (SonarQube — sem apontamentos + bug #20) | [#49](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/49) | Concluído | 0 apontamentos estáticos em `app/dominio/juros.py`; bug #20 corrigido; CC verificada com `radon cc` e evidência em `docs/relatorios/evidencias/sonar/depois/juros/` |


**Defeitos e decisões:**

- [#20](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/20) corrigida (20/11/2026): em `CalculadoraJuros.montante_com_aportes` (`app/dominio/juros.py`), o laço `for mes in range(meses)` percorria índices de `0` a `11`, impedindo o desconto de IR no 12º mês. A iteração foi ajustada para `range(1, meses + 1)`.

- **Ampliação (#39, 20/11/2026):** suíte expandida para 68 casos cobrindo partição de equivalência (`pe_`), análise de valor-limite (`vl_`), tabela de decisão (`td_`) e teste de laços (`laco_`), mantendo **100.00%** de cobertura de linhas e ramos sem alterações em `app/dominio/juros.py`[cite: 7].

- **Mutação (#44, 20/11/2026):** execução isolada com `mutmut` sobre `app/dominio/juros.py` (`tests/unit/test_juros.py`) atingiu **87,25%** (`130/149` mortos, `19` sobreviventes), com os 19 sobreviventes triados e justificados em [`docs/relatorios/cobertura_mutacao.md`](relatorios/cobertura_mutacao.md) e [`docs/relatorios/evidencias/mutacao/juros-mutacao.txt`](relatorios/evidencias/mutacao/juros-mutacao.txt).


### 6.5 Serviços (`AuthService` e `TransacaoService`) — Gabrielle Rosa

| Item | Issue | Situação | Resultado |
|---|---|---|---|
| Testes unitários com mock do repositório (`AuthService` e `TransacaoService`) | [#53](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/53) | Concluído | 16 casos passando em 20/11/2026 (`tests/unit/test_auth_service.py` com 12 casos e `tests/unit/test_transacao_service.py` com 4 casos), isolando `Repositorio` via `pytest-mock` sem acesso a SQLite ou Flask |

### 6.6 `SimuladorEmprestimo` — Vinicius Sales Felinto

| Item | Issue | Situação | Resultado |
|---|---|---|---|
| Testes unitários ampliados + cobertura estrutural todas-arestas | [#41](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/41) | Concluído | 118 casos passando em 22/11/2026 (`tests/unit/test_emprestimo.py`), 100.00% de cobertura estrutural de linhas e ramos (82 stmts, 38 branches); PE, AVL, TD, laços e conferência numérica completa; detalhes em `docs/relatorios/cobertura_mutacao.md` |
| Mutação (escore ≥ 80%) | [#46](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/46) | Concluído | 301 mutantes gerados, 299 mortos e 2 sobreviventes em 22/11/2026: **99,34%** de escore bruto e **100,00%** de escore efetivo (meta ≥ 80% superada); expansão da suíte para 125 casos com foco em dízimas fracionárias, retornos de rejeição e limiar de comprometimento; evidência em `docs/relatorios/evidencias/mutacao/emprestimo-execucao-2-depois.txt` |
| Testes de sistema (Selenium) — Empréstimo, RF05 | [#59](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/59) | Concluído | 6 cenários automatizados em Chrome headless, todos passando (ver seção 6.2); evidências em `tests/system/emprestimo/evidencias/` |
| Inspeção SonarQube — Empréstimo | [#51](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/51) | Concluído | Resolução de todos os 8 apontamentos de acessibilidade em `app/templates/emprestimo.html`; refatoração com docstrings e modularização em `SimuladorEmprestimo` preservando complexidade ciclomática (CC = 10 em `_validar_entrada`, soma de CC = 30); 0 apontamentos abertos; detalhes em `docs/relatorios/inspecao_sonar.md` (seção 6.2) |

**Decisões e particularidades:**

- **Precedência de validação (TC-05):** A verificação de teto proporcional à faixa de renda (`principal > teto_por_renda(renda)`) é executada antes da análise de comprometimento da parcela no método `simular()`. Para renda de R$ 1.000,00 (< 2000), o teto é R$ 150,00 (15%), fazendo com que o valor solicitado de R$ 200,00 seja recusado por `acima_teto` (comportamento registrado e comprovado na evidência manual original da issue #11).
- **Validação nativa de formulário (TC-04):** O campo `meses` no template `emprestimo.html` possui o atributo nativo `min="2"`. O Chrome headless bloqueia o envio via `rangeUnderflow` antes de submeter a requisição POST (evidência `evidenciastc04-prazo-invalido.png`), comportamento verificado pelo método `campo_abaixo_do_minimo("meses")` do Page Object.
- **Mutação e Triagem de Equivalentes (#46):** A suíte foi ampliada de 118 para 125 casos para eliminar mutantes que sobreviviam por falta de teste de parcelas com dízima periódica (R$ 100 em 3 meses a taxa zero e SAC fracionário) e asserções incompletas nos retornos de recusa. Os 2 mutantes sobreviventes remanescentes foram justificados como equivalentes: `teto_por_renda__mutmut_1` (`renda < 0` vs `<= 0`, onde renda 0 resulta em `0.0 * 0.15 = 0.0`) e `simular__mutmut_205` (`round(sum(parcelas), 3)` vs `round(..., 2)`, cujas parcelas de 2 casas produzem somas idênticas em 2 e 3 casas decimais). Escore final: **99,34%** (bruto) e **100,00%** (descontando equivalentes).
- **Inspeção Estática e Acessibilidade (#51):** A classe de domínio `SimuladorEmprestimo` não possuía apontamentos estáticos no perfil Sonar way comprehensive. A atuação focou na adição de docstrings, constantes e modularização, preservando a complexidade ciclomática (CC = 10 em `_validar_entrada`, acumulada = 30) conforme requisito do trabalho. Na camada web (`app/templates/emprestimo.html`), foram corrigidos 8 apontamentos do Sonar (4 bugs e 4 code smells de acessibilidade/WCAG 2.0), vinculando labels a inputs com IDs estáveis.

### 6.7 Testes de integração das rotas Flask (`test_client`) — Vinicius Sales Felinto

Implementação da suíte de testes de integração para validar o ciclo completo das rotas HTTP, controladores, templates Jinja2, gerenciamento de sessões, mensagens flash, camadas de serviço e persistência em banco SQLite temporário.

**Localização:** [`tests/integration/`](../tests/integration/)
- Fixtures e configuração: [`tests/integration/conftest.py`](../tests/integration/conftest.py) (`app` com `TESTING=True` e `DATABASE` temporário via `tmp_path`, `cliente` `test_client`, `conexao_banco`, `cliente_autenticado` e `definir_saldo`).
- Testes das rotas: [`tests/integration/test_rotas.py`](../tests/integration/test_rotas.py).

| Módulo / Rota | Verificações de Integração | Qtd. Casos | Resultado |
|---|---|:---:|:---:|
| Autenticação e Dashboard (`/registro`, `/login`, `/logout`, `/`) | Acesso público anônimo, fluxo completo de cadastro → dashboard com saldo R$ 0,00 e extrato limpo → logout → login → dashboard; validações de erro com flash messages (e-mail duplicado, dados em branco e credenciais inválidas) | 5 | ✅ |
| Rotas Protegidas (`/`, `/pix`, `/emprestimo`, `/tarifas`, `/credito`) | Redirecionamento 302 com cabeçalho `Location: /login` e renderização do formulário ao seguir redirecionamento tanto em requisições `GET` quanto em `POST` sem sessão ativa | 9 | ✅ |
| Transferência PIX (`/pix`) | Formulário GET autenticado; POST de transferência com saldo suficiente (debita saldo, cria extrato no dashboard com descrição `PIX cpf` e mensagem de sucesso); recusa por valor inválido (texto e negativo); recusa por saldo insuficiente e recusa por formato de chave inválida | 6 | ✅ |
| Serviços Financeiros (`/emprestimo`, `/tarifas`, `/credito`) | Exibição de formulários GET; POST de simulação de empréstimo aprovada (parcelamento e total) e reprovada; POST de consulta de tarifas com cálculo de tarifa mensal; POST de análise de crédito com situação, score e limite sugerido | 6 | ✅ |
| Encerramento de Sessão (`/logout`) | Chamada a `/logout` limpando `cliente_id` da sessão Flask e bloqueando novos acessos subsequentes a rotas autenticadas | 2 | ✅ |

**Resultado (22/11/2026):** **28 testes de integração aprovados** (`uv run pytest tests/integration -q` em 20.54s). Assegura que todas as rotas da aplicação web foram exercitadas de ponta a ponta com banco limpo e isolado entre cada execução.

### 6.8 `TarifaBancaria` — Daniel Izu

| Item | Issue | Situação | Resultado |
|---|---|---|---|
| Unitários ampliados + cobertura estrutural (todas-arestas) | [#40](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/40) | Concluído | 122 casos em 22/11/2026 (antes: 44): 118 passam e 4 `xfail` que documentam defeitos; **100%** de cobertura de arestas (antes: 97%, linha 49 não coberta) |
| Defeito: `tarifa_anual` ignora a antiguidade | [#77](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/77) | Corrigido na #50 | Revelado na #40; `tarifa_anual` passou a repassar `antiguidade_meses`; o teste virou regressão (`vl_anual_antiguidade_35/36`) |
| Defeito: meia tarifa do pacote premium usa a tarifa da corrente | [#78](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/78) | Corrigido na #78 | Revelado na #40 (regra R3) e confirmado na interface na #58. **Decisão do grupo:** é defeito no código, e a meia tarifa é 50% da tarifa do próprio tipo de conta, como no desconto de 30% (`premium * 0.7`). Premium com pacote e saldo ≥ 5.000 ou 24 meses: 15,00 → **25,00**; a corrente continua 15,00 (caso novo `td_r3_corrente_pacote_saldo_6000`). Os 3 testes unitários e o de sistema viraram regressão. CC de `tarifa_mensal` 14 → 15; Sonar: 0 apontamentos em tarifas; mutação: 104 mutantes, 96 mortos (**92,3%**; antes 92,1%) |
| Mutação (escore ≥ 80%) | [#45](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/45) | Concluído | 106 mutantes, 100 mortos: **94,3%** (antes: 82,1%; 100% descontando 6 equivalentes justificados); +7 casos (`custom_`, `vl_`, `pe_`) que exercitam os arredondamentos; mutmut executado no Ubuntu (WSL 2); evidências em [`docs/relatorios/evidencias/mutacao/`](relatorios/evidencias/mutacao/) |
| Correções do Sonar | [#50](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/50) | Concluído | 7 apontamentos de tarifas corrigidos (`tarifas.py`: 1 → 0; `tarifas.html`: 6 → 0); projeto: 37 → 30. `tarifa_mensal` reescrita sem aninhamento: complexidade cognitiva ≤ 15 e CC 14 (antes 12). Detalhes na seção 6.4 de [`docs/relatorios/inspecao_sonar.md`](relatorios/inspecao_sonar.md) |

**Técnicas aplicadas** (identificadas pelo prefixo do id de cada caso em `tests/unit/test_tarifas.py`):

- **Partição de equivalência (`pe_`, 21 casos)**: as 18 combinações de tipo de conta × pacote × saldo (negativo / zero / positivo), antiguidade negativa/nova/média/alta e `tarifa_anual`.
- **Análise de valor-limite (`vl_`, 25 casos)**: faixas de isenção (999,99/1000, 4999,99/5000/5000,01, 49999,99/50000), antiguidade 35/36/37 sem pacote e 23/24/25 com pacote, saldo -0,01/0 e 9/10/11 transações.
- **Tabela de decisão (`td_`, 29 casos)**: sem pacote, isenção × antiguidade ≥ 36 × saldo negativo × extras (12 combinações possíveis, precedência isenção > antiguidade > saldo negativo); com pacote, tipo × saldo ≥ 50000 × saldo ≥ 5000 × antiguidade ≥ 24 (12 combinações).
- **Teste de laços**: não se aplica, a classe não possui laços.
- **Baseada em defeitos (mutação, mutmut)**: os 19 sobreviventes da primeira execução foram triados: 13 mortos por casos com tarifas em centavos (as tarifas padrão são redondas e não exercitavam os `round`) e 6 equivalentes justificados. Detalhes em [`docs/relatorios/cobertura_mutacao.md`](relatorios/cobertura_mutacao.md).

**Defeitos e decisões:**

- Os defeitos #77 e #78 ficaram com o teste marcado como `xfail(strict=True)` para não bloquear o mutmut (#45) até serem corrigidos (#77 na #50, #78 na #78); as marcações foram removidas e os casos viraram testes de regressão.
- `_tarifa_com_pacote` é código morto (nunca chamado), e a faixa de isenção da poupança (1000) nunca é consultada por `tarifa_mensal`; ficam como entrada para a #50 (Sonar).
- Os testes foram gerados com IA em duas rodadas, cada uma com a solução inicial preservada e revisada: 2 duplicados removidos, 1 partição inválida acrescentada, oráculo de `tarifa_anual` corrigido (comprovado por mutação manual), `xfail` restrito a `TypeError` e 3 cenários da premium recuperados na tabela de decisão. Detalhes em [`docs/relatorios/cobertura_mutacao.md`](relatorios/cobertura_mutacao.md) e na sessão 20 do [AI-LOG](ai/AI-LOG.md).

### 6.9 Integração serviços ↔ repositório — Daniel Izu ([#54](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/54))

**Escopo e diferença para a #55 (seção 6.7):** na #55, o teste entra pelas rotas HTTP com o `test_client`. Aqui não há HTTP: os testes chamam `AuthService` e `TransacaoService` diretamente sobre o **`SqliteRepositorio` real** (`SqliteRepositorio(get_db)` dentro de `app.app_context()`, com `DATABASE` num arquivo em `tmp_path`) e sobre o **`MemoriaRepositorio`**. O app Flask só fornece o contexto e o banco temporário. **Nenhum mock** é usado.

**Localização:** [`tests/integration/`](../tests/integration/)
- Fixtures acrescentadas em [`conftest.py`](../tests/integration/conftest.py), sem alterar as da #55: `repo_sqlite`, `repo_memoria` e `repositorio`. A `repositorio` é parametrizada em `sqlite` e `memoria`, e o mesmo teste roda nas duas implementações.
- [`test_servicos_repositorio.py`](../tests/integration/test_servicos_repositorio.py): serviços sobre o repositório real.
- [`test_contrato_repositorio.py`](../tests/integration/test_contrato_repositorio.py): contrato da classe abstrata `Repositorio`, chamado diretamente.

| Grupo | Verificações | Casos | Resultado |
|---|---|:---:|:---:|
| `AuthService` com repositório real | Registra e autentica (mesmo id; e-mail salvo em minúsculas e sem espaços; `senha_hash` começa com `pbkdf2:sha256` e é diferente da senha); autentica com e-mail em maiúsculas e espaços; e-mail duplicado → `EmailJaCadastrado` (2 variações); registro inválido (nome, e-mail ou senha vazios; senha com 5 caracteres) → `CredenciaisInvalidas` sem gravar cliente; senha errada e e-mail inexistente → `CredenciaisInvalidas` | 10 × 2 | ✅ |
| `TransacaoService`: PIX aprovado | Saldo 1000, PIX 300 → retorno 700, saldo 700 gravado e 1 transação (`pix`, −300, `PIX email`); dois PIX seguidos (saldo 500, extrato com 2 itens na ordem); o PIX do cliente A não aparece no extrato do B | 3 × 2 | ✅ |
| Transferência recusada | Saldo insuficiente (`SALDO_INSUFICIENTE`), chave inválida (`CHAVE_INVALIDA`) e limite noturno às 22h com 1500 (`FORA_HORARIO`): confere `TransacaoRecusada.resultado`, saldo inalterado e extrato vazio; cliente inexistente → `TransacaoRecusada` | 4 × 2 | ✅ |
| Persistência (só SQLite) | Dados gravados num `app.app_context()` são lidos num contexto novo (conexão nova) e conferem com `SELECT` direto no banco; `DATABASE` fica dentro de `tmp_path` | 2 | ✅ |
| Contrato do `Repositorio` | `criar_cliente` (saldo 0, score 500, ids distintos); busca por id e por e-mail; inexistentes → `None`; `atualizar_saldo` e `atualizar_score` persistem; `registrar_transacao` devolve data ISO; `listar_transacoes` mantém a ordem de inserção | 8 × 2 | ✅ |
| Divergências entre as implementações | Comportamento atual fixado em testes separados por implementação (ver abaixo) | 4 | ✅ |

**Resultado (22/11/2026):** **56 testes novos** passando. `uv run pytest tests/integration -q`: **84 passed** (os 28 da #55 e os 56 novos). Cobertura de linhas e arestas de `app/servicos` e `app/repositorios` com os testes de integração: **100%** (136 statements, 18 ramos). Nenhum `banco.db` criado no workspace: uma fixture autouse compara a existência e o `mtime` de `banco.db` na raiz antes e depois de cada teste. Suíte completa (`uv run pytest`): **638 passed e 3 xfailed** (defeito #78, de outra issue; os bugs de PIX #16 e #17 foram corrigidos depois, no commit `e7881bd`, PR #89). Evidência em [`docs/relatorios/evidencias/integracao/servicos-repositorio.txt`](relatorios/evidencias/integracao/servicos-repositorio.txt).

**Divergências e observações** (o código de produção não foi alterado):

- **E-mail duplicado direto no repositório:** o SQLite recusa com `sqlite3.IntegrityError`, porque a coluna `email` é `UNIQUE`; a memória aceita e cria outro cliente. O `AuthService` evita o caso, porque confere o e-mail antes de criar.
- **`atualizar_saldo` com id inexistente:** o SQLite não faz nada; a memória lança `KeyError`.
- **Tipo do horário:** `TransacaoService.transferir_pix` anota `horario: datetime | None`, mas `TransacaoPix.autorizar` espera `datetime.time`. Os testes sempre passam `horario=time(...)`, porque sem horário o resultado dependeria da hora da execução (o limite noturno começa às 20h).
- Chaves de e-mail com dois `@` (bug #16) e chargeback (bug #17) não foram usadas.
- Os testes foram gerados com IA. A solução inicial foi preservada (`829b937`), e a revisão acrescentou o caso de registro inválido, que leva `auth.py` de 94% para 100% sem depender dos testes de rota da #55 (`093eed1`). Detalhes na sessão 23 do [AI-LOG](ai/AI-LOG.md).

### 6.10 `TransacaoPix` — Alexandre Colmenero

#### 6.10.1 Planejamento dos testes (elaborado antes da execução)

**Objetivo.** Comprovar o requisito funcional RF03 (transferência PIX) e a manutenibilidade da classe (`app/dominio/pix.py`) com as técnicas funcional, estrutural e baseada em defeitos; automatizar o fluxo principal e os fluxos de recusa na interface (Selenium); resolver os apontamentos do Sonar da funcionalidade; preservar a complexidade ciclomática ≥ 10.

**Itens sob teste.** `validar_chave`, `autorizar`, `solicitar_chargeback`, `_eh_noturno` e a rota/tela `/pix`. O chargeback e a lista de chaves bloqueadas não são alcançáveis pela interface — permanecem no nível de unidade.

**Estado inicial (22/11/2026).** 68 casos em `tests/unit/test_pix.py`, todos passando; cobertura de arestas 100% (101 statements, 50 branches); CC máxima 11 (`autorizar`) e 10 (`solicitar_chargeback`). Os defeitos #16 e #17 já foram corrigidos (commit `e7881bd`, PR #89) e têm casos de regressão na suíte.

**Técnicas e casos planejados** (a técnica é identificada no id do `pytest.param` ou em comentário):

| Técnica | Método/Fluxo | Casos planejados |
|---|---|---|
| Partição de equivalência | `validar_chave` | CPF válido (com e sem pontuação); CPF inválido por dígito verificador (1º e 2º), dígitos repetidos, curto/longo e sem dígitos; e-mail válido, sem `@`, com dois `@` (regressão #16), domínio sem ponto e com ponto no início/fim; telefone 10/11 dígitos e formatado; aleatória 31/32/33 caracteres; vazio e tipo desconhecido |
| Análise de valor-limite | `autorizar` | valor 0 e 0,01; limites diurnos 4999,99 / 5000,00 / 5000,01; noturnos 999,99 / 1000,00 / 1000,01; saldo igual e logo abaixo do valor; fronteiras de horário 19:59 / 20:00 / 5:59 / 6:00 / 6:01 |
| Tabela de decisão | `autorizar` | precedência valor → chave → bloqueio → horário/limite → saldo → aprovada; chave bloqueada combinada com valor inválido e com valor válido |
| Tabela de decisão | `solicitar_chargeback` | dias -1 / 0 / 7 / 8 / 30 / 31 / 90 / 91; valor 0, 5000,00 e 5000,01; motivo golpe/fraude/vazio; chave bloqueada em cada faixa (regressão #17) |
| Teste de laços | `_validar_cpf` | laço dos dois dígitos verificadores: falha no 1º, falha no 2º e CPF válido |
| PE + valor-limite | `_eh_noturno` | janela padrão (20h–6h) e janela customizada, inclusive com virada de dia (22h–2h); fronteiras exatas |
| Parâmetros customizados | construtor | `ConfiguracaoPix` com limites e prazo de chargeback próprios (preparação para a mutação) |
| Sistema (Selenium) | `/pix` | CT-01 aprovado; CT-02 chave inválida; CT-03 saldo insuficiente; CT-04 e-mail com dois `@` (regressão #16); CT-05 valor ≤ 0 barrado pelo HTML5; guarda sem login |

**Dados de teste.** CPF válido `529.982.247-25`; CPFs inválidos `123.456.789-00` e dígitos repetidos; e-mails `user@example.com`, `a@b@c.com`, `@example.com`, `user@example` etc.; telefones `(21) 2222-3333` e `21988887777`; chave aleatória de 32 caracteres; valores e horários da tabela acima.

**Oráculos.** Valores esperados explícitos derivados de `docs/aplicacao.md` §4.1 — nunca calculados pelo próprio código sob teste. Nos testes de sistema, o saldo inicial é definido diretamente no SQLite temporário (a interface não tem depósito), e os cenários evitam os limites por horário para não depender do relógio da máquina.

**Ambiente e comandos.**

```bash
uv run pytest tests/unit/test_pix.py --cov=app.dominio.pix --cov-branch --cov-report=term-missing
uv run radon cc app/dominio/pix.py -s
uv run mutmut run   # configuração isolada (only_mutate), sem versionar
uv run pytest tests/system/pix -v   # e EVIDENCIAS=1 para os prints
./scripts/sonar_local.sh scan
```

**Critérios de aceite.**

- #38: casos ampliados e executados; cobertura de arestas ≥ 80% na classe.
- #43: escore de mutação ≥ 80%; sobreviventes triados e justificados.
- #48: apontamentos da funcionalidade PIX resolvidos ou justificados; print "depois"; CC ≥ 10 preservada; suíte verde.
- #56: fluxo principal e recusas automatizados; testes determinísticos e independentes; evidências.

**Riscos e mitigação.**

| Risco | Mitigação |
|---|---|
| `autorizar` usa `datetime.now()` quando o horário não é informado | testes sempre passam `horario` fixo |
| Limites diurno/noturno dependem do horário da execução (sistema) | cenários de sistema usam valores válidos nas duas janelas |
| Saldo inicial zero na interface | fixture define o saldo no SQLite antes do cenário |
| Sonar local desatualizado (análise de 11/11) | re-scan com o script antes e depois das correções |
| Mutantes equivalentes | triagem e justificativa no relatório |

**Resultados:** registrados nas seções 6.10.2 (unitários/cobertura), 6.10.3 (mutação), 6.10.4 (Sonar) e 6.10.5 (sistema), à medida que as issues forem concluídas.

#### 6.10.2 Unitários e cobertura estrutural — issue #38

**Resultado (22/11/2026):** suíte ampliada de 68 para **104 casos**, todos passando; cobertura de arestas mantida em **100%** (101 statements, 50 branches). Os 2 casos que falhavam na Entrega 1 eram os defeitos #16 e #17, corrigidos no commit `e7881bd` (PR #89) e mantidos como regressão. Comando, saída e data em [`docs/relatorios/evidencias/cobertura/pix-cobertura.txt`](relatorios/evidencias/cobertura/pix-cobertura.txt); detalhes na seção `TransacaoPix` de [`docs/relatorios/cobertura_mutacao.md`](relatorios/cobertura_mutacao.md).

#### 6.10.3 Mutação — issue #43

**Resultado (22/11/2026):** `mutmut` isolado em `app/dominio/pix.py` — **148 mutantes, 144 mortos (97,3%)**; os 4 sobreviventes são equivalentes justificados (100% descontando equivalentes). Meta da disciplina: ≥ 80% ✅. A 1ª execução (104 casos) já atingia 91,9%; os 7 casos novos mataram 8 sobreviventes, com mapeamento mutante → teste verificado por `mutmut apply`. Evidências em [`docs/relatorios/evidencias/mutacao/pix-execucao-1-antes.txt`](relatorios/evidencias/mutacao/pix-execucao-1-antes.txt) e [`pix-execucao-2-depois.txt`](relatorios/evidencias/mutacao/pix-execucao-2-depois.txt); detalhes na seção `TransacaoPix` de [`docs/relatorios/cobertura_mutacao.md`](relatorios/cobertura_mutacao.md).

#### 6.10.4 Defeitos #16/#17 e inspeção Sonar — issue #48

**Resultado (22/11/2026):** a funcionalidade PIX passou de **7 para 0 apontamentos** no SonarQube local (perfil *Sonar way comprehensive* + Web padrão): 6 de acessibilidade/IDs em `pix.html` (`id`/`for` em `chave`, `tipo` e `valor`) e 1 `python:S1192` em `routes/pix.py` (constante `_TEMPLATE`). A classe `pix.py` segue com 0 apontamentos e CC preservada (11/10). Projeto: 26 → 19 apontamentos abertos (nenhum de PIX). Os defeitos funcionais #16/#17 já haviam sido corrigidos no commit `e7881bd` (PR #89) e são cobertos pelos testes de regressão. Suíte completa: 699 passed, 4 xfailed (defeito #78, Tarifas — unitários e sistema). Detalhes na seção 6.5 de [`docs/relatorios/inspecao_sonar.md`](relatorios/inspecao_sonar.md); evidências em [`docs/relatorios/evidencias/sonar/depois/pix/`](relatorios/evidencias/sonar/depois/pix/).

#### 6.10.5 Testes de sistema (Selenium) — issue #56

**Resultado (22/11/2026):** `tests/system/pix/` criado com page object (`pagina_pix.py`, seletores por `id` definidos na #48) e 6 cenários automatizados: PIX aprovado com CPF válido; recusa por chave inválida; recusa por saldo insuficiente; regressão do defeito #16 (e-mail com dois `@`); valor zero barrado pelo HTML5 (`min="0.01"`); guarda de autenticação. Saldo inicial definido pela fixture `definir_saldo_sistema` (SQLite temporário), cenários independentes de horário. Resultado: 6/6 passando em execuções repetidas; suíte de sistema completa: 55 passed, 1 xfailed. Evidências em `tests/system/pix/evidencias/` (com `EVIDENCIAS=1`); tabela de cenários na seção 6.2.

---