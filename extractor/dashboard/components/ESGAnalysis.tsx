"use client";
import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";

export default function ESGAnalysis() {
  const [analysis, setAnalysis] = useState("");
  const [year, setYear] = useState("2024");
  const [company, setCompany] = useState("Tesla");

  useEffect(() => {
    fetch(`/api/ai_analysis?year=${year}&company=${company}`)
      .then((res) => res.json())
      .then((data) => setAnalysis(data.analysis));
  }, [year, company]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>AI-Driven ESG Insights</CardTitle>
      </CardHeader>
      <CardContent>
        <Textarea value={analysis} readOnly />
        <Button onClick={() => setAnalysis("")}>Refresh Analysis</Button>
      </CardContent>
    </Card>
  );
}
