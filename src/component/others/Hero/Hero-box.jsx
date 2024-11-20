import React from "react";
import HeroContent from "./Hero-Content";
import HeroImg from "./Hero-Img";
function HeroBox() {
  return (
    <main className="flex overflow-hidden flex-col justify-center px-16 py-10 w-full h-96 bg-gray-100 max-md:px-5 max-md:max-w-full">
      <section className="flex flex-col w-full max-md:max-w-full">
        <article className="flex overflow-hidden w-full h-80 rounded-3xl border-2 border-black border-solid max-md:max-w-full">
          <HeroContent
            title="Software can change the World."
            description="Join us on making an impact."
          />
          <HeroImg imageSrc="https://campus.campus-star.com/app/uploads/2016/11/KMITL-2.jpg" />
        </article>
      </section>
    </main>
  );
}

export default HeroBox;
