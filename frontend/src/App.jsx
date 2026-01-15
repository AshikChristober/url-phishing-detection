import React, { useState } from "react";
import axios from "axios";
import {
  ShieldAlert,
  ShieldCheck,
  ShieldX,
  Globe,
  Loader2
} from "lucide-react";

function App() {
  const [userInput, setUserInput] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/predict",
        { url: userInput }
      );
      setResult(res.data);
    } catch {
      alert("Backend error or invalid URL");
    } finally {
      setLoading(false);
    }
  };

  const getStatus = (label) => {
    switch (label) {
      case "BENIGN":
        return {
          bg: "#e6f7ec",
          border: "#2e7d32",
          text: "#1b5e20",
          icon: <ShieldCheck size={42} />
        };
      case "PHISHING":
      case "MALWARE":
        return {
          bg: "#fdecea",
          border: "#c62828",
          text: "#b71c1c",
          icon: <ShieldAlert size={42} />
        };
      case "DEFACEMENT":
        return {
          bg: "#fff4e5",
          border: "#ef6c00",
          text: "#e65100",
          icon: <ShieldX size={42} />
        };
      default:
        return {
          bg: "#eceff1",
          border: "#455a64",
          text: "#263238",
          icon: <Globe size={42} />
        };
    }
  };

  const status = result ? getStatus(result.final_prediction) : null;

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
        display: "flex",
        justifyContent: "center",
        alignItems: "flex-start",
        padding: "60px 20px",
        color: "#fff",
        fontFamily: "Inter, sans-serif"
      }}
    >
      {/* MAIN CONTAINER */}
      <div
        style={{
          width: "100%",
          maxWidth: "900px"
        }}
      >
        {/* HEADER */}
        <div style={{ textAlign: "center", marginBottom: 40 }}>
          <h1 style={{ fontSize: 36, marginBottom: 10 }}>
            🛡️ URL Phishing Detector
          </h1>
          <p style={{ opacity: 0.8 }}>
            AI-powered malicious URL detection
          </p>
        </div>

        {/* INPUT SECTION */}
        <form
          onSubmit={handleAnalyze}
          style={{
            display: "flex",
            gap: 14,
            marginBottom: 40
          }}
        >
          <input
            type="text"
            placeholder="Paste URL here (https://example.com)"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            disabled={loading}
            style={{
              flex: 1,
              padding: "16px 18px",
              fontSize: 16,
              borderRadius: 12,
              border: "1px solid #444",
              background: "#1e1e1e",
              color: "#fff",
              outline: "none"
            }}
          />

          <button
            type="submit"
            disabled={loading || !userInput}
            style={{
              padding: "16px 34px",
              borderRadius: 12,
              background: "#1976d2",
              color: "#fff",
              border: "none",
              fontWeight: "bold",
              fontSize: 16,
              cursor: "pointer"
            }}
          >
            {loading ? <Loader2 className="spin" /> : "Scan"}
          </button>
        </form>

        {/* RESULT CARD */}
        {result && status && (
          <div
            style={{
              background: status.bg,
              color: status.text,
              border: `3px solid ${status.border}`,
              borderRadius: 20,
              padding: 32,
              boxShadow: "0 25px 60px rgba(0,0,0,0.4)"
            }}
          >
            {/* RESULT HEADER */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 18,
                marginBottom: 22
              }}
            >
              {status.icon}
              <div>
                <h2 style={{ margin: 0, fontSize: 28 }}>
                  {result.final_prediction}
                </h2>
                <p style={{ margin: 0, opacity: 0.85 }}>
                  Final Classification Result
                </p>
              </div>
            </div>

            <hr style={{ borderColor: status.border, opacity: 0.4 }} />

            {/* CONFIDENCE */}
            <h3 style={{ marginTop: 24, marginBottom: 16 }}>
              Confidence Breakdown
            </h3>

            {Object.entries(result.confidences).map(([label, value]) => (
              <div
                key={label}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  padding: "14px 18px",
                  marginBottom: 12,
                  borderRadius: 12,
                  background:
                    label === result.final_prediction
                      ? "#ffffff"
                      : "rgba(255,255,255,0.75)",
                  color: "#000",
                  fontWeight:
                    label === result.final_prediction ? "700" : "500",
                  fontSize: 15
                }}
              >
                <span>{label}</span>
                <span>{value}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      <style>{`
        .spin {
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

export default App;
