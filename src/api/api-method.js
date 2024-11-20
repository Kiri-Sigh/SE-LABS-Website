import axios from "axios";

export async function getData(datapath) {
  const response = await axios.get(datapath);
  console.log(datapath);

  return response.data;
}
export async function getDataAndHeader(datapath, header) {
  const response = await axios.get(datapath, {
    headers: {
      authorization: `${header}`,
    },
  });
  console.log(response.data);
  return response.data;
}

export async function getDataDynamic(datapath, token = null) {
  const config = token
    ? {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`, // Add the token
        },
      }
    : {};
  const response = await axios.get(datapath, config);
  return response.data;
}
export async function fetchUserDetails(token = null) {
  const config = token
    ? {
        headers: {
          Authorization: `Bearer ${token}`, // Add the token
        },
      }
    : {};
  const response = await axios.post(
    "http://127.0.0.1:8000/researcher/researcher/auto_login",
    {},
    config
  );
  return response.data;
}

export async function postData(datapath, header, data) {
  const response = await axios.post(datapath, data, header);
  return response.data;
}
export async function postData2(datapath, data, config) {
  try {
    const response = await axios.post(datapath, data, config); // Send request with config
    return response.data;
  } catch (error) {
    throw error; // Handle error appropriately
  }
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

export async function getImgData(datapath) {
  try {
    const response = await axios.get(datapath, { responseType: "blob" });
    return URL.createObjectURL(response.data);
  } catch (error) {
    console.error("Error fetching image data:", error);
    throw error;
  }
}
