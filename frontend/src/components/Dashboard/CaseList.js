import React, { useState } from 'react';

function CaseList({ cases, onSelectCase, onCaseDeleted, onCaseCreated, showNewCaseModal, setShowNewCaseModal }) {
  const [newCaseData, setNewCaseData] = useState({
    name: '',
    brand_name: '',
    platform: 'x',
    description: '',
    goal: ''
  });
  const [error, setError] = useState('');


  // FAKE DB: Directly call onCaseCreated
  const handleCreateCase = (e) => {
    e.preventDefault();
    setError('');
    if (!newCaseData.name || !newCaseData.platform) {
      setError('Name and Platform are required');
      return;
    }
    onCaseCreated(newCaseData);
    setNewCaseData({
      name: '',
      brand_name: '',
      platform: 'x',
      description: '',
      goal: ''
    });
  };


  const handleDeleteCase = (caseId) => {
    if (window.confirm('Are you sure you want to delete this case?')) {
      onCaseDeleted(caseId);
    }
  };

  return (
    <div>
      {/* New Case Modal */}
      {showNewCaseModal && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Create New Case</h2>
            {error && <div className="alert alert-error">{error}</div>}

            <form onSubmit={handleCreateCase}>
              <div className="form-group">
                <label>Case Name *</label>
                <input
                  type="text"
                  value={newCaseData.name}
                  onChange={(e) => setNewCaseData({ ...newCaseData, name: e.target.value })}
                  placeholder="e.g., Tesla Brand Analysis"
                  required
                />
              </div>

              <div className="form-group">
                <label>Brand Name</label>
                <input
                  type="text"
                  value={newCaseData.brand_name}
                  onChange={(e) => setNewCaseData({ ...newCaseData, brand_name: e.target.value })}
                  placeholder="e.g., Tesla"
                />
              </div>

              <div className="form-group">
                <label>Platform *</label>
                <select
                  value={newCaseData.platform}
                  onChange={(e) => setNewCaseData({ ...newCaseData, platform: e.target.value })}
                >
                  <option value="x">X (Twitter)</option>
                  <option value="facebook">Facebook</option>
                </select>
              </div>

              <div className="form-group">
                <label>Description</label>
                <textarea
                  value={newCaseData.description}
                  onChange={(e) => setNewCaseData({ ...newCaseData, description: e.target.value })}
                  placeholder="Describe your case..."
                  rows="4"
                />
              </div>

              <div className="form-group">
                <label>Goal</label>
                <input
                  type="text"
                  value={newCaseData.goal}
                  onChange={(e) => setNewCaseData({ ...newCaseData, goal: e.target.value })}
                  placeholder="e.g., Sentiment Analysis"
                />
              </div>

              <div className="modal-buttons">
                <button type="submit" className="btn btn-primary">Create</button>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => {
                    setShowNewCaseModal(false);
                    setError('');
                  }}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Cases Grid */}
      <div className="cases-grid">
        {cases.length === 0 ? (
          <div className="empty-state">
            <p>No cases yet. Create one to get started!</p>
          </div>
        ) : (
          cases.map((caseItem) => (
            <div key={caseItem.id} className="case-card">
              <div className="case-header">
                <h3>{caseItem.name}</h3>
                <span className="platform-badge">{caseItem.platform.toUpperCase()}</span>
              </div>
              <p className="case-brand">{caseItem.brand_name}</p>
              <p className="case-description">{caseItem.description}</p>
              <div className="case-footer">
                <button
                  className="btn btn-primary"
                  onClick={() => onSelectCase(caseItem)}
                >
                  View Analytics
                </button>
                <button
                  className="btn btn-danger"
                  onClick={() => handleDeleteCase(caseItem.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default CaseList;
