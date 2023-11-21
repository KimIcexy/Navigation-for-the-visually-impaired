import EncryptedStorage from 'react-native-encrypted-storage';

export const getUser = async () => {
    const user = await EncryptedStorage.getItem('user');
    if (user) {
        return JSON.parse(user);
    }
    return null;
}

export const setUser = async (user) => {
    await EncryptedStorage.setItem('user', JSON.stringify(user));
}

export const removeUser = async () => {
    await EncryptedStorage.removeItem('user');
}

// Can't seem to find a good place, so I put it here too.
// After all, they're still in the 'User management' category.
export const setToken = async (token) => {
    await EncryptedStorage.setItem('token', token);
}

export const getToken = async () => {
    const token = await EncryptedStorage.getItem('token');
    if (token) {
        return token;
    }
    return null;
}

export const removeToken = async () => {
    await EncryptedStorage.removeItem('token');
}