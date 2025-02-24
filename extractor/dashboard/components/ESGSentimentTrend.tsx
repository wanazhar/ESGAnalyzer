"use client";
import { useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

export default function ESGSentimentTrend() {
  const [company, setCompany] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchData = () => {
    if (!company) return;
    setLoading(true);
    fetch(`/api/sentiment_trend?company=${company}`)
      .then((res) => res.json())
      .then((result) => {
        setData(result);
        setLoading(false);
      });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>📈 ESG Sentiment Trend Analysis</CardTitle>
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
          {loading ? <Loader2 className="animate-spin" /> : "Analyze Sentiment Trends"}
        </Button>

        {data && (
          <div className="text-sm">
            <strong>Company:</strong> {data.company}
            <ul className="list-disc ml-4">
              <li><strong>Major Sentiment Shifts:</strong> {Array.isArray(data.sentiment_shifts) ? data.sentiment_shifts.join(", ") : data.sentiment_shifts}</li>
            </ul>

            {/* Line Chart for Sentiment Trends */}
            {data.sentiment_shifts.length > 0 && (
              <LineChart width={400} height={200} data={data.sentiment_shifts}>
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <CartesianGrid stroke="#ccc" />
                <Line type="monotone" dataKey="sentiment_score" stroke="#8884d8" />
              </LineChart>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
