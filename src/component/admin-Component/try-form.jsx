import React, { useState } from "react";
import axios from "axios";

const DynamicForm = ({ frame }) => {
  const [formData, setFormData] = useState({});
  const [files, setFiles] = useState({});

  const handleInputChange = (key, value) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };

  const handleFileChange = (key, file) => {
    setFiles((prev) => ({ ...prev, [key]: file }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    let url = frame.url || "http://127.0.0.1:8000";
    const formBody = new FormData();
    const method = frame.type || "post";

    if (frame.param) {
      const queryParams = frame.param
        .map((param) => {
          if (param.key) {
            const valueObject = Object.fromEntries(
              Object.entries(param).filter(([key]) => key !== "key")
            );
            const value = JSON.stringify(
              Object.fromEntries(
                Object.entries(valueObject).map(([key]) => [
                  key,
                  formData[key] || "",
                ])
              )
            );
            return `${param.key}=${encodeURIComponent(value)}`;
          } else {
            return Object.entries(param)
              .map(
                ([key]) => `${key}=${encodeURIComponent(formData[key] || "")}`
              )
              .join("&");
          }
        })
        .join("&");

      if (queryParams) url += `?${queryParams}`;
    }

    if (frame.body) {
      frame.body.forEach((bodyField) => {
        if (bodyField.key) {
          const valueObject = Object.fromEntries(
            Object.entries(bodyField).filter(([key]) => key !== "key")
          );
          const bodyObject = {
            ...Object.fromEntries(
              Object.entries(valueObject).map(([key, type]) => [
                key,
                formData[key] || "",
              ])
            ),
          };
          formBody.append(bodyField.key, JSON.stringify(bodyObject));
        } else {
          Object.entries(bodyField).forEach(([key, type]) => {
            if (type === "file" && files[key]) {
              formBody.append(key, files[key]);
            } else if (formData[key] !== undefined) {
              formBody.append(key, formData[key]);
            }
          });
        }
      });
    }

    const token = localStorage.getItem("token");
    const config = {
      headers: {
        "Content-Type": frame.body ? "multipart/form-data" : "application/json",
        Authorization: `Bearer ${token}`,
      },
    };

    try {
      let response;
      switch (method) {
        case "post":
          response = await axios.post(url, formBody, config);
          break;
        case "patch":
          response = await axios.patch(url, formBody, config);
          break;
        case "put":
          response = await axios.put(url, formBody, config);
          break;
        case "delete":
          response = await axios.delete(url, config);
          break;
        default:
          console.error("Unsupported method:", method);
          return;
      }

      console.log("Success:", response.data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const renderFields = () => {
    const fields = [];

    if (frame.param) {
      frame.param.forEach((param) => {
        if (param.key) {
          const valueObject = Object.fromEntries(
            Object.entries(param).filter(([key]) => key !== "key")
          );
          Object.keys(valueObject).forEach((fieldKey) => {
            fields.push(
              <div key={`${param.key}-${fieldKey}`}>
                <label>{`${param.key} - ${fieldKey}`}</label>
                <input
                  type="text"
                  value={formData[fieldKey] || ""}
                  onChange={(e) => handleInputChange(fieldKey, e.target.value)}
                />
              </div>
            );
          });
        } else {
          Object.entries(param).forEach(([key, type]) => {
            fields.push(
              <div key={key}>
                <label>{key}</label>
                {type === "checkbox" ? (
                  <input
                    type="checkbox"
                    checked={formData[key] || false}
                    onChange={(e) => handleInputChange(key, e.target.checked)}
                  />
                ) : (
                  <input
                    type={type === "text" ? "text" : type}
                    value={formData[key] || ""}
                    onChange={(e) => handleInputChange(key, e.target.value)}
                  />
                )}
              </div>
            );
          });
        }
      });
    }

    if (frame.body) {
      frame.body.forEach((bodyField) => {
        Object.entries(bodyField).forEach(([key, type]) => {
          fields.push(
            <div key={key}>
              <label>{key}</label>
              {type === "checkbox" ? (
                <input
                  type="checkbox"
                  checked={formData[key] || false}
                  onChange={(e) => handleInputChange(key, e.target.checked)}
                />
              ) : type === "file" ? (
                <input
                  type="file"
                  onChange={(e) => handleFileChange(key, e.target.files[0])}
                />
              ) : (
                <input
                  type={type}
                  value={formData[key] || ""}
                  onChange={(e) => handleInputChange(key, e.target.value)}
                />
              )}
            </div>
          );
        });
      });
    }

    return fields;
  };

  return (
    <form onSubmit={handleSubmit}>
      <h4>Dynamic Form</h4>
      {renderFields()}
      <button type="submit">Submit</button>
    </form>
  );
};

export default DynamicForm;
