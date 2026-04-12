import { WavyBackground } from "./ui/wavy-background";

export default function HeroSection() {
	return (
		<>
			<WavyBackground className="max-w-6xl mx-auto px-4 py-20">
				<div className="text-center mb-12">
					<h1 className="text-6xl md:text-8xl lg:text-9xl font-extrabold text-white tracking-tighter leading-none">
						ForeCast
					</h1>
					<p className="text-xl md:text-2xl text-white/70 mt-6 max-w-3xl mx-auto font-medium leading-relaxed">
						AI-powered time-series analysis <br className="hidden md:block" />
						with <span className="text-white">LangGraph orchestration</span>.
					</p>
				</div>
			</WavyBackground>
		</>
	)
}