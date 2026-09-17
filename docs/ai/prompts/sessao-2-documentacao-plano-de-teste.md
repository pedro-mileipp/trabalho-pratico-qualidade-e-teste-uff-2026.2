# Sessão 2 — Documentação: Plano de Teste e referências

| Campo | Valor |
|---|---|
| Responsável | Alexandre Colmenero (`alexandrelimaxs`) |
| Data | 16/09/2026 |
| Ferramenta | opencode (modelo `opencode-go/deepseek-v4-flash`) |
| Atividade | Criação do Plano de Teste (template e exemplo) e atualização das referências nas docs |
| Artefatos | `docs/plano_de_teste.md`, `docs/plano_de_teste_exemplo.md`, `README.md`, `docs/aplicacao.md` |

## Contexto

Criar o documento de Plano de Teste da Entrega 1 a partir de um template fornecido, manter uma cópia preenchida como referência e atualizar as referências nos documentos do projeto.

## Prompts utilizados (em ordem)

### Prompt 1 — Criação do template de Plano de Teste
> "Crie um arquivo template plano de teste na pasta docs em markdown com o template abaixo:"
>
> [Colado o template completo com as seções: Registro de Mudanças, Introdução, Escopo, Objetivos de Qualidade, Papéis e Responsabilidades, Metodologia de Teste, Cronograma, Entregáveis de Teste, Recursos e Ambiente, Riscos, Termos e Acrônimos]

**Resposta da IA:** criado `docs/plano_de_teste.md` com o template exatamente como fornecido (seções, tabelas e instruções em comentários).

**Decisão:** aceito integralmente; o arquivo é o template em branco a ser preenchido pelo grupo.

**Validação:** leitura do arquivo gerado, conferindo todas as seções do template.

### Prompt 2 — Atualização das referências nas docs
> "Atualize as referencias nas docs pra citar o @docs/plano_de_teste.md"

**Resposta da IA:** identificou as referências existentes e adicionou o link/arquivo:
- `README.md`: "Plano de Teste" na seção Entrega 1 virou link para `docs/plano_de_teste.md`; nova linha na tabela "Estrutura do Repositório".
- `docs/aplicacao.md`: `plano_de_teste.md` adicionado à árvore de diretórios.
- `docs/plano_projeto.md` e enunciado já citavam o arquivo — mantidos.

**Decisão:** aceito.

**Validação:** leitura dos arquivos após as edições; conferência dos links relativos.

### Prompt 3 — Substituição pelo exemplo preenchido
> "Na verdade, use esse texto aqui como o template e nomeie com sufixo exemplo pra usar-mos como referencia."
>
> [Colado o Plano de Teste completo do projeto "MedAlerta", preenchido — usado apenas como modelo de referência]

**Resposta da IA:** criado `docs/plano_de_teste_exemplo.md` com o texto fornecido (exemplo preenchido de outro projeto), mantendo `docs/plano_de_teste.md` como template em branco para o grupo preencher.

**Decisão:** aceito; o exemplo fica apenas como referência de estrutura/preenchimento (o conteúdo é de outro projeto e não deve ser copiado).

**Validação:** leitura do arquivo; conteúdo conferido em relação ao texto colado.

### Prompt 4 — Adicionar referência do exemplo no README
> "Sim" (resposta à oferta de adicionar `docs/plano_de_teste_exemplo.md` à tabela de referências do README)

**Resposta da IA:** adicionada a linha `docs/plano_de_teste_exemplo.md` na tabela "Estrutura do Repositório" do `README.md`, com descrição de referência para preenchimento.

**Decisão:** aceito.

**Validação:** leitura do README após a edição.

## Ações executadas

1. Criação de `docs/plano_de_teste.md` (template em branco).
2. Criação de `docs/plano_de_teste_exemplo.md` (exemplo de referência).
3. Atualização de `README.md` (links e tabela "Estrutura do Repositório").
4. Atualização de `docs/aplicacao.md` (árvore de diretórios).

## Observações

- O conteúdo do exemplo MedAlerta pertence a outro projeto (Java/JUnit) e é usado **somente como referência** de estrutura do Plano de Teste, não de conteúdo — o Plano de Teste do Banco Digital deve refletir a stack Python/Flask/pytest deste trabalho.