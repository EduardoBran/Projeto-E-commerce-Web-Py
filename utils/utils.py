def formata_preco(val):
    return f'R$ {val:.2f}'.replace('.', ',')


def qtd_total_carrinho(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])
