import axios from "axios";
import { useState } from "react";

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

					<button
						onClick={handleSubmit}
						disabled={loading}
						className="mt-2 bg-white text-black font-bold py-3 rounded-lg hover:scale-[1.02] active:scale-[0.98] transition disabled:opacity-50"
					>
						{loading ? "Processing CSV..." : "Run Analysis"}
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
							<p className="text-white/40 italic">Waiting for CSV upload...</p>
						)}
					</div>
				</div>
			</div>
		</>
	);
}