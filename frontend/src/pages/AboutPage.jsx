export default function AboutPage() {
  return (
    <section className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
      <article className="rounded-[2rem] border border-white/10 bg-white/5 p-8 shadow-panel backdrop-blur">
        <p className="text-sm uppercase tracking-[0.3em] text-sunrise">About the dataset</p>
        <h2 className="mt-4 font-display text-3xl font-bold text-white">UCI HHAR dataset</h2>
        <p className="mt-5 leading-8 text-sand/85">
          The Heterogeneity Human Activity Recognition dataset captures smartphone and smartwatch sensor readings across
          multiple users, device models, and everyday activities. This repository focuses on smartphone accelerometer
          and gyroscope streams for practical end-to-end deployment.
        </p>
      </article>

      <article className="rounded-[2rem] border border-white/10 bg-white/5 p-8 shadow-panel backdrop-blur">
        <h3 className="text-2xl font-semibold text-white">What this repository includes</h3>
        <ul className="mt-5 space-y-4 text-sand/85">
          <li>Data download and preprocessing pipeline for the activity-recognition experiment archive</li>
          <li>Random Forest classifier with persisted scaler, label encoder, metrics, and reports</li>
          <li>FastAPI backend with typed request and response models</li>
          <li>React + Vite frontend with Tailwind styling, loading states, and error handling</li>
          <li>Deployment configuration for Render and Vercel</li>
        </ul>
      </article>
    </section>
  );
}

