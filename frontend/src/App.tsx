import "./App.css";
import { WavyBackground } from "./components/ui/wavy-background";
import { useState } from "react";
import axios from "axios";
import HeroSection from "./components/HeroSection";
import CSVComponent from "./components/CsvComponent";
import { cn } from "./lib/utils";
import ValuesComponent from "./components/ValuesComponet";

function App() {
  const [activeTab, setActiveTab] = useState<"manual" | "csv">("manual");

  return (
    <div className="p-4">
      <div className="block h-screen">
        <HeroSection/>
      </div>

      <div className="mt-10 block">
        <div className="flex p-1 bg-zinc-900 border border-zinc-800 rounded-xl shadow-2xl">
          <button
            onClick={() => setActiveTab("manual")}
            className={cn(
              "px-8 py-2.5 text-sm font-semibold rounded-lg transition-all duration-200",
              activeTab === "manual"
                ? "bg-white text-black shadow-[0_0_20px_rgba(255,255,255,0.3)]"
                : "text-zinc-500 hover:text-zinc-200"
            )}
          >
            Manual Entry
          </button>
          <button
            onClick={() => setActiveTab("csv")}
            className={cn(
              "px-8 py-2.5 text-sm font-semibold rounded-lg transition-all duration-200",
              activeTab === "csv"
                ? "bg-white text-black shadow-[0_0_20px_rgba(255,255,255,0.3)]"
                : "text-zinc-500 hover:text-zinc-200"
            )}
          >
            CSV Upload
          </button>
        </div>
      </div>
      { activeTab === "manual" && <ValuesComponent/> }
      { activeTab === "csv" && <CSVComponent/> }
    </div>
  );
}

export default App;