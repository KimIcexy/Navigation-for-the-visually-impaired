import { post } from './generic';

const FaceAPI = {
    valid: function(data, token) {
        const url = '/face/valid/';
        return post(url, data, token);
    },
    register: function(data, token) {
        const url = '/face/register/';
        return post(url, data, token);
    }
}