# Programa para divulgar produtos afiliados

Este projeto entrega um programa em Python (CLI) para ajudar na divulgação de produtos afiliados.

## Recursos

- Cadastro de produtos com nicho, preço, benefícios e link de afiliado
- Listagem rápida dos produtos
- Geração de copy para:
  - Instagram
  - WhatsApp
  - E-mail
- Exportação de uma página HTML simples (vitrine)

## Requisitos

- Python 3.10+

## Como usar

### 1) Cadastrar produto

```bash
python programa_afiliados.py adicionar \
  --nome "Curso de Tráfego Pago" \
  --nicho "Marketing Digital" \
  --preco 197 \
  --link "https://exemplo.com/curso?ref=seu_id" \
  --beneficios "Aulas práticas" "Suporte" "Certificado"
```

### 2) Listar produtos

```bash
python programa_afiliados.py listar
```

### 3) Gerar copy de divulgação

```bash
python programa_afiliados.py copy --id 1 --canal instagram
python programa_afiliados.py copy --id 1 --canal whatsapp
python programa_afiliados.py copy --id 1 --canal email
```

### 4) Exportar HTML

```bash
python programa_afiliados.py exportar-html --saida landing_afiliados.html
```

Abra o arquivo HTML no navegador para visualizar sua vitrine de produtos.

## Banco de dados local

O programa cria automaticamente um arquivo `produtos_afiliados.json` no diretório atual.
Você pode customizar com `--db`.
