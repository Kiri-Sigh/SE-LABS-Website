import React, { useState, useEffect } from "react";
import NewsCard from "../../Cards/News-Card";
import { useInfiniteFetch } from "../../../api/custom-hooks";
import previous from "../../../resource/previous-button.svg";
import next from "../../../resource/next-button.svg";

import { getData, getImgData } from "../../../api/api-method";

import TeamCard from "component/Cards/Team-Card";
import WhiteRoundedButton from "component/etc/tailgrid/buttonX";

function RecentNews({
  toFetchedData = {},
  filter = {},
  componentTitle = "Latest News",
  useFilterButton = false,
  publicationLink = null,
}) {
  const [currentPage, setCurrentPage] = useState(0);
  const [currentIndex, setCurrentIndex] = useState(0);
  const recentNewsQuery = useInfiniteFetch({
    id: toFetchedData.id,
    url: toFetchedData.url,
    pageSize: toFetchedData.pageSize,
    filter,
  });

  const { data, isLoading, fetchNextPage, isError, isFetchingNextPage } =
    recentNewsQuery;

  const topic = data?.pages?.[0]?.[0] ? Object.keys(data.pages[0][0])[0] : null;

  // Check if there's any data
  const hasData = data?.pages?.some((page) => page.length > 0);

  const currentData =
    data?.pages?.reduce((acc, page) => acc.concat(page), []) || [];

  useEffect(() => {
    if (currentData.length < 5 && !isFetchingNextPage && hasData) {
      fetchNextPage();
    }
  }, [currentData, isFetchingNextPage, hasData]);

  const handleNextPage = () => {
    if (currentIndex + 5 >= currentData.length && !isFetchingNextPage) {
      fetchNextPage();
    }
    setCurrentPage((prevPage) => prevPage + 1);
    setCurrentIndex((prevIndex) => prevIndex + 5);
  };

  const handlePreviousPage = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prevIndex) => prevIndex - 5);
    }
    if (currentPage > 0) {
      setCurrentPage((prevPage) => prevPage - 1);
    }
  };

  const visibleData = currentData.slice(currentIndex, currentIndex + 5);

  return (
    <section className="flex flex-col px-16 py-28 w-full bg-gray-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
      <div className="flex flex-wrap gap-10 justify-between items-end w-full max-md:max-w-full">
        <div className="flex flex-col text-black min-w-[240px] w-[768px] max-md:max-w-full">
          <h2 className="text-5xl font-bold leading-tight max-md:max-w-full max-md:text-4xl">
            {componentTitle}
          </h2>
        </div>
        <WhiteRoundedButton
          link={`/${topic?.toLowerCase()}`}
          text={`View ${topic ? topic : ""}`}
        />
      </div>
      <div className="flex flex-col mt-16 w-full max-md:mt-10 max-md:max-w-full">
        <div className="box-border flex relative flex-col shrink-0">
          <div className="flex gap-8 items-start w-full max-md:max-w-full transition-transform duration-500 ease-in-out transform">
            {!isLoading && hasData ? (
              visibleData.map((item, index) => {
                const topicData = item[topic];
                const resolvedID =
                  topic === "News"
                    ? topicData.NID
                    : topic === "Laboratory"
                    ? topicData.LID
                    : topic === "Research"
                    ? topicData.RID
                    : topic === "Publication"
                    ? topicData.PID
                    : topic === "Researcher"
                    ? topicData.UID
                    : null;

                return topic !== "Event" && topic !== "Researcher" ? (
                  <NewsCard
                    key={`page-${currentPage}-item-${index}`}
                    {...item[topic]}
                    type={`${topic}`}
                    ID={resolvedID}
                    publicationLink={publicationLink}
                    className="transition-opacity duration-500 ease-in-out opacity-0 animate-fadeIn"
                  />
                ) : topic === "Researcher" ? (
                  <TeamCard
                    key={`researcher-${currentPage}-${index}`}
                    {...item[topic]}
                    className="transition-opacity duration-500 ease-in-out opacity-0 animate-fadeIn"
                  />
                ) : null;
              })
            ) : isLoading ? (
              <div>Loading...</div>
            ) : (
              <div className="text-center text-lg text-gray-500">
                No recent news available.
              </div>
            )}
          </div>
        </div>
        <div className="flex flex-wrap gap-10 justify-between items-center mt-12 w-full max-md:mt-10 max-md:max-w-full">
          <button
            onClick={handlePreviousPage}
            disabled={currentPage === 0 && currentIndex === 0}
            className="flex gap-2 justify-center items-center px-3 w-12 h-12 bg-white border border-black border-solid rounded-[50px] transition-transform duration-500 ease-in-out transform hover:scale-110"
          >
            <img
              loading="lazy"
              src={previous}
              alt="Previous"
              className="object-contain self-stretch my-auto w-6 aspect-square"
            />
          </button>
          <button
            onClick={handleNextPage}
            disabled={isFetchingNextPage}
            className="flex gap-2 justify-center items-center px-3 w-12 h-12 bg-white border border-black border-solid rounded-[50px] transition-transform duration-500 ease-in-out transform hover:scale-110"
          >
            <img
              loading="lazy"
              src={next}
              alt="Next"
              className="object-contain self-stretch my-auto w-6 aspect-square"
            />
          </button>
        </div>
      </div>
    </section>
  );
}

export default RecentNews;
