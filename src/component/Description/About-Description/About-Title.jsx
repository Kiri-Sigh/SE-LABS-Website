import React from "react";
import se_banner from "./se_banner.jpg";

function About_Title() {
  return (
    <section className="pb-10 bg-gray-100 flex justify-center">
      <img
        loading="lazy"
        src={se_banner}
        alt="AI Laboratory visual representation"
      />
    </section>
  );
}
export default About_Title;
