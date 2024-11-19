import dropdown from "../../resource/drop-down-filter.svg";

import React, { useState } from "react";

function FilterButton({ fetchedLabData = [], setSelectedLab }) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState("Filter by Lab");

  const options =
    Array.isArray(fetchedLabData) && fetchedLabData.length > 0
      ? fetchedLabData.map((item) => item.Laboratory.title)
      : [];

  console.log("fetchedLabData", fetchedLabData);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleOptionClick = (option, index) => {
    setSelectedOption(option);
    setSelectedLab(fetchedLabData[index]);
    setIsOpen(false);
  };

  return (
    <div className="relative">
      <button
        onClick={toggleDropdown}
        className="flex gap-2 justify-center items-center self-stretch px-4 py-3 my-auto bg-blue-500 text-white border  border-solid rounded-[34px] hover:bg-blue-600"
      >
        <span className="self-stretch my-auto">{selectedOption}</span>
        <img
          loading="lazy"
          src={dropdown}
          alt="dropdown icon"
          className="object-contain shrink-0 self-stretch my-auto w-6 aspect-square"
        />
      </button>
      {isOpen && options.length > 0 && (
        <ul className="absolute z-10 mt-1 w-full bg-white border border-black rounded-lg shadow-lg overflow-hidden">
          {options.map((option, index) => (
            <li
              key={option}
              onClick={() => handleOptionClick(option, index)}
              className="px-4 py-2 hover:bg-gray-200 cursor-pointer"
            >
              {option}
            </li>
          ))}
        </ul>
      )}
      {isOpen && options.length === 0 && (
        <div className="absolute z-10 mt-1 w-full bg-white border border-black rounded-lg shadow-lg p-4">
          No labs available
        </div>
      )}
    </div>
  );
}

export default FilterButton;
