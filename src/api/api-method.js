import axios from "axios";

const IP_URL = "http://10.25.15.102:8000"; // Your IP address
const LOCAL_URL = "http://127.0.0.1:8000"; // Local URL
const LOCALHOST_URL = "http://localhost:8000"; // Localhost URL

async function fetchWithFallback(datapath, options = {}, method = "GET") {
    const urls = [LOCALHOST_URL, LOCAL_URL, IP_URL];

    // Check if datapath contains "/user"
    if (!datapath.includes("/user")) {
        try {
            const response = await axios({
                url: datapath
                    .replace(LOCALHOST_URL, IP_URL)
                    .replace(LOCAL_URL, IP_URL),
                method: method,
                ...options,
                timeout: 5000,
            });
            return response.data;
        } catch (error) {
            console.error("Error fetching data from IP_URL:", error);
        }
    }

    // Try each URL in sequence
    for (const baseUrl of urls) {
        try {
            // Replace the base URL part of the path
            const currentPath = datapath
                .replace(LOCALHOST_URL, baseUrl)
                .replace(LOCAL_URL, baseUrl);

            const response = await axios({
                url: currentPath,
                method: method,
                ...options,
                // Add timeout to prevent hanging
                timeout: 5000,
            });

            return response.data;
        } catch (error) {}
    }
}

export async function getData(datapath) {
    return await fetchWithFallback(datapath);
}

export async function getDataDynamic(datapath, token = null) {
    const config = token
        ? {
              headers: {
                  "Content-Type": "application/json",
                  Authorization: `Bearer ${token}`,
              },
          }
        : {};
    return await fetchWithFallback(datapath, config);
}

export async function fetchUserDetails(token = null) {
    const config = token
        ? {
              headers: {
                  Authorization: `Bearer ${token}`,
              },
          }
        : {};
    return await fetchWithFallback(
        "http://localhost:8000/researcher/researcher/auto_login",
        config,
        "POST"
    );
}

export async function postData(datapath, header, data) {
    return await fetchWithFallback(
        datapath,
        {
            data: data,
            headers: header,
        },
        "POST"
    );
}

export async function postData2(datapath, data, config) {
    return await fetchWithFallback(
        datapath,
        {
            data: data,
            ...config,
        },
        "POST"
    );
}

export async function putData(datapath, header, data) {
    return await fetchWithFallback(
        datapath,
        {
            data: data,
            headers: {
                authorization: `${header}`,
            },
        },
        "PUT"
    );
}

export async function patchData(datapath, header, data) {
    return await fetchWithFallback(
        datapath,
        {
            data: data,
            headers: {
                authorization: `${header}`,
            },
        },
        "PATCH"
    );
}

export async function getImgData(datapath) {
    try {
        const response = await fetchWithFallback(datapath, {
            responseType: "blob",
        });
        return URL.createObjectURL(response);
    } catch (error) {
        console.error("Error fetching image data:", error);
        throw error;
    }
}
