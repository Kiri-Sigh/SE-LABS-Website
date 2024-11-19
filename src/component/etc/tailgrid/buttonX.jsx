import React from "react";
import { NavLink } from "react-router-dom";

const WhiteRoundedButton = ({ link, text }) => {
  return (
    <NavLink to={link}>
      <span className="inline-flex items-center justify-center rounded-full border border-transparent bg-white px-7 py-3 text-center text-base font-medium text-dark shadow-1 hover:bg-gray-4 disabled:border-gray-3 disabled:bg-gray-3 disabled:text-dark-5 dark:bg-gray-2 dark:shadow-box-dark dark:hover:bg-dark-3">
        {text}
      </span>
    </NavLink>
  );
};

export default WhiteRoundedButton;
