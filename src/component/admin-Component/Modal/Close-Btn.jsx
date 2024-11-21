import React from "react";
import closeBtn from "../../../resource/modal-close-btn.svg";
function CloseButton({ onClick }) {
  return (
    <button
      onClick={onClick}
      className="flex gap-2.5 justify-center items-center self-start px-1 mb-5 mt-2.5 w-6 h-6 bg-neutral-200 min-h-[24px] rounded-[29px]"
      aria-label="Close newsletter subscription"
    >
      <img
        loading="lazy"
        src={closeBtn}
        className="object-contain self-stretch my-auto w-2.5 aspect-square fill-neutral-600"
        alt=""
      />
    </button>
  );
}

export default CloseButton;
