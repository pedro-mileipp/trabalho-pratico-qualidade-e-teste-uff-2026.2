# 📌 Plano de Teste — Banco Digital

> Plano de Teste da **Entrega 1** do trabalho prático de Qualidade e Teste (UFF 2026.2).

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
| 1.14 | 22/11/2026 | Daniel Izu | Entrega 2: ampliação dos testes unitários e cobertura estrutural todas-arestas (100%) de `TarifaBancaria` (issue #40), defeitos #77 e #78, na seção 6.8; antiguidade passa a ser coberta por testes unitários (seção 1.1.2) |

---

## 📖 1. Introdução

O presente Plano de Teste tem como finalidade descrever as estratégias, processos e métodos utilizados para assegurar a qualidade do sistema **Banco Digital**.

O principal objetivo é verificar se as funcionalidades implementadas atendem aos requisitos definidos, além de garantir uma experiência de uso confiável e adequada ao público alvo.

Para isso, foram adotadas abordagens de **testes unitários** e **testes manuais**, contemplando funcionalidades como autenticação de usuários, transferência PIX, consulta de tarifas, simulação de empréstimo e análise de crédito. O processo de verificação e validação foi conduzido de forma iterativa, possibilitando a identificação antecipada de falhas e a evolução contínua do sistema ao longo da Entrega 1.

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
| Testes de sistema com Selenium, cobertura estrutural e mutação | Previstos para a Entrega 2 |

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

---

## 🔬 2. Metodologia de Teste

### 🔄 2.1 Fases de Teste

No projeto foram conduzidas as seguintes fases de teste na Entrega 1:

- **Teste de Unidade:** classes puras de `app/dominio/` testadas com **pytest**, aplicando partição de equivalência, análise de valor-limite, tabela de decisão e teste de laços. Suíte em `tests/unit/` (1 arquivo por classe).
- **Teste de Sistema (manual):** casos executados na interface do Flask em `tests/testes_manuais/` (PIX, Auth, Tarifas, Empréstimo e Crédito), com evidências por caso.
- **Gestão de casos:** casos manuais registrados no TestLink, com relatório do caso Auth exportado em PDF ([Auth — Relatório TestLink](https://drive.google.com/file/d/14yShZiduI8gixsV5wCQqA70DH2TV4SN4/view?usp=sharing)).

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
  - [#16](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/16) — e-mail com dois `@` aceito como válido (PIX)
  - [#17](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/17) — chave bloqueada ignora regra de valor no chargeback (PIX)
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

### 💻 4.2 Ambiente de Teste

Para a execução do sistema e realização dos testes, é necessário dispor de um ambiente compatível com as tecnologias utilizadas no desenvolvimento do projeto.

**Requisitos de Software:**

- Sistema operacional macOS, Linux ou Windows
- Python **3.12** gerenciado por **uv**
- Navegador Google Chrome
- Banco de dados **SQLite** (arquivo em `/tmp` no ambiente de teste, fora do workspace)
- Servidor de desenvolvimento **Flask**

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

---

## 🚀 6. Entrega 2 — Resultados

> Seção em construção: cada integrante adiciona a subseção da sua classe ao concluir as issues da Entrega 2. O detalhamento (comandos, saídas e casos) fica em [`docs/relatorios/cobertura_mutacao.md`](relatorios/cobertura_mutacao.md).

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
| Testes de sistema (Selenium) — Empréstimo, RF05 | [#59](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/59) | Concluído | 6 cenários automatizados em Chrome headless, todos passando (ver seção 6.2); evidências em `tests/system/emprestimo/evidencias/` |

**Decisões e particularidades:**

- **Precedência de validação (TC-05):** A verificação de teto proporcional à faixa de renda (`principal > teto_por_renda(renda)`) é executada antes da análise de comprometimento da parcela no método `simular()`. Para renda de R$ 1.000,00 (< 2000), o teto é R$ 150,00 (15%), fazendo com que o valor solicitado de R$ 200,00 seja recusado por `acima_teto` (comportamento registrado e comprovado na evidência manual original da issue #11).
- **Validação nativa de formulário (TC-04):** O campo `meses` no template `emprestimo.html` possui o atributo nativo `min="2"`. O Chrome headless bloqueia o envio via `rangeUnderflow` antes de submeter a requisição POST (evidência `evidenciastc04-prazo-invalido.png`), comportamento verificado pelo método `campo_abaixo_do_minimo("meses")` do Page Object.

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
| Defeito: `tarifa_anual` ignora a antiguidade | [#77](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/77) | Aberto | Revelado na #40; teste com `xfail(strict=True)` |
| Defeito: meia tarifa do pacote premium usa a tarifa da corrente | [#78](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/78) | Aberto (a confirmar pelo grupo) | Revelado na tabela de decisão (regra R3); teste com `xfail(strict=True)` |

**Técnicas aplicadas** (identificadas pelo prefixo do id de cada caso em `tests/unit/test_tarifas.py`):

- **Partição de equivalência (`pe_`, 21 casos)**: as 18 combinações de tipo de conta × pacote × saldo (negativo / zero / positivo), antiguidade negativa/nova/média/alta e `tarifa_anual`.
- **Análise de valor-limite (`vl_`, 25 casos)**: faixas de isenção (999,99/1000, 4999,99/5000/5000,01, 49999,99/50000), antiguidade 35/36/37 sem pacote e 23/24/25 com pacote, saldo -0,01/0 e 9/10/11 transações.
- **Tabela de decisão (`td_`, 29 casos)**: sem pacote, isenção × antiguidade ≥ 36 × saldo negativo × extras (12 combinações possíveis, precedência isenção > antiguidade > saldo negativo); com pacote, tipo × saldo ≥ 50000 × saldo ≥ 5000 × antiguidade ≥ 24 (12 combinações).
- **Teste de laços**: não se aplica, a classe não possui laços.

**Defeitos e decisões:**

- Os defeitos #77 e #78 ficam com o teste marcado como `xfail(strict=True)` para não bloquear o mutmut (#45); a correção remove a marcação.
- `_tarifa_com_pacote` é código morto (nunca chamado), e a faixa de isenção da poupança (1000) nunca é consultada por `tarifa_mensal`; ficam como entrada para a #50 (Sonar).
- Os testes foram gerados com IA em duas rodadas, cada uma com a solução inicial preservada e revisada: 2 duplicados removidos, 1 partição inválida acrescentada, oráculo de `tarifa_anual` corrigido (comprovado por mutação manual), `xfail` restrito a `TypeError` e 3 cenários da premium recuperados na tabela de decisão. Detalhes em [`docs/relatorios/cobertura_mutacao.md`](relatorios/cobertura_mutacao.md) e na sessão 19 do [AI-LOG](ai/AI-LOG.md).

---