"use client";
import { useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function ESGForecast() {
  const [year, setYear] = useState(new Date().getFullYear() + 1);
  const [carbonEmissions, setCarbonEmissions] = useState(100);
  const [waterUsage, setWaterUsage] = useState(50);
  const [diversityScore, setDiversityScore] = useState(80);
  const [boardIndependence, setBoardIndependence] = useState(70);
  const [predictedScore, setPredictedScore] = useState(null);

  const predictESG = async () => {
    const response = await fetch("/api/esg_forecast", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        year,
        carbon_emissions: carbonEmissions,
        water_usage: waterUsage,
        diversity_score: diversityScore,
        board_independence: boardIndependence,
      }),
    });

    const data = await response.json();
    setPredictedScore(data.predicted_esg_score);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">📈 ESG Trend Prediction</h1>

      <Card className="p-4">
        <CardHeader>
          <CardTitle>🔮 Enter Sustainability Metrics</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input type="number" value={year} onChange={(e) => setYear(Number(e.target.value))} placeholder="Year" />
          <Input type="number" value={carbonEmissions} onChange={(e) => setCarbonEmissions(Number(e.target.value))} placeholder="Carbon Emissions" />
          <Input type="number" value={waterUsage} onChange={(e) => setWaterUsage(Number(e.target.value))} placeholder="Water Usage" />
          <Input type="number" value={diversityScore} onChange={(e) => setDiversityScore(Number(e.target.value))} placeholder="Diversity Score" />
          <Input type="number" value={boardIndependence} onChange={(e) => setBoardIndependence(Number(e.target.value))} placeholder="Board Independence" />
          <Button onClick={predictESG}>📊 Predict ESG Score</Button>
          {predictedScore && <p className="text-xl font-semibold">Predicted ESG Score: {predictedScore}</p>}
        </CardContent>
      </Card>
    </div>
  );
}
