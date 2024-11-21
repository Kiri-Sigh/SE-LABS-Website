import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import editSlice, { editAction } from "store/edit-slice";

import ModalFrame2 from "../Modal-Frame-2";
import CloseButton from "../Close-Btn";
import DynamicForm from "component/admin-Component/try-form";
import { createFrame, deleteFrame, editFrame, submitFrame } from "./frame";
import DeepObjectViewer from "./etc/deppObjViewer";
import { patchApproval } from "api/custom-hooks";

export const modalFrameWorkButton = {
  createAdmin: {
    highestRole: "Admin",
    type: "create",
    choosable: ["laboratory", "event", "news", "research", "researcher"],
    url: "a",
  },
  editAdmin: {
    highestRole: "Admin",
    type: "edit",
    choosable: [
      "laboratory",
      "event",
      "news",
      "research",
      "researcher",
      "publication",
    ],
    url: "b",
  },
  deleteAdmin: {
    highestRole: "Admin",
    type: "delete",
    choosable: [
      "laboratory",
      "event",
      "news",
      "research",
      "researcher",
      "publication",
    ],
    url: "c",
  },
  createLead: {
    highestRole: "LeadResearcher",
    type: "create",
    choosable: ["event", "news", "research", "researcher"],
    url: "d",
  },
  deleteLead: {
    highestRole: "LeadResearcher",
    type: "delete",
    choosable: ["laboratory", "event", "news", "research", "researcher"],
    url: "e",
  },
  editLead: {
    highestRole: "LeadResearcher",
    type: "edit",
    choosable: [
      "laboratory",
      "event",
      "news",
      "research",
      "researcher",
      "publication",
    ],
    url: "f",
  },
  createResearcher: {
    highestRole: "Researcher",
    type: "create",
    choosable: ["event", "news"],
    url: "g",
  },
};
function NewsFormatData(obj) {
  const data = {
    news_id: obj.NID,
    body: obj.body,
    title: obj.title,
  };

  if (obj.related_laboratory && obj.related_laboratory.LID) {
    data.laboratory_id = obj.related_laboratory.LID;
  }

  if (obj.related_publication && obj.related_publication.PID) {
    data.publication_id = obj.related_publication.PID;
  }

  if (obj.related_research && obj.related_research.RID) {
    data.research_id = obj.related_research.RID;
  }

  return data;
}
function formatResearcherData(obj) {
  const data = {
    researcher_id: obj.UID,
    name: obj.name,
    position: obj.position,
    gmail: obj.gmail,
  };

  if (obj.related_laboratory && obj.related_laboratory.length > 0) {
    data.laboratory_id = obj.related_laboratory[0].LID;
  }

  return data;
}
function formatResearchData(obj) {
  const data = {
    research_id: obj.RID,
    body: obj.body,
    title: obj.title,
  };

  if (obj.related_laboratory && obj.related_laboratory.LID) {
    data.laboratory_id = obj.related_laboratory.LID;
  }

  return data;
}
function formatLaboratoryData(obj) {
  const data = {
    laboratory_id: obj.LID,
    body: obj.body,
    title: obj.title,
  };
  return data;
}
function formatPublicationData(obj) {
  const data = {
    PID: obj.PID,
    title: obj.title,
    body: obj.body,
    link: obj.link, // Always return link
  };

  return data;
}
function formatEventData(obj) {
  const data = {
    event_id: obj.EID, // Event ID
    title: obj.title, // Event title
    body: obj.body, // Event body
    status: obj.status, // Event status
    location: obj.location, // Event location
    start: obj.start, // Event start date
    end: obj.end, // Event end date
  };

  // Include related laboratories if they exist
  if (obj.related_laboratory && obj.related_laboratory.LID) {
    data.laboratory_id = obj.related_laboratory.LID; // LID from related laboratory
  }

  // If related research exists, include the RID field
  if (obj.related_research) {
    // Assuming `related_research` is an object containing the RID
    data.research_id = obj.related_research.RID || null; // RID from related research
  }

  // If related publication exists, include the PID field
  if (obj.related_publication) {
    // Assuming `related_publication` contains the PID
    data.publication_id = obj.related_publication.PID || null; // PID from related publication
  }

  return data;
}
function formatData(obj) {
  if (obj.UID) {
    // This is a Researcher
    return formatResearcherData(obj);
  } else if (obj.LID) {
    // This is a Laboratory
    return formatLaboratoryData(obj);
  } else if (obj.PID) {
    // This is a Publication
    return formatPublicationData(obj);
  } else if (obj.RID) {
    // This is a Publication
    return formatResearchData(obj);
  } else if (obj.EID) {
    // This is a Publication
    return formatEventData(obj);
  } else if (obj.NID) {
    // This is a Publication
    return NewsFormatData(obj);
  }

  return {}; // Default return if no known fields are found
}
const roleActions = {
  Admin: {
    Laboratory: (formMode) => (
      <div className="flex flex-row w-full justify-center rounded-full overflow-hidden">
        <button
          onClick={() => {
            formMode(createFrame.createLab);
          }}
          className="bg-green-300 px-2 py-1 w-full hover:bg-green-500 transition-all ease-linear"
        >
          Create New Lab
        </button>
        <button
          onClick={() => formMode(editFrame.editLab)}
          className="bg-yellow-300 px-2 py-1 w-full hover:bg-yellow-500 transition-all ease-linear"
        >
          Update Lab
        </button>
        <button
          onClick={() => formMode(deleteFrame.deleteLab)}
          className="bg-red-300 px-2 py-1 w-full hover:bg-red-500 transition-all ease-linear"
        >
          Delete Lab
        </button>
      </div>
    ),
    Research: (formMode) => (
      <div className="flex flex-row w-full justify-center rounded-full overflow-hidden">
        <button
          onClick={() => formMode(createFrame.createResearch)}
          className="bg-green-300 px-2 py-1 w-full hover:bg-green-500 transition-all ease-linear"
        >
          Create New Research
        </button>
        <br />
        <button
          onClick={() => formMode(editFrame.editResearch)}
          className="bg-yellow-300 px-2 py-1 w-full hover:bg-yellow-500 transition-all ease-linear"
        >
          Update Research
        </button>
        <br />
        <button
          onClick={() => formMode(deleteFrame.deleteLab)}
          className="bg-red-300 px-2 py-1 w-full hover:bg-red-500 transition-all ease-linear"
        >
          Delete Research
        </button>
      </div>
    ),
    Publication: (formMode) => (
      <div className="flex flex-row w-full justify-center rounded-full overflow-hidden">
        <button
          onClick={() => formMode(editFrame.editPublication)}
          className="bg-yellow-300 px-2 py-1 w-full hover:bg-yellow-500 transition-all ease-linear"
        >
          Update Publication
        </button>
        <br />
        <button
          onClick={() => formMode(deleteFrame.deletePublication)}
          className="bg-red-300 px-2 py-1 w-full hover:bg-red-500 transition-all ease-linear"
        >
          Delete Publication
        </button>
      </div>
    ),
    News: (formMode) => (
      <div className="flex flex-row w-full justify-center rounded-full overflow-hidden">
        <button
          onClick={() => {
            formMode(createFrame.createNews, "news");
          }}
          className="bg-green-300 px-2 py-1 w-full hover:bg-green-500 transition-all ease-linear"
        >
          Create New News
        </button>
        <br />
        <button
          onClick={() => {
            formMode(submitFrame.submitNews);
          }}
          className="bg-yellow-300 px-2 py-1 w-full hover:bg-yellow-500 transition-all ease-linear"
        >
          Commit News
        </button>
        <br />
        <button
          onClick={() => {
            formMode(deleteFrame.deleteNews);
          }}
          className="bg-red-300 px-2 py-1 w-full hover:bg-red-500 transition-all ease-linear"
        >
          Delete News
        </button>
      </div>
    ),
    Event: (formMode) => (
      <div className="flex flex-row w-full justify-center rounded-full overflow-hidden">
        <button
          onClick={() => formMode(createFrame.createEvent, "event")}
          className="bg-green-300 px-2 py-1 w-full hover:bg-green-500 transition-all ease-linear"
        >
          Create New Event
        </button>
        <button
          onClick={() => formMode(submitFrame.submitEvent)}
          className="bg-yellow-300 px-2 py-1 w-full hover:bg-yellow-500 transition-all ease-linear"
        >
          Commit Event
        </button>
        <button
          onClick={() => formMode(deleteFrame.deleteEvent)}
          className="bg-red-300 px-2 py-1 w-full hover:bg-red-500 transition-all ease-linear"
        >
          Delete Event
        </button>
      </div>
    ),
    Researcher: (formMode) => (
      <div className="flex flex-row w-full justify-center rounded-full overflow-hidden">
        <button
          onClick={() => formMode(createFrame.createPeople)}
          className="bg-green-300 px-2 py-1 w-full hover:bg-green-500 transition-all ease-linear"
        >
          Create Researcher
        </button>
        <br />
        <button
          onClick={() => formMode(editFrame.assignToResearch)}
          className="bg-yellow-300 px-2 py-1 w-full hover:bg-yellow-500 transition-all ease-linear"
        >
          assign to research
        </button>
        <br />
        <button
          onClick={() => formMode(editFrame.assignAsLeadR)}
          className="bg-orange-300 px-2 py-1 w-full hover:bg-orange-500 transition-all ease-linear"
        >
          assign as Lead Researcher
        </button>
        <br />
        <button
          onClick={() => formMode(deleteFrame.kickFromResearch)}
          className="bg-red-300 px-2 py-1 w-full hover:bg-red-500 transition-all ease-linear"
        >
          kick from research
        </button>
        <br />
        <button
          onClick={() => formMode(deleteFrame.removeLeadResearcher)}
          className="bg-gray-300 px-2 py-1 w-full hover:bg-gray-500 transition-all ease-linear"
        >
          remove as Lead Researcher
        </button>
      </div>
    ),
  },
  LeadResearcher: {
    Laboratory: (formMode) => (
      <div className="flex flex-row w-full justify-center rounded-full overflow-hidden">
        <button
          onClick={() => formMode(createFrame.createLab)}
          className="bg-green-300 px-2 py-1 w-full hover:bg-green-500 transition-all ease-linear"
        >
          Create New Lab
        </button>
        <br />
        <button
          onClick={() => formMode(editFrame.editLab)}
          className="bg-yellow-300 px-2 py-1 w-full hover:bg-yellow-500 transition-all ease-linear"
        >
          Update Lab
        </button>
        <button
          onClick={() => formMode(deleteFrame.deleteLab)}
          className="bg-red-300 px-2 py-1 w-full hover:bg-red-500 transition-all ease-linear"
        >
          <br />
          Delete Lab
        </button>
      </div>
    ),
    Research: (formMode) => (
      <div className="flex flex-row w-full justify-center rounded-full overflow-hidden">
        <button
          onClick={() => formMode(createFrame.createResearch)}
          className="bg-green-300 px-2 py-1 w-full hover:bg-green-500 transition-all ease-linear"
        >
          Create New Research
        </button>
        <button
          onClick={() => formMode(editFrame.editResearch)}
          className="bg-yellow-300 px-2 py-1 w-full hover:bg-yellow-500 transition-all ease-linear"
        >
          Update Research
        </button>
        <button
          onClick={() => formMode(deleteFrame.deleteResearch)}
          className="bg-red-300 px-2 py-1 w-full hover:bg-red-500 transition-all ease-linear"
        >
          Delete Research
        </button>
      </div>
    ),
    Publication: (formMode) => (
      <div className="flex flex-row w-full justify-center rounded-full overflow-hidden">
        <button
          onClick={() => formMode(editFrame.editPublication)}
          className="bg-yellow-300 px-2 py-1 w-full hover:bg-yellow-500 transition-all ease-linear"
        >
          Update Publication
        </button>
        <br />
        <button
          onClick={() => formMode(deleteFrame.deletePublication)}
          className="bg-red-300 px-2 py-1 w-full hover:bg-red-500 transition-all ease-linear"
        >
          Delete Publication
        </button>
        <br />
      </div>
    ),
    News: (formMode) => (
      <>
        <button onClick={() => formMode(createFrame.createNews, "news")}>
          Create News
        </button>
        <br />
        {/* <button onClick={() => formMode(submitFrame.submitNews)}>Commit News</button> */}
        <button onClick={() => formMode(deleteFrame.deleteNews)}>
          Delete News
        </button>
        <br />
      </>
    ),
    Event: (formMode) => (
      <>
        <br />
        <button onClick={() => formMode(createFrame.createEvent, "event")}>
          <br />
          Create Event
        </button>
        <br />
        {/* <button onClick={() => formMode(submitFrame.submitEvent)}>Commit Event</button> */}
        <button onClick={() => formMode(deleteFrame.deleteEvent)}>
          Delete Event
        </button>
        <br />
      </>
    ),
  },
  Researcher: {
    News: (formMode) => (
      <>
        <br />
        <button onClick={() => formMode(createFrame.createNews)}>
          Create News
        </button>
        <br />
      </>
    ),
    Event: (formMode) => (
      <>
        <br />
        <button onClick={() => formMode(createFrame.createEvent)}>
          Create Event
        </button>
        <br />
      </>
    ),
  },
};

function Modal2() {
  //   const [isDropped, setIsDropped] = useState(false);

  const [selectedOption, setSelectedOption] = useState(null); // Track selected option
  const [url, setUrl] = useState(""); // Track URL based on the selected option
  const [selectChoosableState, setSelectChoosableState] = useState(true);
  const dispatch = useDispatch();
  const isAdminPage = useSelector((state) => state.mainSlice.isAdminPage);
  const highestRole = useSelector((state) => state.mainSlice.highestRole);
  const adminData = useSelector((state) => state.mainSlice.adminData);
  const isSpecificOpen = useSelector((state) => state.editSlice.isSpecificOpen);
  const [type, ID, fullData] = useSelector(
    (state) => state.editSlice.specificTypeAndIDAndData
  );
  const [isDynamic, setIsDynamic] = useState(false);
  // const [formMode, setFormMode] = useState(false);
  const isOpen = useSelector((state) => state.editSlice.isOpen);
  const isCommit = useSelector((state) => state.editSlice.isCommit);
  const [formConfig, setFormConfig] = useState(null); // State to store form configuration
  const [formData, setFormData] = useState(null); // State to store form data
  const [type2, setType2] = useState(null); // State to store form data
  const [type3, setType3] = useState(null); // State to store form data

  const dataAfterCreate = useSelector(
    (state) => state.editSlice.dataAfterCreate
  ); //   const handleDropdownToggle = () => setIsDropped((prev) => !prev);
  console.log("isCommit", isCommit);
  const handleOptionSelect = (option) => {
    setSelectedOption(option); // Store the selected option
    const fetchedUrl = fetchRequiredData(highestRole, option, "url"); // Fetch URL based on selection
    setUrl(fetchedUrl); // Update the URL state
    dispatch(editAction.openModal()); // Open the modal
    setSelectChoosableState(
      fetchRequiredData(highestRole, option, "choosable")
    );
  };
  function RoleBasedActions({ role, entity, formMode }) {
    const actions = roleActions[role]?.[entity];

    return (
      <div>
        {actions ? actions((frame) => formMode(frame)) : "No actions available"}
      </div>
    );
  }
  const formMode = (frame, type) => {
    setFormConfig(frame); // Set the frame for the form
    console.log("fullD", fullData);
    if (fullData) setFormData(formatData(fullData));
    // Set the data for the form
    if (type) setType3(type);
    console.log("FormMode run");
  };
  const chooseTopicToMutate = () => {
    setIsDynamic(true);
    dispatch(editAction.openSpecificModal([null, null, null])); // Open the modal
  };
  const fetchRequiredData = (role, type, want) => {
    if (want === "url") {
      for (const key in modalFrameWorkButton) {
        const frame = modalFrameWorkButton[key];
        if (frame.highestRole === role && frame.type === type) {
          return frame.url; // Return URL if a match is found
        }
      }
    }
    if (want === "choosable") {
      for (const key in modalFrameWorkButton) {
        const frame = modalFrameWorkButton[key];
        if (frame.highestRole === role && frame.type === type) {
          return frame.choosable; // Return URL if a match is found
        }
      }
    }
    return "No URL found"; // Return a default message if no match
  };

  return (
    <>
      <div className="fixed-button-container">
        <button className="fixed-button" onClick={chooseTopicToMutate}>
          Edit...
        </button>
        {/* <button className="fixed-button" onClick={handleDropdownToggle}>
          Open Dropdown
        </button>
        {isDropped && isAdminPage && !selectedOption && (
          <div className={`overlay-dropdown ${isDropped ? "active" : ""}`}>
            <OverlayDD
              possiblePower={["create", "edit", "delete"]}
              close={setIsDropped}
              onSelect={handleOptionSelect} // Pass the selection handler
            />
          </div>
        )} */}
      </div>
      <ModalFrame2>
        <div className="flex justify-end">
          <CloseButton
            onClick={() => {
              dispatch(editAction.reset());
              setFormConfig(null);
              setFormData(null);
              dispatch(editAction.setTypeNull());
              setIsDynamic(false);
              dispatch(editAction.closeSpecificModal());
              setType3(null);
            }}
          />
        </div>
        {/* {!isCommit ? roleActions[highestRole]?.[type] : null}{" "} */}
        {isDynamic && (
          <React.Fragment>
            <div className="grid grid-cols-3 grid-rows-2 gap-0 mb-2 w-full">
              <button
                onClick={() => setType2("Laboratory")}
                className="py-4 bg-black text-white hover:bg-white hover:text-black transition-all ease-linear"
              >
                Laboratory
              </button>
              <button
                onClick={() => setType2("Research")}
                className="py-4 bg-black text-white hover:bg-white hover:text-black transition-all ease-linear"
              >
                Research
              </button>
              <button
                onClick={() => setType2("News")}
                className="py-4 bg-black text-white hover:bg-white hover:text-black transition-all ease-linear"
              >
                News
              </button>
              <button
                onClick={() => setType2("Event")}
                className="py-4 bg-black text-white hover:bg-white hover:text-black transition-all ease-linear"
              >
                Event
              </button>
              <button
                onClick={() => setType2("Publication")}
                className="py-4 bg-black text-white hover:bg-white hover:text-black transition-all ease-linear"
              >
                Publication
              </button>
              <button
                onClick={() => setType2("Researcher")}
                className="py-4 bg-black text-white hover:bg-white hover:text-black transition-all ease-linear"
              >
                Researcher
              </button>
            </div>
          </React.Fragment>
        )}
        {!isCommit && isDynamic && type2 && (
          <RoleBasedActions
            role={highestRole}
            entity={type2}
            formMode={formMode}
          />
        )}
        {!isCommit && !isDynamic && (
          <RoleBasedActions
            role={highestRole}
            entity={type}
            formMode={formMode}
          />
        )}
        {formConfig && !isCommit && (
          <DynamicForm frame={formConfig} data={formData} />
        )}
        {isCommit ? (
          <>
            <div>
              <strong>Type: </strong>
              {type ? type : "error"}
            </div>
            <br />
            {console.log(fullData)}
            <DeepObjectViewer data={fullData} />
            <div className="flex gap-5 py-5">
              <button
                onClick={() => patchApproval(fullData)}
                className="bg-green-300 px-2 py-1 rounded-full border-2 border-transparent hover:border-green-700 transition-all ease-linear"
              >
                Verify!
              </button>
              <button className="bg-red-300 px-2 py-1 rounded-full border-2 border-transparent hover:border-red-700 transition-all ease-linear">
                Reject..
              </button>
            </div>
          </>
        ) : null}
        {isOpen}
        {/* <CloseButton
          onClick={() => {
            dispatch(editAction.reset());
            setFormConfig(null);
            setFormData(null);
            dispatch(editAction.setTypeNull());
            setIsDynamic(false);
            dispatch(editAction.closeSpecificModal());
            setType3(null);
          }}
        /> */}
      </ModalFrame2>
    </>
  );
}

export default Modal2;
//wat da fak
