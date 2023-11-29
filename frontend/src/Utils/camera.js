// Desc: Camera utility functions, get an image from the camera and return it as base64
export const getImage = async (cameraRef) => {
    if (cameraRef) {
        const options = { base64: true }
        const imageFile = await cameraRef.current.takePictureAsync(options);
        const imageData = await fetch(imageFile.uri);
        const blobData = await imageData.blob();
        return {
            'base64': imageFile.base64,
            'name': blobData.name,
            'type': blobData.type,
        }
    }
    return null;
}