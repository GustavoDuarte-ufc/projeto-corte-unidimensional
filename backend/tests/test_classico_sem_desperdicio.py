from app.algorithm.corte_uni import corte_uni


def test_desperdicio_conhecido():

    class ItemAux:
        def __init__(self, item_id, comprimento, quantidade):
            self.id = item_id
            self.comprimento = comprimento
            self.quantidade = quantidade
    
    itens = [
        ItemAux("D", 45, 2),
        ItemAux("E", 55, 2)
    ]

    resultado = corte_uni(100, itens)

    assert resultado["barras_utilizadas"] == 2
    assert resultado["desperdicio_total_mm"] == 0