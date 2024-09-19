import React from "react";
import ContactInfo from "./contactInfo";
import SocialLinks from "./Social-Links";
import "./Footer.css";
function Footer() {
  return (
    <footer className="flex overflow-hidden flex-col justify-center items-center px-16 py-20 max-md:px-5">
      <div className="flex flex-wrap gap-10 items-start p-12 w-full bg-cyan-200 rounded-3xl border border-black border-solid max-w-[1312px] max-md:px-5 max-md:max-w-full">
        <ContactInfo />
        <SocialLinks />
      </div>
    </footer>
  );
}

export default Footer;
