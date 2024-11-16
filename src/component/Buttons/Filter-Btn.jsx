import React from "react";
import dropdown from "../../resource/drop-down-filter.svg";
function FilterButton() {
    return (
        <button className="flex gap-2 justify-center items-center self-stretch px-4 py-3 my-auto bg-blue-500 text-white border  border-solid rounded-[34px] hover:bg-blue-600">
            <span className="self-stretch my-auto">Filter by Lab</span>
            <img
                loading="lazy"
                src={dropdown}
                alt=""
                className="object-contain shrink-0 self-stretch my-auto w-6 aspect-square"
            />
        </button>
    );
}

export default FilterButton;
