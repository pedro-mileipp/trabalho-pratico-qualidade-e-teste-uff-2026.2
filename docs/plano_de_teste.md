# Plano de Teste — Banco Digital

> Trabalho prático de Qualidade e Teste (UFF 2026.2) — Entregas 1 e 2.
>
> Plano oficial do repositório.

## Registro de Mudanças

| Versão | Data | Autor | Descrição |
|------|--------|----------|--------|
| 1.0 | 21/09/2026 | Alexandre Colmenero | Criação do Plano de Teste com base nos testes executados na Entrega 1 |
| 1.1 | 23/09/2026 | Alexandre Colmenero | Atualização para refletir o estado atual dos testes (fix do `test_credito`, tarifas manual preenchida, resultados da suíte) |
| 1.2 | 11/11/2026 | Pedro Mileipp | Entrega 2: `DecisorCredito` (técnicas funcionais e cobertura estrutural, issue #42); #35 reclassificado como erro de teste |
| 1.3 | 11/11/2026 | Pedro Mileipp | Entrega 2: testes de sistema com Selenium — Crédito/RF06 (issue #60) e base compartilhada dos testes de sistema |
| 1.4 | 11/11/2026 | Pedro Mileipp | Entrega 2: requisito não funcional de segurança da autenticação — RNF06 (issue #61) |
| 1.5 | 12/11/2026 | Pedro Mileipp | Entrega 2: mutação do `DecisorCredito` (issue #47) |
| 1.6 | 18/11/2026 | Pedro Mileipp | Entrega 2: correções do Sonar na funcionalidade de crédito (issue #52) |
| 1.7 | 20/11/2026 | Gabrielle Rosa | Entrega 2: correção do bug de desconto de IR no mês 12 em `CalculadoraJuros` (issue #20) |
| 1.8 | 20/11/2026 | Gabrielle Rosa | Entrega 2: testes unitários com mock do repositório para `AuthService` e `TransacaoService` (issue #53) |
| 1.9 | 20/11/2026 | Gabrielle Rosa | Entrega 2: ampliação dos testes unitários e cobertura estrutural todas-arestas (100%) de `CalculadoraJuros` (issue #39) |
| 1.10 | 20/11/2026 | Gabrielle Rosa | Entrega 2: teste de mutação de `CalculadoraJuros` com `mutmut` (escore 87,25%, issue #44) |
| 1.11 | 20/11/2026 | Gabrielle Rosa | Entrega 2: testes de sistema com Selenium — Autenticação/RF01 e RF02 (issue #57) |
| 1.12 | 22/11/2026 | Vinicius Sales Felinto | Entrega 2: testes de sistema com Selenium — Empréstimo/RF05 (issue #59) |
| 1.13 | 22/11/2026 | Vinicius Sales Felinto | Entrega 2: testes de integração das rotas Flask com test_client |
| 1.14 | 22/11/2026 | Vinicius Sales Felinto | Entrega 2: teste de mutação de `SimuladorEmprestimo` com `mutmut` (escore 99,34%, issue #46) |
| 1.14 | 22/11/2026 | Daniel Izu | Entrega 2: ampliação dos testes unitários e cobertura estrutural todas-arestas (100%) de `TarifaBancaria` (issue #40), defeitos #77 e #78; antiguidade passa a ser coberta por testes unitários (seção 1.1.2) |
| 1.15 | 22/11/2026 | Daniel Izu | Entrega 2: teste de mutação de `TarifaBancaria` com `mutmut` (escore 94,3%; 100% descontando equivalentes, issue #45) |
| 1.16 | 22/11/2026 | Vinicius Sales Felinto | Entrega 2: correções do Sonar na funcionalidade de empréstimo (issue #51) |
| 1.16 | 22/11/2026 | Gabrielle Rosa | Entrega 2: inspeção estática SonarQube em `CalculadoraJuros` — 0 apontamentos e evidência pós-correção (issue #49) no registro de mudanças |
| 1.17 | 22/11/2026 | Daniel Izu | Entrega 2: correção dos apontamentos do Sonar em `TarifaBancaria` e `tarifas.html` (7 → 0) e do defeito #77 (issue #50) |
| 1.18 | 22/11/2026 | Daniel Izu | Entrega 2: testes de integração serviços ↔ repositório, sem mocks, no `SqliteRepositorio` e no `MemoriaRepositorio` (issue #54) |
| 1.19 | 22/11/2026 | Alexandre Colmenero | Entrega 2: atualização global do plano (escopo, estado atual, ferramentas e critérios) e planejamento dos testes de `TransacaoPix` — issues #38, #43, #48 e #56 |
| 1.20 | 22/11/2026 | Alexandre Colmenero | Entrega 2: ampliação dos testes unitários de `TransacaoPix` para 104 casos e cobertura estrutural todas-arestas (100%, issue #38) |
| 1.21 | 22/11/2026 | Alexandre Colmenero | Entrega 2: teste de mutação de `TransacaoPix` com `mutmut` (escore 97,3%; 100% descontando 4 equivalentes, issue #43) |
| 1.22 | 22/11/2026 | Daniel Izu | Entrega 2: testes de sistema com Selenium — Tarifas/RF04 (issue #58); defeito #78 confirmado na interface |
| 1.22 | 22/11/2026 | Alexandre Colmenero | Entrega 2: correções do Sonar na funcionalidade PIX (7 → 0 apontamentos, issue #48) |
| 1.23 | 22/11/2026 | Alexandre Colmenero | Entrega 2: testes de sistema com Selenium — PIX/RF03 (issue #56) |
| 1.24 | 22/11/2026 | Daniel Izu | Entrega 2: avaliação ISO/IEC 25010:2023 das 9 características, com escala e evidências (issue #62), em `docs/relatorios/iso25010.md` |
| 1.25 | 22/11/2026 | Daniel Izu | Entrega 2: correção do defeito #78 (meia tarifa do pacote sobre a tarifa do próprio tipo de conta: premium 25,00), decisão do grupo; 4 `xfail` viram regressão e 1 caso novo da corrente; mutação de `TarifaBancaria` 92,3%; estado atual |
| 1.26 | 23/11/2026 | Pedro Mileipp | Entrega 2: inspeção Sonar consolidada das 5 classes (issue #63): 40 → 19 apontamentos, 26 corrigidos, 0 nas classes |
| 2.0 | 23/11/2026 | Alexandre Colmenero | Reorganização do plano  |


---

## 1. Introdução

O **Banco Digital** é uma aplicação web Flask com autenticação, transferência PIX, consulta de tarifas, simulação de empréstimo e análise de crédito, além de classes de domínio responsáveis pelas regras de negócio. Este plano descreve o escopo, a metodologia, as responsabilidades, os recursos e os entregáveis dos testes das **Entregas 1 e 2**.

Na **Entrega 1**, o esforço concentrou-se em testes unitários das classes de domínio e em casos manuais executados na interface, com gestão no TestLink. Na **Entrega 2**, o processo foi ampliado com testes de integração, testes de sistema automatizados (Selenium), cobertura estrutural todas-arestas, teste de mutação, inspeção estática (SonarQube) e um requisito não funcional de segurança da autenticação (RNF06).

O trabalho seguiu a metodologia em **cascata**: o escopo e os critérios foram definidos no início de cada entrega, e as fases de teste foram executadas em ordem sequencial em cada frente. Cada integrante ficou responsável por uma classe de domínio e por uma funcionalidade, produzindo testes, evidências e, quando necessário, issues de defeito no GitHub. O detalhamento dos resultados fica nos relatórios indicados na seção 3.

### 1.1 Escopo

#### 1.1.1 No escopo

| Funcionalidade / módulo | Requisito | O que foi testado |
|---|---|---|
| Autenticação (registro, login, logout) | RF01, RF02 | Criação de conta, validação de e-mail e senha, login, logout e bloqueio de rotas protegidas |
| Transferência PIX | RF03 | Validação de chaves (CPF, e-mail, telefone e aleatória), valor, saldo, limites por horário e chargeback no domínio |
| Consulta de tarifas | RF04 | Tarifa mensal por tipo de conta, saldo, isenção, transações excedentes e pacote de serviços |
| Simulação de empréstimo | RF05 | Tabelas Price e SAC, valor mínimo, prazo, teto por renda e comprometimento da parcela |
| Análise de crédito | RF06 | Aprovação, negação e aprovação parcial por score, renda e valor solicitado |
| Regras de negócio (domínio e serviços) | RF07 | `TransacaoPix`, `CalculadoraJuros`, `TarifaBancaria`, `SimuladorEmprestimo` e `DecisorCredito` (classes de domínio com CC ≥ 10), além de `AuthService` e `TransacaoService` |

Requisitos não funcionais no escopo:

| Requisito | O que foi verificado |
|---|---|
| RNF01 – Usabilidade | Clareza das telas e das mensagens de erro nos testes manuais e de sistema |
| RNF02 – Confiabilidade | Funcionamento correto das regras de negócio e regressão após correções |
| RNF03 – Integridade dos dados | Consistência de saldo e extrato após transferências PIX |
| RNF04 – Manutenibilidade | Cobertura estrutural, mutação, complexidade ciclomática (radon) e inspeção estática |
| RNF05 – Compatibilidade | Execução dos testes em Python 3.12 gerenciado por uv, em macOS e Linux (Ubuntu/WSL 2) |
| RNF06 – Segurança (autenticação) | Rotas protegidas, logout, armazenamento da senha, mensagens de erro e cookie de sessão |

#### 1.1.2 Fora do escopo

| Item | Justificativa |
|---|---|
| Chargeback de PIX pela interface | Não exposto na UI; a regra é coberta por testes unitários |
| Antiguidade e saldo negativo de tarifas na interface | Campos não expostos no formulário; as regras são cobertas por testes unitários |
| Integrações com sistemas externos | Não fazem parte da versão atual do sistema |
| Testes de carga, desempenho e banco de dados em larga escala | Não previstos nas entregas |
| Testes de segurança avançados (pentest, varredura de vulnerabilidades) | Fora do escopo acadêmico; o RNF06 cobre apenas aspectos básicos da autenticação |
| Compatibilidade com navegadores além do Google Chrome | Os testes de sistema usam Chrome headless; outros navegadores não foram avaliados |

### 1.2 Objetivos de Qualidade

- Verificar a conformidade do sistema sob teste (SUT) com os requisitos funcionais RF01 a RF07 e não funcionais RNF01 a RNF06.
- Identificar e registrar defeitos antes da entrega, garantindo que as correções sejam cobertas por testes de regressão.
- Assegurar a manutenibilidade das classes de domínio: CC ≥ 10, cobertura todas-arestas ≥ 80%, mutação ≥ 80% e zero apontamentos do Sonar nas classes.
- Garantir a integridade dos dados de saldo e extrato e a segurança básica da autenticação.
- Manter a rastreabilidade entre requisito, issue, caso de teste e evidência.

### 1.3 Papéis e Responsabilidades

| Papel | Responsável | Atribuições |
|---|---|---|
| Gerente de teste | Todos os integrantes | Plano de Teste, cronograma, critérios de qualidade e acompanhamento das issues |
| Analista de QA | Todos os integrantes | Projeto e execução dos testes da sua classe/funcionalidade, evidências e relatórios |
| Desenvolvedor | Todos os integrantes | Implementação das funcionalidades e correção dos defeitos encontrados |
| Gerente de configuração | Alexandre Colmenero | Repositório, branches e PRs, milestones e versionamento dos artefatos |
| Gestão de casos no TestLink | Gabrielle Rosa e Pedro Mileipp | Cadastro dos casos manuais e exportação dos relatórios |
| Ambiente e instalação | Cada integrante | Execução local com uv, Chrome, SQLite e SonarQube em Docker, conforme o README |

Distribuição por classe de domínio e funcionalidade:

| Integrante | Classe de domínio (unitários, cobertura, mutação e Sonar) | Caso manual (Entrega 1) | Sistema Selenium (Entrega 2) |
|---|---|---|---|
| Alexandre Colmenero | `TransacaoPix` — PIX/RF03 | PIX | PIX |
| Gabrielle Rosa | `CalculadoraJuros` — Juros/RF07 | Autenticação (RF01/RF02) | Autenticação |
| Daniel Izu | `TarifaBancaria` — Tarifas/RF04 | Empréstimo (RF05) | Tarifas |
| Vinicius Sales Felinto | `SimuladorEmprestimo` — Empréstimo/RF05 | Tarifas (RF04) | Empréstimo |
| Pedro Mileipp | `DecisorCredito` — Crédito/RF06 | Crédito | Crédito |

Outras frentes:

- **Integração das rotas Flask (#55):** Vinicius Sales Felinto.
- **Integração serviços ↔ repositório (#54):** Daniel Izu.
- **RNF06 — segurança da autenticação (#61):** Pedro Mileipp.
- **Avaliação ISO/IEC 25010 (#62):** Daniel Izu.

O acompanhamento das atividades e dos defeitos é feito nas [issues e milestones do GitHub](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues).

---

## 2. Metodologia de Teste

### 2.1 Visão Geral

Foi adotada a metodologia em **cascata** (*waterfall*). As fases seguiram uma ordem sequencial: definição do escopo e dos requisitos, projeto dos casos, implementação dos testes, execução, correção e entrega. O escopo e os critérios de aceite foram definidos no início de cada entrega, e, em cada frente, uma fase só avançou após a conclusão da anterior — por exemplo, os testes unitários e a cobertura estrutural vieram antes da mutação, e as correções vieram antes da regressão. A escolha se justifica por:

- os requisitos serem conhecidos e estáveis no início de cada entrega;
- a disciplina exigir documentação, evidências e rastreabilidade formais;
- existir dependência entre as fases (cobertura → mutação; correção → regressão);
- o trabalho ser dividido por classe de domínio e funcionalidade, com cada integrante percorrendo as fases da sua frente.

A disciplina organizou o trabalho em duas entregas; cada uma percorreu as fases em cascata, e a Entrega 2 acrescentou as fases de integração, sistema automatizado, mutação e inspeção estática ao escopo inicial.

Os testes automatizados formam a base de regressão. Os casos manuais da Entrega 1 validaram a interface e serviram de referência para os testes de sistema automatizados da Entrega 2. A geração de testes contou com apoio de IA, sempre com revisão do responsável e registro no [AI-LOG](ai/AI-LOG.md).

As técnicas de projeto de casos utilizadas foram:

- **Funcionais:** partição de equivalência (PE), análise de valor-limite (AVL), tabela de decisão (TD) e teste de laços.
- **Estrutural:** cobertura todas-arestas (*branch coverage*).
- **Baseada em defeitos:** teste de mutação com `mutmut`.
- **Estática:** lint com `ruff`, complexidade com `radon` e inspeção com SonarQube.

A técnica usada em cada caso é registrada no prefixo do id (`pe_`, `vl_`, `td_`, `laco_`) nos arquivos de teste.

### 2.2 Fases de Teste

Além dos níveis unitário, de integração e de sistema, o processo inclui as atividades estruturais, de mutação e de inspeção estática, que dependem dos testes já escritos.

| Fase | Escopo | Ferramentas | Local e critério de saída |
|---|---|---|---|
| Teste unitário | 5 classes de domínio e serviços com repositório mockado | pytest, pytest-mock | `tests/unit/`; casos derivados por PE, AVL, TD e laços |
| Teste de integração | Rotas Flask com `test_client`; serviços sobre `SqliteRepositorio` e `MemoriaRepositorio`, sem mocks | pytest, Flask test client, SQLite temporário | `tests/integration/`; fluxos completos e contrato do repositório |
| Teste de sistema manual | Fluxos principais e de recusa na interface | Google Chrome e TestLink | `tests/testes_manuais/`; 44 casos com evidências (Entrega 1) |
| Teste de sistema automatizado | Fluxos por funcionalidade, incluindo guarda de autenticação | Selenium WebDriver e Chrome headless | `tests/system/<funcionalidade>/`; cenários verdes e prints (Entrega 2) |
| Requisito não funcional | Segurança da autenticação (RNF06) | Flask test client | `tests/rnf/seguranca/`; 22 verificações |
| Cobertura estrutural | Cobertura todas-arestas das 5 classes de domínio | pytest-cov / coverage.py com `branch=True` | [`docs/relatorios/cobertura_mutacao.md`](relatorios/cobertura_mutacao.md); meta ≥ 80% |
| Teste de mutação | Mutantes das 5 classes de domínio | mutmut | Mesmo relatório; meta ≥ 80%, com sobreviventes triados |
| Inspeção estática | Código, templates e complexidade | ruff, radon e SonarQube local | [`docs/relatorios/inspecao_sonar.md`](relatorios/inspecao_sonar.md) §7; análise consolidada antes × depois, com apontamentos resolvidos ou justificados |

### 2.3 Triagem de Erros

Todo defeito identificado em qualquer fase é registrado como issue no GitHub, com passos para reprodução, resultado esperado, resultado obtido, evidência e o teste que o revelou. A triagem classifica cada ocorrência em:

- **Defeito no código:** issue de correção, com prioridade definida pelo impacto no fluxo principal (bloqueante, alta, média ou baixa); após a correção, o teste que revelou o problema passa a fazer parte da regressão.
- **Defeito no teste:** expectativa ou oráculo incorreto; a issue é fechada com a correção do teste, sem alteração no código de produção (ex.: #35, que era erro de expectativa no crédito).
- **Problema de ambiente ou ferramenta:** ajuste de configuração ou de execução, sem issue de código.
- **Mutante sobrevivente:** triado como equivalente (justificado no relatório) ou como lacuna de teste, que gera um novo caso.
- **Apontamento do Sonar:** classificado como correção necessária ou justificativa documentada.

As correções são acompanhadas nas milestones da entrega; issues que permaneçam abertas ao final são registradas como pendências para a próxima versão.

### 2.4 Critérios de Suspensão e Requisitos de Retomada

A execução dos testes é suspensa, no todo ou em parte, quando:

- um defeito crítico impede o funcionamento de um fluxo principal;
- o ambiente necessário (SQLite, Chrome ou SonarQube) fica indisponível;
- uma taxa alta de falhas compromete a continuidade ou a confiabilidade dos resultados.

A execução é retomada após a correção do defeito ou a restauração do ambiente, com a suíte de fumaça verde e os casos afetados reexecutados. Não houve suspensão formal nas entregas: as falhas isoladas foram tratadas como issues e, quando necessário, o teste ficou marcado como `xfail(strict=True)` até a correção (ex.: defeito #78, em Tarifas).

### 2.5 Completude do Teste

O teste é considerado completo quando:

- 100% dos casos planejados foram executados e os resultados registrados;
- todas as falhas identificadas foram corrigidas ou justificadas e documentadas;
- as suítes unitária, de integração, de sistema e de RNF estão verdes;
- a cobertura todas-arestas é ≥ 80% nas 5 classes de domínio;
- o escore de mutação é ≥ 80% nas mesmas classes, com sobreviventes triados;
- os apontamentos do Sonar nas classes de domínio foram resolvidos e os demais justificados, inclusive os 5 novos dos testes de integração e o Quality Gate documentado;
- as evidências e as issues da entrega estão registradas.

### 2.6 Atividades do projeto, estimativas e cronograma

As atividades foram realizadas em paralelo entre os integrantes, respeitando a ordem das fases em cada frente. A tabela registra o período de cada atividade nas duas entregas:

| Atividade | Entrega 1 | Entrega 2 |
|---|---|---|
| Planejamento dos testes e atualização do plano | 15/09 a 23/09/2026 | 11/11 a 23/11/2026 |
| Testes unitários e cobertura estrutural | 16/09 a 21/09/2026 | 11/11 a 22/11/2026 |
| Casos de teste manuais e TestLink | 16/09 a 20/09/2026 | — |
| Testes de integração | — | 22/11/2026 |
| Testes de sistema com Selenium | — | 11/11 a 22/11/2026 |
| Teste de mutação | — | 12/11 a 22/11/2026 |
| RNF06 — segurança da autenticação | — | 11/11/2026 |
| Inspeção estática com SonarQube | — | 18/11 a 23/11/2026 |
| Avaliação ISO/IEC 25010 | — | 22/11/2026 |
| Consolidação dos resultados e entrega | 23/09/2026 | 23/11/2026 |

---

## 3. Entregáveis de Teste

Os entregáveis produzidos estão listados abaixo. Os detalhes de execução, casos e evidências ficam nos arquivos indicados; este plano não replica os resultados por classe.

**Entregáveis por fase**

| Momento | Entregáveis |
|---|---|
| Antes da execução | Plano de Teste; issues e milestones das entregas; casos manuais projetados; dados de teste (contas, chaves PIX e valores de fronteira) |
| Durante a execução | Evidências (screenshots e saídas de pytest, cobertura, mutação e Sonar); resultados de execução; issues de defeito; registro de uso de IA |
| Após a execução | Casos manuais preenchidos; suítes unitária, de integração, de sistema e de RNF; relatórios de cobertura/mutação, Sonar, RNF e ISO 25010; relatório do TestLink; plano atualizado |

**Resumo dos resultados (23/11/2026)**

| Entregável | Onde | Resultado |
|---|---|---|
| Casos de teste manuais (44) | [`tests/testes_manuais/`](../tests/testes_manuais/) | Executados na Entrega 1 com evidências por caso; relatório do TestLink do Auth em [PDF](https://drive.google.com/file/d/14yShZiduI8gixsV5wCQqA70DH2TV4SN4/view?usp=sharing) |
| Suíte automatizada | [`tests/`](../tests/) | **710 testes passando**: 548 unitários, 84 de integração, 56 de sistema e 22 de RNF (22/11/2026) |
| Cobertura estrutural | [`docs/relatorios/cobertura_mutacao.md`](relatorios/cobertura_mutacao.md) | **100%** de cobertura todas-arestas nas 5 classes de domínio |
| Teste de mutação | [`docs/relatorios/cobertura_mutacao.md`](relatorios/cobertura_mutacao.md) | **87,3% a 99,3%**; todas as classes acima de 80%; sobreviventes triados e justificados no relatório |
| Inspeção estática — antes × depois | [`docs/relatorios/inspecao_sonar.md`](relatorios/inspecao_sonar.md) §7.3 | **40 → 19** abertos; bugs **17 → 5**; code smells **22 → 13**; cobertura **60,6% → 69,7%**; duplicação **0%** |
| Inspeção estática — correções | [`docs/relatorios/inspecao_sonar.md`](relatorios/inspecao_sonar.md) §7.2–7.4 | **26 corrigidos** (1 na classe e 25 em telas/rotas); **0** nas 5 classes; **5 novos** em testes de integração; 19 restantes fora do domínio (auth 13, CSRF 1, testes 5); 1 vulnerabilidade (CSRF) |
| RNF06 — segurança da autenticação | [`docs/relatorios/rnf_seguranca.md`](relatorios/rnf_seguranca.md) | 22 testes verdes; 5 riscos documentados com recomendações |
| Avaliação ISO/IEC 25010 | [`docs/relatorios/iso25010.md`](relatorios/iso25010.md) | 9 características avaliadas com escala, evidências e melhorias recomendadas |
| Relatório de defeitos | [GitHub Issues](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues) | 5 defeitos de código e 1 erro de teste, todos encerrados (#16, #17, #20, #35, #77 e #78) |
| Rastreabilidade | [GitHub Issues e Milestones](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues) | Atividades, requisitos e defeitos ligados a issues; os ids dos casos indicam a técnica aplicada |
| Registro de uso de IA | [`docs/ai/AI-LOG.md`](ai/AI-LOG.md) | Sessões de geração, revisão e correção de testes e documentos |
| Evidências | [`docs/relatorios/evidencias/`](relatorios/evidencias/) e `tests/system/*/evidencias/` | Prints, saídas de cobertura e mutação, JSON do SonarQube e evidências finais em `evidencias/sonar/final/` |

---

## 4. Necessidades de Recursos e Ambiente

### 4.1 Ferramentas de Teste

| Ferramenta | Uso |
|---|---|
| uv | Ambiente Python 3.12 e execução de todos os comandos |
| pytest e pytest-mock | Testes unitários, de integração, de sistema e de RNF; mock do repositório nos serviços |
| pytest-cov / coverage.py | Cobertura de linhas e de arestas (`branch=True`) |
| mutmut | Teste de mutação das classes de domínio |
| ruff e radon | Lint e medição de complexidade ciclomática (CC ≥ 10) |
| Selenium WebDriver e Google Chrome | Testes de sistema em modo headless |
| TestLink | Gestão dos casos de teste manuais da Entrega 1 |
| GitHub Issues e Milestones | Registro de defeitos, atividades e rastreabilidade |
| SonarQube Community Build (Docker) | Inspeção estática com o perfil *Sonar way comprehensive* (407 regras), com evidências antes e depois |
| SQLite | Banco temporário dos testes, sem persistência no workspace |

### 4.2 Ambiente de Teste

**Software:**

- macOS, Linux ou Windows (uma execução de mutmut foi feita em Ubuntu via WSL 2);
- Python **3.12** gerenciado por **uv**;
- Google Chrome atualizado, com o driver resolvido pelo Selenium Manager;
- SQLite em arquivo temporário (`DATABASE` fora do workspace);
- servidor de desenvolvimento Flask;
- Docker para o SonarQube local;
- acesso ao TestLink e ao GitHub.

**Hardware:**

- execução nas máquinas dos integrantes, sem servidor dedicado;
- para reproduzir a suíte completa com Chrome headless e SonarQube local, recomenda-se 4 GB de RAM, 2 núcleos e cerca de 5 GB livres em disco.

A execução é local (`uv run pytest`); o repositório ainda não possui pipeline de CI.

---

## 5. Termos / Acrônimos

| Termo / acrônimo | Definição |
|---|---|
| API | *Application Programming Interface* |
| SUT | *System Under Test* — sistema sob teste |
| RF | Requisito funcional |
| RNF | Requisito não funcional |
| QA | *Quality Assurance* — garantia da qualidade |
| PE | Partição de equivalência |
| AVL / BVA | Análise de valor-limite (*Boundary Value Analysis*) |
| TD | Tabela de decisão |
| CC | Complexidade ciclomática |
| Cobertura de arestas | Critério estrutural que exige a passagem por todos os desvios |
| `xfail` | Marcação do pytest para um teste cuja falha é esperada e documentada |
| pytest | Framework de testes em Python |
| Flask | Microframework web usado no projeto |
| SQLite | Banco de dados local embarcado |
| Selenium | Framework de automação dos testes de sistema |
| mutmut | Ferramenta de teste de mutação para Python |
| SonarQube | Plataforma de inspeção estática de código |
| TestLink | Ferramenta de gestão de casos de teste |
