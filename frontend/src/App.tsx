import "./App.css";
import { WavyBackground } from "./components/ui/wavy-background";
import { useState } from "react";
import axios from "axios";

function App() {
  const [inputValue, setInputValue] = useState(""); // Comma separated string
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null); // Changed to object
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setResult(null);

      // Convert "1, 2, 3" string to [1, 2, 3] numeric array
      const numericValues = inputValue
        .split(",")
        .map((v) => parseFloat(v.trim()))
        .filter((v) => !isNaN(v));

      if (numericValues.length === 0) {
        alert("Please enter valid numeric values separated by commas.");
        return;
      }

      const res = await axios.post("http://127.0.0.1:8000/forecast", {
        values: numericValues,
        query: query || null,
      });

      setResult(res.data); // Stores the whole object (explanation, forecast, etc.)
    } catch (err) {
      console.error(err);
      //@ts-ignore
      setResult({ explanation: "Error fetching result. Check console or backend." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <WavyBackground className="max-w-6xl mx-auto px-4 py-20">
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-6xl font-bold text-white">ForeCast</h1>
        <p className="text-lg text-white/80 mt-4 max-w-2xl mx-auto">
          AI-powered time-series analysis with LangGraph orchestration.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-10 items-start">
        {/* INPUT SECTION */}
        <div className="flex flex-col gap-4 bg-black/20 p-6 rounded-2xl backdrop-blur-sm border border-white/10">
          <h2 className="text-2xl text-white font-semibold">Data Input</h2>
          
          <label className="text-white/60 text-sm">Historical Values (Comma separated)</label>
          <input
            type="text"
            placeholder="10, 12, 15, 14, 18..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            className="p-3 rounded-lg bg-white/10 text-white border border-white/20 focus:border-white/50 outline-none transition"
          />

          <label className="text-white/60 text-sm">Specific Question (Optional)</label>
          <input
            type="text"
            placeholder="Is there a trend? / Predict next 7 days..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="p-3 rounded-lg bg-white/10 text-white border border-white/20 focus:border-white/50 outline-none transition"
          />

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="mt-2 bg-white text-black font-bold py-3 rounded-lg hover:scale-[1.02] active:scale-[0.98] transition disabled:opacity-50"
          >
            {loading ? "Analyzing..." : "Run Analysis"}
          </button>
        </div>

        {/* OUTPUT SECTION */}
        <div className="flex flex-col gap-4">
          <h2 className="text-2xl text-white font-semibold">Analysis Results</h2>
          <div className="p-6 rounded-2xl bg-black/40 border border-white/10 text-white min-h-[300px] backdrop-blur-md">
            {result ? (
              <div className="space-y-4">
                <div>
                  <span className="text-xs font-bold uppercase text-blue-400">Model Used</span>
                  <p className="text-lg">{result.model_selected || result.model}</p> 
                </div>
                <div>
                  <span className="text-xs font-bold uppercase text-blue-400">AI Explanation</span>
                  <p className="text-sm leading-relaxed text-white/90 whitespace-pre-line">
                    {result.explanation}
                  </p>
                </div>
                {result.anomalies?.length > 0 && (
                  <div>
                    <span className="text-xs font-bold uppercase text-red-400">Anomalies Detected</span>
                    <p className="text-sm text-red-200">{result.anomalies.length} outliers found.</p>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-white/40 italic">Waiting for data...</p>
            )}
          </div>
        </div>
      </div>
    </WavyBackground>
  );
}

export default App;