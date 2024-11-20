import React, { useRef } from "react";
import TeamCard from "../Cards/Team-Card";
import previous from "../../resource/previous-button.svg";
import next from "../../resource/next-button.svg";

const OurTeam = ({ teamMembers }) => {
  const scrollRef = useRef(null);

  const scrollLeft = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollBy({ left: -300, behavior: "smooth" });
    }
  };

  const scrollRight = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollBy({ left: 300, behavior: "smooth" });
    }
  };

  return (
    <section className="flex flex-col px-16 py-28 w-full bg-sky-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
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
      <div className="relative mt-16 w-full max-md:mt-10 max-md:max-w-full">
        <button
          onClick={scrollLeft}
          className="absolute left-0 top-1/2 transform -translate-y-1/2 bg-white p-2 rounded-full shadow-md hover:bg-gray-200"
        >
          <img src={previous} alt="Previous" className="w-6 h-6" />
        </button>
        <div ref={scrollRef} className="flex overflow-x-auto space-x-4 p-4">
          {teamMembers.map((member, index) => (
            <div key={index} className="flex-shrink-0 w-64">
              <TeamCard
                title={member.title}
                body={member.body}
                date={member.date}
                ID={member.ID}
                related_laboratory={member.related_laboratory}
                type={member.type}
                name={member.name}
                gmail={member.gmail}
              />
            </div>
          ))}
        </div>
        <button
          onClick={scrollRight}
          className="absolute right-0 top-1/2 transform -translate-y-1/2 bg-white p-2 rounded-full shadow-md hover:bg-gray-200"
        >
          <img src={next} alt="Next" className="w-6 h-6" />
        </button>
      </div>
    </section>
  );
};

export default OurTeam;
