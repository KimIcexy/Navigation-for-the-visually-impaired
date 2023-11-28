import * as React from 'react';
import {NavigationContainer} from '@react-navigation/native';

import Screen from './src/Layout/Screen';

export default function App() {
  return (
    <NavigationContainer>
      <Screen />
    </NavigationContainer>
  );
}
