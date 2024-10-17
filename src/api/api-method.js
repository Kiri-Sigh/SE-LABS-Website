import axios from "axios";

export async function getData(datapath) {
  const response = await axios.get(datapath);
  return response.data;
}
export async function getDataAndHeader(datapath, header) {
  const response = await axios.get(datapath, {
    headers: {
      authorization: `${header}`,
    },
  });
  return response.data;
}

export async function postData(datapath, header, data) {
  const response = await axios.post(datapath, data, {
    headers: {
      authorization: `${header}`,
    },
  });
  return response.data;
}
export async function putData(datapath, header, data) {
  const response = await axios.put(datapath, data, {
    headers: {
      authorization: `${header}`,
    },
  });
  return response.data;
}

export async function patchData(datapath, header, data) {
  const response = await axios.patch(datapath, data, {
    headers: {
      authorization: `${header}`,
    },
  });
  return response.data;
}
