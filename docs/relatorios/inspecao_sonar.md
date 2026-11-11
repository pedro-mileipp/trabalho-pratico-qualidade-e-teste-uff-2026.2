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

## 6. Seção “depois” (a preencher)

Após as correções das issues de Sonar de cada classe (#48–#52), repetir a análise com o mesmo perfil e registrar:

- print do dashboard “Overall Code”;
- print da lista de issues da classe;
- comparação dos apontamentos (resolvidos × justificados);
- commit analisado e data;
- resultado da suíte e da cobertura.
