import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import editSlice, { editAction } from "store/edit-slice";

import ModalFrame2 from "../Modal-Frame-2";
import CloseButton from "../Close-Btn";
import DynamicForm from "component/admin-Component/try-form";
import { createFrame, deleteFrame, editFrame, submitFrame } from "./frame";
import DeepObjectViewer from "./etc/deppObjViewer";

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
      <>
        <button
          onClick={() => {
            formMode(createFrame.createLab);
          }}
        >
          Create New Lab
        </button>
        <button onClick={() => formMode(editFrame.editLab)}>Update Lab</button>
        <button onClick={() => formMode(deleteFrame.deleteLab)}>
          Delete Lab
        </button>
      </>
    ),
    Research: (formMode) => (
      <>
        <button onClick={() => formMode(createFrame.createResearch)}>
          Create New Research
        </button>
        <br />
        <button onClick={() => formMode(editFrame.editResearch)}>
          Update Research
        </button>
        <br />
        <button onClick={() => formMode(deleteFrame.deleteLab)}>
          Delete Research
        </button>
      </>
    ),
    Publication: (formMode) => (
      <>
        <button onClick={() => formMode(editFrame.editPublication)}>
          Update Publication
        </button>
        <br />
        <button onClick={() => formMode(deleteFrame.deletePublication)}>
          Delete Publication
        </button>
      </>
    ),
    News: (formMode) => (
      <>
        <button onClick={() => formMode(createFrame.createNews, "A", "news")}>
          Create New News
        </button>
        <br />
        <button onClick={() => formMode(submitFrame.submitNews)}>
          Commit News
        </button>
        <br />
        <button onClick={() => formMode(deleteFrame.deleteNews)}>
          Delete News
        </button>
      </>
    ),
    Event: (formMode) => (
      <>
        <button onClick={() => formMode(createFrame.createEvent, "a", "event")}>
          Create New Event
        </button>
        <br />
        <button onClick={() => formMode(submitFrame.submitEvent)}>
          Commit Event
        </button>
        <br />
        <button onClick={() => formMode(deleteFrame.deleteEvent)}>
          Delete Event
        </button>
      </>
    ),
    Researcher: (formMode) => (
      <>
        <button onClick={() => formMode(createFrame.createPeople)}>
          Create Researcher
        </button>
        <br />
        <button onClick={() => formMode(editFrame.assignToResearch)}>
          assign to research
        </button>
        <br />
        <button onClick={() => formMode(editFrame.assignAsLeadR)}>
          assign as Lead Researcher
        </button>
        <br />
        <button onClick={() => formMode(deleteFrame.kickFromResearch)}>
          kick from research
        </button>
        <br />
        <button onClick={() => formMode(deleteFrame.removeLeadResearcher)}>
          remove as Lead Researcher
        </button>
      </>
    ),
  },
  LeadResearcher: {
    Laboratory: (formMode) => (
      <>
        <button onClick={() => formMode(createFrame.createLab)}>
          Create New Lab
        </button>
        <br />
        <button onClick={() => formMode(editFrame.editLab)}>Update Lab</button>
        <button onClick={() => formMode(deleteFrame.deleteLab)}>
          <br />
          Delete Lab
        </button>
      </>
    ),
    Research: (formMode) => (
      <>
        <button onClick={() => formMode(createFrame.createResearch)}>
          Create New Research
        </button>
        <br />
        <button onClick={() => formMode(editFrame.editResearch)}>
          Update Research
        </button>
        <br />
        <button onClick={() => formMode(deleteFrame.deleteResearch)}>
          Delete Research
        </button>
      </>
    ),
    Publication: (formMode) => (
      <>
        <button onClick={() => formMode(editFrame.editPublication)}>
          Update Publication
        </button>
        <br />
        <button onClick={() => formMode(deleteFrame.deletePublication)}>
          Delete Publication
        </button>
        <br />
      </>
    ),
    News: (formMode) => (
      <>
        <button onClick={() => formMode(createFrame.createNews, true, "news")}>
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
        <button
          onClick={() => formMode(createFrame.createEvent, true, "event")}
        >
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
  const formMode = (frame) => {
    setFormConfig(frame); // Set the frame for the form
    if (fullData) setFormData(formatData(fullData));
    // Set the data for the form
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
          Open Dropdown
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
        <h2>This is the modal content</h2>
        {/* {!isCommit ? roleActions[highestRole]?.[type] : null}{" "} */}
        {isDynamic && (
          <React.Fragment>
            <p>select</p>
            <br />
            <button onClick={() => setType2("Laboratory")}>Laboratory</button>
            <br />
            <button onClick={() => setType2("Research")}>Research</button>
            <br />
            <button onClick={() => setType2("News")}>News</button>
            <br />
            <button onClick={() => setType2("Event")}>Event</button>
            <br />
            <button onClick={() => setType2("Publication")}>Publication</button>
            <br />
            <button onClick={() => setType2("Researcher")}>Researcher</button>
            <br />
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
            <strong>type: </strong>
            {type ? type : "error"}
            <br />
            <DeepObjectViewer data={fullData} />
            <br />
            <button>commit!</button>
            <br /> <button>reject..</button>
            <br />
          </>
        ) : null}
        {isOpen}
        <CloseButton
          onClick={() => {
            dispatch(editAction.reset());
            setFormConfig(null);
            setFormData(null);
            dispatch(editAction.setTypeNull());
            setIsDynamic(false);
            dispatch(editAction.closeSpecificModal());
          }}
        />
      </ModalFrame2>
    </>
  );
}

export default Modal2;
