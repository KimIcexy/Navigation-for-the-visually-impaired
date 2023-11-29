import { get, post, postForm } from './generic'

const UserAPI = {
    login: function(data) {
        const url = '/api/login/';
        return post(url, data, "");
    },
    loginWithFace: function(data) {
        const url = `/api/login/face/`;
        return postForm(url, data, "");
    },
    register: function(data) {
        const url = '/api/register/';
        return post(url, data, "");
    },
    logout: function(token) {
        const url = '/api/logout/';
        return get(url, token);
    },
}

export default UserAPI;