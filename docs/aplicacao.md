# Aplicação — Banco Digital

Documentação do sistema web **Banco Digital** desenvolvido para a disciplina **Qualidade e Teste** (UFF 2026.2).

| Campo | Valor |
|---|---|
| Sistema | Banco Digital (web) |
| Stack | Python 3.12 · Flask · SQLite |
| Gerenciador de projeto | uv (`.python-version` + `pyproject.toml` + `uv.lock`) |
| Domínios | PIX, juros, tarifas, empréstimo, crédito |

---

## 1. Visão geral

O **Banco Digital** é uma aplicação web em que o cliente se autentica, visualiza saldo e extrato e usa serviços bancários: transferência PIX, simulação de empréstimo, consulta de tarifas e análise de crédito. As regras de negócio são isoladas em classes puras (sem dependência do Flask) no pacote `app/dominio/`, o que torna o sistema adequado às técnicas de teste da disciplina (unitário, integração, sistema, cobertura e mutação).

## 2. Arquitetura em camadas

```
app/web        ──►  app/servicos   ──►  app/dominio
  (rotas,            (orquestração,        (regras puras,
   templates)         casos de uso)         sem framework)
        │
        └──────── app/repositorios  ──►  SQLite / memória
```

| Camada | Responsabilidade | Depende de |
|---|---|---|
| `app/dominio/` | Regras de negócio puras; classes sob teste (CC ≥ 10) | nada (apenas stdlib) |
| `app/repositorios/` | Persistência; interface injetável para isolamento nos testes | `app/modelos.py` |
| `app/servicos/` | Orquestra domínio + repositório (casos de uso) | domínio + repositório |
| `app/web/` | HTTP: rotas (blueprints) e templates Jinja2 | serviços + repositório |
| `app/db.py` | Conexão SQLite por request (Flask `g`) | Flask |
| `app/modelos.py` | Dataclasses `Cliente` e `Transacao` | — |

A dependência entre camadas é sempre de cima para baixo: a camada web nunca importa o domínio diretamente quando há um serviço; os repositórios são **injetados** nos serviços, permitindo trocar SQLite por memória/mocks nos testes.

## 3. Estrutura de diretórios

```
app/
├── __init__.py               # create_app(): factory do Flask, registra blueprints, init_db()
├── config.py                 # Config: SECRET_KEY e DATABASE (via variável de ambiente)
├── db.py                     # get_db(), close_db(), init_db() e ESQUEMA SQL
├── modelos.py                # Cliente, Transacao (dataclasses)
├── dominio/                  # LÓGICA PURA — alvo dos testes (CC >= 10)
│   ├── pix.py                # TransacaoPix, ChaveTipo, ResultadoPix, ConfiguracaoPix
│   ├── juros.py              # CalculadoraJuros, TabelaTaxas
│   ├── tarifas.py            # TarifaBancaria, TarifasBase, TipoConta
│   ├── emprestimo.py         # SimuladorEmprestimo, SistemaAmortizacao, ResultadoEmprestimo
│   └── credito.py            # DecisorCredito, RegistroHistorico, ResultadoCredito, SituacaoCredito
├── repositorios/
│   ├── repositorio.py        # Repositorio (ABC) — contrato de persistência
│   ├── sqlite_repositorio.py # SqliteRepositorio — implementação com SQLite
│   └── memoria_repositorio.py# MemoriaRepositorio — implementação em memória (útil em testes)
├── servicos/
│   ├── auth.py               # AuthService, EmailJaCadastrado, CredenciaisInvalidas
│   └── transacoes.py         # TransacaoService, TransacaoRecusada
├── web/
│   ├── helpers.py            # login_required (decorator de sessão)
│   ├── routes/               # Blueprints: auth, dashboard, pix, emprestimo, tarifas, credito
│   └── templates/            # Jinja2: base, login, registro, dashboard, pix, emprestimo, tarifas, credito
tests/                        # (a ser implementado nas entregas)
docs/
├── descricao_trabalho.md     # enunciado
├── plano_projeto.md          # plano do projeto
└── aplicacao.md              # este documento
pyproject.toml                # dependências + config de ferramentas (ruff)
.python-version               # versão do Python (3.12)
uv.lock                       # trava de dependências
```

## 4. Módulos de domínio

Cada classe a seguir é **não-CRUD**, possui desvios/laços e **complexidade ciclomática ≥ 10** em pelo menos um método (medida com `radon cc`). É o alvo dos testes estrutural e de mutação da Entrega 2.

### 4.1 `TransacaoPix` (`app/dominio/pix.py`)

Autorização e chargeback de transferências PIX.

- `validar_chave(chave, tipo)` — valida chave por tipo: CPF (algoritmo do dígito verificador), e-mail, telefone (10/11 dígitos) ou aleatória (32 chars).
- `autorizar(chave, tipo, valor, saldo, horario)` — retorna `ResultadoPix`: checa valor > 0, chave válida, chave bloqueada, horário noturno, limite (diurno/noturno) e saldo.
- `solicitar_chargeback(chave, valor, dias, motivo)` — decide chargeback por prazo, valor e motivo (golpe/fraude).
- `_eh_noturno(momento)` — janela noturna configurável (padrão 20h–6h, com tratamento de virada de dia).

### 4.2 `CalculadoraJuros` (`app/dominio/juros.py`)

Juros compostos, faixas de taxa por prazo, mora e aportes.

- `taxa_para_prazo(meses)` — taxa por faixa de prazo (tabela).
- `taxa_mensal(taxa_anual)` — conversão anual → mensal.
- `calcular_montante(principal, meses, taxa_anual)` — juros compostos com laço.
- `juros_de_mora(valor, dias_atraso)` — multa escalonada (15/60/+) + juros diários.
- `total_a_pagar(...)` — montante + mora.
- `montante_com_aportes(...)` — **CC 11**: laço mensal, capitalização do aporte, incidência de IR por ano e teto.

### 4.3 `TarifaBancaria` (`app/dominio/tarifas.py`)

Cobrança de tarifas por tipo de conta, saldo, pacote e transações.

- `tarifa_mensal(tipo, saldo, tem_pacote, quantidade_transacoes, antiguidade_meses)` — **CC 12**: poupança gratuita, pacote, isenção por faixa de saldo, desconto por antiguidade, taxa negativa e tarifa por transações excedentes.
- `tarifa_por_transacao_extra(quantidade)` — transações acima da cota gratuita.
- `tarifa_anual(...)` — 12× a tarifa mensal.

### 4.4 `SimuladorEmprestimo` (`app/dominio/emprestimo.py`)

Simulação de empréstimo com amortização Price e SAC.

- `taxa_por_prazo(meses)` — taxa crescente por prazo.
- `teto_por_renda(renda)` — teto proporcional à faixa de renda.
- `parcelas_price(principal, taxa, meses)` — fórmula Price.
- `parcelas_sac(principal, taxa, meses)` — laço de amortização.
- `simular(principal, meses, renda, sistema, score, inadimplente)` — **CC 12**: validações (valor mínimo, prazos, renda, inadimplência, score), teto por renda, sistema de amortização e comprometimento da renda.

### 4.5 `DecisorCredito` (`app/dominio/credito.py`)

Análise de crédito por histórico, score e limite.

- `calcular_score(registros)` — **CC 11**: laço sobre histórico com 7 tipos de evento + clamp 0–1000.
- `limite_por_score(score, renda)` — faixas de limite por score/renda.
- `decidir(registros, renda, valor_solicitado)` — aprova/nega/parcial com motivo.

## 5. Camada de persistência

### 5.1 Contrato

`app/repositorios/repositorio.py` define o ABC `Repositorio`:

- `criar_cliente`, `buscar_cliente_por_email`, `buscar_cliente_por_id`
- `atualizar_saldo`, `atualizar_score`
- `registrar_transacao`, `listar_transacoes`

### 5.2 Implementações

- **`SqliteRepositorio`** — recebe uma factory de conexão (`get_db` do Flask). A conexão é gerenciada pelo contexto do Flask (`teardown_appcontext`), portanto o repositório **não fecha** conexões. Usada na aplicação web.
- **`MemoriaRepositorio`** — dicionários em memória; alternativa determinística para testes unitários/serviços.

### 5.3 Esquema (SQLite)

```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    saldo REAL NOT NULL DEFAULT 0,
    score INTEGER NOT NULL DEFAULT 500
);

CREATE TABLE transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL REFERENCES clientes (id),
    tipo TEXT NOT NULL,
    descricao TEXT,
    valor REAL NOT NULL,
    data TEXT NOT NULL
);
```

## 6. Camada de serviços (casos de uso)

- **`AuthService`** (`app/servicos/auth.py`) — `registrar()` valida campos e senha, impede e-mail duplicado e gera hash (`pbkdf2:sha256`, compatível com Python 3.9); `autenticar()` valida credenciais. Erros: `EmailJaCadastrado`, `CredenciaisInvalidas`.
- **`TransacaoService`** (`app/servicos/transacoes.py`) — `transferir_pix()` consulta o cliente, autoriza via `TransacaoPix`, debita o saldo e registra a transação; recusa com `TransacaoRecusada` (carrega o `ResultadoPix`).

## 7. Camada web

### 7.1 Rotas (blueprints)

| Blueprint | Rota | Métodos | Descrição |
|---|---|---|---|
| `auth` | `/registro` | GET/POST | Cria conta e autentica |
| `auth` | `/login` | GET/POST | Autentica |
| `auth` | `/logout` | GET | Encerra sessão |
| `dashboard` | `/` | GET | Saldo + extrato (exige login) |
| `pix` | `/pix` | GET/POST | Transferência PIX (exige login) |
| `emprestimo` | `/emprestimo` | GET/POST | Simulação de empréstimo (exige login) |
| `tarifas` | `/tarifas` | GET/POST | Consulta de tarifa (exige login) |
| `credito` | `/credito` | GET/POST | Análise de crédito (exige login) |

Todas as rotas, exceto auth, usam o decorator `login_required` (`app/web/helpers.py`), que redireciona ao login quando não há `cliente_id` na sessão.

### 7.2 Templates

- `base.html` — layout, navegação condicional por sessão e exibição de mensagens flash.
- `login.html`, `registro.html` — formulários de autenticação.
- `dashboard.html` — saldo, score e extrato.
- `pix.html`, `emprestimo.html`, `tarifas.html`, `credito.html` — formulários e resultados dos serviços.

## 8. Configuração e ciclo de vida

### 8.1 Factory `create_app()`

Em `app/__init__.py`:

1. Cria a aplicação Flask e carrega `Config`.
2. Chama `init_db()` (cria o esquema se necessário).
3. Registra os 6 blueprints.

### 8.2 Configuração (`app/config.py`)

| Variável | Padrão | Uso |
|---|---|---|
| `SECRET_KEY` | `dev-secret-key` | assinatura de sessão |
| `DATABASE` | `<raiz>/banco.db` | caminho do arquivo SQLite (env `DATABASE`) |

## 9. Como executar

```bash
uv sync --all-extras          # cria ambiente Python 3.12 e instala dependências
uv run flask --app app:create_app run   # sobe em http://127.0.0.1:5000
```

Banco de dados local criado automaticamente em `banco.db` na primeira execução.

## 10. Qualidade e lint

```bash
uv run ruff check app/        # lint (PLR1730/DTZ005 ignorados com justificativa no pyproject)
uv run radon cc app/dominio -s  # complexidade ciclomática por método/classe
```

Todos os 5 módulos de domínio possuem método com CC ≥ 10, atendendo ao requisito do enunciado.

## 11. Notas de implementação

- O hash de senha usa `pbkdf2:sha256` explicitamente para compatibilidade com ambientes cujo Python não oferece `hashlib.scrypt` (ex.: CPython 3.9 sem OpenSSL 1.1+).
- Templates ficam em `app/templates/` (pasta padrão do Flask), não dentro do blueprint.
- `ruff` ignora `PLR1730` (preservar os `if`s de complexidade das classes de domínio) e `DTZ005` (datetimes naive intencionais), conforme justificado em `pyproject.toml`.
- Testes, CI, cobertura, mutação e demais artefatos da disciplina serão implementados nas entregas subsequentes, conforme `docs/plano_projeto.md`.