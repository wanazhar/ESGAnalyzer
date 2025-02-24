"use client";
import { useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function ESGDataAggregator() {
  const [company, setCompany] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchData = () => {
    if (!company) return;
    setLoading(true);
    fetch(`/api/esg_data?company=${company}`)
      .then((res) => res.json())
      .then((result) => {
        setData(result);
        setLoading(false);
      });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>📊 Multi-Source ESG Data Aggregation</CardTitle>
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
          {loading ? "Fetching..." : "Get ESG Data"}
        </Button>

        {data && (
          <div className="text-sm">
            <strong>Company:</strong> {data.company}
            <ul className="list-disc ml-4">
              <li>FMP: {JSON.stringify(data.FMP)}</li>
              <li>Finhub: {JSON.stringify(data.Finhub)}</li>
              <li>Refinitiv: {JSON.stringify(data.Refinitiv)}</li>
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
