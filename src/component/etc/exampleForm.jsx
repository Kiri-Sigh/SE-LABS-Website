import React, { useState } from "react";
import axios from "axios";
import { postData, postData2 } from "api/api-method"; // Assuming you have this utility function

const MyFormComponent = () => {
  const [title2, setTitle] = useState("a");
  const [body2, setDescription] = useState("ab");
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Create FormData object
    const formData = new FormData();
    // formData.append("title", title);
    console.log(body2);

    // formData.append("news", body);
    console.log(file);
    const news = {
      title: title2,
      body: body2,
      related_laboratory: {
        LID: "1e53d026-017a-4635-8a32-073e1794b5cf",
        related_research: {
          RID: "3b8be3a4-06cf-4355-b6a5-b27de60782fb",
        },
      },
    };
    // Construct the related laboratory and research object
    formData.append("news", JSON.stringify(news));
    if (file) {
      formData.append("image", file);
    }
    for (let [key, value] of formData.entries()) {
      console.log(key, value);
    }

    const relatedLaboratory = {
      LID: "1e53d026-017a-4635-8a32-073e1794b5cf",
      related_research: {
        RID: "3b8be3a4-06cf-4355-b6a5-b27de60782fb",
      },
    };

    // Get the token from localStorage
    const token = localStorage.getItem("token");
    if (token) {
      console.log(formData);
      // formData.append("related_laboratory", JSON.stringify(relatedLaboratory));

      // Construct request configuration with Authorization header
      const config = {
        headers: {
          "Content-Type": "multipart/form-data", // Correct MIME type for file uploads
          Authorization: `Bearer ${token}`, // Add the token
        },
      };
      // Send the form data using your postData function
      try {
        const response = await postData2(
          "http://127.0.0.1:8000/researcher/news?research_id=3b8be3a4-06cf-4355-b6a5-b27de60782fb", // URL for the API endpoint
          formData, // The formData as body of the request
          config // Configuration with headers
        );
        console.log("File uploaded successfully", response.data);
      } catch (error) {
        console.error("Error uploading file:", error);
      }
    } else {
      console.log("No token found");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h4>Form to Submit News</h4>
      <div>
        <label>Title:</label>
        <input
          type="text"
          value={title2}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Description:</label>
        <textarea
          value={body2}
          onChange={(e) => setDescription(e.target.value)}
          required
        />
      </div>
      <div>
        <label>File:</label>
        <input type="file" onChange={handleFileChange} required />
      </div>
      <button type="submit">Submit</button>
    </form>
  );
};

export default MyFormComponent;
