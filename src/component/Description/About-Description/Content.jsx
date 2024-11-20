import React from "react";

const ContentSection = ({ id, title, level, children }) => {
  const HeadingTag = `h${level}`;
  const headingClasses = {
    2: "text-5xl font-bold leading-tight pb-4",
    3: "text-4xl font-bold leading-tight py-6",
    4: "text-3xl font-bold leading-tight pt-6 pb-5",
    5: "text-2xl font-bold leading-snug pt-5 pb-4",
    6: "text-xl font-bold leading-snug pt-5 pb-4",
  };

  return (
    <section id={id} className="w-full max-md:max-w-full scroll-mt-20">
      <HeadingTag className={headingClasses[level]}>{title}</HeadingTag>
      {children}
    </section>
  );
};

export default ContentSection;
