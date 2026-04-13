import axios from "axios";
import { useState } from "react";
import { BackgroundGradient } from "./ui/background-gradient";
import GraphComponent from "./GraphComponent";
import { Button } from "./ui/moving-border";

export default function CSVComponent() {
	const [file, setFile] = useState<File | null>(null);
	const [targetColumn, setTargetColumn] = useState<string>("");
	const [query, setQuery] = useState<string>("");
	const [result, setResult] = useState<any>(null);
	const [loading, setLoading] = useState<boolean>(false);

	const handleSubmit = async () => {
		if (!file || !targetColumn) {
			alert("Please upload a CSV file and specify the target column.");
			return;
		}

		try {
			setLoading(true);
			setResult(null);

			// Create FormData to send the file and text inputs
			const formData = new FormData();
			formData.append("file", file);
			formData.append("target_column", targetColumn.trim());
			if (query.trim()) {
				formData.append("user_query", query.trim());
			}

			console.log("Submitting CSV for column:", targetColumn);

			// Hit the backend CSV endpoint
			const res = await axios.post("http://127.0.0.1:8000/forecast/csv", formData, {
				headers: {
					"Content-Type": "multipart/form-data",
				},
			});

			setResult(res.data);
		} catch (err) {
			console.error(err);
			setResult({
				explanation: "Error processing CSV. Ensure the column name is correct and numeric."
			});
		} finally {
			setLoading(false);
		}
	};

	return (
		<>
			<div className="grid grid-cols-1 md:grid-cols-2 gap-10 items-start">
				{/* INPUT SECTION */}
				<div className="flex flex-col gap-4 bg-black/20 p-6 rounded-2xl backdrop-blur-sm border border-white/10">
					<h2 className="text-2xl text-white font-semibold">CSV Data Input</h2>

					<label className="text-white/60 text-sm">Upload CSV File</label>
					<input
						type="file"
						accept=".csv"
						onChange={(e) => setFile(e.target.files?.[0] || null)}
						className="p-2 rounded-lg bg-white/10 text-white border border-white/20 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-white file:text-black hover:file:bg-gray-200"
					/>

					<label className="text-white/60 text-sm">Target Column Name</label>
					<input
						type="text"
						placeholder="e.g., sales, temperature, price"
						value={targetColumn}
						onChange={(e) => setTargetColumn(e.target.value)}
						className="p-3 rounded-lg bg-white/10 text-white border border-white/20 focus:border-white/50 outline-none transition"
					/>

					<label className="text-white/60 text-sm">Specific Question (Optional)</label>
					<input
						type="text"
						placeholder="Analyze this data for..."
						value={query}
						onChange={(e) => setQuery(e.target.value)}
						className="p-3 rounded-lg bg-white/10 text-white border border-white/20 focus:border-white/50 outline-none transition"
					/>

					<div className="mt-2">
						<Button
							borderRadius="0.5rem"
							onClick={handleSubmit}
							disabled={loading}
							containerClassName="w-full"
							className="w-full dark:bg-zinc-900 text-white dark:text-black dark:border-slate-800 font-bold py-3 transition duration-200 hover:scale-[1.01] active:scale-[0.99] disabled:opacity-50"
						>
							{loading ? (
								<div className="flex items-center gap-2">
									<div className="h-4 w-4 border-2 border-current border-t-transparent animate-spin rounded-full" />
									<span>Processing CSV...</span>
								</div>
							) : (
								"Run Analysis"
							)}
						</Button>
					</div>
				</div>

				{/* OUTPUT SECTION */}
				<div className="w-full mt-4">
					<BackgroundGradient className="rounded-[22px] w-full dark:bg-zinc-900 overflow-hidden">
						<div className="sm:p-8 rounded-[20px] bg-zinc-950/90 flex flex-col gap-2">
							<h2 className="text-2xl text-white font-bold tracking-tight">
								Analysis Results
							</h2>

							<div className="p-6 rounded-xl bg-white/5 border border-white/10 text-white min-h-[300px] backdrop-blur-md">
								{result ? (
									<div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-500">
										{/* Model Info */}
										<div className="flex flex-col gap-1">
											<span className="text-[10px] font-black uppercase tracking-widest text-blue-500">
												Engine
											</span>
											<p className="text-lg font-medium text-blue-100">
												{result.model_selected || result.model || "Proprietary Model"}
											</p>
										</div>

										{/* AI Explanation */}
										<div className="flex flex-col gap-1">
											<span className="text-[10px] font-black uppercase tracking-widest text-emerald-500">
												AI Insight
											</span>
											<p className="text-sm leading-relaxed text-zinc-200 whitespace-pre-line bg-zinc-900/50 p-3 rounded-lg border border-white/5">
												{result.explanation}
											</p>
										</div>

										{/* Anomalies section */}
										{result.anomalies?.length > 0 && (
											<div className="flex flex-col gap-1 border-t border-white/5 pt-4">
												<span className="text-[10px] font-black uppercase tracking-widest text-red-500">
													Risk Assessment
												</span>
												<div className="flex items-center gap-2 text-red-200">
													<div className="h-2 w-2 rounded-full bg-red-500 animate-pulse" />
													<p className="text-sm font-semibold">
														{result.anomalies.length} outliers detected in the sequence.
													</p>
												</div>
											</div>
										)}
									</div>
								) : (
									<div className="h-full flex flex-col items-center justify-center space-y-3 opacity-40">
										<p className="text-sm italic">Waiting for csv to upload</p>
									</div>
								)}
							</div>
						</div>
					</BackgroundGradient>
				</div>
				<GraphComponent result={result} label={targetColumn || "Forecast Values"} />
			</div>
		</>
	);
}