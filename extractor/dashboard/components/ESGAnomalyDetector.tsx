"use client";
import { useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

export default function ESGAnomalyDetector() {
  const [company, setCompany] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchData = () => {
    if (!company) return;
    setLoading(true);
    fetch(`/api/esg_anomaly?company=${company}`)
      .then((res) => res.json())
      .then((result) => {
        setData(result);
        setLoading(false);
      });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>🚨 ESG Anomaly Detection & AI Insights</CardTitle>
      </CardHeader>
      <CardContent>
        <Input
          type="text"
          placeholder="Enter company symbol (e.g., AAPL, TSLA)"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          className="mb-2"
        />
        <Button onClick={fetchData} disabled={loading} className="mb-3">
          {loading ? <Loader2 className="animate-spin" /> : "Analyze ESG Anomalies"}
        </Button>

        {data && (
          <div className="text-sm">
            <strong>Company:</strong> {data.company}
            <ul className="list-disc ml-4">
              <li><strong>Anomalies:</strong> {Array.isArray(data.anomalies) ? data.anomalies.join(", ") : data.anomalies}</li>
              <li><strong>AI Insights:</strong> {data.ai_insights}</li>
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
