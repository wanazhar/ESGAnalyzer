"use client";
import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Loader2 } from "lucide-react";
import { HeatmapChart } from "recharts";

export default function ESGTransparencyHeatmap({ sector, region }) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/esg_ranking?sector=${sector}&region=${region}`)
      .then((res) => res.json())
      .then((result) => {
        setData(result.ranked_esg_scores);
        setLoading(false);
      });
  }, [sector, region]);

  return (
    <Card>
      <CardContent>
        {loading ? (
          <Loader2 className="animate-spin" />
        ) : (
          <HeatmapChart
            width={600}
            height={400}
            data={Object.entries(data || {}).map(([company, score]) => ({
              name: company,
              value: score,
            }))}
            colors={["#d73027", "#fee08b", "#1a9850"]}
          />
        )}
      </CardContent>
    </Card>
  );
}
