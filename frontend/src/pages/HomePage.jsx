import { Link } from "react-router-dom";
import FeatureCard from "../components/FeatureCard";

const highlights = [
  {
    title: "Sensor Fusion Ready",
    description:
      "The model combines accelerometer and gyroscope streams from the HHAR smartphone recordings for activity classification.",
  },
  {
    title: "Production API",
    description:
      "A FastAPI backend exposes health, metadata, and prediction endpoints with typed validation and structured error handling.",
  },
  {
    title: "Deployment Friendly",
    description:
      "The repository includes Render, Vercel, Docker, environment templates, and training scripts for reproducible delivery.",
  },
];

export default function HomePage() {
  return (
    <section className="space-y-10">
      <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-[2rem] border border-white/10 bg-white/5 p-8 shadow-panel backdrop-blur">
          <p className="mb-3 text-sm uppercase tracking-[0.3em] text-sunrise">Assignment-ready repository</p>
          <h2 className="max-w-2xl font-display text-4xl font-bold text-white md:text-5xl">
            Recognize human movement from mobile sensor data with a full-stack ML application.
          </h2>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-sand/85">
            This project turns raw smartphone motion streams into activity predictions for walking, biking, sitting,
            standing, and stair navigation tasks.
          </p>
          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              to="/predict"
              className="rounded-full bg-sunrise px-6 py-3 font-semibold text-white transition hover:scale-[1.02]"
            >
              Try Prediction
            </Link>
            <Link
              to="/about"
              className="rounded-full border border-sand/40 px-6 py-3 font-semibold text-sand transition hover:bg-white/10"
            >
              Learn More
            </Link>
          </div>
        </div>

        <div className="rounded-[2rem] border border-sunrise/30 bg-sunrise/10 p-8 shadow-panel">
          <p className="text-sm uppercase tracking-[0.3em] text-sand/70">Model inputs</p>
          <div className="mt-6 grid grid-cols-2 gap-3 text-sm">
            {["acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"].map((item) => (
              <div key={item} className="rounded-2xl bg-black/20 px-4 py-4 text-center font-semibold text-sand">
                {item}
              </div>
            ))}
          </div>
          <p className="mt-6 leading-7 text-sand/80">
            The backend derives motion magnitudes, scales features, and runs the trained classifier to produce activity
            probabilities.
          </p>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {highlights.map((item) => (
          <FeatureCard key={item.title} title={item.title} description={item.description} />
        ))}
      </div>
    </section>
  );
}

