import pytest
from app.algorithm.corte_uni import corte_uni

def test_item_maior_que_barra():

    class ItemAux:
        def __init__(self, item_id, comprimento, quantidade):
            self.id = item_id
            self.comprimento = comprimento
            self.quantidade = quantidade

    itens = [
        ItemAux("A", 7000, 1)
    ]

    with pytest.raises(ValueError):
        corte_uni(6000, itens)