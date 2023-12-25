import { postForm } from "./generic";

const NavigateAPI = {
    navigate: function(data, token) {
        const url = '/api/navigate/';
        return postForm(url, data, token);
    }
}

export default NavigateAPI;