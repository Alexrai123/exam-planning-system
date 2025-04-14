import React from 'react';
import { useAuth } from '../../context/AuthContext';

const UserDebug = () => {
  const { currentUser } = useAuth();

  return (
    <div style={{ padding: '20px', border: '1px solid #ccc', borderRadius: '5px', margin: '20px 0' }}>
      <h3>User Debug Information</h3>
      <p><strong>User Object:</strong> {JSON.stringify(currentUser)}</p>
      <p><strong>Role:</strong> {currentUser?.role || 'No role found'}</p>
      <p><strong>Role Type:</strong> {typeof currentUser?.role}</p>
      <p><strong>Is SECRETARIAT:</strong> {currentUser?.role === 'SECRETARIAT' ? 'Yes' : 'No'}</p>
      <p><strong>Is secretariat:</strong> {currentUser?.role === 'secretariat' ? 'Yes' : 'No'}</p>
    </div>
  );
};

export default UserDebug;
