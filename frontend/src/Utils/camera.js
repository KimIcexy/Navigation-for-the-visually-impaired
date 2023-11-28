// Desc: Camera utility functions, get an image from the camera and return it as a blob
export const getImage = async (cameraRef) => {
    if (cameraRef) {
        const imageFile = await cameraRef.takePictureAsync();
        const imageData = await fetch(imageFile.uri);
        const blobData = await imageData.blob();
        return blobData;
    }
    return null;
}