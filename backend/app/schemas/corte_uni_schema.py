from pydantic import BaseModel, ConfigDict, Field, model_validator

class Item(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "item_1",
                "comprimento": 1150,
                "quantidade": 3
            }
        }
    )

    id: str = Field(..., description="Identificador único do item a ser cortado.", example="item_1")
    comprimento: int = Field(..., gt=0, description="Comprimento do item em milímetros.", example=1150)
    quantidade: int = Field(..., gt=0, description="Quantidade de peças desse item.", example=3)

class CorteUniRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "comprimento_padrao": 3100,
                "itens": [
                    {"id": "item_1", "comprimento": 1150, "quantidade": 3},
                    {"id": "item_2", "comprimento": 800, "quantidade": 2}
                ]
            }
        }
    )

    comprimento_padrao: int = Field(..., gt=0, description="Comprimento da barra padrão em milímetros.", example=3100)
    itens: list[Item] = Field(..., description="Lista de itens que devem ser cortados.")

    @model_validator(mode="after")
    def validar_restricoes(self):
        for item in self.itens:
            if item.comprimento > self.comprimento_padrao:
                raise ValueError(
                    f"O item {item.id} tem comprimento maior que o padrão"
                )
        return self