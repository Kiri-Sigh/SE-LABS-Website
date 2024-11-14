import { NavLink } from "react-router-dom";
import React from "react";

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
  return (
    <nav className="flex gap-8 justify-center items-center self-stretch my-auto text-xl text-white min-w-[240px] max-md:max-w-full">
      <ul className="flex gap-4">
        {Object.entries(navItems).map(([key, value]) => (
          <li
            key={key}
            className="gap-1 self-stretch my-auto whitespace-nowrap"
          >
            <NavLink
              to={`/${key}`}
              className={({ isActive }) =>
                isActive
                  ? " focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
                  : "hover:underline focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
              }
            >
              {value}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
}

export default MainNavigation;
