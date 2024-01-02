import Svg, { Path } from 'react-native-svg';

import { PHONE_HEIGHT, PHONE_WIDTH } from '../Constant/Phone.jsx';

const convertDataPath = (data) => {
    // Convert from pixel by pixel data to path data
    let path = '';
    for (let i = 0; i < data.length; i++) {
        const { x, y } = data[i];
        if (i == 0) {
            path += `M ${x} ${y} `;
        }
        else {
            path += `L ${x} ${y} `;
        }
    }
    return path;
}

export const PathComponent = ({ data }) => {
    const path = convertDataPath(data);
    // The original image is 640x480
    // Scale it to the phone's size
    const phoneSize = 
    return (
        <Svg height="100%" width="100%" viewBox="0 0 100 100">
            <Path
                d={path}
                stroke="red"
                strokeWidth="1"
                fill="none"
            />
        </Svg>
    )
}