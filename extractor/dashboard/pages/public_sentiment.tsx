import { useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

export default function PublicSentiment() {
  const [keyword, setKeyword] = useState("ESG");
  const [sentimentData, setSentimentData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);

  const fetchSentiment = async () => {
    setLoading(true);
    const response = await fetch(`/api/social_sentiment?keyword=${keyword}`);
    const data = await response.json();
    setSentimentData(data);
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">🌍 Public Perception & ESG Sentiment</h1>

      <Card className="p-4">
        <CardHeader>
          <CardTitle>🔍 Search ESG Sentiment</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input value={keyword} onChange={(e) => setKeyword(e.target.value)} placeholder="Enter ESG topic..." />
          <Button onClick={fetchSentiment} disabled={loading}>{loading ? "Analyzing..." : "Analyze Sentiment"}</Button>

          {sentimentData && (
            <div className="mt-4 space-y-4">
              <h2 className="text-lg font-semibold">📊 Sentiment Analysis</h2>
              <p>Overall Sentiment Score: {sentimentData.overall_sentiment.toFixed(2)}</p>
              <Progress value={(sentimentData.overall_sentiment + 1) * 50} />

              {/* Paginated Tweets */}
              <h3 className="font-semibold">📝 Twitter Insights</h3>
              <ul className="list-disc pl-6">
                {sentimentData.twitter.tweets.slice((page - 1) * 5, page * 5).map((tweet, index) => (
                  <li key={index} className="text-gray-600">{tweet}</li>
                ))}
              </ul>
              <div className="flex justify-between">
                <Button onClick={() => setPage(page - 1)} disabled={page === 1}>Previous</Button>
                <Button onClick={() => setPage(page + 1)} disabled={page * 5 >= sentimentData.twitter.tweets.length}>Next</Button>
              </div>

              {/* Lazy Loaded News */}
              <h3 className="font-semibold">📰 News Highlights</h3>
              {sentimentData.news.articles.slice(0, page * 2).map((article, index) => (
                <div key={index} className="p-2 border rounded-md">
                  <p className="font-semibold">{article.title}</p>
                  <p className="text-sm text-gray-500">{article.summary}</p>
                </div>
              ))}
              {page * 2 < sentimentData.news.articles.length && (
                <Button onClick={() => setPage(page + 1)}>Load More</Button>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
