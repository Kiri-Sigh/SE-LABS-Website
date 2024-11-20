import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import OverlayDD from "./overlay-dropdown";
import Modal from "./Modal/Modal-Frame";
import OkBtn from "./Modal/OK-btn";
import DropDown from "./Modal/relate/dropdown";
import { editAction } from "store/edit-slice";
import CloseButton from "./Modal/Close-Btn";
import DynamicForm from "./try-form";
import { submitFrame } from "./Modal/input/frame";

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

function OverlayButton() {
  const [isDropped, setIsDropped] = useState(false);
  const [selectedOption, setSelectedOption] = useState(null); // Track selected option
  const [url, setUrl] = useState(""); // Track URL based on the selected option
  const [selectChoosableState, setSelectChoosableState] = useState(null);
  const dispatch = useDispatch();
  const isAdminPage = useSelector((state) => state.mainSlice.isAdminPage);
  const highestRole = useSelector((state) => state.mainSlice.highestRole);
  const adminData = useSelector((state) => state.mainSlice.adminData);

  const handleDropdownToggle = () => setIsDropped((prev) => !prev);

  const handleOptionSelect = (option) => {
    setSelectedOption(option); // Store the selected option
    const fetchedUrl = fetchRequiredData(highestRole, option, "url"); // Fetch URL based on selection
    setUrl(fetchedUrl); // Update the URL state
    dispatch(editAction.openModal()); // Open the modal
    setSelectChoosableState(
      fetchRequiredData(highestRole, option, "choosable")
    );
  };
  const chooseTopicToMutate = (type) => {
    let bigObj;
    if (type === "laboratory") {
    }
    let data = adminData;
    bigObj.append(data);
    return bigObj;
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
        <button className="fixed-button" onClick={handleDropdownToggle}>
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
        )}
      </div>
      <Modal>
        <h2>This is the modal content</h2>
        {selectChoosableState &&
          selectChoosableState.map((value) => {
            return (
              <React.Fragment key={value}>
                <button onClick={() => chooseTopicToMutate(value)}>
                  {value}
                </button>
                <br />
              </React.Fragment>
            );
          })}

        <CloseButton onClick={() => dispatch(editAction.closeModal())} />

        <div>
          <p>
            <strong>Selected Option:</strong> {selectedOption || "None"}
          </p>
          <p>
            <strong>URL:</strong> {url || "None"}
          </p>
        </div>
        <div className="flex space-x-4">
          <DropDown />
          <DropDown />
          <DynamicForm frame={submitFrame.submitNews} />
        </div>
        <OkBtn />
      </Modal>
    </>
  );
}

export default OverlayButton;
