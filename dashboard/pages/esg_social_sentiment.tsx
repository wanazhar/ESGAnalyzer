import { useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
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
            <div className="mt-4">
              <BarChart width={600} height={300} data={sentimentData}>
                <XAxis dataKey="source" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="positive" fill="#4CAF50" />
                <Bar dataKey="negative" fill="#F44336" />
              </BarChart>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
