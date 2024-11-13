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

export async function getDataDynamic(datapath, header = null) {
  const config = header
    ? {
        headers: {
          authorization: `${header}`,
        },
      }
    : {};
  const response = await axios.get(datapath, config);
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
