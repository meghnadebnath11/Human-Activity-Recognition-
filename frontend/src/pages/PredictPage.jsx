import { useEffect, useState } from "react";
import { fetchMetadata, submitPrediction } from "../services/api";

const initialForm = {
  acc_x: "0.12",
  acc_y: "9.74",
  acc_z: "0.41",
  gyro_x: "0.02",
  gyro_y: "0.08",
  gyro_z: "0.01",
};

export default function PredictPage() {
  const [formData, setFormData] = useState(initialForm);
  const [metadata, setMetadata] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [metadataLoading, setMetadataLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadMetadata() {
      try {
        const data = await fetchMetadata();
        setMetadata(data);
      } catch (apiError) {
        setError(apiError.message);
      } finally {
        setMetadataLoading(false);
      }
    }

    loadMetadata();
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    setPrediction(null);

    try {
      const payload = Object.fromEntries(
        Object.entries(formData).map(([key, value]) => [key, Number.parseFloat(value)]),
      );
      const result = await submitPrediction(payload);
      setPrediction(result);
    } catch (apiError) {
      setError(apiError.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="grid gap-8 lg:grid-cols-[0.9fr_1.1fr]">
      <form
        onSubmit={handleSubmit}
        className="rounded-[2rem] border border-white/10 bg-white/5 p-8 shadow-panel backdrop-blur"
      >
        <div className="mb-6">
          <p className="text-sm uppercase tracking-[0.3em] text-sunrise">Live prediction</p>
          <h2 className="mt-3 font-display text-3xl font-bold text-white">Enter sensor readings</h2>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          {Object.entries(formData).map(([key, value]) => (
            <label key={key} className="flex flex-col gap-2">
              <span className="text-sm font-semibold uppercase tracking-wide text-sand/80">{key}</span>
              <input
                className="rounded-2xl border border-white/15 bg-black/20 px-4 py-3 outline-none transition focus:border-sunrise"
                name={key}
                value={value}
                onChange={handleChange}
                type="number"
                step="0.01"
                required
              />
            </label>
          ))}
        </div>

        <button
          type="submit"
          disabled={loading}
          className="mt-8 rounded-full bg-sunrise px-6 py-3 font-semibold text-white transition disabled:cursor-not-allowed disabled:opacity-70"
        >
          {loading ? "Predicting..." : "Get Prediction"}
        </button>

        {error ? <p className="mt-4 rounded-2xl bg-red-500/15 px-4 py-3 text-sm text-red-200">{error}</p> : null}
      </form>

      <div className="space-y-6">
        <div className="rounded-[2rem] border border-white/10 bg-white/5 p-8 shadow-panel backdrop-blur">
          <h3 className="text-2xl font-semibold text-white">Model snapshot</h3>
          {metadataLoading ? (
            <p className="mt-4 text-sand/80">Loading model metadata...</p>
          ) : metadata?.model_loaded ? (
            <div className="mt-4 space-y-3 text-sand/85">
              <p>Accuracy: {(metadata.accuracy * 100).toFixed(2)}%</p>
              <p>Macro F1: {metadata.macro_f1.toFixed(4)}</p>
              <p>Classes: {metadata.classes.join(", ")}</p>
            </div>
          ) : (
            <p className="mt-4 text-sand/80">Metadata is unavailable until model artifacts are present.</p>
          )}
        </div>

        <div className="rounded-[2rem] border border-white/10 bg-white/5 p-8 shadow-panel backdrop-blur">
          <h3 className="text-2xl font-semibold text-white">Prediction result</h3>
          {prediction ? (
            <div className="mt-5">
              <p className="text-lg text-sand/85">Predicted activity</p>
              <p className="mt-2 font-display text-4xl font-bold text-white">{prediction.predicted_activity}</p>
              <div className="mt-6 space-y-3">
                {Object.entries(prediction.class_probabilities).map(([label, value]) => (
                  <div key={label}>
                    <div className="mb-1 flex items-center justify-between text-sm text-sand/80">
                      <span>{label}</span>
                      <span>{(value * 100).toFixed(2)}%</span>
                    </div>
                    <div className="h-3 rounded-full bg-black/20">
                      <div className="h-3 rounded-full bg-ocean" style={{ width: `${value * 100}%` }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <p className="mt-4 text-sand/80">Submit sensor values to see the predicted activity and class scores.</p>
          )}
        </div>
      </div>
    </section>
  );
}
