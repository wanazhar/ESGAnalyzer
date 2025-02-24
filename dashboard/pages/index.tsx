import Link from "next/link";

export default function Home() {
  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold">🌍 ESG Analyzer Dashboard</h1>
      <p className="text-gray-600 mt-2">Analyze, compare, and monitor ESG trends in real-time.</p>
      <div className="grid grid-cols-2 gap-6 mt-6">
        <Link href="/esg_comparison" className="block bg-blue-500 text-white p-4 rounded-lg">
          📊 ESG Comparison Matrix
        </Link>
        <Link href="/esg_forecast" className="block bg-green-500 text-white p-4 rounded-lg">
          🔮 ESG Forecasting
        </Link>
        <Link href="/esg_social_sentiment" className="block bg-yellow-500 text-white p-4 rounded-lg">
          🗣️ Public ESG Sentiment
        </Link>
        <Link href="/esg_transparency_score" className="block bg-purple-500 text-white p-4 rounded-lg">
          🔍 ESG Transparency Scores
        </Link>
      </div>
    </div>
  );
}
