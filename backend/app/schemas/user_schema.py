from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=100,
        description="Nome completo do usuário.",
        example="Teste Teste"
    )

    email: EmailStr = Field(
        description="Endereço de e-mail do usuário.",
        example="teste1@gmail.com"
    )

    password: str = Field(
        min_length=8,
        max_length=100,
        description="Senha de acesso com pelo menos 8 caracteres.",
        example="senha1234"
    )


class UserResponse(BaseModel):
    id: str = Field(description="Identificador único do usuário.", example="64f0c1d2e4b0a1b2c3d4e5f6")
    name: str = Field(description="Nome completo do usuário.", example="Teste Teste")
    email: EmailStr = Field(description="E-mail do usuário.", example="teste1@gmail.com")
    role: str = Field(description="Perfil do usuário no sistema.", example="user")


class UserLogin(BaseModel):
    email: EmailStr = Field(description="E-mail cadastrado do usuário.", example="teste@gmail.com")
    password: str = Field(description="Senha de acesso do usuário.", example="12345678")