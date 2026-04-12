import "./App.css";
import { WavyBackground } from "./components/ui/wavy-background";
import { useState } from "react";
import axios from "axios";
import HeroSection from "./components/HeroSection";
import CSVComponent from "./components/CsvComponent";

function App() {

  return (
    <>
    <div className="block h-[80vh]">
      <WavyBackground className="max-w-6xl mx-auto px-4 py-20">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-bold text-white">ForeCast</h1>
          <p className="text-lg text-white/80 mt-4 max-w-2xl mx-auto">
            AI-powered time-series analysis with LangGraph orchestration.
          </p>
        </div>
      </WavyBackground>
    </div>
    <div className="block h-[50vh] mb-20">
      <HeroSection/>
    </div>
    <CSVComponent/>
    </>
  );
}

export default App;