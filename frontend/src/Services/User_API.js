import { get, post, postForm } from './generic'

const UserAPI = {
    login: function(data) {
        const url = '/api/user/login/';
        return post(url, data, "");
    },
    loginWithFace: function(data) {
        const url = `/api/user/login/face/`;
        return postForm(url, data, "");
    },
    register: function(data) {
        const url = '/api/user/register/';
        return post(url, data, "");
    },
    logout: function(token) {
        const url = '/api/user/logout/';
        return get(url, token);
    },
}

export default UserAPI;