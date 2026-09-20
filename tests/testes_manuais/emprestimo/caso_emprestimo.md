# Caso de Teste Manual — Simulação de Empréstimo

> Documento da issue **#11** - caso de teste manual da funcionalidade emprestimo do Banco Digital.

## 1. Identificação

| Campo | Valor |
|---|---|
| Funcionalidade | Empréstimo — Simulação (`/emprestimo`) |
| Issue | [#11](https://github.com/pedro-mileipp/trabalho-pratico-qualidade-e-teste-uff-2026.2/issues/11) |
| Executor | Daniel Izu |
| Data de execução | 19/09/2026 |
| Ambiente | Windows 11 · Google Chrome · `DATABASE=$env:TEMP\teste.db` |
| Build testado | commit  `main` |
| Técnica aplicada | Partição de equivalência + análise de valor-limite |

## 2. Pré-condições e preparação

1. `uv sync --all-extras`
2. Subir a aplicação com banco fora do workspace (evita criar `banco.db` no repositório):
   ```powershell
   $env:DATABASE="$env:TEMP\teste.db"
   uv run flask --app app:create_app run
3. Garantir acesso às telas de `/emprestimo` 

### Dados de teste

| Dado | Valor | Classificação |
|---|---|---|
| Valor do empréstimo válido | `1000` | entrada válida |
| Prazo válido | `12` | entrada válida |
| Renda mensal válida | `5000` | entrada válida |
| Valor do empréstimo abaixo do mínimo | `50` | entrada inválida |
| Prazo abaixo do mínimo | `1` | entrada inválida |
| Renda insuficiente / comprometimento acima do limite | renda mensal `1000`, valor solicitado `200`, prazo `2` | entrada inválida (1ª parcela > 30% da renda) |

## 3. Casos de teste executados

> A execução na interface cobriu 8 cenários (válidos e inválidos). Por decisão de escopo, este documento registra **os 5 casos representativos**: simulação Price válida, simulação SAC válida, valor abaixo do mínimo, prazo inválido e o limite de comprometimento de renda.

| ID | Cenário | Pré-condição | Passos | Dados de entrada | Resultado esperado | Resultado obtido | Status | Evidência |
|---|---|---|---|---|---|---|---|---|
| TC-01 | Simulação válida com Tabela Price | Conta logada, renda R$ 5000 | 1) Acessar `/emprestimo`; 2) preencher valor, prazo e renda; 3) selecionar sistema Price; 4) Simular | valor emprestimo `1000`, prazo `12`, renda `5000`, sistema `Price` | Aprovado; exibe aprovação com 1ª parcela `100.46` e total `1205.52` | Aprovado; exibidas 1ª parcela `100.46` e total `1205.52` | PASS | `evidenciastc01-simulacao-price-aprovado.png` |
| TC-02 | Simulação válida com Tabela SAC | Conta logada, renda R$ 5000 | 1) Acessar `/emprestimo`; 2) preencher valor, prazo e renda; 3) selecionar sistema SAC; 4) Simular | valor emprestimo `1000`, prazo `12`, renda `5000`, sistema `SAC` | Sucesso: exibe aprovação com 1ª parcela `113.33` e total `1194.96` | Aprovado; exibidas 1ª parcela `113.33` e total `1194.96` | PASS | `evidenciastc02-simulacao-sac-aprovado.png` |
| TC-03 | Valor solicitado abaixo do mínimo | Conta logada, renda R$ 5000 | 1) Acessar `/emprestimo`; 2) preencher valor R$ 50,00 e demais campos; 3) simular | renda `5000.00`, valor `50.00`, prazo `12`, sistema `Price` | Mensagem de erro "valor_abaixo_minimo" (mínimo permitido R$ 100,00), recusa do empréstimo | Mensagem de erro "valor_abaixo_minimo" exibida na tela; simulação recusada | PASS | `evidenciastc03-valor-abaixo-minimo.png` |
| TC-04 | Prazo abaixo do mínimo permitido | Conta logada, renda R$ 5000 | 1) Acessar `/emprestimo`; 2) preencher prazo de 1 mês e demais campos; 3) simular | renda `5000.00`, valor `1000.00`, prazo `1`, sistema `Price` | Mensagem de erro "prazo_curto" (mínimo permitido 2 meses), recusa do empréstimo | Mensagem de erro "prazo_curto" exibida na tela; simulação recusada | PASS | `evidenciastc04-prazo-invalido.png` |
| TC-05 | Comprometimento de renda excedido | Conta logada, renda R$ 1000 | 1) Acessar `/emprestimo`; 2) preencher valor e prazo curtos; 3) simular | renda `1000.00`, valor `200.00`, prazo `2`, sistema `Price` | Mensagem de erro "comprometimento_acima" (1ª parcela excede 30% da renda), recusa do empréstimo | Mensagem de erro "comprometimento_acima" exibida na tela; simulação recusada | PASS | `evidenciastc05-comprometimento-renda.png` |

## 4. Defeitos e observações

- O fluxo principal de simulação de empréstimo atende ao esperado para valores válidos e para as validações de limite mínimo.
- A regra de valor mínimo, prazo mínimo e comprometimento de renda foram validadas corretamente no backend e na interface.
- A mensagem de erro para comprometimento de renda pode ser melhorada em UX, para indicar com precisão que a causa é a parcela acima do limite estabelecido.
- A tela de empréstimo bloqueia entradas inválidas e mantém a consistência das regras de negócio, reduzindo risco de simulações inconsistentes.

## 5. Conclusão

Os testes manuais realizados para a funcionalidade de simulação de empréstimo cobriram o fluxo principal e os cenários de borda relevantes. O comportamento observado foi consistente com os requisitos da issue #11, e a área principal de melhoria apontada foi a clareza da mensagem de erro para casos de comprometimento de renda e validações de limite.


