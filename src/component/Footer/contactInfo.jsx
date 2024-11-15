import React from "react";

function ContactInfo() {
  return (
    <div className="flex overflow-hidden flex-col text-sm min-w-[240px] w-[864px] max-md:max-w-full">
      <img
        loading="lazy"
        src="https://cdn.builder.io/api/v1/image/assets/TEMP/5efedf53fa5e098141a63a5eb5e0add0b77b3820af95f07957e7aae03d04a014?placeholderIfAbsent=true&apiKey=48b4d741997c411b883c3a9cff6347e7"
        className="object-contain aspect-[2.33] w-[63px]"
        alt="Company logo"
      />
      <div className="flex flex-col mt-8 w-full max-md:max-w-full">
        <div className="flex flex-col w-full text-white max-md:max-w-full">
          <h2 className="font-semibold max-md:max-w-full">Address:</h2>
          <p className="mt-1 max-md:max-w-full">
            1 Chalong Krung 1 Alley, Lat Krabang, Khet Lat Krabang, Krung Thep
            Maha Nakhon 10520
          </p>
        </div>
        <div className="flex flex-col mt-6 w-full max-md:max-w-full">
          <h2 className="font-semibold text-white max-md:max-w-full">
            Contact:
          </h2>
          <div className="flex flex-col mt-1 w-full text-white max-md:max-w-full">
            <a href="tel:023298000" className="underline max-md:max-w-full">
              02 329 8000
            </a>
            <a
              href="mailto:info@kmitl.ac.th"
              className="underline max-md:max-w-full"
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
