import { useState } from "react";

export default function ESGComparison() {
  const [companies, setCompanies] = useState(["Tesla", "Apple", "Microsoft"]);
  const data = {
    Tesla: { E: 80, S: 70, G: 65 },
    Apple: { E: 75, S: 85, G: 80 },
    Microsoft: { E: 90, S: 80, G: 85 },
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">📊 ESG Comparison</h1>
      <table className="w-full border mt-4">
        <thead>
          <tr className="bg-gray-100">
            <th className="border p-2">Company</th>
            <th className="border p-2">Environmental</th>
            <th className="border p-2">Social</th>
            <th className="border p-2">Governance</th>
          </tr>
        </thead>
        <tbody>
          {companies.map((company) => (
            <tr key={company} className="border">
              <td className="border p-2">{company}</td>
              <td className="border p-2">{data[company].E}</td>
              <td className="border p-2">{data[company].S}</td>
              <td className="border p-2">{data[company].G}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
