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

### 6.2 `SimuladorEmprestimo` e funcionalidade de empréstimo — Vinicius Felinto (#51)

**Ambiente:** a mesma imagem do SonarQube (`26.11.0.134175-community`, via `docker-compose.yml` do projeto), com o perfil Python **Sonar way comprehensive** (407 regras) e o perfil Web padrão, como no “antes”. Data: 22/11/2026.

**Apontamentos da classe e da funcionalidade**

| Arquivo | Antes | Depois | Situação |
|---|---:|---:|---|
| `app/dominio/emprestimo.py` (`SimuladorEmprestimo`) | 0 | 0 | Classe sem apontamentos estáticos no perfil comprehensive; regras e CC preservadas |
| `app/web/routes/emprestimo.py` | 0 | 0 | Sem apontamentos |
| `app/templates/emprestimo.html` | **8** | **0** | 8 corrigidos (status `CLOSED` / `FIXED` no SonarQube) |

Como a classe de domínio `SimuladorEmprestimo` não possuía apontamentos estáticos abertos no Sonar, a atuação focou em:
1. **Qualidade e manutenibilidade do domínio**: adição de docstrings detalhadas, extração de constantes de negócio (`_DEFAULT_TAXA_BASE`, `_DEFAULT_PRAZO_MIN`, etc.), método auxiliar `_faixa_valor_renda` e validação modularizada com `_validar_entrada`, mantendo rigorosamente a complexidade ciclomática do método em **CC = 10** (e complexidade agregada da classe em 30), atendendo ao requisito essencial da disciplina (CC ≥ 10).
2. **Correção de apontamentos da funcionalidade no template**: resolução dos 8 apontamentos de acessibilidade e consistência em `app/templates/emprestimo.html`, associando rótulos aos respectivos campos de formulário e definindo `id`s padronizados.

| Linha | Regra | Tipo / severidade | Apontamento | Correção |
|---|---|---|---|---|
| 7 | `Web:S6853` | Code smell / maior | Rótulo “Valor do empréstimo (R$)” sem associação | `<label for="principal">` |
| 8 | `Web:InputWithoutLabelCheck` | Bug / maior | Campo `principal` sem `id` | `id="principal"` |
| 9 | `Web:S6853` | Code smell / maior | Rótulo “Prazo (meses)” sem associação | `<label for="meses">` |
| 10 | `Web:InputWithoutLabelCheck` | Bug / maior | Campo `meses` sem `id` | `id="meses"` |
| 11 | `Web:S6853` | Code smell / maior | Rótulo “Renda mensal (R$)” sem associação | `<label for="renda">` |
| 12 | `Web:InputWithoutLabelCheck` | Bug / maior | Campo `renda` sem `id` | `id="renda"` |
| 13 | `Web:S6853` | Code smell / maior | Rótulo “Sistema de amortização” sem associação | `<label for="sistema">` |
| 14 | `Web:InputWithoutLabelCheck` | Bug / maior | Campo `sistema` sem `id` | `id="sistema"` |

**Impacto da correção:**
- Eliminação completa de 4 bugs e 4 code smells de acessibilidade (WCAG 2.0 / Reliability).
- Melhoria na usabilidade para leitores de tela e tecnologias assistivas.
- Identificadores estáveis para automação de testes E2E/Selenium.

**Verificação da suíte e complexidade:**
- **Testes unitários de empréstimo:** 125 testes passando (`tests/unit/test_emprestimo.py`).
- **Testes de sistema:** 6 testes passando (`tests/system/emprestimo/test_emprestimo_sistema.py`).
- **Suíte geral:** 554 testes passando (4 xfailed previstos em tarifas).
- **Complexidade ciclomática (`radon cc app/dominio/emprestimo.py -s`):**
  - `SimuladorEmprestimo._validar_entrada`: CC = 10 (Classificação B)
  - `SimuladorEmprestimo._faixa_valor_renda`: CC = 5 (A)
  - `SimuladorEmprestimo.taxa_por_prazo`: CC = 5 (A)
  - `SimuladorEmprestimo.simular`: CC = 5 (A)
  - `SimuladorEmprestimo.parcelas_price`: CC = 2 (A)
  - `SimuladorEmprestimo.parcelas_sac`: CC = 2 (A)
  - **Soma da complexidade da classe: 30** (cumpre com folga o requisito de CC ≥ 10 da disciplina).

**Evidências** em `docs/relatorios/evidencias/sonar/depois/emprestimo/`:
- `issues-emprestimo-antes.json` — os 8 apontamentos abertos antes da correção;
- `issues-emprestimo-depois.json` — 0 apontamentos abertos nos arquivos de empréstimo após nova análise;
- `dashboard-depois.png` — print do dashboard SonarQube após a análise;
- `issues-emprestimo-resolvidos.png` — print da lista de issues demonstrando a resolução.
### 6.2 `CalculadoraJuros` — Gabrielle Rosa (#49)

**Ambiente:** SonarQube Community Build (`26.11.0.134175-community`, instância local), com o perfil Python **Sonar way comprehensive** (407 regras), na mesma base de comparação do relatório[cite: 12].

**Apontamentos da classe**

| Arquivo | Antes | Depois | Situação |
|---|---:|---:|---|
| `app/dominio/juros.py` (`CalculadoraJuros`) | 0 | 0 | Nenhum apontamento estático no SonarQube; defeito funcional **#20** (desconto de IR no mês 12 em `montante_com_aportes`) corrigido com `range(1, meses + 1)` |

**Verificação:**
- Complexidade ciclomática verificada via `.venv/bin/radon cc app/dominio -s` (mantendo CC ≥ 10).
- Suíte unitária de `CalculadoraJuros` (`tests/unit/test_juros.py`) executada com `.venv/bin/pytest` passando.

**Evidências** em `docs/relatorios/evidencias/sonar/depois/juros/`:
- `issues-juros-depois.png` — print da tela de issues do SonarQube confirmando `0 issues` para `app/dominio/juros.py`.

### 6.3 `TarifaBancaria` e funcionalidade de tarifas — Daniel Izu (#50)

**Ambiente:** a mesma imagem do SonarQube (`26.11.0.134175-community`, via `docker-compose.yml` do projeto), numa instância local nova no Ubuntu (WSL 2), com o perfil Python **Sonar way comprehensive** (407 regras) e o perfil Web padrão, como no “antes”. Scanner: imagem oficial `sonar-scanner-cli` (SonarScanner CLI 8.4.0.16527), chamada pelo `scripts/sonar_local.sh scan`. Data: 22/11/2026.

**Reprodução do “antes” na mesma instância.** Antes das correções, o código da `main` (commit `68d4f53`) foi analisado: **37 apontamentos** (15 bugs, 21 code smells, 1 vulnerabilidade). Os 7 apontamentos da funcionalidade de tarifas são os mesmos do relatório original (seções 2 e 3). A diferença no total do projeto (40 → 37) vem dos 4 apontamentos de `credito.html` corrigidos na #52 (−4) e de 1 apontamento novo em `tests/integration/conftest.py:26` (`python:S9100`), arquivo criado depois da análise original (+1). Comparação feita apontamento por apontamento (arquivo, regra e linha) com `antes/issues-antes.json`.

**Apontamentos da classe e da funcionalidade**

| Arquivo | Antes | Depois | Situação |
|---|---:|---:|---|
| `app/dominio/tarifas.py` (`TarifaBancaria`) | **1** | **0** | Corrigido (status `CLOSED` / `FIXED` no SonarQube) |
| `app/web/routes/tarifas.py` | 0 | 0 | Sem apontamentos |
| `app/templates/tarifas.html` | **6** | **0** | 6 corrigidos (status `CLOSED` / `FIXED`) |

| Linha | Regra | Tipo / severidade | Apontamento | Correção |
|---|---|---|---|---|
| `tarifas.py:27` | `python:S3776` | Code smell / crítica | `tarifa_mensal` com complexidade cognitiva 16 (limite 15) | Regra do pacote reescrita como retornos antecipados sem `if` aninhado (detalhes abaixo) |
| `tarifas.html:7` | `Web:S6853` | Code smell / maior | Rótulo “Tipo de conta” sem associação com o campo | `<label for="tipo">` |
| `tarifas.html:8` | `Web:InputWithoutLabelCheck` | Bug / maior | Campo `tipo` sem `id` | `id="tipo"` |
| `tarifas.html:13` | `Web:S6853` | Code smell / maior | Rótulo “Saldo (R$)” sem associação com o campo | `<label for="saldo">` |
| `tarifas.html:14` | `Web:InputWithoutLabelCheck` | Bug / maior | Campo `saldo` sem `id` | `id="saldo"` |
| `tarifas.html:15` | `Web:S6853` | Code smell / maior | Rótulo “Transações no mês” sem associação com o campo | `<label for="transacoes">` |
| `tarifas.html:16` | `Web:InputWithoutLabelCheck` | Bug / maior | Campo `transacoes` sem `id` | `id="transacoes"` |

**Correção do `python:S3776` sem reduzir a complexidade ciclomática.** As duas métricas medem coisas diferentes: a complexidade **cognitiva** do Sonar pesa os `if` aninhados, e a complexidade **ciclomática** do `radon` conta as decisões. No código original, as regras do pacote ficavam dentro de `if tem_pacote:`, e o aninhamento levava a complexidade cognitiva a 16. Elas passaram a ser uma sequência de retornos antecipados com condições compostas (ex.: `if tem_pacote and tipo is TipoConta.PREMIUM and saldo >= ...: return 0.0`), sem aninhamento. Resultado:

| Métrica (`TarifaBancaria`) | Antes | Depois |
|---|---:|---:|
| Complexidade cognitiva de `tarifa_mensal` (Sonar) | 16 (apontada) | ≤ 15 (sem apontamento) |
| CC de `tarifa_mensal` (`radon cc`) | 12 | **14** |
| CC da classe (soma dos métodos) | 24 | 22 |

O requisito da disciplina (CC ≥ 10 por classe, e um método com CC ≥ 10, conforme `docs/aplicacao.md`) continua atendido. A soma da classe caiu porque o método `_tarifa_com_pacote` (CC 4) foi removido: era código morto, nunca chamado, e reimplementava a regra do pacote de forma diferente da usada na tela (corrente com pacote e saldo R$ 6.000 dava 30,00 no método e 15,00 em `tarifa_mensal`). Os testes que o chamavam diretamente passaram a verificar a mesma regra por `tarifa_mensal` com pacote.

> Uma primeira versão da correção moveu o ramo com pacote para dentro de `_tarifa_com_pacote` (delegação). Ela também resolvia o apontamento, mas deixava `tarifa_mensal` com CC 7 e nenhum método da classe com CC ≥ 10. A versão final, plana, foi adotada para manter o requisito.

**Defeito funcional corrigido junto:** a #50 pede corrigir também os bugs funcionais da classe. O defeito [#77](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/77) (`tarifa_anual` ignorava a antiguidade) foi corrigido: o método passou a receber e repassar `antiguidade_meses` (36 meses: 288,00 em vez de 360,00). O `xfail` saiu, e os casos `vl_anual_antiguidade_35` e `vl_anual_antiguidade_36` viraram testes de regressão. O defeito [#78](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/78) **não foi corrigido**: aguarda a confirmação do grupo, porque a especificação não define o valor; o teste continua com `xfail(strict=True)`.

Assim como na #52, a correção do HTML melhora a acessibilidade (leitores de tela passam a anunciar o rótulo de cada campo, e clicar no rótulo foca o campo) e dá `id`s estáveis aos campos, que poderão ser usados pelo page object do Selenium de tarifas (#58).

**Projeto inteiro**

| Métrica | Antes (reprodução) | Depois |
|---|---:|---:|
| Apontamentos abertos | 37 | **30** |
| Bugs (tipo) | 15 | 12 |
| Code smells (tipo) | 21 | 17 |
| Vulnerabilidades (tipo) | 1 | 1 |
| Security (impacto) | 1 | 1 |
| Reliability (impacto) | 30 | **24** |
| Maintainability (impacto) | 6 | **5** |
| Cobertura | 69,9% | 69,5% |

A cobertura do projeto caiu 0,4 ponto porque o método removido (`_tarifa_com_pacote`) estava 100% coberto e saiu do total; `tarifas.py` continua com 100% de cobertura de arestas.

**Verificação:**

- `tests/unit/test_tarifas.py`: 128 passando e 3 `xfail` (#78); 100% de cobertura de arestas.
- Unitários, integração e segurança: 542 passando; as 2 falhas são os bugs de PIX #16 e #17, de outra classe e anteriores a esta issue. Sistema (Selenium): 31 passando.
- Mutação (`mutmut`, só em `tarifas.py`): 101 mutantes, 93 mortos (**92,1%**). Dos 8 sobreviventes, 7 são equivalentes (os 6 justificados na #45, com outros números porque o código mudou, e 1 novo do mesmo tipo: o padrão `antiguidade_meses` 0 → 1 de `tarifa_anual`) e 1 (`round(corrente * 0.5, 2)` → `round(..., 3)`) só se distingue em meio centavo exato, onde o arredondamento de `float` é ambíguo; não foi criado teste frágil para ele. Ver `docs/relatorios/cobertura_mutacao.md`.
- `uv run ruff check app/`: sem apontamentos.

**Evidências** em `docs/relatorios/evidencias/sonar/depois/tarifas/`:

- `antes-main/issues-abertas.json` e `antes-main/scanner.txt` — reprodução do “antes” (37 apontamentos, 7 de tarifas);
- `depois-branch/issues-abertas.json` — 30 apontamentos abertos, nenhum de tarifas;
- `depois-branch/issues-resolvidas.json` — os 7 apontamentos de tarifas com status `CLOSED` / `FIXED`;
- `depois-branch/scanner.txt` — log do scanner do “depois”;
- `issues-tarifas-resolvidos.png` — print da lista de issues filtrada por `tarifas.py` e `tarifas.html`, com os 7 corrigidos;
- `issues-tarifas-abertos.png` — print da mesma lista filtrada por abertos: 0 issues;
- `dashboard-depois.png` — print do dashboard “Overall Code” depois da correção;
- `pytest-solucao-inicial.txt` e `pytest-solucao-final.txt` — testes e `radon cc` antes e depois da revisão.

**Observações para a reprodução:**

- O mutmut 3 e o SonarQube local exigem Linux: no Windows, foram usados o WSL 2 com Ubuntu e o Docker instalado nele. O WSL desliga o Ubuntu alguns segundos depois do último comando, e o container do SonarQube cai junto; é preciso manter um terminal do Ubuntu aberto durante a análise.
- Numa instância nova, a interface exige trocar a senha padrão do `admin` antes de mostrar as telas. Para não alterar a senha usada pelo `scripts/sonar_local.sh`, os prints foram tirados com um usuário local só de leitura, criado pela API.
