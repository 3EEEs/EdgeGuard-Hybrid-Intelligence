import React, { useState, useEffect } from 'react';

const CloudGallery = () => {
    const [media, setMedia] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Replace with your Flask backend URL if different
        fetch('http://127.0.0.1:5000/get_cloud_media')
            .then(res => res.json())
            .then(data => {
                setMedia(data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Error fetching S3 media:", err);
                setLoading(false);
            });
    }, []);

    if (loading) return <p className="text-white">Loading captures from S3...</p>;

    return (
        <div className="gallery-grid">
            {media.length === 0 ? (
                <p className="text-gray-400">No motion events found in the cloud.</p>
            ) : (
                media.map((item, index) => (
                    <div key={index} className="gallery-item">
                        <img src={item.url} alt={item.name} className="rounded-lg border border-gray-700" />
                        <p className="text-xs mt-2 text-gray-400 truncate">{item.name}</p>
                    </div>
                ))
            )}

            <style jsx>{`
        .gallery-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
          gap: 1.5rem;
          margin-top: 1rem;
        }
        .gallery-item {
          background: #2a2d34;
          padding: 0.5rem;
          border-radius: 8px;
          transition: transform 0.2s;
        }
        .gallery-item:hover {
          transform: scale(1.02);
        }
        img {
          width: 100%;
          height: auto;
          display: block;
        }
      `}</style>
        </div>
    );
};

export default CloudGallery;