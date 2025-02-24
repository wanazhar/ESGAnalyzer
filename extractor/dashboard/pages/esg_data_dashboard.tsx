import { useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

export default function ESGDataDashboard() {
  const [company, setCompany] = useState("Tesla");
  const [esgData, setEsgData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchESGData = async () => {
    setLoading(true);
    const response = await fetch(`/api/esg_data_aggregator?company=${company}`);
    const data = await response.json();
    setEsgData(data);
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">🌍 ESG Data Aggregation Dashboard</h1>

      <Card className="p-4">
        <CardHeader>
          <CardTitle>🔍 Fetch Multi-Source ESG Data</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input value={company} onChange={(e) => setCompany(e.target.value)} placeholder="Enter company name..." />
          <Button onClick={fetchESGData} disabled={loading}>{loading ? "Fetching..." : "Get ESG Data"}</Button>

          {esgData && (
            <div className="mt-4 space-y-4">
              <h2 className="text-lg font-semibold">🏆 Aggregated ESG Scores</h2>
              
              {/* ESG Data Breakdown */}
              <BarChart width={400} height={250} data={[
                { category: "Environmental", score: esgData.aggregated_esg_scores["Environmental"] || 0 },
                { category: "Social", score: esgData.aggregated_esg_scores["Social"] || 0 },
                { category: "Governance", score: esgData.aggregated_esg_scores["Governance"] || 0 },
              ]}>
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="score" fill="#8884d8" />
              </BarChart>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
