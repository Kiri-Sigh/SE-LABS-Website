import axios from "axios";
import { submitFrame } from "./Modal/input/frame";
import { useEffect, useState } from "react";

const DynamicForm = ({ frame, data = null, type = null }) => {
  const [formData, setFormData] = useState({});
  const [files, setFiles] = useState({});
  console.log("DynamicForm", type);
  // Initialize formData with inherited data
  useEffect(() => {
    if (data) {
      setFormData(data);
    }
  }, [data]);

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

    // Construct queryParams for URL if frame.param exists
    if (frame.param) {
      const queryParams = frame.param
        .map((param) => {
          if (param.key) {
            // Convert object-like values to JSON strings
            const valueObject = Object.fromEntries(
              Object.entries(param).filter(([key]) => key !== "key")
            );
            const value = JSON.stringify(
              Object.fromEntries(
                Object.entries(valueObject).map(([key, type]) => [
                  key,
                  formData[key] || "",
                ])
              )
            );
            return `${param.key}=${encodeURIComponent(value)}`;
          }

          return Object.keys(param)
            .map((key) => {
              if (formData[key]) {
                return `${key}=${encodeURIComponent(formData[key] || "")}`;
              } else {
                return "";
              }
            })
            .join("&");
        })
        .join("&");
      if (queryParams) url += `?${queryParams}`;
    }
    console.log(url);
    // Append form data to FormData object from frame.body
    if (frame.body) {
      frame.body.forEach((bodyField) => {
        if (bodyField.key) {
          const valueObject = Object.fromEntries(
            Object.entries(bodyField).filter(([key]) => key !== "key")
          );

          const bodyObject = {
            ...Object.fromEntries(
              Object.entries(valueObject).map(([key]) => [
                key,
                formData[key] || "",
              ])
            ),
          };

          // Handle related_laboratory logic
          if (bodyField.related_laboratory) {
            const { research_id, laboratory_id } = formData;

            if (laboratory_id) {
              bodyObject.related_laboratory = {
                LID: laboratory_id,
                related_research: research_id ? { RID: research_id } : null,
              };
            } else {
              bodyObject.related_laboratory = null;
            }
          }

          formBody.append(bodyField.key, JSON.stringify(bodyObject));
        } else {
          // For fields that are not related to keys, append to FormData
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
      // Dynamically handle request methods (POST, PATCH, PUT, DELETE)
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
      console.log("wat??", type);

      console.log("Success:", response.data);
      if (response.status === 200) {
        console.log("wat");
        if (type !== null) {
          const commitData = await getCommitData(type);
          console.log("wat2");

          if (commitData) {
            const patchData = {
              ...commitData,
              is_approved: true,
            };
            const patchUrl =
              type === "event"
                ? submitFrame.submitEvent.url
                : submitFrame.submitNews.url;
            const patchParam =
              type === "event"
                ? { event_id: commitData.event_id }
                : { news_id: commitData.news_id };

            await axios.patch(
              `${patchUrl}/${patchUrl}`,
              {},
              {
                params: patchParam,
                headers: config.headers,
              }
            );
          }
        }
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const getCommitData = async (type) => {
    const path =
      type === "event"
        ? `http://127.0.0.1:8000/lead_researcher/event/commit`
        : `http://127.0.0.1:8000/lead_researcher/news/commit`;

    try {
      const response = await axios.get(path, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      const commitData =
        type === "event"
          ? response.data.find((item) => item.event_id === formData.event_id)
          : response.data.find((item) => item.news_id === formData.news_id);
      console.log(commitData);
      return commitData;
    } catch (error) {
      console.error("Error fetching commit data:", error);
    }
  };

  const renderFields = () => {
    const fields = [];

    // Render fields from frame.param
    if (frame.param) {
      frame.param.forEach((param) => {
        Object.entries(param).forEach(([key, type]) => {
          if (key === "body") {
            fields.push(
              <div key={key} className="my-2">
                <label className="mr-2">{key}</label>
                <textarea
                  value={formData[key] || ""}
                  onChange={(e) => handleInputChange(key, e.target.value)}
                  onInput={(e) => {
                    e.target.style.height = "auto"; // Reset the height to auto before expanding
                    e.target.style.height = `${e.target.scrollHeight}px`; // Set the height to the scroll height
                  }}
                  className="resize-none w-full max-h-40 border-2 border-gray-200 hover:border-black transition-all duration-300"
                />
              </div>
            );
          } else {
            // For regular fields, render an input element
            fields.push(
              <div key={key} className="my-2">
                <label className="mr-2">{key}</label>
                <input
                  className={`border-2 border-gray-200 hover:border-black transition-all duration-300 ${
                    type !== "checkbox" ? "w-full" : ""
                  }`}
                  type={type}
                  value={
                    type === "checkbox"
                      ? formData[key] || false
                      : formData[key] || ""
                  }
                  onChange={(e) =>
                    handleInputChange(
                      key,
                      type === "checkbox" ? e.target.checked : e.target.value
                    )
                  }
                />
              </div>
            );
          }
        });
      });
    }

    // Render fields from frame.body
    if (frame.body) {
      frame.body.forEach((bodyField) => {
        if (bodyField.key) {
          const valueObject = Object.fromEntries(
            Object.entries(bodyField).filter(([key]) => key !== "key")
          );
          Object.keys(valueObject).forEach((key) => {
            fields.push(
              <div key={key} className="my-2">
                <label className="mr-2">{key}</label>
                <textarea
                  value={formData[key] || ""}
                  onChange={(e) => handleInputChange(key, e.target.value)}
                  onInput={(e) => {
                    e.target.style.height = "auto"; // Reset the height to auto before expanding
                    e.target.style.height = `${e.target.scrollHeight}px`; // Set the height to the scroll height
                  }}
                  className="resize-none w-full max-h-40 border-2 border-gray-200 hover:border-black transition-all duration-300"
                />
              </div>
            );
          });
        } else {
          Object.entries(bodyField).forEach(([key, type]) => {
            fields.push(
              <div key={key} className="my-4">
                <label className="mr-2">{key}</label>
                {type === "file" ? (
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
        }
      });
    }

    return fields;
  };

  return (
    <form onSubmit={handleSubmit}>
      {renderFields()}
      <button
        type="submit"
        className="bg-green-300 px-2 py-1 rounded-full border-2 border-transparent hover:border-green-700 transition-all ease-linear"
      >
        Submit
      </button>
    </form>
  );
};

export default DynamicForm;

// import React, { useState } from "react";
// import axios from "axios";

// const DynamicForm = ({ frame }) => {
//   const [formData, setFormData] = useState({});
//   const [files, setFiles] = useState({});

//   // Handle text and textarea input changes
//   const handleInputChange = (key, value) => {
//     setFormData((prev) => ({ ...prev, [key]: value }));
//   };

//   // Handle file input changes
//   const handleFileChange = (key, file) => {
//     setFiles((prev) => ({ ...prev, [key]: file }));
//   };

//   // Handle form submission
//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     let url = frame.url || "http://127.0.0.1:8000";
//     const formBody = new FormData();

//     // Build query parameters
//     if (frame.param) {
//       const queryParams = frame.param
//         .map((param) => {
//           if (param.key) {
//             // Convert object-like values to JSON strings
//             const valueObject = Object.fromEntries(
//               Object.entries(param).filter(([key]) => key !== "key")
//             );
//             const value = JSON.stringify(
//               Object.fromEntries(
//                 Object.entries(valueObject).map(([key, type]) => [
//                   key,
//                   formData[key] || "",
//                 ])
//               )
//             );
//             return `${param.key}=${encodeURIComponent(value)}`;
//           }
//           return Object.keys(param)
//             .map((key) => `${key}=${encodeURIComponent(formData[key] || "")}`)
//             .join("&");
//         })
//         .join("&");
//       url += `?${queryParams}`;
//     }

//     // Build body
//     if (frame.body) {
//       frame.body.forEach((bodyField) => {
//         if (bodyField.key) {
//           const valueObject = Object.fromEntries(
//             Object.entries(bodyField).filter(([key]) => key !== "key")
//           );

//           // Handle related_laboratory if defined
//           const relatedLaboratory =
//             valueObject.related_laboratory !== undefined
//               ? {
//                   LID: formData.LID || "",
//                   related_research: { RID: formData.RID || "" },
//                 }
//               : undefined;

//           const bodyObject = {
//             ...Object.fromEntries(
//               Object.entries(valueObject).map(([key, type]) => [
//                 key,
//                 formData[key] || "",
//               ])
//             ),
//             ...(relatedLaboratory
//               ? { related_laboratory: relatedLaboratory }
//               : {}),
//           };

//           formBody.append(bodyField.key, JSON.stringify(bodyObject));
//         } else {
//           Object.entries(bodyField).forEach(([key, type]) => {
//             if (type === "file" && files[key]) {
//               formBody.append(key, files[key]);
//             } else if (formData[key]) {
//               formBody.append(key, formData[key]);
//             }
//           });
//         }
//       });
//     }

//     const token = localStorage.getItem("token");

//     const config = {
//       headers: {
//         "Content-Type": "multipart/form-data",
//         Authorization: `Bearer ${token}`,
//       },
//     };

//     try {
//       const response =
//         frame.type === "post"
//           ? await axios.post(url, formBody, config)
//           : await axios.put(url, formBody, config);

//       console.log("Response:", response.data);
//       alert("Form submitted successfully!");
//       // Optionally reset form
//       setFormData({});
//       setFiles({});
//     } catch (error) {
//       console.error("Error submitting form:", error);
//       alert("Error submitting form. Please try again.");
//     }
//   };

//   // Render the dynamic fields
//   const renderFields = () => {
//     const fields = [];

//     // Render params
//     if (frame.param) {
//       frame.param.forEach((param) => {
//         if (param.key) {
//           const valueObject = Object.fromEntries(
//             Object.entries(param).filter(([key]) => key !== "key")
//           );
//           Object.keys(valueObject).forEach((fieldKey) => {
//             fields.push(
//               <div key={`${param.key}-${fieldKey}`} className="form-group">
//                 <label>{`${param.key} - ${fieldKey}:`}</label>
//                 <input
//                   type="text"
//                   value={formData[fieldKey] || ""}
//                   onChange={(e) => handleInputChange(fieldKey, e.target.value)}
//                 />
//               </div>
//             );
//           });
//         } else {
//           Object.entries(param).forEach(([key, type]) => {
//             fields.push(
//               <div key={key} className="form-group">
//                 <label>{key}:</label>
//                 <input
//                   type="text"
//                   value={formData[key] || ""}
//                   onChange={(e) => handleInputChange(key, e.target.value)}
//                 />
//               </div>
//             );
//           });
//         }
//       });
//     }

//     // Render body
//     if (frame.body) {
//       frame.body.forEach((bodyField) => {
//         if (bodyField.key) {
//           Object.entries(bodyField).forEach(([key, type]) => {
//             if (key !== "key") {
//               fields.push(
//                 <div key={key} className="form-group">
//                   <label>{key}:</label>
//                   {type === "textArea" ? (
//                     <textarea
//                       value={formData[key] || ""}
//                       onChange={(e) => handleInputChange(key, e.target.value)}
//                       required
//                     />
//                   ) : (
//                     <input
//                       type={type === "text" ? "text" : type}
//                       value={formData[key] || ""}
//                       onChange={(e) => handleInputChange(key, e.target.value)}
//                     />
//                   )}
//                 </div>
//               );
//             }
//           });
//         } else {
//           Object.entries(bodyField).forEach(([key, type]) => {
//             fields.push(
//               <div key={key} className="form-group">
//                 <label>{key}:</label>
//                 <input
//                   type={type === "file" ? "file" : "text"}
//                   onChange={(e) =>
//                     type === "file"
//                       ? handleFileChange(key, e.target.files[0])
//                       : handleInputChange(key, e.target.value)
//                   }
//                   required
//                 />
//               </div>
//             );
//           });
//         }
//       });
//     }

//     return fields;
//   };

//   return (
//     <form onSubmit={handleSubmit} className="dynamic-form">
//       <h4>Dynamic Form</h4>
//       {renderFields()}
//       <button type="submit">Submit</button>
//     </form>
//   );
// };

// export default DynamicForm;
