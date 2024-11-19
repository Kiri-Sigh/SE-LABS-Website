import React from "react";
import "./Table-Of-Content.css";

const TableOfContents = () => {
  const items = [
    { title: "Who are we?", id: "heading-2" },
    { title: "Why Software Engineering?", id: "heading-3" },
    { title: "Missions and Values", id: "heading-4" },
    { title: "Leadership", id: "heading-5" },
    { title: "Faculty", id: "heading-6" },
  ];

  return (
    <nav className="flex flex-col w-80 min-w-[240px] bg-blue-200 rounded-xl overflow-hidden">
      <h2 className="text-2xl font-bold leading-snug bg-blue-400 p-5">
        Table of contents
      </h2>
      <ul className="flex flex-col w-full text-lg">
        {items.map((item, index) => (
          <a href={`#${item.id}`}>
            <li key={index} className="gap-2.5 px-5 py-3 w-full highlight-anim">
              {item.title}
            </li>
          </a>
        ))}
      </ul>
    </nav>
  );
};

export default TableOfContents;
