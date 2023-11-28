import AsyncStorage from '@react-native-async-storage/async-storage';

export const getUser = async () => {
    const user = await AsyncStorage.getItem('user');
    if (user) {
        return JSON.parse(user);
    }
    return null;
}

export const setUser = async (user) => {
    await AsyncStorage.setItem('user', JSON.stringify(user));
}

export const removeUser = async () => {
    await AsyncStorage.removeItem('user');
}

// Can't seem to find a good place, so I put it here too.
// After all, they're still in the 'User management' category.
export const setToken = async (token) => {
    await AsyncStorage.setItem('token', token);
}

export const getToken = async () => {
    const token = await AsyncStorage.getItem('token');
    if (token) {
        return token;
    }
    return null;
}

export const removeToken = async () => {
    await AsyncStorage.removeItem('token');
}