// Desc: Convert a blob image to a base64 string
export const getBase64Image = async (blob) => {
    if (blob) {
        const base64 = await new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                resolve(reader.result);
            };
            reader.onerror = () => {
                reject(new Error('Failed to convert image to base64'));
            };
            reader.readAsDataURL(blob);
        })
        return base64;
    }
    return null;
}