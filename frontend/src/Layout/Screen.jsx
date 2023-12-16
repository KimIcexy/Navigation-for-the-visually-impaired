import * as React from "react";
import { useState, useEffect } from "react";
import { createStackNavigator } from "@react-navigation/stack";

// Import all screens here
import { Home, Register, Login, FaceRegister, Loading, FaceDetection, Navigation } from "../Screens/";
import { useUser } from '../Hooks/useAuth.js';

const Stack = createStackNavigator();

const options = { headerShown: false};

export default () => {
    const { status, user } = useUser();

    return (
        <Stack.Navigator>
            <Stack.Screen name="Home" component={Home} options={options} />
            <Stack.Screen name="FaceDetection" component={FaceDetection} options={options} />
            <Stack.Screen name="FaceRegister" component={FaceRegister} options={options} />
            <Stack.Screen name="Login" component={Login} options={options} />
            <Stack.Screen name="Register" component={Register} options={options} />
            <Stack.Screen name="Loading" component={Loading} options={options} />
            <Stack.Screen name="Navigation" component={Navigation} options={options} />
        </Stack.Navigator>
    )
}