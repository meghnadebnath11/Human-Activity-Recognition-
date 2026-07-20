import { NavLink, Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import AboutPage from "./pages/AboutPage";
import PredictPage from "./pages/PredictPage";

const navigationClass = ({ isActive }) =>
  `rounded-full px-4 py-2 text-sm font-semibold transition ${
    isActive ? "bg-sand text-ink" : "text-sand/80 hover:bg-white/10 hover:text-sand"
  }`;

export default function App() {
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(249,115,22,0.18),_transparent_40%),linear-gradient(135deg,_#07111f,_#0f172a_65%,_#0f766e)] text-sand">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col px-6 py-6 md:px-10">
        <header className="mb-10 flex flex-col gap-6 rounded-[2rem] border border-white/10 bg-white/5 p-6 shadow-panel backdrop-blur md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-sand/70">HHAR Intelligent Sensing</p>
            <h1 className="font-display text-3xl font-bold md:text-4xl">Human Activity Recognition Dashboard</h1>
          </div>
          <nav className="flex flex-wrap gap-2">
            <NavLink className={navigationClass} to="/">
              Home
            </NavLink>
            <NavLink className={navigationClass} to="/predict">
              Predict
            </NavLink>
            <NavLink className={navigationClass} to="/about">
              About
            </NavLink>
          </nav>
        </header>

        <main className="flex-1">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/predict" element={<PredictPage />} />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

