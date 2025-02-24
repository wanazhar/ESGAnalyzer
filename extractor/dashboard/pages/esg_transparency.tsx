"use client";
import { useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Heatmap } from "recharts";

export default function ESGTransparency() {
  const [company, setCompany] = useState("");
  const [transparencyScore, setTransparencyScore] = useState<number | null>(null);

  const fetchTransparencyScore = async () => {
    const response = await fetch(`/api/esg_transparency?company=${company}`);
    const data = await response.json();
    if (data.transparency_score) {
      setTransparencyScore(data.transparency_score);
    } else {
      setTransparencyScore(null);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">🔍 ESG Transparency Score</h1>

      <Card className="p-4">
        <CardHeader>
          <CardTitle>📊 Enter Company Name</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input type="text" value={company} onChange={(e) => setCompany(e.target.value)} placeholder="Company Name" />
          <Button onClick={fetchTransparencyScore}>🔎 Check Transparency Score</Button>

          {transparencyScore !== null && (
            <div className="mt-4">
              <h2 className="text-lg font-semibold">Transparency Score: {transparencyScore.toFixed(2)}</h2>
              <Heatmap
                width={400}
                height={200}
                data={[{ x: 1, y: 1, value: transparencyScore }]}
                colorRange={["#ff0000", "#00ff00"]}
              />
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
