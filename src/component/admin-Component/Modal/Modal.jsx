import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { editAction } from "../../../store/edit-slice";
import Modal from "./Modal-Frame";
// import NewsletterSubscription from "./example-input";
import ImageUploader from "./input/Add-Img";
import DropDown from "./relate/dropdown";
import InputLong from "./input/Input-Long";
import "./scrollbar.css";
import CloseButton from "./Close-Btn";
import OkBtn from "./OK-btn";
import { useForm } from "react-hook-form";
import { editFrame, createFrame } from "./input/frame";
// let object = {};
const Modals = (object) => {
  const dispatch = useDispatch();
  // const isCreating = useSelector((state) => state.editAction.isCreate);
  const { register, handleSubmit, setValue } = useForm();
  // const value = useSelector();
  const onSubmit = (data) => {
    // console.log("Form Data:", data);
  };
  const prototypeFrame = editFrame.editLab;
  // console.log("Prototype Frame:", prototypeFrame);

  return (
    <div>
      <button onClick={() => dispatch(editAction.openModal())}>
        Open Modal
      </button>

      {/* Modal will automatically open or close based on Redux state */}
      <Modal>
        <h2>This is the modal content</h2>

        {/* <NewsletterSubscription /> */}
        <CloseButton onClick={() => dispatch(editAction.closeModal())} />
        <form onSubmit={handleSubmit(onSubmit)}>
          {mapModal(prototypeFrame, register, setValue)}
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
};

export default Modals;

function mapModal(prototypeFrame, register, setValue) {
  return Object.entries(prototypeFrame).map(([key, value]) => {
    switch (value) {
      case "text":
        return (
          <ImageUploader
            key={key}
            setValue={setValue}
            register={register}
            name="image"
          />
        );
      default:
        return <InputLong key={key} register={register} name={`file-${key}`} />;
    }
  });
}
// /////////////custom VALIDATION//////////////
// <input
//   {...register("password", {
//     required: "Password is required",
//     validate: (value) =>
//       value.length >= 6 || "Password must be at least 6 characters long",
//   })}
// />

//////////////arr to object////////////////////////////////
// const myObject = { a: 1, b: 2, c: 3 };

// const mappedEntries = Object.entries(myObject).map(([key, value]) => {
//   return [key, value * 2];  // Keep it as an array [key, value]
// });

// const newObject = Object.fromEntries(mappedEntries);

// console.log(newObject);  // Output: { a: 2, b: 4, c: 6 }

////////////object mapping/////////////////////
// const myObject = { a: 1, b: 2, c: 3 };

// const mappedEntries = Object.entries(myObject).map(([key, value]) => {
//   return { [key]: value * 2 }; // Transforming both key and value
// });

// console.log(mappedEntries);
// // Output: [{ a: 2 }, { b: 4 }, { c: 6 }]
