from app.algorithm.corte_uni import corte_uni


def test_duas_barras():

    class ItemAux:
        def __init__(self, item_id, comprimento, quantidade):
            self.id = item_id
            self.comprimento = comprimento
            self.quantidade = quantidade
    
    itens = [
        ItemAux("C", 4000, 2)
    ]

    resultado = corte_uni(6000, itens)

    assert resultado["barras_utilizadas"] == 2
    assert resultado["desperdicio_total_mm"] == 4000