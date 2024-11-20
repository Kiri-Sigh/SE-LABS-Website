import { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { createPortal } from "react-dom";
import { editAction } from "store/edit-slice";

export default function ModalFrame2({ children }) {
  const dispatch = useDispatch();

  // Use selector to access modal state from the Redux store
  let isOpen = useSelector((state) => {
    // console.log("Modal open state:", state.editSlice.isSpecificOpen);
    return state.editSlice.isSpecificOpen;
  });

  const specificTypeAndID = useSelector((state) => {
    // console.log("Redux state:", state);
    return state.editSlice.specificTypeAndID;
  });

  useEffect(() => {
    const modal = document.getElementById("modalDialog");
    if (isOpen) {
      console.log("Opening modal...");
      modal.showModal();
    } else {
      console.log("Closing modal...");
      modal.close();
    }
    return () => modal && modal.close();
  }, [isOpen]);

  return createPortal(
    <dialog
      id="modalDialog"
      className="relative w-full  bg-white p-6 rounded-lg max-h-[90vh] max-w-[45vw]  overflow-y-auto "
      onClose={() => {
        dispatch(editAction.closeSpecificModal());
        dispatch(editAction.reset());
      }}
    >
      {children}
    </dialog>,
    document.getElementById("modal")
  );
}
