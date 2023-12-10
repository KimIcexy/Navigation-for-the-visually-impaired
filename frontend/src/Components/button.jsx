import { Pressable, Text } from "react-native";

import { ButtonStyle } from "../Constant/Style.jsx";

const Button = ({ text, onPress, style }) => {
    return (
        <Pressable style={[ButtonStyle.container, style]} onPress={onPress}>
            <Text style={ButtonStyle.text}>{text}</Text>
        </Pressable>
    );
}

export default Button;