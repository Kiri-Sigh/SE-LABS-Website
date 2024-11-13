import React from "react";
import locate from "../../resource/location.svg";
import time from "../../resource/time.svg";

const EventCard = ({
  title,
  body,
  start,
  end,
  EID,
  related_laboratory,
  status,
  location,
}) => {
  return (
    <div className="flex flex-col justify-center p-8 w-full bg-cyan-200 rounded-2xl border border-black border-solid max-md:px-5 max-md:max-w-full mb-8">
      <div className="flex flex-col w-full max-md:max-w-full">
        <div className="flex flex-wrap gap-4 items-center w-full max-md:max-w-full">
          <h3 className="flex-1 shrink self-stretch my-auto text-2xl font-bold leading-snug text-black basis-4 max-md:max-w-full">
            {title}
          </h3>
          <span
            className={`self-stretch px-2 py-1 my-auto text-sm font-semibold text-black rounded-xl border border-black border-solid w-[91px]`}
          >
            {status}
          </span>
        </div>
        <p className="mt-4 text-base text-black max-md:max-w-full">{body}</p>
        <div className="flex flex-wrap gap-6 items-start mt-4 w-full text-lg text-black whitespace-nowrap max-md:max-w-full">
          <div className="flex gap-3 items-center">
            <img
              loading="lazy"
              src={locate}
              alt=""
              className="object-contain shrink-0 self-stretch my-auto w-6 aspect-square"
            />
            <span className="self-stretch my-auto">{location}</span>
          </div>
          <div className="flex gap-3 items-center">
            <img
              loading="lazy"
              src={time}
              alt=""
              className="object-contain shrink-0 self-stretch my-auto w-6 aspect-square"
            />
            <span className="self-stretch my-auto">
              {start}-{end}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventCard;
