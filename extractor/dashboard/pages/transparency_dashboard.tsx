import { useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

export default function TransparencyDashboard() {
  const [company, setCompany] = useState("Tesla");
  const [scoreData, setScoreData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchTransparencyScore = async () => {
    setLoading(true);
    const response = await fetch(`/api/transparency_score?company=${company}`);
    const data = await response.json();
    setScoreData(data);
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">📊 ESG Transparency Score Dashboard</h1>

      <Card className="p-4">
        <CardHeader>
          <CardTitle>🔍 Check ESG Transparency</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input value={company} onChange={(e) => setCompany(e.target.value)} placeholder="Enter company name..." />
          <Button onClick={fetchTransparencyScore} disabled={loading}>{loading ? "Analyzing..." : "Analyze Transparency"}</Button>

          {scoreData && (
            <div className="mt-4 space-y-4">
              <h2 className="text-lg font-semibold">🏆 Transparency Score</h2>
              <Progress value={scoreData.transparency_score} />
              <p>Transparency Score: {scoreData.transparency_score}%</p>

              {/* Heatmap (Bar Chart) */}
              <h3 className="font-semibold">🌡️ Trustworthiness Heatmap</h3>
              <BarChart width={300} height={200} data={[
                { category: "Environmental", score: scoreData.external_sources["Environmental"] || 0 },
                { category: "Social", score: scoreData.external_sources["Social"] || 0 },
                { category: "Governance", score: scoreData.external_sources["Governance"] || 0 },
              ]}>
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="score" fill="#82ca9d" />
              </BarChart>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
