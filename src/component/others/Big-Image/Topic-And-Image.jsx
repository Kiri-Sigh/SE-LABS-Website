import React from "react";

const TopicAndImage = () => {
  return (
    <section className="flex overflow-hidden flex-col justify-center px-16 py-28 w-full bg-sky-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
      <div className="flex flex-col w-full max-md:max-w-full">
        <h1 className="overflow-hidden w-full text-5xl font-bold leading-tight text-black max-md:max-w-full max-md:text-4xl">
          AI LABORATORY
        </h1>
        <div className="flex flex-col mt-20 w-full max-md:mt-10 max-md:max-w-full">
          <img
            loading="lazy"
            src="https://picsum.photos/700/400"
            alt="AI Laboratory visual representation"
            className="object-contain w-full aspect-[2.19] max-md:max-w-full"
          />
        </div>
      </div>
    </section>
  );
};

export default TopicAndImage;
