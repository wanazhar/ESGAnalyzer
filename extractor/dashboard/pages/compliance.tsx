"use client";
import { useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

export default function ESGCompliance() {
  const [reportData, setReportData] = useState("");
  const [complianceResult, setComplianceResult] = useState(null);

  const checkCompliance = async () => {
    const response = await fetch("/api/check_compliance", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ report_data: JSON.parse(reportData) }),
    });

    const data = await response.json();
    setComplianceResult(data.compliance_result);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">✅ ESG Compliance Checker</h1>

      <Card className="p-4">
        <CardHeader>
          <CardTitle>📑 Upload ESG Report Data</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Textarea value={reportData} onChange={(e) => setReportData(e.target.value)} placeholder="Paste JSON report data here..." />
          <Button onClick={checkCompliance}>Check Compliance</Button>

          {complianceResult && (
            <div className="mt-4 space-y-2">
              <h2 className="text-lg font-semibold">Results:</h2>
              {complianceResult.map((item, index) => (
                <p key={index} className={item.includes("✅") ? "text-green-500" : "text-red-500"}>
                  {item}
                </p>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
