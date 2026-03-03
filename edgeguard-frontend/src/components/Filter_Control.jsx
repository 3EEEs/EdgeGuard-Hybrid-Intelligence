import React from 'react';

const FilterControl = ({ onFilterChange, sensitivity, setSensitivity }) => {
  return (
    <div className="card p-3 mb-4 bg-light">
      <h5>Dashboard Controls</h5>
      <hr />
      
      {/* Risk Mitigation: Sensitivity Slider for Motion Logic */}
      <div className="mb-3">
        <label htmlFor="sensitivityRange" className="form-label">
          Motion Sensitivity: <strong>{sensitivity}%</strong>
        </label>
        <input 
          type="range" 
          className="form-range" 
          id="sensitivityRange" 
          min="0" 
          max="100" 
          value={sensitivity}
          onChange={(e) => setSensitivity(e.target.value)}
        />
        <div className="form-text">Adjusts local pixel variance threshold.</div>
      </div>

      <div className="mb-3">
        <label className="form-label">Filter by Label</label>
        <select 
          className="form-select" 
          onChange={(e) => onFilterChange(e.target.value)}
        >
          <option value="All">All Events</option>
          <option value="Person">Person Only</option>
          <option value="Car">Car Only</option>
          <option value="Animal">Animal Only</option>
        </select>
      </div>
    </div>
  );
};

export default FilterControl;