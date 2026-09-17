# 📌 Plano de Teste MedAlerta

> 📢 **Instruções Gerais**
>
> - Cada integrante deve preencher as seções sob sua responsabilidade.
> - Substitua os campos em branco com informações do projeto.
> - Apague estas instruções após o preenchimento, se desejar.
> - Use linguagem clara e objetiva.
> - Sempre que possível, seja específico (evite respostas genéricas).

---

## 📝 Registro de Mudanças

> 📢 **Instrução:** Registre qualquer alteração feita neste documento.

| Versão | Data | Autor    | Descrição |
|------|--------|----------|--------   |
| 1.0  | 18/04/2026 | Leonardo Carvalho | Criação do documento de acordo com o template |
| 1.1  | 25/04/2026 | Leonardo Carvalho | Preenchimento do documento com algumas informações dos testes realizados até o momento |
| 1.2  | 27/04/2026 | Sandro Henrique | Finalização da primeira entrega do Plano de Testes, preenchendo as informações faltantes (Requisitos funcionais e não funcionais que estão dentro e fora do escopo) |
| 1.3  | 22/06/2026 | Gabriel Soares | Alinhamento Entrega 2: E2E/RNF por integrante, metodologia, Java 17, links Issues e Sonar |

---

## 📖 1. Introdução

> 📢 **Instrução:** Descreva o objetivo deste plano de teste e o sistema que será testado.

O presente Plano de Teste tem como finalidade descrever as estratégias, processos e métodos que serão utilizados para assegurar a qualidade do sistema MedAlerta.

O principal objetivo é verificar se as funcionalidades implementadas atendem aos requisitos definidos, além de garantir uma experiência de uso confiável e adequada ao público alvo.

Para isso, serão adotadas abordagens de testes unitários e testes manuais, contemplando funcionalidades como cadastro de usuários, gerenciamento de medicamentos, geração de alertas, controle de estoque e etc. O processo de verificação e validação será conduzido de forma iterativa, possibilitando a identificação antecipada de falhas, a evolução contínua do sistema e entrega progressiva de qualidade ao longo do desenvolvimento.


---

## 🎯 1.1. Escopo


### ✅ 1.1.1 No Escopo

> 📢 **Instrução:** Liste as funcionalidades que SERÃO testadas.

| Nome do Módulo | Papéis Aplicáveis | Descrição |
| :--- | :---: | :--- |
| Login de Usuário | Cliente | O Cliente pode se autenticar no sistema, caso já tenha uma conta criada no sistema |
| Adicionar Contato Médico | Cliente | O Cliente pode adicionar vários contatos médicos em uma agenda no sistema |
| Cadastro de Cliente | Cliente | O Cliente pode realizar um cadastro no sistema preenchendo suas informações |
| Cadastro de Remédio | Cliente | O Cliente pode adicionar vários remédios, contendo as informações necessárias |
| Cadastro de Farmácia | Cliente | A Farmácia pode cadastrar seus dados no sistema |


### Requisitos Funcionais no Escopo

| Requisito | Descrição |
|----------|-----------|
| RF01 – Autenticação de usuários | Validar login e acesso ao sistema |
| RF02 – Cadastro de usuários | Testar criação e validação de contas |
| RF03 – Cadastro de medicamentos | Testar inclusão e edição de medicamentos |
| RF04 – Gerenciamento de horários | Validar agendamento e controle de horários de medicação |
| RF05 – Geração de alertas | Verificar notificações e lembretes de uso |
| RF06 – Cadastro de Contatos Médicos | Testar o gerenciamento e cadastro de contatos médicos |
| RF07 – Cadastro de Farmácia | Validar o cadastro de farmácias e suas informações no sistema |
| RF08 – Regras de negócio | Testar lógica de uso de medicamentos, datas e verificações do sistema |

### Requisitos Não Funcionais no Escopo

| Requisito | Descrição |
|----------|-----------|
| RNF01 – Usabilidade | Verificar facilidade de uso da interface |
| RNF02 – Confiabilidade | Garantir funcionamento correto dos alertas e regras do sistema |
| RNF03 – Integridade dos dados | Validar consistência dos dados cadastrados |
| RNF04 – Manutenibilidade | Validar código por meio de testes unitários, JaCoCo, PIT e Sonar |
| RNF05 – Compatibilidade | Testes em ambiente Java 17 suportado pelo projeto |
| RNF06 – Estresse (concorrência) | Múltiplos usuários simultâneos sem falhas (`EstresseMultiUsuarioTest`) |
| RNF07 – Segurança (autenticação) | Bloqueio de acesso com credenciais inválidas (`EntrarPessoaSegurancaTest`) |

---

### ❌ 1.1.2 Fora do Escopo

> 📢 **Instrução:** Liste o que NÃO será testado.

Esses recursos não serão testados porque não estão incluídos nas especificações de requisitos do software

### Requisitos Funcionais Fora do Escopo

| Requisito | Justificativa |
|----------|----------------|
| Integrações com hardware/dispositivos médicos | Não implementadas no projeto |
| Integrações com sistemas externos | Não fazem parte da versão atual |
| Funcionalidades de integração com serviços externos (e-mail/SMS/APIs) | Não implementadas na versão atual do sistema |

### Requisitos Não Funcionais Fora do Escopo

| Requisito | Justificativa |
|----------|----------------|
| Testes de carga em larga escala | Não previstos para esta fase |
| Testes de segurança avançados | Fora do escopo acadêmico do projeto |
| Testes de desempenho em larga escala | Não aplicável nesta entrega |
| Testes de banco de dados em alto volume | Não contemplados |
| Testes de disponibilidade e infraestrutura | Não fazem parte do escopo atual |

---

## 🧪 1.2. Objetivos de Qualidade

> 📢 **Instrução:** Descreva o que os testes pretendem garantir (ex: funcionamento correto, segurança, etc).

Os testes têm como objetivo garantir que as principais funcionalidades do sistema operem corretamente, atendendo aos requisitos definidos e proporcionando uma experiência confiável ao usuário.
Nos testes funcionais (manuais), busca-se validar operações como **autenticação de usuários**, **cadastro de clientes** e **gerenciamento de contatos médicos**.

Nos testes unitários, o foco é verificar o funcionamento correto das classes do sistema, incluindo o **gerenciamento de uso de medicamentos**, **cálculo de horários**, **envio de notificações** e **controle de quantidade disponível**.

Além disso, os testes visam garantir a integridade dos dados, o tratamento de entradas inválidas e a estabilidade do sistema durante sua execução.

## 👥 1.3. Papéis e Responsabilidades

> 📢 **Instrução:** Defina quem faz o quê no projeto.

| Papel | Responsável |
|------|-------------|
| Plano de Teste  | Leonardo e Sandro  |
| Testes manuais | Todos |
| Testes unitários | Todos |
| Organização do github | Alexandre |
| Slides | Sandro, Gabriel e Mateus |
| Planilha para testes manuais | Sandro |
| TestLink | Gabriel — [http://vania.ic.uff.br/testlink/](http://vania.ic.uff.br/testlink/) — plano **TEP: Teste em produção** |

### Entrega 2 — Classe sob teste (contribuição individual)

| Integrante | Classe | Pacote | Testes | Meta JaCoCo (branches) | Meta PIT |
|------------|--------|--------|--------|------------------------|----------|
| **Alexandre Colmenero** | **`Uso`** | **`backend.usuario`** | **`UsoTest` / `CadastroMedicamentoE2ETest`** | **≥ 80%** | **≥ 80%** |
| **Gabriel Soares** | **`Data`** | **`backend.gerenciamento`** | **`DataTest` / `InicioE2ETest` / RNF** (`EntrarPessoaSegurancaTest`, `EstresseMultiUsuarioTest`, `InicioUsabilidadeTest`) | **≥ 80%** | **≥ 80%** |
| Leonardo Carvalho | `Agenda` | `backend` | `AgendaTest` / `AgendaContatoMedicoE2ETest` (CT-CE-02 unitário) | ≥ 80% | ≥ 80% |
| Mateus Magalhães | `PessoaFisica` | `backend.usuario` | `PessoaFisicaTest` / `FluxoCadastroLoginE2ETest` (CT-CE-03) / `CadastroPessoaE2ETest` | ≥ 80% | ≥ 80% |
| Sandro Henrique | `FuncoesArquivos` | `backend` | `FuncoesArquivosTest` / `CadastroFarmaciaE2ETest` / `EntrarFarmaciaE2ETest` | ≥ 80% | ≥ 80% |

> Detalhamento completo: [`DIVISAO_CLASSES_ENTREGA2.md`](./DIVISAO_CLASSES_ENTREGA2.md)

**Gabriel Soares (`Data`):** testes estruturais e PIT na classe `Data`; E2E `InicioE2ETest`; testes RNF de segurança, estresse e usabilidade documentados em [`TESTES_FUNCIONAIS.md`](./TESTES_FUNCIONAIS.md).

**Alexandre Colmenero (`Uso`):** testes estruturais e PIT em `Uso`; E2E `CadastroMedicamentoE2ETest`; casos CT-AVL-01/02.

**Issues do projeto:** [GitHub Issues](https://github.com/vaniacourses/trabalho-qualidade-e-teste-grupo-5/issues). **Inspeção SonarQube:** responsabilidade compartilhada; evidências na [Apresentação Entrega 2](https://canva.link/aop9a2ac2q3hgo9).

---

## 🔬 2. Metodologia de Teste

### 🔄 2.1 Fases de Teste

> 📢 **Instrução:** Descreva como cada tipo de teste será realizado no projeto.

No projeto serão conduzidas as seguintes fases de teste:

- **Teste de Unidade:** classes isoladas em `src/test/java/backend` (JUnit + Mockito).
- **Teste de Integração:** fluxos reais em `src/test/java/backend/integracao`.
- **Teste de Sistema (E2E):** AssertJ Swing em `src/test/java/frontend` (equivalente a Selenium neste projeto desktop).
- **Teste Estrutural / Mutação:** JaCoCo (branches ≥ 80%) e PIT (≥ 80%) por integrante.
- **Inspeção estática:** SonarQube (Docker local) — evidências compartilhadas na [Apresentação Entrega 2](https://canva.link/aop9a2ac2q3hgo9).
- **Teste manual:** casos em [`testes_manuais/`](./testes_manuais/).

---

### ⛔ 2.2 Critérios de Suspensão e Retomada

> 📢 **Instrução:** Defina quando os testes devem parar e quando devem voltar.

A execução dos testes poderá ser suspensa caso sejam identificadas falhas críticas que impeçam o funcionamento das principais funcionalidades do sistema, ou quando uma alta taxa de falhas comprometer a continuidade dos testes.

Os testes serão retomados após a correção dos problemas identificados, garantindo que o sistema esteja novamente em condições adequadas para execução dos testes.

---

### ✅ 2.3 Completude do Teste

> 📢 **Instrução:** Defina quando os testes serão considerados finalizados.

Os testes serão considerados concluídos quando:

- 100% dos casos de teste planejados forem executados
- Os resultados dos testes forem devidamente registrados
- As falhas identificadas forem documentadas
- As principais funcionalidades do sistema tiverem sido avaliadas

---

## 📅 2.4. Atividades do projeto, estimativas e cronograma

> 📢 **Instrução:** Planeje as datas das atividades de teste.

| Atividade | Início | Fim | 
|----------|--------|------|
| Planejamento dos testes | 15/04/2026 | 19/04/2026 |
| Execução dos testes manuais e unitários | 20/04/2026 | 27/04/2026 | 
| Consolidação dos resultados e entrega | 24/04/2026 | 27/04/2026 |
| Plano de Testes | 24/04/2026 | 27/04/2026 |

---

## 📦 3. Entregáveis de Teste

> 📢 **Instrução:** Liste os artefatos gerados antes, durante e depois dos testes.

Os entregáveis de teste são fornecidos conforme abaixo

#### Antes da fase de teste

- Documento de planos de teste.
- Documentos de casos de teste
- Especificações de projeto de teste.

#### Durante o teste

- Simuladores de ferramentas de teste.
- Dados de teste.
- Matriz de rastreabilidade de testes
- Logs de erros e logs de execução.

#### Após o término dos ciclos de teste

- Resultados de teste / relatórios
- Relatório de erros
- Diretrizes  para instalação e para procedimentos de teste
- Notas de lançamento


---

## 🖥️ 4. Necessidades de Recursos e Ambiente

### 🧰 4.1 Ferramentas de Teste

> 📢 **Instrução:** Liste as ferramentas que serão utilizadas.

| No. | Recursos | Descrição |
| :--- | :---: | :--- |
| 1 | JUnit 5 | Framework utilizado para a criação e execução dos testes unitários do sistema |
| 2 | Mockito | Biblioteca utilizada para simular dependências e facilitar a execução de testes unitários |
| 3 | Eclipse / VS Code | IDEs usadas no desenvolvimento |
| 4 | JaCoCo / PIT / SonarQube | Cobertura, mutação e inspeção estática |
| 5 | AssertJ Swing | Testes E2E da interface Swing |
---

### 💻 4.2 Ambiente de Teste

> 📢 **Instrução:** Descreva o ambiente onde os testes serão executados.

Para a execução do sistema e realização dos testes, é necessário dispor de um ambiente compatível com as tecnologias utilizadas no desenvolvimento do projeto.

**Requisitos de Software:** 

- Sistema operacional Windows, Linux ou macOS com suporte a Java 17
- Java Development Kit (JDK) **17**
- Framework de testes JUnit 5
- Biblioteca Mockito
- Ambiente de desenvolvimento integrado (IDE), como Eclipse IDE ou IntelliJ IDEA
  



## 📚 5. Termos e Acrônimos

> 📢 **Instrução:** Defina termos técnicos utilizados no documento.

| Termo | Significado |
|------|-------------|
| JUnit | Framework para testes unitários em Java |
| Mockito | Biblioteca para criação de mocks em testes |
| RF | Requisito Funcional |
| RNF | Requisito não Funcional |

---