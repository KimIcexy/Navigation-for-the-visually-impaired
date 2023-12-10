import * as React from "react";
import { createStackNavigator } from "@react-navigation/stack";

// Import all screens here
import { Home, Register, Login, FaceRegister } from "../Screens/";

const Stack = createStackNavigator();

const options = { headerShown: false};

export default () => {
    return (
        <Stack.Navigator>
            <Stack.Screen name="Home" component={Home} options={options} />
            <Stack.Screen name="Register" component={Register} options={options}  />
            <Stack.Screen name="Login" component={Login} options={options}  />
            <Stack.Screen name="FaceRegister" component={FaceRegister} options={options}  />
        </Stack.Navigator>
    )
}