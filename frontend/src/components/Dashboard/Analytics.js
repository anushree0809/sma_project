import React, { useState } from 'react';
import './Analytics.css';

// Hardcoded analytics data for each case
const analyticsDataByCase = {
  1: {
    sentiment: {
      statistics: { positive: 62, negative: 18, neutral: 20 },
      summary: 'Mostly positive sentiment for iPhone launch.'
    },
    trends: {
      top_trends: [['#iPhone', 120], ['#AppleEvent', 95], ['#Tech', 80]]
    },
    network: {
      nodes: 120,
      connections: 340,
      summary: 'Highly connected tech discussion network.'
    },
    recommendations: {
      suggestions: ['Post more video content', 'Use trending hashtags']
    },
    fake_news: {
      risk_score: 12,
      flagged_posts: 2
    },
    segmentation: {
      groups: ['Tech Enthusiasts', 'Apple Fans', 'Reviewers']
    },
    visualization: {
      chart: 'Engagement graph available'
    },
    ads: {
      best_ad_time: '7 PM',
      ctr: '5.2%'
    },
    monitoring: {
      active_users: 2300,
      mentions_per_min: 45
    },
    competitors: {
      top_competitor: 'Samsung',
      comparison: 'Higher engagement but slightly lower sentiment'
    },
    influencers: {
      influencers: [['@techguru', 120000, 'Gold']]
    },
    prediction: {
      predictions: [{ post: 'New iPhone review', engagement: 1200 }],
      avg_predicted_engagement: 1200
    }
  }
};

// Module names
const moduleConfig = {
  sentiment: { name: '😊 Sentiment Analysis' },
  trends: { name: '#️⃣ Trending Topics' },
  network: { name: '🕸️ Network Analysis' },
  recommendations: { name: '💡 Recommendations' },
  fake_news: { name: '🚨 Fake News Detection' },
  segmentation: { name: '👥 User Segmentation' },
  visualization: { name: '📈 Visualization' },
  ads: { name: '📢 Ad Optimization' },
  influencers: { name: '⭐ Influencers' },
  monitoring: { name: '📡 Real-time Monitoring' },
  competitors: { name: '🏆 Competitor Analysis' },
  prediction: { name: '🔮 Popularity Prediction' }
};

function Analytics({ caseId = 1, moduleId }) {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const config = moduleConfig[moduleId] || { name: 'Analytics Module' };

  const handleAnalyze = () => {
    setLoading(true);

    setTimeout(() => {
      const caseAnalytics = analyticsDataByCase[caseId] || analyticsDataByCase[1];
      const fakeResults = caseAnalytics[moduleId] || { message: 'No data available' };

      setResults(fakeResults);
      setLoading(false);
    }, 500);
  };

  return (
    <div className="analytics-container modern-analytics">
      <div className="analytics-header modern-header">
        <h2>{config.name}</h2>

        <button
          className="btn btn-primary modern-analyze-btn"
          onClick={handleAnalyze}
          disabled={loading}
        >
          {loading ? 'Analyzing...' : '▶️ Analyze'}
        </button>
      </div>

      {!results && !loading && (
        <div className="empty-state modern-empty">
          Click <b>Analyze</b> to run {config.name}
        </div>
      )}

      {loading && <div className="loading-spinner">Analyzing...</div>}

      {results && (
        <div className="results-container modern-results">

          {/* 😊 Sentiment */}
          {moduleId === 'sentiment' && results.statistics && (
            <div className="result-card">
              <h3>Sentiment</h3>
              <p>Positive: {results.statistics.positive}%</p>
              <p>Negative: {results.statistics.negative}%</p>
              <p>Neutral: {results.statistics.neutral}%</p>
              <p>{results.summary}</p>
            </div>
          )}

          {/* #️⃣ Trends */}
          {moduleId === 'trends' && results.top_trends && (
            <div className="result-card">
              <h3>Top Trends</h3>
              <ul>
                {results.top_trends.map((t, i) => (
                  <li key={i}>
                    {t[0]} - {t[1]} mentions
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* 🕸️ Network */}
          {moduleId === 'network' && (
            <div className="result-card">
              <h3>Network Analysis</h3>
              <p>Nodes: {results.nodes}</p>
              <p>Connections: {results.connections}</p>
              <p>{results.summary}</p>
            </div>
          )}

          {/* 💡 Recommendations */}
          {moduleId === 'recommendations' && (
            <div className="result-card">
              <h3>Recommendations</h3>
              <ul>
                {results.suggestions.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>
          )}

          {/* 🚨 Fake News */}
          {moduleId === 'fake_news' && (
            <div className="result-card">
              <h3>Fake News Detection</h3>
              <p>Risk Score: {results.risk_score}%</p>
              <p>Flagged Posts: {results.flagged_posts}</p>
            </div>
          )}

          {/* 👥 Segmentation */}
          {moduleId === 'segmentation' && (
            <div className="result-card">
              <h3>User Segments</h3>
              <ul>
                {results.groups.map((g, i) => (
                  <li key={i}>{g}</li>
                ))}
              </ul>
            </div>
          )}

          {/* 📈 Visualization */}
          {moduleId === 'visualization' && (
            <div className="result-card">
              <h3>Visualization</h3>
              <p>{results.chart}</p>
            </div>
          )}

          {/* 📢 Ads */}
          {moduleId === 'ads' && (
            <div className="result-card">
              <h3>Ad Optimization</h3>
              <p>Best Time: {results.best_ad_time}</p>
              <p>CTR: {results.ctr}</p>
            </div>
          )}

          {/* ⭐ Influencers */}
          {moduleId === 'influencers' && (
            <div className="result-card">
              <h3>Influencers</h3>
              <ul>
                {results.influencers.map((inf, i) => (
                  <li key={i}>
                    {inf[0]} - {inf[1]} followers ({inf[2]})
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* 📡 Monitoring */}
          {moduleId === 'monitoring' && (
            <div className="result-card">
              <h3>Real-time Monitoring</h3>
              <p>Active Users: {results.active_users}</p>
              <p>Mentions/min: {results.mentions_per_min}</p>
            </div>
          )}

          {/* 🏆 Competitors */}
          {moduleId === 'competitors' && (
            <div className="result-card">
              <h3>Competitor Analysis</h3>
              <p>Top Competitor: {results.top_competitor}</p>
              <p>{results.comparison}</p>
            </div>
          )}

          {/* 🔮 Prediction */}
          {moduleId === 'prediction' && (
            <div className="result-card">
              <h3>Predictions</h3>
              <ul>
                {results.predictions.map((p, i) => (
                  <li key={i}>
                    {p.post} → {p.engagement} engagements
                  </li>
                ))}
              </ul>
              <p>Average: {results.avg_predicted_engagement}</p>
            </div>
          )}

          {/* JSON */}
          <pre className="result-json">
            {JSON.stringify(results, null, 2)}
          </pre>

        </div>
      )}
    </div>
  );
}

export default Analytics;