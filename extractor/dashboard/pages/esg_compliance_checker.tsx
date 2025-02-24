import { useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";

export default function ESGComplianceChecker() {
  const [reportText, setReportText] = useState("");
  const [complianceData, setComplianceData] = useState(null);
  const [loading, setLoading] = useState(false);

  const checkCompliance = async () => {
    setLoading(true);
    const response = await fetch("/api/check_compliance", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ report: reportText }),
    });
    const data = await response.json();
    setComplianceData(data);
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">📜 ESG Compliance Checker</h1>

      <Card className="p-4">
        <CardHeader>
          <CardTitle>✅ Validate ESG Report</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input value={reportText} onChange={(e) => setReportText(e.target.value)} placeholder="Paste ESG report text..." />
          <Button onClick={checkCompliance} disabled={loading}>{loading ? "Checking..." : "Check Compliance"}</Button>

          {complianceData && (
            <div className="mt-4 space-y-4">
              <h2 className="text-lg font-semibold">⚠️ Missing Disclosures</h2>
              {Object.keys(complianceData.missing).length > 0 ? (
                <Alert className="bg-yellow-100 border-yellow-400 text-yellow-800">
                  <AlertDescription>
                    {Object.entries(complianceData.missing).map(([standard, items]) => (
                      <div key={standard}>
                        <strong>{standard}</strong>: {items.join(", ")}
                      </div>
                    ))}
                  </AlertDescription>
                </Alert>
              ) : (
                <Alert className="bg-green-100 border-green-400 text-green-800">
                  <AlertDescription>✅ ESG Report is Fully Compliant!</AlertDescription>
                </Alert>
              )}

              <h2 className="text-lg font-semibold">💡 Improvement Suggestions</h2>
              {Object.entries(complianceData.suggestions).map(([standard, items]) => (
                <Alert key={standard} className="bg-blue-100 border-blue-400 text-blue-800">
                  <AlertDescription>
                    <strong>{standard}:</strong> {items.join(", ")}
                  </AlertDescription>
                </Alert>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
