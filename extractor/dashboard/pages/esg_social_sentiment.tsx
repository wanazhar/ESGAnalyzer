import { useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

export default function ESGSocialSentiment() {
  const [company, setCompany] = useState("");
  const [sentimentData, setSentimentData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchSentiment = async () => {
    setLoading(true);
    const response = await fetch("/api/social_sentiment", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ company }),
    });
    const data = await response.json();
    setSentimentData(data);
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">📢 ESG Social Sentiment</h1>

      <Card className="p-4">
        <CardHeader>
          <CardTitle>📝 Analyze Public ESG Perception</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input value={company} onChange={(e) => setCompany(e.target.value)} placeholder="Enter company name..." />
          <Button onClick={fetchSentiment} disabled={loading}>{loading ? "Analyzing..." : "Fetch Sentiment"}</Button>

          {sentimentData && (
            <div className="mt-4 space-y-4">
              <h2 className="text-lg font-semibold">📊 Sentiment Breakdown</h2>
              <BarChart width={600} height={300} data={sentimentData.overview}>
                <XAxis dataKey="source" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="positive" fill="#4CAF50" />
                <Bar dataKey="negative" fill="#F44336" />
              </BarChart>

              <h2 className="text-lg font-semibold">⚠️ Greenwashing Alerts</h2>
              {sentimentData.greenwashing_alerts.length > 0 ? (
                <Alert className="bg-red-100 border-red-400 text-red-800">
                  <AlertDescription>
                    🚨 {sentimentData.greenwashing_alerts.join(", ")}
                  </AlertDescription>
                </Alert>
              ) : (
                <Alert className="bg-green-100 border-green-400 text-green-800">
                  <AlertDescription>No Greenwashing Concerns Detected! ✅</AlertDescription>
                </Alert>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
