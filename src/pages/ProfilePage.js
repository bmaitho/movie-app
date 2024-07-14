import React, { useState, useEffect } from 'react';
import './ProfilePage.css';

function ProfilePage() {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    fetch('/check_session')
      .then(response => response.json())
      .then(data => setProfile(data))
      .catch(error => console.error('Error fetching profile:', error));
  }, []);

  return (
    <div className="profile-page">
      <h2>Profile Page</h2>
      {profile ? (
        <div>
          <p>Username: {profile.username}</p>
          <p>Email: {profile.email}</p>
        </div>
      ) : (
        <p>Please log in to view your profile.</p>
      )}
    </div>
  );
}

export default ProfilePage;
