import React from "react";

function HeroContent({ title, description }) {
  return (
    <div className="flex flex-col flex-1 shrink justify-center p-12 text-black bg-gradient-to-l from-blue-200 to-blue-500 border-r-2 border-black border-solid basis-0 min-w-[240px] max-md:px-5 max-md:max-w-full">
      <div className="flex flex-col w-full max-md:max-w-full">
        <h1 className="text-6xl font-bold leading-[67px] max-md:max-w-full max-md:text-4xl max-md:leading-[54px]">
          {title}
        </h1>
        <p className="mt-6 text-lg leading-7 max-md:max-w-full">
          {description}
        </p>
      </div>
    </div>
  );
}

export default HeroContent;
