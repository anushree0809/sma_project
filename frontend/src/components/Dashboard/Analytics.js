
import React, { useState } from 'react';
import './Analytics.css';

// Hardcoded analytics data for each case by id
const analyticsDataByCase = {
  1: {
    sentiment: { statistics: { positive: 62, negative: 18, neutral: 20 }, summary: 'Mostly positive sentiment for iPhone launch.' },
    trends: { top_trends: [['#iPhone', 120], ['#AppleEvent', 95], ['#Tech', 80]] },
    influencers: { influencers: [['@techguru', 120000, 'Gold'], ['@applefan', 95000, 'Silver']] },
    prediction: { predictions: [{ post: 'New iPhone review', engagement: 1200 }], avg_predicted_engagement: 1200 }
  },
  2: {
    sentiment: { statistics: { positive: 40, negative: 30, neutral: 30 }, summary: 'Mixed reviews for Tesla vehicles.' },
    trends: { top_trends: [['#Tesla', 100], ['#EV', 80], ['#ElonMusk', 60]] },
    influencers: { influencers: [['@teslafan', 80000, 'Gold'], ['@evreview', 60000, 'Silver']] },
    prediction: { predictions: [{ post: 'Tesla Model S', engagement: 900 }], avg_predicted_engagement: 900 }
  },
  3: {
    sentiment: { statistics: { positive: 55, negative: 15, neutral: 30 }, summary: 'Coca-Cola campaign well received.' },
    trends: { top_trends: [['#CokeSummer', 70], ['#CocaCola', 60], ['#Refresh', 40]] },
    influencers: { influencers: [['@cokeinfluencer', 50000, 'Gold']] },
    prediction: { predictions: [{ post: 'Coke Summer Ad', engagement: 700 }], avg_predicted_engagement: 700 }
  },
  4: {
    sentiment: { statistics: { positive: 48, negative: 22, neutral: 30 }, summary: 'Samsung Galaxy buzz is strong.' },
    trends: { top_trends: [['#SamsungGalaxy', 90], ['#Android', 70], ['#Tech', 50]] },
    influencers: { influencers: [['@samsungfan', 70000, 'Gold']] },
    prediction: { predictions: [{ post: 'Galaxy Launch', engagement: 800 }], avg_predicted_engagement: 800 }
  },
  5: {
    sentiment: { statistics: { positive: 60, negative: 10, neutral: 30 }, summary: 'Nike influencer impact is high.' },
    trends: { top_trends: [['#Nike', 80], ['#JustDoIt', 60], ['#Sneakers', 40]] },
    influencers: { influencers: [['@nikeathlete', 90000, 'Gold']] },
    prediction: { predictions: [{ post: 'Nike Ad', engagement: 950 }], avg_predicted_engagement: 950 }
  },
  6: {
    sentiment: { statistics: { positive: 35, negative: 40, neutral: 25 }, summary: 'Pepsi vs Coke: Pepsi has more negative sentiment.' },
    trends: { top_trends: [['#Pepsi', 60], ['#Coke', 55], ['#SodaWars', 30]] },
    influencers: { influencers: [['@sodareviewer', 30000, 'Silver']] },
    prediction: { predictions: [{ post: 'Pepsi vs Coke', engagement: 600 }], avg_predicted_engagement: 600 }
  },
  7: {
    sentiment: { statistics: { positive: 25, negative: 50, neutral: 25 }, summary: 'Meta privacy changes are controversial.' },
    trends: { top_trends: [['#MetaPrivacy', 40], ['#Facebook', 30], ['#Data', 20]] },
    influencers: { influencers: [['@privacyadvocate', 20000, 'Silver']] },
    prediction: { predictions: [{ post: 'Meta Privacy', engagement: 400 }], avg_predicted_engagement: 400 }
  },
  8: {
    sentiment: { statistics: { positive: 70, negative: 10, neutral: 20 }, summary: 'Adidas sports event is a hit.' },
    trends: { top_trends: [['#Adidas', 60], ['#Sports', 50], ['#Event', 30]] },
    influencers: { influencers: [['@adidasstar', 40000, 'Gold']] },
    prediction: { predictions: [{ post: 'Adidas Event', engagement: 750 }], avg_predicted_engagement: 750 }
  },
  9: {
    sentiment: { statistics: { positive: 80, negative: 5, neutral: 15 }, summary: 'Netflix show launch is overwhelmingly positive.' },
    trends: { top_trends: [['#Netflix', 100], ['#ShowLaunch', 80], ['#Binge', 60]] },
    influencers: { influencers: [['@netflixfan', 60000, 'Gold']] },
    prediction: { predictions: [{ post: 'Netflix Show', engagement: 1100 }], avg_predicted_engagement: 1100 }
  },
  10: {
    sentiment: { statistics: { positive: 65, negative: 20, neutral: 15 }, summary: 'Amazon Prime Day buzz is high.' },
    trends: { top_trends: [['#PrimeDay', 120], ['#Amazon', 100], ['#Deals', 80]] },
    influencers: { influencers: [['@dealhunter', 85000, 'Gold']] },
    prediction: { predictions: [{ post: 'Prime Day', engagement: 1300 }], avg_predicted_engagement: 1300 }
  }
};

const moduleConfig = {
  sentiment: { name: 'Sentiment Analysis' },
  trends: { name: 'Trending Topics' },
  influencers: { name: 'Influencer Detection' },
  prediction: { name: 'Popularity Prediction' }
};

function Analytics({ caseId, moduleId }) {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const config = moduleConfig[moduleId];

  // Hardcoded fake analytics results for demo
  const handleAnalyze = () => {
    setLoading(true);
    setError('');
    setTimeout(() => {
      const caseAnalytics = analyticsDataByCase[caseId] || {};
      const fakeResults = caseAnalytics[moduleId] || { message: 'No demo data available for this module/case.' };
      setResults(fakeResults);
      setLoading(false);
    }, 600);
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

      {error && <div className="alert alert-error">{error}</div>}

      {!results && !loading && (
        <div className="empty-state modern-empty">
          <p>Click <b>Analyze</b> to run {config.name} for this case.</p>
        </div>
      )}

      {loading && <div className="loading-spinner modern-spinner">Analyzing...</div>}

      {results && (
        <div className="results-container modern-results">
          {moduleId === 'sentiment' && results.statistics && (
            <div className="results-grid modern-grid">
              <div className="result-card modern-card">
                <h3>Overall Sentiment</h3>
                <div className="sentiment-bar-group">
                  <div className="sentiment-bar positive">
                    <span className="sentiment-value">{results.statistics.positive}</span>
                    <span className="label">Positive</span>
                  </div>
                  <div className="sentiment-bar negative">
                    <span className="sentiment-value">{results.statistics.negative}</span>
                    <span className="label">Negative</span>
                  </div>
                  <div className="sentiment-bar neutral">
                    <span className="sentiment-value">{results.statistics.neutral}</span>
                    <span className="label">Neutral</span>
                  </div>
                </div>
                {results.summary && <div className="sentiment-summary">{results.summary}</div>}
              </div>
            </div>
          )}

          {moduleId === 'trends' && results.top_trends && (
            <div className="results-grid modern-grid">
              <div className="result-card modern-card">
                <h3>Top Trends</h3>
                <ul className="trends-list modern-list">
                  {results.top_trends.map((trend, idx) => (
                    <li key={idx} className="trend-item modern-item">
                      <span className="trend-tag">{trend[0]}</span>
                      <span className="trend-count">{trend[1]} occurrences</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {moduleId === 'influencers' && results.influencers && (
            <div className="results-grid modern-grid">
              <div className="result-card modern-card">
                <h3>Top Influencers</h3>
                <table className="results-table modern-table">
                  <thead>
                    <tr>
                      <th>Username</th>
                      <th>Followers</th>
                      <th>Tier</th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.influencers.map((inf, idx) => (
                      <tr key={idx}>
                        <td>{inf[0]}</td>
                        <td>{inf[1]}</td>
                        <td><span className="badge modern-badge">{inf[2]}</span></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {moduleId === 'prediction' && results.predictions && (
            <div className="results-grid modern-grid">
              <div className="result-card modern-card">
                <h3>Engagement Predictions</h3>
                <ul className="prediction-list modern-list">
                  {results.predictions.map((pred, idx) => (
                    <li key={idx} className="prediction-item modern-item">
                      <span className="prediction-post">{pred.post}</span>: <b>{pred.engagement}</b> engagements
                    </li>
                  ))}
                </ul>
                <p className="avg-prediction modern-avg">
                  Average Predicted Engagement: <strong>{results.avg_predicted_engagement}</strong>
                </p>
              </div>
            </div>
          )}

          <div className="result-json modern-json">
            <h4>Full Results (JSON)</h4>
            <pre>{JSON.stringify(results, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  );
}

export default Analytics;
