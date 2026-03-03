import React from 'react';

const Filter_Control = ({ onFilterChange, sensitivity, setSensitivity }) => {
  
  const handleSensitivityChange = (e) => {
    const newVal = e.target.value;
    setSensitivity(newVal);
    // Integration: Sync with local Python edge script
    console.log(`Syncing Sensitivity: ${newVal}% to Edge...`);
  };

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
    paddingBottom: '10px'
  };

  return (
    <div style={panelStyle}>
      <div style={headerStyle}>
        <h3 style={{ margin: 0, fontSize: '1.2rem' }}>Edge Logic Control</h3>
      </div>
      
      <div className="panel-content">
        {/* Risk Mitigation: Sensitivity Slider */}
        <div style={{ marginBottom: '25px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.9rem', color: '#8b949e' }}>Low</span>
            <span style={{ fontWeight: 'bold', color: '#58a6ff' }}>{sensitivity}%</span>
            <span style={{ fontSize: '0.9rem', color: '#8b949e' }}>High</span>
          </div>
          <input 
            type="range" 
            className="custom-slider" 
            style={{ width: '100%', cursor: 'pointer' }}
            min="0" max="100" 
            value={sensitivity}
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