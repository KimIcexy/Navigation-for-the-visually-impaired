import * as React from "react";
import { createStackNavigator } from "@react-navigation/stack";

// Import all screens here
import { Home, Register, Login, FaceRegister } from "../Screens/";

const Stack = createStackNavigator();

export default () => {
    return (
        <Stack.Navigator>
            <Stack.Screen name="Home" component={Home} />
            <Stack.Screen name="Register" component={Register} />
            <Stack.Screen name="Login" component={Login} />
            <Stack.Screen name="FaceRegister" component={FaceRegister} />
        </Stack.Navigator>
    )
}