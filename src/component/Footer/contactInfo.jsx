import React from "react";

function ContactInfo() {
  return (
    <div className="flex overflow-hidden flex-col text-sm min-w-[240px] w-[864px] max-md:max-w-full">
      <img
        loading="lazy"
        src="https://www.se.kmitl.ac.th/assets/se.png"
        className="object-contain aspect-[2.33] w-[63px]"
        alt="Company logo"
      />
      <div className="flex flex-col mt-8 w-full max-md:max-w-full">
        <div className="flex flex-col w-full text-gray-800 max-md:max-w-full">
          <h2 className="font-semibold text-gray-800 max-md:max-w-full">
            Address:
          </h2>
          <p className="mt-1 text-gray-800 max-md:max-w-full">
            1 Chalong Krung 1 Alley, Lat Krabang, Khet Lat Krabang, Krung Thep
            Maha Nakhon 10520
          </p>
        </div>
        <div className="flex flex-col mt-6 w-full max-md:max-w-full">
          <h2 className="font-semibold text-gray-800 max-md:max-w-full">
            Contact:
          </h2>
          <div className="flex flex-col mt-1 w-full text-gray-800 max-md:max-w-full">
            <a
              href="tel:023298000"
              className="underline text-gray-800 max-md:max-w-full"
            >
              02 329 8000
            </a>
            <a
              href="mailto:info@kmitl.ac.th"
              className="underline text-gray-800 max-md:max-w-full"
            >
              info@kmitl.ac.th
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ContactInfo;
