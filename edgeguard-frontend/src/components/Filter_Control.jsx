// src/components/Filter_Control.jsx
import React, { useState } from 'react';
import axios from 'axios';

export default function Filter_Control() {
    const [threshold, setThreshold] = useState(200);

    const handleThresholdChange = async (e) => {
        const newVal = e.target.value;
        setThreshold(newVal);
        try {
            await axios.post('http://127.0.0.1:5000/set_threshold', { threshold: newVal });
        } catch (error) {
            console.error("Failed to update threshold", error);
        }
    };

    return (
        <div className="panel" style={{ background: '#1a1d24', padding: '1rem', borderRadius: '8px', border: '1px solid #2a2d34' }}>
            <h2>Edge Controls</h2>
            <div style={{ marginTop: '1rem' }}>
                <label>Motion Sensitivity (Threshold): {threshold}</label>
                <input 
                    type="range" 
                    min="50" 
                    max="400" 
                    value={threshold} 
                    onChange={handleThresholdChange}
                    style={{ width: '100%', marginTop: '0.5rem' }}
                />
            </div>
        </div>
    );
}
