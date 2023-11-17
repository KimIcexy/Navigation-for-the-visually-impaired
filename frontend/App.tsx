import * as React from 'react';
import { NavigationContainer } from "@react-navigation/native";
// import {Text, View} from 'react-native';

// import Layout from './src/Layout';
import Screen from './src/Layout/Screen';

export default function App() {
  return (
    <NavigationContainer>
      <Screen />
    </NavigationContainer>
  );
}
