import React from "react";
import NewsCard from "../Cards/News-Card.jsx";
import previous from "../../resource/previous-button.svg";
import next from "../../resource/next-button.svg";
import ViewAllButton from "../Buttons/View-All-Btn.jsx";
import FilterButton from "../Buttons/Filter-Btn.jsx";
import { useInfiniteFetch } from "api/custom-hooks.js";
import EventCard from "component/Cards/Event-Card.jsx";

function GridCards({ toFetchedData = {}, topic = "", url = "" }) {
  const recentNewsGridQuery = useInfiniteFetch({
    id: toFetchedData.id,
    url: url,
    pageSize: toFetchedData.pageSize,
  });
  const { data, isLoading, isError } = recentNewsGridQuery;

  // Helper function to chunk array into groups of 5
  const chunkArray = (arr, size) => {
    const result = [];
    for (let i = 0; i < arr.length; i += size) {
      result.push(arr.slice(i, i + size));
    }
    return result;
  };

  return (
    <section className="flex overflow-hidden flex-col px-16 py-28 w-full bg-sky-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
      <div className="flex flex-wrap gap-10 justify-between items-end w-full max-md:max-w-full">
        <div className="flex flex-col text-black min-w-[240px] w-[768px] max-md:max-w-full"></div>
        <div className="flex items-center gap-4">
          <FilterButton />
          <ViewAllButton />
        </div>
      </div>
      <div className="flex flex-col mt-6 w-full max-md:mt-5 max-md:max-w-full">
        {/* Reduced margin-top */}
        <div className="box-border flex relative flex-col shrink-0">
          <div className="w-full max-md:max-w-full mt-4">
            {" "}
            {/* Wrapper for all rows */}
            {!isLoading ? (
              data.pages.map((itemArr, pageIndex) =>
                chunkArray(itemArr, 4).map((row, rowIndex) => (
                  <div
                    key={`${pageIndex}-${rowIndex}`}
                    className="flex gap-4 mb-6 flex-wrap"
                  >
                    {row.map((item, itemIndex) => {
                      return topic === "news" ? (
                        <NewsCard
                          key={`${pageIndex}-${rowIndex}-${itemIndex}`}
                          {...item.News}
                        />
                      ) : topic === "events" ? (
                        <EventCard
                          key={`${pageIndex}-${rowIndex}-${itemIndex}`}
                          {...item.Event}
                        />
                      ) : null;
                    })}
                  </div>
                ))
              )
            ) : (
              <div>Loading...</div>
            )}
          </div>
        </div>
      </div>
      {!isError && (
        <button className="px-8 py-5 mt-8 w-full text-lg text-black bg-white rounded-2xl border border-black border-solid max-md:px-5 max-md:max-w-full">
          Load More
        </button>
      )}
      {/* Pagination and navigation controls */}
    </section>
  );
}

export default GridCards;
