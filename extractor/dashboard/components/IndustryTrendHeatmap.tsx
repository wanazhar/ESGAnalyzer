"use client";
import { useEffect, useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from "@/components/ui/table";
import { Heatmap } from "@nivo/heatmap";

export default function IndustryTrendHeatmap() {
  const [trends, setTrends] = useState([]);
  const [year, setYear] = useState(new Date().getFullYear());

  useEffect(() => {
    fetch(`/api/industry_trends?year=${year}`)
      .then((res) => res.json())
      .then((data) => setTrends(data));
  }, [year]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>📊 ESG Industry Trend Heatmap ({year})</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Industry</TableHead>
              <TableHead>ESG Score Change</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {trends.map((trend, index) => (
              <TableRow key={index}>
                <TableCell>{trend.industry}</TableCell>
                <TableCell className={trend.change >= 0 ? "text-green-500" : "text-red-500"}>
                  {trend.change.toFixed(2)}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>

        <div className="mt-4 h-64">
          <Heatmap
            data={trends.map(trend => ({
              industry: trend.industry,
              change: trend.change,
            }))}
            keys={["change"]}
            indexBy="industry"
            colors={{ scheme: "red_yellow_green" }}
            margin={{ top: 10, right: 30, bottom: 40, left: 100 }}
            axisLeft={{
              tickSize: 5,
              tickPadding: 5,
              tickRotation: 0,
            }}
          />
        </div>
      </CardContent>
    </Card>
  );
}
