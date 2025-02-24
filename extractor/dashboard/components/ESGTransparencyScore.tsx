"use client";
import { useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";
import { Heatmap } from "recharts";

export default function ESGTransparencyScore() {
  const [company, setCompany] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchData = () => {
    if (!company) return;
    setLoading(true);
    fetch(`/api/esg_transparency?company=${company}`)
      .then((res) => res.json())
      .then((result) => {
        setData(result);
        setLoading(false);
      });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>🔍 ESG Transparency Score</CardTitle>
      </CardHeader>
      <CardContent>
        <Input
          type="text"
          placeholder="Enter company symbol (e.g., TSLA, AAPL)"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          className="mb-2"
        />
        <Button onClick={fetchData} disabled={loading} className="mb-3">
          {loading ? <Loader2 className="animate-spin" /> : "Check ESG Transparency"}
        </Button>

        {data && (
          <div className="text-sm">
            <strong>Company:</strong> {data.company}
            <h3 className="mt-2 font-bold">📊 Transparency Score: {data.transparency_score}%</h3>

            <h3 className="mt-2 font-bold">⚠️ Discrepancies:</h3>
            {Object.keys(data.discrepancies).length === 0 ? (
              <p>No major discrepancies detected.</p>
            ) : (
              <ul className="list-disc ml-4">
                {Object.entries(data.discrepancies).map(([metric, values]: any, index: number) => (
                  <li key={index}>
                    <strong>{metric}:</strong> Reported: {values.reported}, External: {values.external}
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
