"use client";
import { useState } from "react";
import ESGTransparencyHeatmap from "@/components/ESGTransparencyHeatmap";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Select, SelectTrigger, SelectValue, SelectItem, SelectContent } from "@/components/ui/select";

const sectors = ["All", "Technology", "Finance", "Energy", "Healthcare"];
const regions = ["All", "North America", "Europe", "Asia", "Global"];

export default function Dashboard() {
  const [selectedSector, setSelectedSector] = useState("All");
  const [selectedRegion, setSelectedRegion] = useState("All");

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">📊 ESG Analytics Dashboard</h1>

      {/* Sector & Region Filters */}
      <div className="flex gap-4">
        <Card className="p-4 w-1/2">
          <CardHeader>
            <CardTitle>📁 Filter by Sector</CardTitle>
          </CardHeader>
          <CardContent>
            <Select value={selectedSector} onValueChange={setSelectedSector}>
              <SelectTrigger>
                <SelectValue placeholder="Select Sector" />
              </SelectTrigger>
              <SelectContent>
                {sectors.map((sector) => (
                  <SelectItem key={sector} value={sector}>
                    {sector}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </CardContent>
        </Card>

        <Card className="p-4 w-1/2">
          <CardHeader>
            <CardTitle>🌍 Filter by Region</CardTitle>
          </CardHeader>
          <CardContent>
            <Select value={selectedRegion} onValueChange={setSelectedRegion}>
              <SelectTrigger>
                <SelectValue placeholder="Select Region" />
              </SelectTrigger>
              <SelectContent>
                {regions.map((region) => (
                  <SelectItem key={region} value={region}>
                    {region}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </CardContent>
        </Card>
      </div>

      {/* ESG Transparency Heatmap */}
      <Card className="p-4">
        <CardHeader>
          <CardTitle>🌍 ESG Transparency Heatmap</CardTitle>
        </CardHeader>
        <CardContent>
          <ESGTransparencyHeatmap sector={selectedSector} region={selectedRegion} />
        </CardContent>
      </Card>
    </div>
  );
}
