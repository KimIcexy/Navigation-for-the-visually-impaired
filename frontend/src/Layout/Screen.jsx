import * as React from "react";
import { useState, useEffect } from "react";
import { createStackNavigator } from "@react-navigation/stack";

// Import all screens here
import { Home, Register, Login, FaceRegister, Loading } from "../Screens/";
import { getUser } from "../Utils/user";

const Stack = createStackNavigator();

const options = { headerShown: false};

export default () => {
    const [state, setState] = useState(false); // Is loading
    const [user, setUser] = useState(null); // User data

    useEffect(() => {
        getUser().then((user) => {
            setUser(user);
            setState(true);
        });
    }, []);

    return (
        <Stack.Navigator>
            {state ? (
                <>
                    <Stack.Screen name="Home" component={Home} options={options} />
                    {user ? (
                        <>
                            <Stack.Screen name="FaceRegister" component={FaceRegister} options={options} />
                        </>
                    ) : (
                        <>
                            <Stack.Screen name="Login" component={Login} options={options} />
                            <Stack.Screen name="Register" component={Register} options={options} />
                        </>
                    )}
                </>
            ) : 
                <Stack.Screen name="Loading" component={Loading} options={options} />
            }
        </Stack.Navigator>
    )
}