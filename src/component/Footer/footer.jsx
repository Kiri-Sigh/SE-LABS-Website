import React from "react";
import ContactInfo from "./contactInfo";
import SocialLinks from "./Social-Links";
import "./Footer.css";

function Footer() {
  return (
    <footer className="flex flex-col items-center px-8 py-16 bg-gray-100 text-white max-md:px-4">
      <div className="flex flex-wrap gap-4 items-start p-8 w-full bg-gray-200 rounded-lg border border-gray-700 shadow-lg max-w-[1312px] max-md:px-5">
        <div className="flex flex-col gap-6 w-full md:w-1/2">
          <h2 className="text-2xl font-bold text-gray-800">Contact Us</h2>
          <ContactInfo />
        </div>
        <div className="flex flex-col gap-6 w-full md:w-1/2">
          {/* <h2 className="text-2xl font-bold text-gray-800">Follow Us</h2> */}
          <SocialLinks />
        </div>
      </div>
      <div className="text-center text-sm text-gray-800 mt-8">
        © {new Date().getFullYear()} Software Engineering, King Mongkut's
        Institute of Technology Ladkrabang.
      </div>
    </footer>
  );
}

export default Footer;
