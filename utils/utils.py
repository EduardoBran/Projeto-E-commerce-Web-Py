from datetime import datetime


def formata_preco(val):
    return f'R$ {val:.2f}'.replace('.', ',')


def qtd_total_carrinho(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])


def total_carrinho(carrinho):
    return sum(
        [
            # obtem item preco_quantitativo_promocional
            item.get('preco_quantitativo_promocional')
            # se o preco_quantitativo_promocional estiver preenchido
            if item.get('preco_quantitativo_promocional')
            # caso não esteja, obtem o preco_quantitativo
            else item.get('preco_quantitativo')
            # para cada item no carrinho
            for item in carrinho.values()
        ]
    )


def formata_data(data):
    return data.strftime(('%d/%m/%Y'))
