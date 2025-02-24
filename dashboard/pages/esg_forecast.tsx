import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";

const data = [
  { year: "2023", score: 72 },
  { year: "2024", score: 75 },
  { year: "2025", score: 78 },
  { year: "2026", score: 80 },
];

export default function ESGForecast() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">🔮 ESG Trend Forecast</h1>
      <LineChart width={600} height={300} data={data}>
        <XAxis dataKey="year" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="score" stroke="#82ca9d" />
      </LineChart>
    </div>
  );
}
