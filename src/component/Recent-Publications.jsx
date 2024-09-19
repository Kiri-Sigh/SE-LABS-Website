import React from "react";

function PublicationCard({ image, lab, title, description }) {
  return (
    <article className="flex flex-col flex-1 shrink border border-black border-solid basis-0 min-w-[240px] rounded-[30px]">
      <img
        loading="lazy"
        src={image}
        alt={title}
        className="object-contain w-full aspect-[1.39] rounded-[30px_30px_0px_0px]"
      />
      <div className="flex flex-col justify-center p-6 w-full bg-cyan-200 rounded-none border border-black border-solid max-md:px-5">
        <div className="flex flex-col w-full">
          <div className="flex gap-4 items-center self-start text-sm font-semibold text-black">
            <span className="self-stretch px-2 py-1 my-auto bg-sky-100 rounded-2xl border border-black border-solid">
              {lab}
            </span>
          </div>
          <div className="flex flex-col mt-4 w-full text-black">
            <h2 className="text-2xl font-bold leading-snug">{title}</h2>
            <p className="mt-2 text-base leading-6">{description}</p>
          </div>
        </div>
      </div>
    </article>
  );
}

export default PublicationCard;
