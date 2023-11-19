import { get, post } from './generic'

const UserAPI = {
    login: function(data) {
        const url = '/api/login/';
        return post(url, data, "");
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