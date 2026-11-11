---
origin: native
type: skill
status: active
version: "1.0.0"
kind: skill-proc
resolver-status: exposed
name: content-design
description: "Use when: antes de salvar qualquer artefato persistido — página wiki, resumo, conceito, README — cuidar de ESTRUTURA (front-load, 1 ideia/frase, concreto). NÃO é revisão de voz: para tom/AI-slop use [voice-registers](../voice-registers/SKILL.md). Aplicar antes de salvar texto que outra pessoa (ou sessão futura) vai ler. triage-classification só decide approved/disapproved e content-synthesis só comprime fontes: dar estrutura à página de ingest, ao resumo ou à nota antes de salvar é aqui."
triggers:
  positive:
    - "escrever página"
    - "escrever conceito"
    - "vou salvar esta nota no vault, revisa a estrutura antes"
    - "revisar estrutura da página de ingest"
    - "documentar no vault com estrutura"
    - "content design"
    - "redigir wiki"
  negative:
    - "artefato transitório"
    - "nota de pipeline"
    - "conversa no chat"
    - "voz/tom/AI-slop do texto (use voice-registers; esta cuida de estrutura)"
updated: 2026-09-24
consolidated-by: "R3 (absorveu content-design-review como modos) + 2026-09-02 (content-design-review promovido a skill-proc; deixa de ser modo)"
reads: []
writes: []
reviewed-scope: "checagem mecanica + semantica: 5/5 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 9 secoes, 106 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---


<what-to-do>

Aplique 5 regras ao texto **antes de salvar**. Não mudam o conteúdo — mudam a ordem e o corte. Objetivo: leitor sabe se precisa do resto na 1ª linha. Isso é hot-path aplicado à escrita — economia de token na leitura futura.

## Quando NÃO usar

- **Artefato transitório** (draft, scratchpad, /tmp) — 5 regras são para persistido. Exceção: rascunho de texto externo (comentário de GitHub, corpo de PR, resposta a revisor) mora no scratchpad mas vai ser publicado. As 5 regras valem; a cadeia está em escrita.
- **Nota processada por pipeline** (receipts, manifests) — formato de máquina não passa por content-design.
- **Conversa no chat** — content-design é para arquivos salvos, não mensagens. Texto que sai do chat para um PR ou issue deixa de ser conversa.

Disambiguation: `content-design` governa escrita de qualquer artefato persistido; `writing-shape` molda material bruto em artigo; `content-design-review` revisa contra as regras — design escreve, review confere.


## As 5 regras

**1. Comece da necessidade do leitor.** Escreva o que a pessoa precisa pra decidir ou fazer algo — não o que você quer contar. Corte introdução-aquecimento ("Neste documento exploraremos...").

**2. Front-load tudo.** Pirâmide invertida: conclusão → detalhe → background. Vale no documento, na seção, no parágrafo e na frase. O veredito vai na linha 1, nunca no §4.

**3. Uma ideia por frase. Um tópico por parágrafo.** Frase com 2 ideias → quebre em 2.

**4. Específico e concreto.** Dê o número, o nome, a data. Corte abstração vaga: "uma gama de", "indo adiante", "de certa forma", "em termos de".

**5. Corte o que não adiciona sentido.** Curto é mais claro. Remova duplicata.

## Fluxo

1. Leia o rascunho inteiro.
2. Ache a conclusão/veredito. Se não está na 1ª linha → mova pra cima (regra 2).
3. Varra frase a frase: 2 ideias → quebra (3). Palavra vaga → número/nome (4). Não adiciona → corta (5).
4. Cheque abertura: fala da necessidade do leitor ou de você? (1)
5. Salve.

## Checklist pré-save

- [ ] Linha 1 entrega o ponto (leitor decide se lê o resto)
- [ ] Nenhuma frase com "e também" carregando 2ª ideia
- [ ] Zero "uma gama de / indo adiante / de certa forma"
- [ ] Números e nomes onde havia vago
- [ ] Nada repetido

## Escopo

Aplica a: página wiki, resumo de estudo, conceito, entity, README, ADR, relatório.
Não aplica a: transcript cru (`.raw/`), captura de inbox (fica cru até ingest).

## Relação com outras camadas

- **voice-registers** ([voice-registers](../voice-registers/SKILL.md)) — camada de **voz**: registro por corpus (Karpathy/Thariq/Boris) + catálogo de AI-slop + `voice-lint.py`. Este arquivo molda estrutura; aquele molda voz. Rodar este primeiro — `voice-registers` chama este de volta no passo 1.
- **content-design-review** (content-design-review) — validador pareado (padrão emil: gera aqui, reprova lá). Rodar após redigir, antes de salvar: audita as 5 regras com veredito acionável por linha.
- **Caveman** comprime a *conversa* (output ao usuário). Content-design molda o *artefato salvo*. Ortogonais.
- **Karpathy 4P** reduz erro de raciocínio. Content-design reduz atrito de leitura.
- Regra 2 (front-load) = mesmo princípio de hot-path/ponteiro, na escala da frase.

</what-to-do>

## Completion

- [ ] Artefato perseguido passa as 5 regras ou violações explicitadas.
- [ ] Conclusão na primeira linha (front-load).
- [ ] Revisão final relê o artefato do disco (não da memória).

## Failure modes

- **Veredito enterrado**: conclusão fica no §3+ → mova para a linha 1 antes de salvar (regra 2).
- **Aplicar em artefato transitório**: draft, receipt ou manifest de máquina → fora do escopo; exceção é texto externo que vai ser publicado.
- **Confundir estrutura com voz**: corrigir tom aqui → voz é `voice-registers`; esta skill só molda estrutura.
- **Revisão pela memória**: checar o checklist sem reler o arquivo → releia do disco antes de concluir.

## Skills pareadas

- **content-design-review** (content-design-review) — validador invocavel (`kind: skill-proc` desde 2026-09-02; era modo `reference` desta skill). Gera aqui, reprova la.
- **writing-great-skills** — vocabulario e principios para escrever/editar skills. Vive **fora do vault** (`~/.agents/skills/writing-great-skills/SKILL.md`, exposto como skill do harness); nao ha arquivo no vault, entao nao ha wikilink.
