import React from "react";
import EventCard from "../../Cards/Event-Card";
import { getData } from "../../../api/api-method";
const RecentEvents = ({ listData, topic = "events" }) => {
  return (
    <section className="flex overflow-hidden flex-col px-16 py-28 w-full bg-sky-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
      <div className="flex flex-col w-full text-black max-md:max-w-full">
        <h2 className="text-5xl font-bold leading-tight max-md:max-w-full max-md:text-4xl">
          Latest Events
        </h2>
        <p className="mt-6 text-lg max-md:max-w-full">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse
          varius enim in eros elementum tristique.
        </p>
      </div>
      <div className="flex flex-col mt-20 w-full max-md:mt-10 max-md:max-w-full">
        {listData.map((event, index) => (
          <EventCard key={index} {...event} />
        ))}
        <button className="px-8 py-5 mt-8 w-full text-lg text-black bg-white rounded-2xl border border-black border-solid max-md:px-5 max-md:max-w-full">
          Load More
        </button>
      </div>
    </section>
  );
};

export default RecentEvents;

//  function fetch(topic){
//   if (topic=news)
//   const data = getData();
//  }
