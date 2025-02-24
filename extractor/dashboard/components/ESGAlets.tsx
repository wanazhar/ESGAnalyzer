"use client";
import { useEffect, useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

export default function ESGAlerts() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetch("/api/esg_alerts")
      .then((res) => res.json())
      .then((data) => setAlerts(data));
  }, []);

  return (
    <Card>
      <CardHeader>
        <CardTitle>⚠️ ESG Anomaly Alerts</CardTitle>
      </CardHeader>
      <CardContent>
        {alerts.length === 0 ? (
          <p>No anomalies detected.</p>
        ) : (
          alerts.map((alert, index) => (
            <Alert key={index}>
              <AlertTitle>{alert.company}</AlertTitle>
              <AlertDescription>{alert.message}</AlertDescription>
            </Alert>
          ))
        )}
      </CardContent>
    </Card>
  );
}
