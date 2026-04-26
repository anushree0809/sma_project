import React, { useState, useEffect } from 'react';
import Analytics from './Analytics';

function CaseDetail({ caseData, onBack }) {
  const [activeModule, setActiveModule] = useState('sentiment');
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);

  const token = localStorage.getItem('access_token');

  const modules = [
    { id: 'sentiment', name: '1️⃣ Sentiment Analysis', icon: '😊' },
    { id: 'trends', name: '2️⃣ Trending Topics', icon: '#️⃣' },
    { id: 'network', name: '3️⃣ Network Analysis', icon: '🕸️' },
    { id: 'recommendations', name: '4️⃣ Recommendations', icon: '💡' },
    { id: 'fake-news', name: '5️⃣ Fake News Detection', icon: '🚨' },
    { id: 'segmentation', name: '6️⃣ User Segmentation', icon: '👥' },
    { id: 'visualization', name: '7️⃣ Visualization', icon: '📈' },
    { id: 'ads', name: '8️⃣ Ad Optimization', icon: '📢' },
    { id: 'influencers', name: '9️⃣ Influencers', icon: '⭐' },
    { id: 'monitoring', name: '🔟 Real-time Monitoring', icon: '📡' },
    { id: 'competitors', name: '1️⃣1️⃣ Competitor Analysis', icon: '🏆' },
    { id: 'prediction', name: '1️⃣2️⃣ Popularity Prediction', icon: '🔮' }
  ];

  const handleAddSampleData = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/data/sample-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ case_id: caseData.id })
      });

      if (response.ok) {
        const data = await response.json();
        alert(`${data.posts_count} sample posts added!`);
        fetchPosts();
      }
    } catch (error) {
      alert('Error adding sample data');
    } finally {
      setLoading(false);
    }
  };

  const fetchPosts = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/cases/${caseData.id}/posts`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        setPosts(data.posts);
      }
    } catch (error) {
      console.error('Error fetching posts:', error);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, [caseData.id]);

  return (
    <div className="case-detail">
      <div className="container">
        <button className="btn btn-secondary" onClick={onBack}>
          ← Back to Cases
        </button>

        <div className="case-info">
          <h1>{caseData.name}</h1>
          <p className="case-description">{caseData.description}</p>
          <button
            className="btn btn-primary"
            onClick={handleAddSampleData}
            disabled={loading}
          >
            {loading ? 'Adding...' : '📥 Add Sample Data'}
          </button>
        </div>

        <div className="case-stats">
          <div className="stat">
            <span className="stat-value">{posts.length}</span>
            <span className="stat-label">Posts</span>
          </div>
          <div className="stat">
            <span className="stat-value">
              {posts.reduce((sum, p) => sum + p.likes, 0)}
            </span>
            <span className="stat-label">Total Likes</span>
          </div>
        </div>

        {/* Module Navigation */}
        <div className="modules-grid">
          {modules.map((module) => (
            <button
              key={module.id}
              className={`module-btn ${activeModule === module.id ? 'active' : ''}`}
              onClick={() => setActiveModule(module.id)}
              title={module.name}
            >
              <span className="module-icon">{module.icon}</span>
              <span className="module-label">{module.name}</span>
            </button>
          ))}
        </div>

        {/* Analytics Component */}
        <Analytics
          caseId={caseData.id}
          moduleId={activeModule}
          posts={posts}
          onPostsUpdate={fetchPosts}
        />
      </div>
    </div>
  );
}

export default CaseDetail;
