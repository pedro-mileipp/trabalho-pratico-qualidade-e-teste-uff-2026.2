# Inspeção de código com SonarQube — Banco Digital

> Relatório da inspeção estática do código-fonte da **Entrega 2** (Qualidade e Teste — UFF 2026.2).
>
> **Status:** seção “antes” concluída em 11/11/2026. A seção “depois” será preenchida após as correções das issues de cada classe.

## 1. Ambiente e método

| Item | Valor |
|---|---|
| Ferramenta | SonarQube Community Build 26.11.0.134175 |
| Execução | Docker local (`sonarqube:26.11.0.134175-community`), `http://localhost:9000` |
| Reprodução | `docker-compose.yml` + `scripts/sonar_local.sh` (ver README) |
| Projeto | `banco-digital-uff-2026-2` — Banco Digital - UFF 2026.2 |
| Perfil Python | **Sonar way comprehensive** (407 regras ativas) |
| Commit analisado | `1b5bbe901a0a2637f1951658e854460159f1f6e8` (`main`) |
| Data da análise | 11/11/2026 |
| Scanner | SonarScanner CLI 8.1.0.6389 |

O perfil padrão `Sonar way core` foi executado primeiro, mas não apontou nenhum problema nas classes de domínio. Para que a inspeção das classes fosse efetiva, o projeto foi associado ao perfil **Sonar way comprehensive**, que encontrou o apontamento de complexidade em `TarifaBancaria`. Essa decisão está registrada para que a comparação “antes × depois” use o mesmo perfil.

### Comandos executados

```bash
# Cobertura usada pelo Sonar (as 8 falhas são os bugs #16/#17/#20 e os testes do #35)
# --cov-fail-under=0 evita que o gate local de 80% impeça a geração do XML
uv run pytest tests/unit --cov=app --cov-branch --cov-report=xml --cov-fail-under=0

# Cobertura estrutural do domínio: exibe as 5 classes no critério todas-arestas
uv run pytest tests/unit --cov --cov-branch --cov-report=term-missing

# Análise estática
sonar-scanner \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token="$SONAR_TOKEN"
```

### Reprodução por outro integrante

O ambiente está versionado em `docker-compose.yml` e `scripts/sonar_local.sh`:

```bash
./scripts/sonar_local.sh bootstrap  # sobe o container, gera o token e associa o perfil
./scripts/sonar_local.sh scan       # gera coverage.xml e envia a análise
```

O token fica em `.sonar/token` (ignorado pelo Git). A imagem do SonarQube está fixada em `sonarqube:26.11.0.134175-community`; se o `sonar-scanner` não estiver instalado, o script usa a imagem oficial do scanner via Docker. O `.coveragerc` define `relative_files = True` para que os caminhos do `coverage.xml` funcionem tanto no scanner local quanto no container.

### Evidências

- `docs/relatorios/evidencias/sonar/antes/dashboard-overall.png` — visão geral (Overall Code).
- `docs/relatorios/evidencias/sonar/antes/issues-geral.png` — lista geral de issues.
- `docs/relatorios/evidencias/sonar/antes/pix.png`
- `docs/relatorios/evidencias/sonar/antes/juros.png`
- `docs/relatorios/evidencias/sonar/antes/tarifas.png`
- `docs/relatorios/evidencias/sonar/antes/emprestimo.png`
- `docs/relatorios/evidencias/sonar/antes/credito.png`
- `docs/relatorios/evidencias/sonar/antes/issues-antes.json` — resposta da API com as 40 issues.
- `docs/relatorios/evidencias/sonar/antes/scanner-antes.txt` — log completo do scanner.
- `docs/relatorios/evidencias/sonar/antes/pytest-coverage.txt` — execução da suíte e cobertura no momento da análise.
- `docs/relatorios/evidencias/sonar/antes/cobertura-dominio.txt` — cobertura de arestas das 5 classes de domínio (99,3%, com 1 arquivo vazio ignorado).

## 2. Visão geral — antes das correções

| Métrica | Valor |
|---|---:|
| Issues abertas | 40 |
| Bugs (tipo) | 17 |
| Code smells (tipo) | 22 |
| Vulnerabilidades | 1 |
| Security (impacto) | 1 |
| Reliability (impacto) | 34 |
| Maintainability (impacto) | 5 |
| Cobertura | 59,8% |
| Linhas para cobrir | 728 |
| Duplicações | 0,0% |
| Linhas de código | 1.086 (1,1 mil) |

A cobertura acima é a do projeto inteiro usada pelo Sonar. A cobertura estrutural do domínio, no critério todas-arestas, é de **99,3%** e está registrada em [`docs/relatorios/evidencias/sonar/antes/cobertura-dominio.txt`](evidencias/sonar/antes/cobertura-dominio.txt), com as 5 classes visíveis.

### Distribuição por arquivo

| Arquivo | Issues |
|---|---:|
| `app/templates/emprestimo.html` | 8 |
| `app/templates/tarifas.html` | 6 |
| `app/templates/registro.html` | 6 |
| `app/templates/pix.html` | 6 |
| `app/templates/login.html` | 4 |
| `app/templates/credito.html` | 4 |
| `app/web/routes/auth.py` | 2 |
| `app/web/routes/pix.py` | 1 |
| `app/web/routes/dashboard.py` | 1 |
| `app/dominio/tarifas.py` | 1 |
| `app/__init__.py` | 1 |
| **Total** | **40** |

## 3. Apontamentos por classe de domínio

| Classe | Arquivo | Issues | Apontamentos |
|---|---|---:|---|
| `TransacaoPix` | `app/dominio/pix.py` | **0** | Nenhum apontamento estático. Os defeitos funcionais **#16** (e-mail com dois `@`) e **#17** (chargeback de chave bloqueada) são semânticos e foram revelados pelos testes, não pelo Sonar. |
| `CalculadoraJuros` | `app/dominio/juros.py` | **0** | Nenhum apontamento estático. |
| `TarifaBancaria` | `app/dominio/tarifas.py` | **1** | `python:S3776` — `tarifa_mensal` com complexidade cognitiva **16** (limite 15), na linha 27. Severidade: crítica. |
| `SimuladorEmprestimo` | `app/dominio/emprestimo.py` | **0** | Nenhum apontamento estático. |
| `DecisorCredito` | `app/dominio/credito.py` | **0** | Nenhum apontamento estático. |

### Detalhe do apontamento de `TarifaBancaria`

| Campo | Valor |
|---|---|
| Arquivo | `app/dominio/tarifas.py:27` |
| Regra | `python:S3776` — Cognitive Complexity of functions should not be too high |
| Mensagem | “Refactor this function to reduce its Cognitive Complexity from 16 to the 15 allowed.” |
| Tipo / severidade | Code smell / crítica |
| Esforço | 6 min |
| Observação | A redução deve preservar a complexidade ciclométrica (CC) ≥ 10 exigida pela disciplina. Se não for possível reduzir sem conflitar com o requisito, o apontamento deve ser justificado no relatório “depois”. |

## 4. Apontamentos fora das classes de domínio

| Arquivo:linha | Regra | Tipo / severidade | Descrição |
|---|---|---|---|
| `app/__init__.py:10` | `python:S4502` | Vulnerabilidade / crítica | “Make sure disabling CSRF protection is safe here.” (apontamento do Sonar; avaliar se é falso positivo no contexto da app factory). |
| `app/web/routes/auth.py:27` | `python:S1192` | Code smell / crítica | Definir constante para o literal `"registro.html"` repetido 3 vezes. |
| `app/web/routes/auth.py:52` | `python:S6965` | Code smell / maior | Especificar os métodos HTTP aceitos pela rota de logout. |
| `app/web/routes/dashboard.py:12` | `python:S6965` | Code smell / maior | Especificar os métodos HTTP aceitos pela rota do dashboard. |
| `app/web/routes/pix.py:31` | `python:S1192` | Code smell / crítica | Definir constante para o literal `"pix.html"` repetido 3 vezes. |
| `app/templates/*.html` | Diversas | Bugs / code smells | 34 apontamentos de acessibilidade, IDs ausentes em campos e rótulos sem associação, principalmente em formulários. |

## 5. Leitura dos resultados

1. O SonarQube **não encontrou problemas estáticos em `TransacaoPix`**. Isso não significa que a classe estava correta: os defeitos #16 e #17 são de regra de negócio e só aparecem com testes de partição/valor-limite.
2. A classe `TarifaBancaria` tem um apontamento real de complexidade cognitiva. A correção deve ser feita com cuidado para não reduzir a CC da classe abaixo de 10.
3. Os 34 apontamentos em templates são principalmente de acessibilidade e não fazem parte do escopo individual das classes de domínio; ficam registrados para a consolidação da issue #63.
4. A cobertura de 59,8% é a do projeto inteiro e reflete a ausência de testes de integração/sistema no momento da análise. No escopo das classes de domínio, a cobertura de arestas é de **99,3%** (5 classes medidas; apenas 1 arquivo vazio ignorado).

## 6. Seção “depois”

Após as correções das issues de Sonar de cada classe (#48–#52), repetir a análise com o mesmo perfil e registrar:

- print do dashboard “Overall Code”;
- print da lista de issues da classe;
- comparação dos apontamentos (resolvidos × justificados);
- commit analisado e data;
- resultado da suíte e da cobertura.

### 6.1 `DecisorCredito` e funcionalidade de crédito — Pedro Mileipp (#52)

**Ambiente:** a mesma imagem do SonarQube (`26.11.0.134175-community`, via `docker-compose.yml` do projeto), numa instância local nova, com o perfil Python **Sonar way comprehensive** (407 regras) e o perfil Web padrão, como no “antes”. Data: 18/11/2026.

**Reprodução do “antes” na mesma instância.** Antes de aplicar a correção, o código da `main` (commit `6a1f9eb`) foi analisado de novo: **40 apontamentos** (17 bugs, 22 code smells, 1 vulnerabilidade), com a mesma distribuição por arquivo da seção 2. Isso confirma que o ambiente reproduz o “antes” original e que a comparação abaixo usa a mesma base. A cobertura do projeto ficou em 60,6% (no original, 59,8%), porque a suíte unitária cresceu nas issues #42 e #47.

**Apontamentos da classe e da funcionalidade**

| Arquivo | Antes | Depois | Situação |
|---|---:|---:|---|
| `app/dominio/credito.py` (`DecisorCredito`) | 0 | 0 | Classe sem apontamentos estáticos no perfil comprehensive; nada a corrigir |
| `app/web/routes/credito.py` | 0 | 0 | Sem apontamentos |
| `app/templates/credito.html` | **4** | **0** | 4 corrigidos (status `CLOSED` / `FIXED` no SonarQube) |

Como a classe `DecisorCredito` não tem apontamentos, a correção foi feita nos apontamentos da mesma funcionalidade (a tela de crédito):

| Linha | Regra | Tipo / severidade | Apontamento | Correção |
|---|---|---|---|---|
| 7 | `Web:S6853` | Code smell / maior | Rótulo “Renda mensal” sem associação com o campo | `<label for="renda">` |
| 8 | `Web:InputWithoutLabelCheck` | Bug / maior | Campo `renda` sem `id` | `id="renda"` |
| 9 | `Web:S6853` | Code smell / maior | Rótulo “Valor solicitado” sem associação com o campo | `<label for="valor">` |
| 10 | `Web:InputWithoutLabelCheck` | Bug / maior | Campo `valor` sem `id` | `id="valor"` |

Além de resolver os apontamentos, a correção melhora a acessibilidade (leitores de tela passam a anunciar o rótulo de cada campo, e clicar no rótulo foca o campo) e deu `id`s estáveis aos campos: o page object do Selenium (`tests/system/credito/pagina_credito.py`) passou a localizá-los por `id`.

**Projeto inteiro**

| Métrica | Antes (reprodução) | Depois |
|---|---:|---:|
| Apontamentos abertos | 40 | **36** |
| Bugs (tipo) | 17 | 15 |
| Code smells (tipo) | 22 | 20 |
| Vulnerabilidades (tipo) | 1 | 1 |
| Security (impacto) | 1 | 1 |
| Reliability (impacto) | 34 | **30** |
| Maintainability (impacto) | 5 | 5 |
| Cobertura | 60,6% | 60,6% |

O dashboard “Overall Code” (print `dashboard-depois.png`) mostra a visão por impacto: Security 1, Reliability 30 e Maintainability 5. Os 4 apontamentos corrigidos eram todos de Reliability.

**Verificação:** os 131 testes de crédito continuam passando (96 unitários, 13 de sistema com Selenium e 22 de segurança). A complexidade ciclomática do `DecisorCredito` não mudou (soma dos métodos: 24), porque o domínio não foi alterado.

**Evidências** em `docs/relatorios/evidencias/sonar/depois/credito/`:

- `issues-credito-antes.json` — os 4 apontamentos abertos antes da correção;
- `issues-credito-depois.json` — 0 apontamentos abertos nos arquivos de crédito;
- `issues-credito-resolvidos.json` — os 4 apontamentos com status `CLOSED` / `FIXED`;
- `issues-credito-resolvidos.png` — print da lista de issues filtrada por `app/templates/credito.html`, com os 4 corrigidos;
- `dashboard-depois.png` — print do dashboard “Overall Code” depois da correção.

**Observação para a reprodução:** numa instância nova, o comando `bootstrap` do `scripts/sonar_local.sh` não consegue associar o perfil comprehensive, porque o projeto ainda não existe no SonarQube antes do primeiro scan (a API devolve HTTP 404, “Project not found”). Aqui, o projeto foi criado antes pela API (`api/projects/create`) e só então o perfil foi associado.

### 6.3 `CalculadoraJuros` e funcionalidade de autenticação — Daniel Izu (#49)

> A issue #49 estava atribuída a Gabrielle Rosa; a execução abaixo foi feita por Daniel Izu.

**Ambiente:** a mesma instância e o mesmo perfil da seção 6.2 (SonarQube `26.11.0.134175-community` no Docker do Ubuntu, WSL 2; perfil Python **Sonar way comprehensive**, 407 regras; perfil Web padrão). Para não sobrescrever as análises do projeto principal, que estavam sendo usadas nos prints da #50, a #49 foi analisada num projeto separado da mesma instância, `banco-digital-uff-2026-2-issue49`, com os mesmos perfis. Data: 22/11/2026.

**`CalculadoraJuros` não tem apontamentos.** Tanto na análise original (seção 3) quanto na reprodução desta seção, `app/dominio/juros.py` tem **0 apontamentos** no perfil comprehensive. Diferente de tarifas e crédito, a classe **não tem tela nem rota**: nenhum arquivo de `app/web` ou `app/templates` usa a `CalculadoraJuros` (ela é testada só no nível de unidade, conforme o escopo do Plano de Teste). Não há, portanto, apontamento a corrigir na classe nem numa tela da mesma funcionalidade. O defeito funcional citado na #49 (#20, desconto de IR no mês 12) já tinha sido corrigido pela Gabrielle (seção 6.4 do Plano de Teste). A complexidade da classe não mudou (soma dos métodos 30; maior método 11).

**Correção feita: a funcionalidade de autenticação**, que tinha 12 apontamentos e não estava atribuída a ninguém. É a mesma abordagem da #52 (seção 6.1), em que a classe não tinha apontamentos e foram corrigidos os da tela da funcionalidade.

**Reprodução do “antes”** (`main`, commit `bbabd18`): 37 apontamentos no projeto (15 bugs, 21 code smells, 1 vulnerabilidade), 12 deles na autenticação.

| Arquivo | Antes | Depois | Situação |
|---|---:|---:|---|
| `app/dominio/juros.py` (`CalculadoraJuros`) | 0 | 0 | Classe sem apontamentos; nada a corrigir |
| `app/templates/login.html` | **4** | **0** | 4 corrigidos (`CLOSED` / `FIXED`) |
| `app/templates/registro.html` | **6** | **0** | 6 corrigidos (`CLOSED` / `FIXED`) |
| `app/web/routes/auth.py` | **2** | **0** | 2 corrigidos (`CLOSED` / `FIXED`) |

| Linha | Regra | Tipo / severidade | Apontamento | Correção |
|---|---|---|---|---|
| `login.html:7`, `:9` | `Web:S6853` | Code smell / maior | Rótulos “E-mail” e “Senha” sem associação com os campos | `<label for="email">`, `<label for="senha">` |
| `login.html:8`, `:10` | `Web:InputWithoutLabelCheck` | Bug / maior | Campos `email` e `senha` sem `id` | `id="email"`, `id="senha"` |
| `registro.html:7`, `:9`, `:11` | `Web:S6853` | Code smell / maior | Rótulos “Nome”, “E-mail” e “Senha” sem associação | `<label for="nome">`, `for="email"`, `for="senha"` |
| `registro.html:8`, `:10`, `:12` | `Web:InputWithoutLabelCheck` | Bug / maior | Campos `nome`, `email` e `senha` sem `id` | `id="nome"`, `id="email"`, `id="senha"` |
| `auth.py:27` | `python:S1192` | Code smell / crítica | Literal `"registro.html"` repetido 3 vezes | Constante `TEMPLATE_REGISTRO` |
| `auth.py:52` | `python:S6965` | Code smell / maior | Rota `/logout` sem os métodos HTTP declarados | `methods=["GET"]` |

**Decisão sobre o `/logout`:** a regra pede declarar os métodos aceitos. Foi declarado só `GET`, porque a tela sai pelo link `<a href="{{ url_for('auth.logout') }}">` de `base.html`, e os testes de integração e de segurança usam `GET /logout`. Fica registrado, como risco conhecido, que logout por `GET` permite que outro site encerre a sessão do usuário por um link ou imagem (CSRF de logout); o impacto é baixo (não expõe dados) e mudar para `POST` exigiria trocar o link por um formulário, fora do escopo desta issue.

As páginas de login e de registro passam a ter rótulos anunciados por leitores de tela, como nas telas de crédito e de tarifas. Os `id`s repetidos (`email`, `senha`) estão em páginas diferentes, sem conflito. O page object do Selenium de autenticação localiza os campos por `name`, então continua funcionando.

**Projeto inteiro (projeto de análise da #49)**

| Métrica | Antes (`main`) | Depois |
|---|---:|---:|
| Apontamentos abertos | 37 | **25** |
| Bugs (tipo) | 15 | 10 |
| Code smells (tipo) | 21 | 14 |
| Vulnerabilidades (tipo) | 1 | 1 |
| Security (impacto) | 1 | 1 |
| Reliability (impacto) | 30 | **20** |
| Maintainability (impacto) | 6 | **4** |
| Cobertura | 69,9% | 69,8% |

A queda foi de exatamente 12 apontamentos, então a correção não criou nenhum novo. A cobertura caiu 0,1 ponto porque a constante nova fica em `routes/auth.py`, que não é executado pelos testes unitários usados no `coverage.xml` do Sonar. Esta tabela não inclui as correções de tarifas da #50 (seção 6.2), feitas em outra branch; com as duas, o projeto vai de 37 para 18 apontamentos.

**Verificação:** unitários, integração e segurança — 546 passando (as 2 falhas são os bugs de PIX #16 e #17, anteriores); sistema (Selenium) de autenticação — 12 passando; `ruff` sem apontamentos; `radon cc` da `CalculadoraJuros` inalterado.

**Evidências** em `docs/relatorios/evidencias/sonar/depois/juros-auth/`:

- `antes-main/issues-abertas.json` e `antes-main/scanner.txt` — reprodução do “antes” (37 apontamentos, 12 da autenticação, 0 de `juros.py`);
- `depois-branch/issues-abertas.json` — 25 apontamentos, nenhum da autenticação nem de `juros.py`;
- `depois-branch/issues-resolvidas.json` — os 12 apontamentos com status `CLOSED` / `FIXED`;
- `depois-branch/scanner.txt` — log do scanner do “depois”;
- `issues-juros.png` — lista de issues filtrada por `app/dominio/juros.py` (abertos e resolvidos): 0 issues;
- `issues-auth-resolvidos.png` — lista filtrada por `login.html`, `registro.html` e `auth.py`, com os 12 corrigidos;
- `issues-auth-abertos.png` — a mesma lista filtrada por abertos: 0 issues;
- `dashboard-depois.png` — dashboard “Overall Code” do projeto de análise depois da correção;
- `pytest-solucao-inicial.txt` — testes e `ruff` da solução.
