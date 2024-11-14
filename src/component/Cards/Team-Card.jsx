import React from "react";
import "./Card.css";

const TeamCard = ({
  title,
  body,
  date,
  ID,
  related_laboratory,
  type,
  name,
  gmail,
}) => {
  return (
    <div className="flex flex-col rounded-3xl border border-black border-solid min-w-[240px] w-[390px]">
      <img
        loading="lazy"
        src={"a"}
        alt={name}
        className=" w-full rounded-tl-3xl rounded-tr-3xl aspect-[1.3]"
      />
      <div className="flex flex-col p-6 w-full bg-cyan-200 rounded-none border border-black border-solid max-md:px-5 rounded-bl-3xl rounded-br-3xl">
        <div className="flex flex-col w-full text-2xl font-bold leading-snug text-black line-clamp-2 indent-clamp ">
          <div className="w-full ">{name}</div>
        </div>
        <div className="flex gap-4 items-center mt-6 w-full text-sm font-semibold text-black whitespace-nowrap ">
          <img
            loading="lazy"
            src="https://w7.pngwing.com/pngs/712/520/png-transparent-google-mail-gmail-logo-icon.png"
            alt="Email icon"
            className="object-contain shrink-0 self-stretch my-auto w-12 rounded-3xl aspect-square"
          />
          <div className="flex-1 shrink self-stretch my-auto min-w-[240px]">
            {"email"}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TeamCard;
