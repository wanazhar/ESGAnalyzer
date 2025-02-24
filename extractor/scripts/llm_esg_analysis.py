import React, { useEffect, useState } from "react";
import { Heatmap } from "@/components/ui/heatmap";
import { Select } from "@/components/ui/select";
import { Alert } from "@/components/ui/alert";
import { Input } from "@/components/ui/input";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import { Chatbot } from "@/components/ui/chatbot";

const ESGHeatmap = ({ company }) => {
  const [esgData, setEsgData] = useState([]);
  const [historicalData, setHistoricalData] = useState([]);
  const [futurePredictions, setFuturePredictions] = useState([]);
  const [selectedYear, setSelectedYear] = useState("2024");
  const [selectedFactor, setSelectedFactor] = useState("Overall");
  const [alerts, setAlerts] = useState([]);
  const [threshold, setThreshold] = useState(20); // Default threshold
  const [chatHistory, setChatHistory] = useState([]);
  const [userQuery, setUserQuery] = useState("");
  
  useEffect(() => {
    fetch(`/api/esg_comparison?company=${company}&year=${selectedYear}&factor=${selectedFactor}`)
      .then(response => response.json())
      .then(data => {
        setEsgData(data);
        checkForAlerts(data);
      });
    fetch(`/api/esg_trend?company=${company}&factor=${selectedFactor}`)
      .then(response => response.json())
      .then(data => setHistoricalData(data));
    fetch(`/api/esg_predictions?company=${company}&factor=${selectedFactor}`)
      .then(response => response.json())
      .then(data => setFuturePredictions(data));
  }, [company, selectedYear, selectedFactor, threshold]);

  const checkForAlerts = (data) => {
    const newAlerts = data.filter(item => item.discrepancy > threshold);
    setAlerts(newAlerts);
  };

  const handleChatSubmit = () => {
    if (!userQuery.trim()) return;
    const newChat = [...chatHistory, { user: userQuery, response: "Thinking..." }];
    setChatHistory(newChat);
    fetch("/api/llm_esg_chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ company, query: userQuery })
    })
      .then(response => response.json())
      .then(data => {
        setChatHistory([...newChat.slice(0, -1), { user: userQuery, response: data.answer }]);
      });
    setUserQuery("");
  };

  return (
    <div className="p-4 bg-white shadow rounded-lg">
      <h2 className="text-xl font-semibold mb-2">ESG Score Consistency for {company}</h2>
      <div className="flex space-x-4 mb-4">
        <Select value={selectedYear} onChange={e => setSelectedYear(e.target.value)}>
          {["2024", "2023", "2022", "2021"].map(year => (
            <option key={year} value={year}>{year}</option>
          ))}
        </Select>
        <Select value={selectedFactor} onChange={e => setSelectedFactor(e.target.value)}>
          {["Overall", "Environmental", "Social", "Governance"].map(factor => (
            <option key={factor} value={factor}>{factor}</option>
          ))}
        </Select>
        <Input
          type="number"
          value={threshold}
          onChange={e => setThreshold(Number(e.target.value))}
          placeholder="Set discrepancy threshold"
          className="w-32"
        />
      </div>
      {alerts.length > 0 && (
        <div className="mb-4">
          {alerts.map((alert, index) => (
            <Alert key={index} variant="destructive">
              Warning: {alert.source} shows a high discrepancy of {alert.discrepancy} in {selectedFactor} for {selectedYear}.
            </Alert>
          ))}
        </div>
      )}
      <Heatmap 
        data={esgData} 
        xKey="source" 
        yKey="year" 
        valueKey="discrepancy" 
        colorScale={['#4CAF50', '#FFC107', '#F44336']} 
      />
      <h2 className="text-xl font-semibold mt-6 mb-2">Historical ESG Trends</h2>
      <LineChart width={600} height={300} data={historicalData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="year" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="score" stroke="#8884d8" />
      </LineChart>
      <h2 className="text-xl font-semibold mt-6 mb-2">Future ESG Predictions</h2>
      <LineChart width={600} height={300} data={futurePredictions}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="year" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="predicted_score" stroke="#82ca9d" />
      </LineChart>
      <h2 className="text-xl font-semibold mt-6 mb-2">AI-Powered ESG Chat</h2>
      <div className="mb-4">
        <Input
          type="text"
          value={userQuery}
          onChange={e => setUserQuery(e.target.value)}
          placeholder="Ask AI about ESG trends"
          className="w-full mb-2"
        />
        <button className="bg-blue-500 text-white p-2 rounded" onClick={handleChatSubmit}>Submit</button>
      </div>
      <div className="bg-gray-100 p-4 rounded-lg">
        {chatHistory.map((chat, index) => (
          <div key={index} className="mb-2">
            <p><strong>User:</strong> {chat.user}</p>
            <p><strong>AI:</strong> {chat.response}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ESGHeatmap;
