import axios from "axios";
import { BACKEND_URL } from '@env'

const baseURL = BACKEND_URL

export const configToken = function (token) {
    return {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }
}

export const get = function (url, token) {
    console.log(baseURL + url)
    return new Promise((resolve, reject) =>
    axios
      .get(baseURL + url, configToken(token))
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

export const post = function (url, data, token) {
  console.log(baseURL + url)
  return new Promise((resolve, reject) =>
    axios
      .post(baseURL + url, data, configToken(token))
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

export const put = function (url, data, token) {
  console.log(baseURL + url)
  return new Promise((resolve, reject) =>
    axios
      .put(baseURL + url, data, configToken(token))
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

export const patch = function (url, data, token) {
  console.log(baseURL + url)
  return new Promise((resolve, reject) =>
    axios
      .patch(baseURL + url, data, configToken(token))
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

export const delele = function (url, token) {
  console.log(baseURL + url)
  return new Promise((resolve, reject) =>
    axios
      .delete(baseURL + url, configToken(token))
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