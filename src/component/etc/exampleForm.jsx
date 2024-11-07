import React, { useState } from "react";
import axios from "axios";
import { postData } from "api/api-method";

const MyFormComponent = () => {
  const [title, setTitle] = useState("a");
  const [body, setDescription] = useState("ab");
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Create FormData object
    const formData = new FormData();
    formData.append("title", title);
    formData.append("body", body);
    if (file) {
      formData.append("file", file, file.name);
    }
    formData.append("related_laboratory", {
      LID: null,
      related_research: {
        RID: "2a7502f6-7101-4fea-a259-2d1aa65f6155",
      },
    });
    console.log(localStorage.getItem("token"));
    try {
      const response = await postData(
        "http://127.0.0.1:8000/researcher/news?research_id=2a7502f6-7101-4fea-a259-2d1aa65f6155",

        {
          "Content-Type": "multipart/form-data",
          Authorization: localStorage.getItem("token"), // replace with your actual token if needed
        },
        formData
      );
      console.log("File uploaded successfully", response.data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h4>form to news</h4>
      <div>
        <label>Title:</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Description:</label>
        <textarea
          value={body}
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
