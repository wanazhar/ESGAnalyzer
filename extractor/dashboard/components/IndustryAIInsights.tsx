"use client";
import { useEffect, useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";

export default function IndustryAIInsights() {
  const [insights, setInsights] = useState("");
  const [year, setYear] = useState(new Date().getFullYear());
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchInsights();
  }, [year]);

  const fetchInsights = () => {
    setLoading(true);
    fetch(`/api/industry_ai_insights?year=${year}`)
      .then((res) => res.json())
      .then((data) => {
        setInsights(data.insights);
        setLoading(false);
      });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>🧠 AI-Generated ESG Industry Insights ({year})</CardTitle>
      </CardHeader>
      <CardContent>
        <Textarea value={insights} readOnly className="h-40 w-full text-gray-900" />
        <Button onClick={fetchInsights} disabled={loading} className="mt-3">
          {loading ? "Generating insights..." : "Refresh Insights"}
        </Button>
      </CardContent>
    </Card>
  );
}
