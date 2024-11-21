import React, { useState } from "react";
import previous from "../../resource/previous-button.svg";
import next from "../../resource/next-button.svg";
import { useInfiniteFetchCommit } from "api/custom-hooks";
import WhiteRoundedButton from "component/etc/tailgrid/buttonX";
import CommitCard from "./Commit-Card";

function RecentCommit({
  toFetchedData = {},
  filter = {},
  componentTitle = "Why",
  useFilterButton = false,
  publicationLink = null,
}) {
  const [currentPage, setCurrentPage] = useState(0);
  const token = localStorage.getItem("token");

  const recentNewsQuery = useInfiniteFetchCommit({
    id: toFetchedData.id,
    url: toFetchedData.url,
    pageSize: toFetchedData.pageSize,
    filter,
    token,
  });

  const { data, isLoading, fetchNextPage, isError, isFetchingNextPage } =
    recentNewsQuery;
  if (data) console.log(data);
  const topic = data?.pages?.[0]?.[0] ? Object.keys(data.pages[0][0])[0] : null;

  // Check if there's any data
  const hasData = data?.pages?.some((page) => page.length > 0);

  const handleNextPage = () => {
    if (currentPage + 1 >= data.pages.length && !isFetchingNextPage) {
      fetchNextPage();
    }
    if (!isError) setCurrentPage((prevPage) => prevPage + 1);
  };

  const handlePreviousPage = () => {
    if (currentPage > 0) setCurrentPage((prevPage) => prevPage - 1);
  };

  const currentData =
    data?.pages[currentPage] && data.pages[currentPage].length > 0
      ? data.pages[currentPage]
      : [];

  return (
    <section className="flex overflow-hidden flex-col px-16 pt-4 w-full bg-sky-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
      <div className="flex flex-wrap gap-10 justify-between items-end w-full max-md:max-w-full">
        <div className="flex flex-col text-black min-w-[240px] w-[768px] max-md:max-w-full">
          <h2 className="text-5xl leading-tight max-md:max-w-full max-md:text-4xl">
            {componentTitle}
          </h2>
        </div>
      </div>
      <div className="flex flex-col mt-10 w-full max-md:mt-10 max-md:max-w-full">
        <div className="box-border flex relative flex-col shrink-0">
          <div className="flex gap-8 items-start w-full max-md:max-w-full transition-transform duration-500 ease-in-out">
            {!isLoading && hasData ? (
              currentData.map((item, index) => {
                const topicData = item[topic];
                const resolvedID =
                  topic === "News"
                    ? topicData.NID
                    : topic === "Event"
                    ? topicData.EID
                    : null;

                return topic === "Event" || topic === "News" ? (
                  <CommitCard
                    key={`page-${currentPage}-item-${index}`}
                    {...item[topic]}
                    type={`${topic}`}
                    ID={resolvedID}
                    fullData={item[topic]}
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
            disabled={currentPage === 0}
            className="flex gap-2 justify-center items-center px-3 w-12 h-12 bg-white border border-black border-solid rounded-[50px]"
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
            className="flex gap-2 justify-center items-center px-3 w-12 h-12 bg-white border border-black border-solid rounded-[50px]"
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

export default RecentCommit;
