import React from "react";
import HeroContent from "./Hero-Content";
import HeroImg from "./Hero-Img";
function HeroBox() {
  return (
    <main className="flex overflow-hidden flex-col justify-center px-16 py-20 w-full bg-sky-100 max-md:px-5 max-md:max-w-full">
      <section className="flex flex-col w-full max-md:max-w-full">
        <article className="flex overflow-hidden flex-wrap w-full rounded-3xl border border-black border-solid max-md:max-w-full">
          <HeroContent
            title="Software can change the WORLD!?"
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse varius enim in eros elementum tristique. Duis cursus, mi quis viverra ornare, eros dolor interdum nulla, ut commodo diam libero vitae erat."
          />
          <HeroImg imageSrc="https://picsum.photos/300/295" />
        </article>
      </section>
    </main>
  );
}

export default HeroBox;
