import * as React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import { LogBox } from 'react-native';

import Screen from './src/Layout/Screen';

export default function App() {
  LogBox.ignoreAllLogs();
  return (
    <NavigationContainer>
      <Screen />
    </NavigationContainer>
  );
}
