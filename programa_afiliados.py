#!/usr/bin/env python3
"""Programa CLI para divulgar produtos afiliados.

Recursos:
- Cadastro de produtos (nome, nicho, preço, link de afiliado e benefícios)
- Listagem de produtos
- Geração de copy para Instagram, WhatsApp e e-mail
- Exportação de página HTML simples com os produtos

Uso rápido:
  python programa_afiliados.py adicionar --nome "Curso X" --nicho "Educação" --preco 197 \
      --link "https://exemplo.com/?ref=seu_id" --beneficios "Aulas ao vivo" "Certificado"
  python programa_afiliados.py listar
  python programa_afiliados.py copy --id 1 --canal instagram
  python programa_afiliados.py exportar-html --saida landing.html
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from textwrap import dedent

DB_PADRAO = Path("produtos_afiliados.json")


@dataclass
class Produto:
    id: int
    nome: str
    nicho: str
    preco: float
    link_afiliado: str
    beneficios: list[str]
    criado_em: str


class RepositorioProdutos:
    def __init__(self, caminho_db: Path) -> None:
        self.caminho_db = caminho_db
        self._garantir_db()

    def _garantir_db(self) -> None:
        if not self.caminho_db.exists():
            self.caminho_db.write_text("[]", encoding="utf-8")

    def carregar(self) -> list[Produto]:
        dados = json.loads(self.caminho_db.read_text(encoding="utf-8"))
        return [Produto(**item) for item in dados]

    def salvar(self, produtos: list[Produto]) -> None:
        serializado = [asdict(p) for p in produtos]
        self.caminho_db.write_text(
            json.dumps(serializado, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def proximo_id(self) -> int:
        produtos = self.carregar()
        return (max((p.id for p in produtos), default=0)) + 1


def adicionar_produto(args: argparse.Namespace, repo: RepositorioProdutos) -> None:
    produtos = repo.carregar()
    produto = Produto(
        id=repo.proximo_id(),
        nome=args.nome,
        nicho=args.nicho,
        preco=args.preco,
        link_afiliado=args.link,
        beneficios=args.beneficios,
        criado_em=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    produtos.append(produto)
    repo.salvar(produtos)
    print(f"✅ Produto cadastrado com sucesso! ID: {produto.id}")


def listar_produtos(_: argparse.Namespace, repo: RepositorioProdutos) -> None:
    produtos = repo.carregar()
    if not produtos:
        print("Nenhum produto cadastrado ainda.")
        return

    print("\n=== PRODUTOS AFILIADOS ===")
    for p in produtos:
        print(f"\nID: {p.id}")
        print(f"Nome: {p.nome}")
        print(f"Nicho: {p.nicho}")
        print(f"Preço: R$ {p.preco:.2f}")
        print(f"Benefícios: {', '.join(p.beneficios)}")
        print(f"Link: {p.link_afiliado}")
        print(f"Criado em: {p.criado_em}")


def gerar_copy(args: argparse.Namespace, repo: RepositorioProdutos) -> None:
    produtos = repo.carregar()
    produto = next((p for p in produtos if p.id == args.id), None)

    if produto is None:
        print(f"❌ Produto com ID {args.id} não encontrado.")
        return

    beneficios = " | ".join(produto.beneficios)

    modelos = {
        "instagram": dedent(
            f"""
            🚀 {produto.nome} ({produto.nicho})

            Quer resultado mais rápido com algo realmente útil?
            ✅ {beneficios}

            Oferta por apenas R$ {produto.preco:.2f}.
            Toque no link da bio para garantir 👇
            {produto.link_afiliado}

            #afiliados #marketingdigital #{produto.nicho.lower().replace(' ', '')}
            """
        ).strip(),
        "whatsapp": dedent(
            f"""
            Oi! Tenho uma indicação que pode te ajudar:
            *{produto.nome}*

            Benefícios principais:
            - """ + "\n- ".join(produto.beneficios) + f"""

            Investimento: R$ {produto.preco:.2f}
            Link de acesso: {produto.link_afiliado}
            """
        ).strip(),
        "email": dedent(
            f"""
            Assunto: Recomendação especial: {produto.nome}

            Olá,

            Quero te apresentar o produto *{produto.nome}*, focado no nicho de {produto.nicho}.
            Ele oferece: {beneficios}.

            Valor atual: R$ {produto.preco:.2f}
            Acesso pelo meu link de afiliado: {produto.link_afiliado}

            Se quiser, posso te explicar para quem ele é ideal.
            """
        ).strip(),
    }

    print("\n=== COPY GERADA ===\n")
    print(modelos[args.canal])


def exportar_html(args: argparse.Namespace, repo: RepositorioProdutos) -> None:
    produtos = repo.carregar()
    if not produtos:
        print("❌ Cadastre produtos antes de exportar a página HTML.")
        return

    cards = []
    for p in produtos:
        beneficios_html = "".join(f"<li>{b}</li>" for b in p.beneficios)
        cards.append(
            f"""
            <article class=\"card\">
                <h2>{p.nome}</h2>
                <p><strong>Nicho:</strong> {p.nicho}</p>
                <p><strong>Preço:</strong> R$ {p.preco:.2f}</p>
                <ul>{beneficios_html}</ul>
                <a href=\"{p.link_afiliado}\" target=\"_blank\" rel=\"noopener\">Quero saber mais</a>
            </article>
            """
        )

    html = f"""
    <!doctype html>
    <html lang=\"pt-BR\">
    <head>
      <meta charset=\"UTF-8\" />
      <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
      <title>Vitrine de Produtos Afiliados</title>
      <style>
        body {{ font-family: Arial, sans-serif; margin: 0; background: #f7f7fb; color: #222; }}
        header {{ padding: 24px; background: #2b2d42; color: white; }}
        main {{ max-width: 980px; margin: 24px auto; display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }}
        .card {{ background: white; padding: 16px; border-radius: 12px; box-shadow: 0 4px 14px rgba(0,0,0,.08); }}
        .card a {{ display: inline-block; margin-top: 8px; background: #ef233c; color: white; text-decoration: none; padding: 10px 12px; border-radius: 8px; }}
      </style>
    </head>
    <body>
      <header>
        <h1>Vitrine de Produtos Afiliados</h1>
        <p>Escolha um produto e acesse pelo link recomendado.</p>
      </header>
      <main>
        {''.join(cards)}
      </main>
    </body>
    </html>
    """

    saida = Path(args.saida)
    saida.write_text(dedent(html).strip() + "\n", encoding="utf-8")
    print(f"✅ Página HTML exportada em: {saida}")


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Programa para divulgar produtos afiliados")
    parser.add_argument(
        "--db",
        type=Path,
        default=DB_PADRAO,
        help="Caminho do arquivo JSON usado como banco local",
    )

    sub = parser.add_subparsers(dest="comando", required=True)

    p_add = sub.add_parser("adicionar", help="Cadastrar um novo produto")
    p_add.add_argument("--nome", required=True)
    p_add.add_argument("--nicho", required=True)
    p_add.add_argument("--preco", required=True, type=float)
    p_add.add_argument("--link", required=True)
    p_add.add_argument("--beneficios", nargs="+", required=True)
    p_add.set_defaults(func=adicionar_produto)

    p_list = sub.add_parser("listar", help="Listar produtos cadastrados")
    p_list.set_defaults(func=listar_produtos)

    p_copy = sub.add_parser("copy", help="Gerar texto de divulgação")
    p_copy.add_argument("--id", required=True, type=int)
    p_copy.add_argument("--canal", choices=["instagram", "whatsapp", "email"], required=True)
    p_copy.set_defaults(func=gerar_copy)

    p_html = sub.add_parser("exportar-html", help="Exportar landing page em HTML")
    p_html.add_argument("--saida", default="landing_afiliados.html")
    p_html.set_defaults(func=exportar_html)

    return parser


def main() -> None:
    parser = criar_parser()
    args = parser.parse_args()
    repo = RepositorioProdutos(args.db)
    args.func(args, repo)


if __name__ == "__main__":
    main()
