import { post, postForm } from './generic';

const FaceAPI = {
    valid: function(data, token) {
        const url = '/api/face/valid/';
        return postForm(url, data, token);
    },
    register: function(data, token) {
        const url = '/api/face/register/';
        return postForm(url, data, token);
    }
}

export default FaceAPI;