import React, { useState } from 'react';
import Login from './Login';
import Welcome from './Welcome';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  return (
    <div className="h-screen flex justify-center items-center">
      {isLoggedIn ? <Welcome /> : <Login onLogin={handleLogin} />}
    </div>
  );
};

export default App;