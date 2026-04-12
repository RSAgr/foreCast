import {
	LineChart,
	Line,
	XAxis,
	YAxis,
	CartesianGrid,
	Tooltip,
	ResponsiveContainer
} from 'recharts';

export default function GraphComponent({ result , label}: { result: any , label : string}) {
	return (
		<>
			{result?.forecast && (
				<div className="mt-8 border-t border-white/10 pt-6 ml-[8vw]">
					<span className="text-[10px] font-black uppercase tracking-widest text-blue-500 mb-4 block">
						{label}
					</span>

					<div className="h-[300px] w-full bg-white/5 rounded-xl p-4 border border-white/5">
						<ResponsiveContainer width="100%" height="100%">
							<LineChart
								/* Mapping the flat array [10, 20, 15] to [{name: 0, value: 10}, ...] */
								data={result.forecast.map((val: number, i: number) => ({
									index: i + 1,
									value: val
								}))}
							>
								<CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
								<XAxis
									dataKey="index"
									stroke="#666"
									fontSize={12}
									tickLine={false}
									axisLine={false}
								/>
								<YAxis
									stroke="#666"
									fontSize={12}
									tickLine={false}
									axisLine={false}
									tickFormatter={(val) => `${val.toFixed(1)}`}
								/>
								<Tooltip
									contentStyle={{ backgroundColor: '#18181b', border: '1px solid #3f3f46', borderRadius: '8px' }}
									itemStyle={{ color: '#60a5fa' }}
								/>
								<Line
									type="monotone"
									dataKey="value"
									stroke="#3b82f6"
									strokeWidth={3}
									dot={{ r: 4, fill: '#3b82f6' }}
									activeDot={{ r: 6, strokeWidth: 0 }}
									animationDuration={1500}
								/>
							</LineChart>
						</ResponsiveContainer>
					</div>
				</div>
			)}
		</>
	)
}