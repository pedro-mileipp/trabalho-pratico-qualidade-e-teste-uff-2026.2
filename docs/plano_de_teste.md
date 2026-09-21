# 📌 Plano de Teste — Banco Digital

> Plano de Teste da **Entrega 1** do trabalho prático de Qualidade e Teste (UFF 2026.2).

---

## 📝 Registro de Mudanças

| Versão | Data | Autor | Descrição |
|------|--------|----------|--------|
| 1.0 | 21/09/2026 | Alexandre Colmenero | Criação do Plano de Teste com base nos testes executados na Entrega 1 |

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
| RNF06 – Segurança (autenticação) | Bloqueio de acesso às rotas sem sessão (`login_required`) |

---

### ❌ 1.1.2 Fora do Escopo

Esses recursos não foram testados porque não estão expostos na interface ou não fazem parte do escopo da Entrega 1.

### Requisitos Funcionais Fora do Escopo

| Requisito | Justificativa |
|----------|----------------|
| Chargeback de PIX pela interface | Não exposto na UI na Entrega 1 (regra de domínio, coberta por testes unitários) |
| Antiguidade e saldo negativo de tarifas | Campos não expostos no formulário web; saldo negativo coberto por testes unitários, antiguidade a cobrir na Entrega 2 |
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

Nos testes unitários, o foco foi verificar o funcionamento correto das classes de domínio, incluindo a **validação de chaves PIX**, o **cálculo de juros**, a **tarifa bancária**, a **simulação de empréstimo** e a **decisão de crédito**, além de revelar os defeitos naturais presentes no código (#16, #17, #20, BUG-1 e BUG-2).

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
| Testes unitários por integrante | 16/09/2026 | 20/09/2026 |
| Casos de teste manuais | 16/09/2026 | 20/09/2026 |
| Gestão de casos no TestLink | 20/09/2026 | 20/09/2026 |
| Plano de Teste | 21/09/2026 | 21/09/2026 |
| Consolidação dos resultados e entrega | 21/09/2026 | 21/09/2026 |

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
- Issues de defeitos (#16, #17 e #20).

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

---