import React from "react";
import { NavLink } from "react-router-dom";
import "./header.css";
import { useSelector } from "react-redux";

function MainNavigation() {
  const navItems = {
    about: "About us",
    publications: "Publications",
    laboratory: "Laboratory",
    research: "Research",
    people: "People",
    news: "News",
    events: "Events",
  };
  const isAdmin = useSelector((state) => state.mainSlice.isAdminPage);
  return (
    <nav className="flex gap-8 justify-center items-center self-stretch my-auto text-xl text-white min-w-[240px] max-md:max-w-full">
      <ul className="flex gap-4">
        {Object.entries(navItems).map(([key, value]) => (
          <li
            key={key}
            className="gap-1 self-stretch my-auto whitespace-nowrap"
          >
            {isAdmin ? (
              <NavLink
                to={`/admin/${key}`}
                className={
                  "focus:outline-none focus:ring-white focus:ring-opacity-50 underline-anim"
                }
              >
                {value}
              </NavLink>
            ) : (
              <NavLink
                to={`/${key}`}
                className={
                  "focus:outline-none focus:ring-white focus:ring-opacity-50 underline-anim"
                }
              >
                {value}
              </NavLink>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
}

export default MainNavigation;
