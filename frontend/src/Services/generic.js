import axios from "axios";

export const configToken = function (token) {
    return {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }
}

export const get = function (url, token) {
    return new Promise<{ data }>((resolve, reject) =>
    axios
      .get(url, configToken(token))
      .then((res) => {
        // return data
        return resolve({ data: res.data });
      })
      .catch((err) => {
        // return err message
        if (!err.response) return reject(err.message);
        return reject(err.response.data.message);
      })
  );
};