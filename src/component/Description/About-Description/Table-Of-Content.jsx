import React from "react";

const TableOfContents = () => {
  const items = [
    { title: "Heading 2", level: 0 },
    { title: "Heading 3", level: 1 },
    { title: "Heading 4", level: 2 },
    { title: "Heading 5", level: 3 },
    { title: "Heading 6", level: 4 },
  ];

  return (
    <nav className="flex flex-col w-80 min-w-[240px]">
      <h2 className="text-2xl font-bold leading-snug">Table of contents</h2>
      <ul className="flex flex-col mt-4 w-full text-lg">
        {items.map((item, index) => (
          <li key={index} className={`gap-2.5 px-${4} py-3 w-full `}>
            {item.title}
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default TableOfContents;
