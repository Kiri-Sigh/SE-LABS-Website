import React from "react";

function OverlayDD({ possiblePower, onSelect, close }) {
  const handleOptionClick = (option) => {
    onSelect(option); // Send the selected option to the parent
    close(false); // Close the dropdown
  };

  return (
    <ul className="z-5 w-full bg-white border border-gray-300 rounded-lg shadow-lg">
      {possiblePower.length > 0 ? (
        possiblePower.map((option) => (
          <li
            key={option}
            onClick={() => handleOptionClick(option)}
            className="px-2 py-2 hover:bg-gray-100 cursor-pointer"
          >
            {option}
          </li>
        ))
      ) : (
        <li className="px-4 py-2 text-gray-400">No options available</li>
      )}
    </ul>
  );
}

export default OverlayDD;
