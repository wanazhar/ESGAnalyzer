"use client";
import { useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function ESGData() {
  const [company, setCompany] = useState("");
  const [esgData, setEsgData] = useState(null);

  const fetchEsgData = async () => {
    const response = await fetch(`/api/esg_data?company=${company}`);
    const data = await response.json();
    setEsgData(data);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">🌍 ESG Data Aggregation</h1>

      <Card className="p-4">
        <CardHeader>
          <CardTitle>🔎 Search ESG Data</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input type="text" value={company} onChange={(e) => setCompany(e.target.value)} placeholder="Company Name" />
          <Button onClick={fetchEsgData}>Fetch ESG Data</Button>

          {esgData && (
            <div className="mt-4">
              <h2 className="text-lg font-semibold">ESG Scores</h2>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={[esgData]}>
                  <XAxis dataKey="company" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="environmental" fill="#4caf50" />
                  <Bar dataKey="social" fill="#2196f3" />
                  <Bar dataKey="governance" fill="#ff9800" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
