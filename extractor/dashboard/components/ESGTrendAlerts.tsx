"use client";
import { useEffect, useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";

export default function ESGTrendAlerts() {
  const [alerts, setAlerts] = useState([]);
  const [aiInsights, setAiInsights] = useState({});
  
  useEffect(() => {
    fetch("/api/esg_trend_alerts")
      .then((res) => res.json())
      .then((data) => setAlerts(data));
  }, []);

  const fetchAiInsight = (company, year) => {
    fetch(`/api/esg_ai_insights?company=${company}&year=${year}`)
      .then((res) => res.json())
      .then((data) => {
        setAiInsights(prev => ({ ...prev, [`${company}-${year}`]: data.ai_insight }));
      });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>📉 ESG Trend Anomaly Alerts</CardTitle>
      </CardHeader>
      <CardContent>
        {alerts.length === 0 ? (
          <p>No ESG trend anomalies detected.</p>
        ) : (
          alerts.map((alert, index) => (
            <Alert key={index}>
              <AlertTitle>{alert.company} ({alert.year})</AlertTitle>
              <AlertDescription>{alert.message}</AlertDescription>
              <Button
                className="mt-2"
                onClick={() => fetchAiInsight(alert.company, alert.year)}
              >
                🔍 AI Insights
              </Button>
              {aiInsights[`${alert.company}-${alert.year}`] && (
                <p className="mt-2 text-sm text-gray-600">
                  {aiInsights[`${alert.company}-${alert.year}`]}
                </p>
              )}
            </Alert>
          ))
        )}
      </CardContent>
    </Card>
  );
}
