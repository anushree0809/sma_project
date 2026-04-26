import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import CaseList from './CaseList';
import CaseDetail from './CaseDetail';
import Analytics from './Analytics';

function Dashboard({ user, onLogout }) {
  const [currentView, setCurrentView] = useState('cases');
  const [selectedCase, setSelectedCase] = useState(null);
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showNewCaseModal, setShowNewCaseModal] = useState(false);

  const token = localStorage.getItem('access_token');


  // FAKE DB: Use local state for cases

  useEffect(() => {
    // Optionally, load from localStorage for persistence
    const storedCases = localStorage.getItem('fake_cases');
    if (storedCases) {
      setCases(JSON.parse(storedCases));
    } else {
      // Pre-populate with sample data if no cases exist
      const sampleCases = [
        {
          id: 1,
          name: 'iPhone Launch Analysis',
          brand_name: 'Apple',
          platform: 'x',
          description: 'Analyze public sentiment on X (Twitter) about the latest iPhone launch.',
          goal: 'Sentiment Analysis'
        },
        {
          id: 2,
          name: 'Tesla Brand Monitoring',
          brand_name: 'Tesla',
          platform: 'x',
          description: 'Track mentions and reviews of Tesla vehicles on X.',
          goal: 'Competitor Analysis'
        },
        {
          id: 3,
          name: 'Coca-Cola Summer Campaign',
          brand_name: 'Coca-Cola',
          platform: 'facebook',
          description: 'Evaluate engagement for Coca-Cola’s summer marketing campaign.',
          goal: 'Engagement Tracking'
        },
        {
          id: 4,
          name: 'Samsung Galaxy Buzz',
          brand_name: 'Samsung',
          platform: 'x',
          description: 'Monitor buzz around the new Samsung Galaxy release.',
          goal: 'Trend Detection'
        },
        {
          id: 5,
          name: 'Nike Influencer Impact',
          brand_name: 'Nike',
          platform: 'facebook',
          description: 'Assess the impact of influencers on Nike’s brand perception.',
          goal: 'Influencer Analysis'
        },
        {
          id: 6,
          name: 'Pepsi vs Coke',
          brand_name: 'Pepsi',
          platform: 'x',
          description: 'Compare sentiment and engagement between Pepsi and Coca-Cola.',
          goal: 'Competitor Benchmarking'
        },
        {
          id: 7,
          name: 'Meta Privacy Feedback',
          brand_name: 'Meta',
          platform: 'facebook',
          description: 'Collect user feedback on Meta’s new privacy features.',
          goal: 'User Feedback Analysis'
        },
        {
          id: 8,
          name: 'Adidas Sports Event',
          brand_name: 'Adidas',
          platform: 'x',
          description: 'Analyze engagement during Adidas-sponsored sports events.',
          goal: 'Event Analytics'
        },
        {
          id: 9,
          name: 'Netflix Show Launch',
          brand_name: 'Netflix',
          platform: 'facebook',
          description: 'Track reactions to the launch of a new Netflix original series.',
          goal: 'Sentiment Analysis'
        },
        {
          id: 10,
          name: 'Amazon Prime Day',
          brand_name: 'Amazon',
          platform: 'x',
          description: 'Monitor social media buzz and deals during Amazon Prime Day.',
          goal: 'Trend Analysis'
        }
      ];
      setCases(sampleCases);
      localStorage.setItem('fake_cases', JSON.stringify(sampleCases));
    }
    setLoading(false);
  }, []);

  // Save cases to localStorage on change
  useEffect(() => {
    localStorage.setItem('fake_cases', JSON.stringify(cases));
  }, [cases]);

  const handleCaseSelect = (caseItem) => {
    setSelectedCase(caseItem);
    setCurrentView('case-detail');
  };


  const handleCaseCreated = (newCase) => {
    // Assign a fake ID
    const fakeId = Date.now();
    setCases([...cases, { ...newCase, id: fakeId }]);
    setShowNewCaseModal(false);
  };


  const handleCaseDeleted = (caseId) => {
    setCases(cases.filter(c => c.id !== caseId));
  };

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-left">
          <h1 className="app-title">📊 Social Media Analytics</h1>
        </div>
        <div className="header-right">
          <span className="user-info">Welcome, {user.username}!</span>
          <button className="btn btn-secondary" onClick={onLogout}>
            Logout
          </button>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="dashboard-nav">
        <button
          className={`nav-btn ${currentView === 'cases' ? 'active' : ''}`}
          onClick={() => setCurrentView('cases')}
        >
          📁 My Cases
        </button>
        {selectedCase && (
          <button
            className={`nav-btn ${currentView === 'case-detail' ? 'active' : ''}`}
            onClick={() => setCurrentView('case-detail')}
          >
            📊 Analytics
          </button>
        )}
      </nav>

      {/* Main Content */}
      <main className="dashboard-content">
        {currentView === 'cases' && (
          <div className="container">
            <div className="section-header">
              <h2>Your Cases</h2>
              <button
                className="btn btn-primary"
                onClick={() => setShowNewCaseModal(true)}
              >
                + New Case
              </button>
            </div>

            {loading ? (
              <div className="loading-spinner">Loading...</div>
            ) : (
              <CaseList
                cases={cases}
                onSelectCase={handleCaseSelect}
                onCaseDeleted={handleCaseDeleted}
                onCaseCreated={handleCaseCreated}
                showNewCaseModal={showNewCaseModal}
                setShowNewCaseModal={setShowNewCaseModal}
              />
            )}
          </div>
        )}

        {currentView === 'case-detail' && selectedCase && (
          <CaseDetail
            caseData={selectedCase}
            onBack={() => {
              setCurrentView('cases');
              setSelectedCase(null);
            }}
          />
        )}
      </main>
    </div>
  );
}

export default Dashboard;
