import { manipulateAsync, FlipType } from 'expo-image-manipulator';

// Resize an image from base64 to base64
export const resizeImage = async (base64, width, height) => {
    const { type, image } = base64;
    const newImage = await manipulateAsync(`data:${type};base64,${image}`, [{resize: { width: width, height: height }}, {flip: FlipType.Horizontal}], { base64: true });
    return newImage.base64;
}