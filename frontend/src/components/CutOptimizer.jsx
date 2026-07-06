import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../hooks/useAuth";
import "../components/CutOptimizer.css";

export default function CutOptimizer() {
  const [comprimentoPadrao, setComprimentoPadrao] = useState("");
  const [itens, setItens] = useState([]);
  const [resultado, setResultado] = useState(null);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState(null);
  const itemCounterRef = useRef(0);
  const navigate = useNavigate();
  const { signOut } = useAuth();

  // Limpar resultado quando o usuário edita os dados
  useEffect(() => {
    if (resultado) {
      setResultado(null);
    }
  }, [comprimentoPadrao, itens]);

  const adicionarItem = () => {
    itemCounterRef.current += 1;
    setItens([
      ...itens,
      {
        id: `item_${itemCounterRef.current}`,
        comprimento: "",
        quantidade: "",
      },
    ]);
  };

  const removerItem = (index) => {
    setItens(itens.filter((_, i) => i !== index));
  };

  const atualizarItem = (index, campo, valor) => {
    const novosItens = [...itens];
    novosItens[index][campo] = valor;
    setItens(novosItens);
  };

  const isPositiveInteger = (value) => {
    return /^[1-9][0-9]*$/.test(value);
  };

  const validarFormulario = () => {
    if (!comprimentoPadrao || !isPositiveInteger(comprimentoPadrao)) {
      setErro("Comprimento padrão deve ser um número inteiro maior que 0");
      return false;
    }

    const padrao = Number(comprimentoPadrao);

    if (itens.length === 0) {
      setErro("Adicione pelo menos um item");
      return false;
    }

    for (let item of itens) {
      if (!item.comprimento || !isPositiveInteger(item.comprimento)) {
        setErro(`Item ${item.id}: comprimento deve ser um número inteiro maior que 0`);
        return false;
      }

      if (!item.quantidade || !isPositiveInteger(item.quantidade)) {
        setErro(`Item ${item.id}: quantidade deve ser um número inteiro maior que 0`);
        return false;
      }

      const comp = Number(item.comprimento);
      const qtd = Number(item.quantidade);
      if (comp > padrao) {
        setErro(
          `Item ${item.id}: comprimento (${comp}mm) não pode ser maior que o padrão (${padrao}mm)`
        );
        return false;
      }
    }

    return true;
  };

  const handleLogout = async () => {
    await signOut();
    navigate("/login");
  };

  const otimizar = async () => {
    setErro(null);
    setResultado(null);

    if (!validarFormulario()) {
      return;
    }

    setLoading(true);

    try {
      const payload = {
        comprimento_padrao: Number(comprimentoPadrao),
        itens: itens.map((item) => ({
          id: item.id,
          comprimento: Number(item.comprimento),
          quantidade: Number(item.quantidade),
        })),
      };

      console.log("Enviando para a API:", payload);

      const response = await api.post("/otimizar/otimizar", payload);
      console.log("Resposta da API:", response.data);
      setResultado(response.data);
    } catch (error) {
      console.error("Erro na requisição:", error);
      setErro(error.response?.data?.detail || "Erro ao otimizar corte");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="cut-optimizer-container">
      <div className="solver-header">
        <h2>Otimizador de Corte Unidimensional</h2>
        <button className="btn-logout solver-logout" onClick={handleLogout}>
          Logout
        </button>
      </div>

      <div className="form-section">
        <div className="form-group">
          <label htmlFor="comprimento">Comprimento Padrão (mm):</label>
          <input
            id="comprimento"
            type="number"
            value={comprimentoPadrao}
            onChange={(e) => setComprimentoPadrao(e.target.value)}
            placeholder="Ex: 3100"
            min="1"
          />
        </div>

        <div className="items-section">
          <h3>Itens para Corte</h3>
          {itens.length === 0 && (
            <p className="empty-message">Nenhum item adicionado ainda</p>
          )}

          {itens.map((item, index) => (
            <div key={index} className="item-card">
              <div className="item-fields">
                <div className="form-group">
                  <label>ID do Item:</label>
                  <input
                    type="text"
                    value={item.id}
                    onChange={(e) => atualizarItem(index, "id", e.target.value)}
                    placeholder="Ex: madeira_1"
                  />
                </div>

                <div className="form-group">
                  <label>Comprimento (mm):</label>
                  <input
                    type="number"
                    value={item.comprimento}
                    onChange={(e) =>
                      atualizarItem(index, "comprimento", e.target.value)
                    }
                    placeholder="Ex: 1150"
                    min="1"
                  />
                </div>

                <div className="form-group">
                  <label>Quantidade:</label>
                  <input
                    type="number"
                    value={item.quantidade}
                    onChange={(e) =>
                      atualizarItem(index, "quantidade", e.target.value)
                    }
                    placeholder="Ex: 3"
                    min="1"
                  />
                </div>

                <button
                  className="btn-remove"
                  onClick={() => removerItem(index)}
                >
                  Remover
                </button>
              </div>
            </div>
          ))}

          <button className="btn-add-item" onClick={adicionarItem}>
            + Adicionar Item
          </button>
        </div>

        {erro && <div className="erro-message">{erro}</div>}

        <button
          className="btn-otimizar"
          onClick={otimizar}
          disabled={loading}
        >
          {loading ? "Otimizando..." : "Otimizar Corte"}
        </button>
      </div>

      {resultado && (
        <div className="resultado-section">
          <h3>Resultado da Otimização</h3>

          <div className="resultado-resumo">
            <div className="info-box">
              <strong>Barras Utilizadas:</strong>
              <span>{resultado.barras_utilizadas}</span>
            </div>

            <div className="info-box">
              <strong>Desperdício Total (mm):</strong>
              <span>{resultado.desperdicio_total_mm.toFixed(2)}</span>
            </div>

            <div className="info-box">
              <strong>Tempo de Execução (s):</strong>
              <span>{resultado.tempo_execucao_segundos.toFixed(3)}</span>
            </div>
          </div>

          <div className="plano-corte">
            <h4>Plano de Corte</h4>
            {resultado.plano_de_corte.length === 0 ? (
              <p>Nenhum padrão de corte gerado</p>
            ) : (
              resultado.plano_de_corte.map((padrao, idx) => (
                <div key={idx} className="padrao-card">
                  <div className="padrao-header">
                    <strong>Barra {padrao.padrao_id + 1}</strong>
                    <span className="quantidade">
                      Quantidade: {padrao.quantidade_barras}x
                    </span>
                  </div>

                  <div className="padrao-details">
                    <p>
                      <strong>Comprimento Utilizado:</strong>{" "}
                      {padrao.comprimento_utilizado_por_barra} mm
                    </p>
                    <p>
                      <strong>Sobra por Barra:</strong>{" "}
                      {padrao.sobra_por_barra} mm
                    </p>
                  </div>

                  <div className="itens-cortados">
                    <strong>Itens a Cortar:</strong>
                    <ul>
                      {padrao.itens_cortados.map((item, itemIdx) => (
                        <li key={itemIdx}>
                          {item.item_id}: {item.quantidade}x
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
