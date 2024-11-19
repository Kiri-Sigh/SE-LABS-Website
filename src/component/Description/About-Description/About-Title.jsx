import React from "react";
import se_banner from "./se_banner.jpg";

function About_Title() {
  return (
    <section className="flex overflow-hidden flex-col justify-center pt-10 w-full bg-gray-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
      <div className="flex flex-col w-full max-md:max-w-full">
        <h1 className="overflow-hidden w-full text-5xl pl-16 font-bold leading-tight text-black max-md:masrc/component/others/Big-Image/se_banner.jpgx-w-full max-md:text-4xl">
          About Us
        </h1>
        <div className="flex flex-col w-full -mt-10 max-md:mt-10 max-md:max-w-full">
          <img
            loading="lazy"
            src={se_banner}
            alt="AI Laboratory visual representation"
            className="object-contain w-full aspect-[2.19] max-md:max-w-full"
          />
        </div>
      </div>
    </section>
  );
}
export default About_Title;
