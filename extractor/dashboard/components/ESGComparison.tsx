"use client";
import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectItem } from "@/components/ui/select";
import { Bar } from "react-chartjs-2";

export default function ESGComparison() {
  const [esgData, setEsgData] = useState({});
  const [year, setYear] = useState("");
  const [company, setCompany] = useState("");

  useEffect(() => {
    fetch(`/api/esg_comparison?year=${year}&company=${company}`)
      .then((res) => res.json())
      .then((data) => setEsgData(data));
  }, [year, company]);

  const chartData = {
    labels: Object.keys(esgData),
    datasets: [
      {
        label: "ESG Mentions",
        data: Object.values(esgData).map((items) => items.length),
        backgroundColor: ["green", "blue", "purple"],
      },
    ],
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>ESG Comparison</CardTitle>
      </CardHeader>
      <CardContent>
        <Select onValueChange={setYear}>
          <SelectItem value="">All Years</SelectItem>
          <SelectItem value="2023">2023</SelectItem>
          <SelectItem value="2024">2024</SelectItem>
        </Select>
        <Select onValueChange={setCompany}>
          <SelectItem value="">All Companies</SelectItem>
          <SelectItem value="Tesla">Tesla</SelectItem>
          <SelectItem value="Apple">Apple</SelectItem>
        </Select>
        <Bar data={chartData} />
      </CardContent>
    </Card>
  );
}
