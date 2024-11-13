import React, { useState } from "react";
import axios from "axios";
import { postData } from "api/api-method";

const LoginComp = () => {
  const [user, setUser] = useState("");
  const [pw, setPw] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new URLSearchParams();
    formData.append("username", "admintest123@gmail.com");
    formData.append("password", "1212312121");
    console.log(formData);
    try {
      const response = await postData(
        "http://127.0.0.1:8000/token",

        {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        formData.toString()
      );
      if (response?.access_token) {
        localStorage.setItem("token", response.access_token);
      }
      console.log("Request submitted successfully:", response.access_token);
      console.log(response);
    } catch (error) {
      console.error("Error submitting request:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>login</h3>
      <div>
        <label>Username:</label>
        <input
          type="text"
          value={"user"}
          onChange={(e) => setUser(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Password:</label>
        <input
          type="password"
          value={"pw"}
          onChange={(e) => setPw(e.target.value)}
          required
        />
      </div>
      <button type="submit">Submit</button>
    </form>
  );
};

export default LoginComp;
