import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

export default function ESGDashboard() {
  const [data, setData] = useState({});
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/esg")
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch((error) => console.error("Error fetching ESG data:", error));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">ESG Comparison Dashboard</h1>
      <Input 
        placeholder="Search company..." 
        value={search} 
        onChange={(e) => setSearch(e.target.value)} 
        className="mb-4" 
      />

      {Object.keys(data)
        .filter(company => company.toLowerCase().includes(search.toLowerCase()))
        .map((company) => (
          <Card key={company} className="mb-6">
            <CardContent>
              <h2 className="text-xl font-semibold">{company}</h2>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Category</TableHead>
                    <TableHead>Company Claim</TableHead>
                    <TableHead>External Sentiment</TableHead>
                    <TableHead>LLM Opinion</TableHead>
                    <TableHead>Reliability Score</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {data[company].contradictions.map((entry, idx) => (
                    <TableRow key={idx}>
                      <TableCell>{entry.category}</TableCell>
                      <TableCell>{entry.company_claim}</TableCell>
                      <TableCell>{entry.external_sentiment}</TableCell>
                      <TableCell>{entry.llm_opinion.split("\n")[1]}</TableCell>
                      <TableCell>
                        <Badge variant={
                          entry.llm_opinion.includes("High") ? "success" : 
                          entry.llm_opinion.includes("Medium") ? "warning" : "destructive"
                        }>
                          {entry.llm_opinion.split("\n")[0].replace("Reliability Score: ", "")}
                        </Badge>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
      ))}
    </div>
  );
}
