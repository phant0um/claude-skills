---
origin: native
type: skill
status: active
version: "1.0.0"
kind: skill-proc
resolver-status: exposed
name: editor-md
description: "Use when: limpar Markdown convertido de PDF (acentos quebrados, parágrafos partidos, hifenização) antes de ingerir ou estudar. Converter MD em HTML é conversor-md-html."
updated: 2026-11-10
disable-model-invocation: true
---

# editor-md

Pipeline de limpeza para .md originados de PDF. Resolve em 5 etapas o que a conversão PDF→MD quebra sistematicamente.

## Quando usar

- Arquivo .md com frontmatter `tags: [pdf2md]` ou `converted:`
- Usuário menciona "bagunçado", "quebrado", "mal formatado", "PDF convertido"
- Diretório de aulas/apostilas exportadas de plataformas (Estratégia Concursos, FIAP, etc.)

## Parâmetros

```
/editor-md [arquivo_ou_dir] [--domain juridico|contabil|geral|auto] [--verify-only]
```

- `--domain auto` (padrão): detecta pelo conteúdo
- `--verify-only`: só lista problemas, não modifica
- Sem argumento: usa arquivo/diretório atual da conversa

## Etapas

### ETAPA 1 — Bash Cleanup (determinístico)

Execute `scripts/01-bash-cleanup.py [arquivo_ou_dir]`.

Remove:
- Watermarks de plataforma (nome do aluno, email, CPF, URLs de plataforma)
- Cabeçalhos/rodapés repetidos por página (nome do professor + "Aula N")
- Page numbers isolados (linhas com apenas dígitos)
- TOC dot-lines (`......... 42`)
- Picture placeholders (`==> picture [NxN] <==`, `Start/End of picture text`)
- Base64 blobs
- Tags HTML residuais (`<br>`, `<img>`, `<style>`)
- Social media promo (Instagram, YouTube, Telegram, inscreva-se)
- Linhas de boas-vindas do professor (padrão: "Olá, amigos do...")
- Runs de linhas em branco (>2 → 2)

### ETAPA 2 — Restauração de Acentos (determinístico)

Execute `scripts/02-accent-restore.py [arquivo_ou_dir] --domain [domain]`.

Aplica dicionário de substituições por domínio (ver `references/accent-dict.json`).

Domínios disponíveis:
- `juridico`: vocabulário de Direito Constitucional, Administrativo, LGPD
- `contabil`: vocabulário de Contabilidade Geral, Pública, MCASP, CPC
- `geral`: termos comuns a todos os domínios (padrão mínimo)
- `auto`: aplica todos os domínios

Corrige padrões sistêmicos de perda de acento:
- ç → c: "Governança" → "Governana", "execução" → "execuao"
- ã/ão → a/ao: "relação" → "relao", "gestão" → "gesto"
- í → i: "política" → "poltica", "público" → "pblico"
- ê → e: "sistêmico" → "sistmico", "três" → "trs"
- ó → o: "obrigatório" → "obrigatrio", "título" → "ttulo"
- Palavras coladas: "políticade" → "política de", "legitimidadedo" → "legitimidade do"

### ETAPA 3 — Restauração Estrutural [Haiku]

Para cada arquivo, com chunks de 30KB:

1. Une parágrafos quebrados no meio da frase (hifenização de PDF, quebra de coluna)
2. Restaura acentos restantes por contexto (o que o dicionário não cobre)
3. Converte linhas em maiúsculas seguidas de conteúdo → headers `##`
4. Remove headers vazios (## sem conteúdo na linha seguinte)
5. Normaliza formatação de listas (`- ` consistente)
6. Preserva 100% do conteúdo — NÃO resumir, NÃO remover conceitos

**Prompt para Haiku:**
> "Arquivo de estudo em PT-BR, conversão PDF→MD. Reformata preservando 100% do conteúdo. Una parágrafos quebrados no meio da frase. Restaura acentos pelo contexto. Remove headers vazios. NÃO reescreve, NÃO resume. Frontmatter intacto."

### ETAPA 4 — Reorganização de Referências [Haiku]

Se o arquivo contiver seção `## Referências` (ou `REFERÊNCIAS`, `Referências Bibliográficas`) fora do final:

1. Extrai a seção completa
2. Move para o final do documento
3. Consolida múltiplas seções de referências em uma

NÃO mover referências normativas integradas ao texto (Decreto 4.320/64, Lei 101/2000, art. 5º CF/88).

### ETAPA 5 — Verificação

Execute `scripts/03-verify.py [arquivo_ou_dir]`.

Reporta padrões conhecidos ainda presentes:
- Doubled chars: `ÍÍ`, `íÍ`, `ÍÍndice`
- Known broken words: `Sumrio`, `Captulo`, `Ttulo`, `OBRIGATRI`
- Page number lines isoladas
- Author + Aula patterns
- Espaços excessivos entre seções (>3 linhas em branco)

Output format:
```
arquivo.md: 3 issues
  line 42: "ÍÍndice" → "Índice"
  line 108: isolated page number "167"
  line 203: author header "Professor X Aula 3"
CLEAN: 0 issues remaining
```

## Constraints

Perda aqui é irreversível e silenciosa — o material de estudo original não volta,
e nenhum gate determinístico cobre estas quatro. Por isso carregam os quatro
campos de constraint (`when`/`auth`/`else`/`effect`), no formato de
prompt-contracts:
sobrevivem a handoff e compactação como regra, não como preferência.

```yaml
negatives:
  - id: EM1                              # conteúdo de estudo
    when: remoção de texto que não seja artefato de conversão
    auth: usuário, no turno atual
    else: manter o trecho e reportar como suspeito
    effect: deny — só formatação e artefato saem; dúvida preserva
  - id: EM2                              # frontmatter
    when: qualquer escrita no bloco YAML
    auth: usuário, no turno atual
    else: parar e reportar
    effect: deny — frontmatter é intocável, inclusive tags e status
  - id: EM3                              # referência normativa
    when: apagar ou mover citação de lei/decreto/artigo integrada ao texto
    auth: usuário, no turno atual
    else: manter na posição original e reportar
    effect: deny — norma citada é conteúdo, não artefato de PDF
  - id: EM4                              # escopo de arquivo
    when: arquivo sem extensão .md
    auth: nenhuma — não há exceção
    else: pular o arquivo e listar no relatório
    effect: deny — processar binário ou PDF corrompe o original
```

Demais (reversíveis, cobertas por revisão): NÃO resumir ou parafrasear — editor,
não redator; preservar wikilinks `...` intactos.

## Edge Cases

- Arquivos >200KB: processar por seção (split em `##` headers, processar cada chunk, reunir)
- PDFs de múltiplas colunas: parágrafos quebrados em colunas geram frases alternadas — Haiku reconhece o padrão
- Arquivos já limpos: etapas 1-2 são idempotentes; etapa 5 reporta CLEAN
- `--verify-only`: roda apenas etapa 5, sem modificar

## Lições (CGE-AM, 2026-05-30)

155 aulas de cursos Estratégia Concursos: conversão perdeu ç/ã/ê/í/ó sistematicamente em todo vocabulário jurídico-contábil. Headers repetidos em cada página do PDF. Palavras coladas (espaço perdido). Solução: pipeline 5 etapas + dicionário de 80+ termos por domínio.

## Linhagem

- **Upstream:** original (vault-michel).
- **Original (vault):** limpeza determinística de PDF→MD, restauração de acentos PT-BR por dicionário de domínio.
- **Critério:** mecanismo > autor. Fonte rastreável, não privilegiada.
