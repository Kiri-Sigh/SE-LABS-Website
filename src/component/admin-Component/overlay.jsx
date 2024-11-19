import React, { useState } from "react";
import ReactDOM from "react-dom";
import "./OverlayButton.css";
import { useDispatch } from "react-redux";
import { useForm } from "react-hook-form";
import { editFrame } from "./Modal/input/frame";
import { editAction } from "store/edit-slice";
import Modal from "./Modal/Modal-Frame";
import CloseButton from "./Modal/Close-Btn";
import DropDown from "./Modal/relate/dropdown";
import OkBtn from "./Modal/OK-btn";
import ImageUploader from "./Modal/input/Add-Img";
import InputLong from "./Modal/input/Input-Long";

function OverlayButton() {
  const dispatch = useDispatch();
  // const isCreating = useSelector((state) => state.editAction.isCreate);
  const { register, handleSubmit, setValue } = useForm();
  const [formData, setFormData] = useState({});
  // const value = useSelector();
  const onSubmit = (data) => {
    // console.log("Form Data:", data);
  };
  const prototypeFrame = editFrame.createLab;
  // console.log("Prototype Frame:", prototypeFrame);

  return (
    <div>
      <button
        className="fixed-button"
        onClick={() => dispatch(editAction.openModal())}
      >
        Open Modal
      </button>

      {/* Modal will automatically open or close based on Redux state */}
      <Modal>
        <h2>This is the modal content</h2>

        <CloseButton onClick={() => dispatch(editAction.closeModal())} />
        <form onSubmit={handleSubmit(onSubmit)}>
          {/* {Object.entries(prototypeFrame).map(([key, value]) => {
            switch (value) {
              case "file":
                return (
                  <ImageUploader
                    key={key}
                    onChange={(e) => setFormData(e.target.value)}
                  />
                );
              case "text":
                return <input key={key} value={""} name="image" />;
              default:
                return <InputLong key={key} name={`file-${key}`} />;
            }
          })} */}
          {/* <ImageUploader setValue={setValue} register={register} name="image" /> */}
          <div className="flex space-x-4">
            <DropDown register={register} name="dropdown1" />
            <DropDown register={register} name="dropdown2" />
          </div>
          {/* <InputLong register={register} name="input1" />
            <InputLong register={register} name="input2" />
            <InputLong register={register} name="input3" /> */}
          <OkBtn />
        </form>
      </Modal>
    </div>
  );
}

export default OverlayButton;
