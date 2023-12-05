import { manipulateAsync } from 'expo-image-manipulator';

// Desc: Camera utility functions, get an image from the camera and return it as base64
export const getImage = async (cameraRef) => {
    if (cameraRef) {
        const options = { base64: true };
        const imageFile = await cameraRef.current.takePictureAsync(options);
        const image = await manipulateAsync(imageFile.uri, [{ resize: { width: 480, height: 640 } }], { base64: true });
        const imageData = await fetch(imageFile.uri);
        const blobData = await imageData.blob();
        return {
            'base64': image.base64,
            'type': blobData.type,
        }
    }
    return null;
}