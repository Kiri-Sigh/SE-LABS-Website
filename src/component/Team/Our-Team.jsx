import React from "react";
import TeamCard from "../Cards/Team-Card";
import previous from "../../resource/previous-button.svg";
import next from "../../resource/next-button.svg";

const OurTeam = ({ teamMembers }) => {
  return (
    <section className="flex overflow-hidden flex-col px-16 py-28 w-full bg-sky-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
      <div className="flex flex-wrap gap-10 justify-between items-end w-full max-md:max-w-full">
        <div className="flex flex-col text-black min-w-[240px] w-[768px] max-md:max-w-full">
          <h2 className="text-5xl font-bold leading-tight max-md:max-w-full max-md:text-4xl">
            Our Team
          </h2>
          <p className="mt-6 text-lg max-md:max-w-full">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </p>
        </div>
        <button className="flex flex-col text-base text-black w-[104px] px-6 py-3 max-w-full bg-white rounded-xl border border-black border-solid max-md:px-5">
          View all
        </button>
      </div>
      <div className="flex flex-col mt-16 w-full max-md:mt-10 max-md:max-w-full">
        <div className="flex gap-8 items-start w-full max-md:max-w-full">
          {teamMembers.map((member, index) => (
            <TeamCard key={index} {...member} />
          ))}
        </div>
        <div className="flex flex-wrap gap-10 justify-between items-center mt-12 w-full max-md:mt-10 max-md:max-w-full">
          <div className="flex gap-2 items-start self-stretch my-auto">
            {[...Array(6)].map((_, index) => (
              <div
                key={index}
                className={`flex shrink-0 w-2 h-2 rounded-full ${
                  index === 0 ? "bg-black" : "bg-stone-300"
                }`}
              />
            ))}
          </div>
          <div className="flex gap-4 items-start self-stretch my-auto">
            <button className="flex gap-2 justify-center items-center px-3 w-12 h-12 bg-white border border-black border-solid rounded-[50px]">
              <img
                loading="lazy"
                src={previous}
                alt="Previous"
                className="object-contain self-stretch my-auto w-6 aspect-square"
              />
            </button>
            <button className="flex gap-2 justify-center items-center px-3 w-12 h-12 bg-white border border-black border-solid rounded-[50px]">
              <img
                loading="lazy"
                src={next}
                alt="Next"
                className="object-contain self-stretch my-auto w-6 aspect-square"
              />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default OurTeam;
