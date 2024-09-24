import React from "react";

const Quote = ({ text }) => {
  return (
    <blockquote className="flex overflow-hidden items-start py-9 w-full text-xl leading-7 text-black max-md:max-w-full">
      <div className="flex overflow-hidden flex-wrap flex-1 shrink gap-5 pr-5 w-full basis-0 bg-white bg-opacity-0 min-w-[240px] max-md:max-w-full">
        <div className="flex shrink-0 w-0.5 bg-black h-[84px]" />
        <p className="flex-1 shrink self-start basis-0 max-md:max-w-full">
          {text}
        </p>
      </div>
    </blockquote>
  );
};

export default Quote;
