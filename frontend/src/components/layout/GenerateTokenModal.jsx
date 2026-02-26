import { useState } from "react";
import api from "../../services/api";
import "../../styles/GenerateTokenModal.css";

function GenerateTokenModal({ employeeId, onClose }) {
  const [token, setToken] = useState(null);
  const [expires, setExpires] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateToken = async () => {
    setLoading(true);

    try {
      const res = await api.post(
        `/employees/${employeeId}/generate-token`
      );

      setToken(res.data.token);
      setExpires(res.data.expires_at);
    } catch (err) {
      console.error("Token error:", err);
      alert("Failed to generate token");
    } finally {
      setLoading(false);
    }
  };

  const copyToken = () => {
    navigator.clipboard.writeText(token);
    alert("Token copied!");
  };

  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <h3>Generate Registration Token</h3>

        {!token ? (
          <button
            className="generate-btn"
            onClick={generateToken}
            disabled={loading}
          >
            {loading ? "Generating..." : "Generate Token"}
          </button>
        ) : (
          <>
            <div className="token-box">
              <p>{token}</p>
            </div>

            <p className="expiry">
              Expires at: {new Date(expires).toLocaleString()}
            </p>

            <button className="copy-btn" onClick={copyToken}>
              Copy Token
            </button>
          </>
        )}

        <button className="close-btn" onClick={onClose}>
          Close
        </button>
      </div>
    </div>
  );
}

export default GenerateTokenModal;