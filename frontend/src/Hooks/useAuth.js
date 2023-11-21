import { useState, useEffect } from 'react';

import { getUser } from '../Utils/user.js';

export const useUser = () => {
    const [status, setStatus] = useState('Loading');
    const [user, setUser] = useState(null);
  
    useEffect(() => {
      const userRetrieve = async () => {
        const currentUser = await getUser();
        setUser(currentUser);
      };
  
      userRetrieve();
      setStatus('Done');
    }, []);
  
    return { status, user };
  };