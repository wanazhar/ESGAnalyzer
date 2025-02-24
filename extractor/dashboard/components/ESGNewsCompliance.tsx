"use client";
import { useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

export default function ESGNewsCompliance() {
  const [company, setCompany] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchData = () => {
    if (!company) return;
    setLoading(true);
    fetch(`/api/news_compliance?company=${company}`)
      .then((res) => res.json())
      .then((result) => {
        setData(result);
        setLoading(false);
      });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>🌍 ESG News & Compliance Checker</CardTitle>
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
          {loading ? <Loader2 className="animate-spin" /> : "Analyze ESG News & Compliance"}
        </Button>

        {data && (
          <div className="text-sm">
            <strong>Company:</strong> {data.company}
            <h3 className="mt-2 font-bold">🔍 Recent ESG News:</h3>
            <ul className="list-disc ml-4">
              {data.news_headlines.map((headline: string, index: number) => (
                <li key={index}>{headline}</li>
              ))}
            </ul>
            
            <h3 className="mt-2 font-bold">📊 News Sentiment:</h3>
            <p>Positive: {data.news_sentiment.positive}</p>
            <p>Neutral: {data.news_sentiment.neutral}</p>
            <p>Negative: {data.news_sentiment.negative}</p>

            <h3 className="mt-2 font-bold">⚠️ Compliance Gaps:</h3>
            {typeof data.compliance_gaps === "string" ? (
              <p>{data.compliance_gaps}</p>
            ) : (
              <ul className="list-disc ml-4">
                {Object.entries(data.compliance_gaps).map(([standard, gaps]: any, index: number) => (
                  <li key={index}><strong>{standard}:</strong> {gaps.join(", ")}</li>
                ))}
              </ul>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
