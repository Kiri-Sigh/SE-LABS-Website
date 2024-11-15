import React from "react";

function HeroImg({ imageSrc }) {
  return (
    <div className="flex flex-col flex-1 shrink my-auto basis-24 max-md:max-w-full">
      <img
        loading="lazy"
        src={imageSrc}
        alt="Illustration representing software changing the world"
        className="object-contain w-full h-auto max-h-full max-w-full"
      />
    </div>
  );
}

export default HeroImg;
