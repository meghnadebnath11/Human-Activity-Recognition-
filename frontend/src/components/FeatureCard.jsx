export default function FeatureCard({ title, description }) {
  return (
    <div className="rounded-[1.5rem] border border-white/10 bg-white/5 p-6 shadow-panel backdrop-blur">
      <h3 className="mb-3 text-xl font-semibold text-white">{title}</h3>
      <p className="leading-7 text-sand/80">{description}</p>
    </div>
  );
}

