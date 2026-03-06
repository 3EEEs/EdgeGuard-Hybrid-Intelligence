import React, { useState, useEffect } from 'react';

const BACKEND_URL = 'http://127.0.0.1:5000';

const Filter_Control = ({ onFilterChange }) => {

  const [threshold, setThreshold] = useState(200);
  const [syncStatus, setSyncStatus] = useState('idle');

  useEffect(() => {
    fetch(`${BACKEND_URL}/get_threshold`)
      .then((res) => res.json())
      .then((data) => setThreshold(data.motion_threshold))
      .catch(() => {});
  }, []);

  const handleSensitivityChange = async (e) => {
    const newVal = parseInt(e.target.value);
    setThreshold(newVal);
    setSyncStatus('syncing');
    // Integration: Sync with local Python edge script
    try {
      const res = await fetch(`${BACKEND_URL}/set_threshold`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ threshold: newVal }),
      });
      if (!res.ok) throw new Error();
      setSyncStatus('ok');
    } catch {
      setSyncStatus('error');
    }
  };

  const statusColor = { idle: '#8b949e', syncing: '#e3b341', ok: '#3fb950', error: '#f85149' }[syncStatus];
  const statusLabel = { idle: 'Ready', syncing: 'Syncing...', ok: 'Synced ✓', error: 'Backend offline' }[syncStatus];

  // Styles to replicate the "box" from your original screenshot
  const panelStyle = {
    backgroundColor: '#1a1d23', // Dark panel background
    border: '1px solid #2d333b', // Subtle border for definition
    borderRadius: '8px',
    padding: '20px',
    height: '90%',
    display: 'flex',
    flexDirection: 'column',
    color: '#f0f6fc'
  };

  const headerStyle = {
    borderBottom: '1px solid #2d333b',
    marginBottom: '20px',
    paddingBottom: '10px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  };

  return (
    <div style={panelStyle}>
      <div style={headerStyle}>
        <h3 style={{ margin: 0, fontSize: '1.2rem' }}>Edge Logic Control</h3>
        <span style={{ fontSize: '0.75rem', color: statusColor }}>{statusLabel}</span>
      </div>

      <div className="panel-content">
        {/* Risk Mitigation: Sensitivity Slider */}
        <div style={{ marginBottom: '25px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.9rem', color: '#8b949e' }}>Easy (50)</span>
            <span style={{ fontWeight: 'bold', color: '#58a6ff' }}>{threshold} px</span>
            <span style={{ fontSize: '0.9rem', color: '#8b949e' }}>Hard (400)</span>
          </div>
          <input
            type="range"
            className="custom-slider"
            style={{ width: '100%', cursor: 'pointer' }}
            min="50" max="400" step="10"
            value={threshold}
            onChange={handleSensitivityChange}
          />
        </div>

        {/* UI Filtering Dropdown */}
        <div className="filter-group">
          <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem' }}>
            Filter Dashboard View:
          </label>
          <select
            style={{
              width: '100%',
              padding: '8px',
              backgroundColor: '#0d1117',
              color: '#f0f6fc',
              border: '1px solid #30363d',
              borderRadius: '6px'
            }}
            onChange={(e) => onFilterChange(e.target.value)}
          >
            <option value="All">All Detections</option>
            <option value="Person">Person Only</option>
            <option value="Car">Car Only</option>
          </select>
        </div>
      </div>
    </div>
  );
};

export default Filter_Control;