// src/routes/ErrorPage.js
import React from "react";
import { useNavigate } from "react-router-dom";

const ErrorPage = (error = "") => {
  const navigate = useNavigate();

  return (
    <div style={{ textAlign: "center", padding: "50px" }}>
      <h1>Oops! Page Not Found</h1>
      <p>Sorry, the page you're looking for doesn't exist.</p>
      <button onClick={() => navigate(-1)} style={{ margin: "10px" }}>
        Go Back
      </button>
      <button onClick={() => navigate("/")} style={{ margin: "10px" }}>
        Go to Home Page
      </button>
    </div>
  );
};

export default ErrorPage;
