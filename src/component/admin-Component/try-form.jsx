// import React, { useState } from "react";
// import axios from "axios";

// const DynamicForm = ({ frame }) => {
//   const [formData, setFormData] = useState({});
//   const [files, setFiles] = useState({});

//   const handleInputChange = (key, value) => {
//     setFormData((prev) => ({ ...prev, [key]: value }));
//   };

//   const handleFileChange = (key, file) => {
//     setFiles((prev) => ({ ...prev, [key]: file }));
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     let url = frame.url || "http://127.0.0.1:8000";
//     const formBody = new FormData();
//     const method = frame.type || "post";

//     if (frame.param) {
//       const queryParams = frame.param
//         .map((param) =>
//           Object.entries(param)
//             .map(([key]) => `${key}=${encodeURIComponent(formData[key] || "")}`)
//             .join("&")
//         )
//         .join("&");

//       if (queryParams) url += `?${queryParams}`;
//     }

//     if (frame.body) {
//       frame.body.forEach((bodyField) => {
//         if (bodyField.key) {
//           const valueObject = Object.fromEntries(
//             Object.entries(bodyField).filter(([key]) => key !== "key")
//           );

//           const bodyObject = {
//             ...Object.fromEntries(
//               Object.entries(valueObject).map(([key]) => [
//                 key,
//                 formData[key] || "",
//               ])
//             ),
//           };

//           // Handle related_laboratory logic
//           if (bodyField.related_laboratory) {
//             const { research_id, laboratory_id } = formData;

//             if (laboratory_id) {
//               bodyObject.related_laboratory = {
//                 LID: laboratory_id,
//                 related_research: research_id ? { RID: research_id } : null,
//               };
//             } else {
//               bodyObject.related_laboratory = null;
//             }
//           }
//           console.log(bodyObject);
//           formBody.append(bodyField.key, JSON.stringify(bodyObject));
//         } else {
//           Object.entries(bodyField).forEach(([key, type]) => {
//             if (type === "file" && files[key]) {
//               formBody.append(key, files[key]);
//             } else if (formData[key] !== undefined) {
//               formBody.append(key, formData[key]);
//             }
//           });
//         }
//       });
//     }

//     const token = localStorage.getItem("token");
//     const config = {
//       headers: {
//         "Content-Type": frame.body ? "multipart/form-data" : "application/json",
//         Authorization: `Bearer ${token}`,
//       },
//     };

//     try {
//       let response;
//       switch (method) {
//         case "post":
//           response = await axios.post(url, formBody, config);
//           break;
//         case "patch":
//           response = await axios.patch(url, formBody, config);
//           break;
//         case "put":
//           response = await axios.put(url, formBody, config);
//           break;
//         case "delete":
//           response = await axios.delete(url, config);
//           break;
//         default:
//           console.error("Unsupported method:", method);
//           return;
//       }

//       console.log("Success:", response.data);
//     } catch (error) {
//       console.error("Error:", error);
//     }
//   };

//   const renderFields = () => {
//     const fields = [];

//     // Render fields from frame.param
//     if (frame.param) {
//       frame.param.forEach((param) => {
//         Object.entries(param).forEach(([key, type]) => {
//           fields.push(
//             <div key={key}>
//               <label>{key}</label>
//               <input
//                 type={type}
//                 value={type === "checkbox" ? false : formData[key] || ""}
//                 onChange={(e) => handleInputChange(key, e.target.value)}
//               />
//             </div>
//           );
//         });
//       });
//     }

//     // Render fields from frame.body
//     if (frame.body) {
//       frame.body.forEach((bodyField) => {
//         if (bodyField.key) {
//           const valueObject = Object.fromEntries(
//             Object.entries(bodyField).filter(([key]) => key !== "key")
//           );
//           Object.keys(valueObject).forEach((key) => {
//             fields.push(
//               <>
//                 {valueObject[key] === "huh" ? (
//                   <></>
//                 ) : (
//                   <div key={key}>
//                     <label>{key}</label>
//                     <input
//                       type={
//                         valueObject[key] === "textArea" ? "textarea" : "text"
//                       }
//                       value={formData[key] || ""}
//                       onChange={(e) => handleInputChange(key, e.target.value)}
//                     />
//                   </div>
//                 )}
//               </>
//             );
//           });
//         } else {
//           Object.entries(bodyField).forEach(([key, type]) => {
//             fields.push(
//               <div key={key}>
//                 <label>{key}</label>
//                 {type === "file" ? (
//                   <input
//                     type="file"
//                     onChange={(e) => handleFileChange(key, e.target.files[0])}
//                   />
//                 ) : type === "huh" ? (
//                   <br />
//                 ) : (
//                   <input
//                     type={type}
//                     value={formData[key] || ""}
//                     onChange={(e) => handleInputChange(key, e.target.value)}
//                   />
//                 )}
//               </div>
//             );
//           });
//         }
//       });
//     }

//     return fields;
//   };

//   return (
//     <form onSubmit={handleSubmit}>
//       <h4>Dynamic Form</h4>
//       {renderFields()}
//       <button type="submit">Submit</button>
//     </form>
//   );
// };

// export default DynamicForm;
import React, { useState, useEffect } from "react";
import axios from "axios";
import { submitFrame } from "./Modal/input/frame";

const DynamicForm = ({ frame, data = null, send = null, type = null }) => {
  const [formData, setFormData] = useState({});
  const [files, setFiles] = useState({});

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

    if (frame.param) {
      const queryParams = frame.param
        .map((param) =>
          Object.entries(param)
            .map(([key]) => `${key}=${encodeURIComponent(formData[key] || "")}`)
            .join("&")
        )
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
      //hereif (send === "Admin" || send === "LeadResearcher") {
      if (send === null) return;
      const commitData = await getCommitData(type);

      // After fetching commit data, patch if necessary
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

        // Send patch request
        await axios.patch(patchUrl, patchData, {
          params: patchParam,
          headers: config.headers,
        });
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

      // Filter commit data based on NID (News ID) or EID (Event ID)
      const commitData =
        type === "event"
          ? response.data.find((item) => item.event_id === formData.event_id)
          : response.data.find((item) => item.news_id === formData.news_id);

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
          fields.push(
            <div key={key}>
              <label>{key}</label>
              <input
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
              <div key={key}>
                <label>{key}</label>
                <input
                  type={valueObject[key] === "textArea" ? "textarea" : "text"}
                  value={formData[key] || ""}
                  onChange={(e) => handleInputChange(key, e.target.value)}
                />
              </div>
            );
          });
        } else {
          Object.entries(bodyField).forEach(([key, type]) => {
            fields.push(
              <div key={key}>
                <label>{key}</label>
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
      <h4>Dynamic Form</h4>
      {renderFields()}
      <button type="submit">Submit</button>
    </form>
  );
};

export default DynamicForm;
