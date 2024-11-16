import React, { useState } from "react";
import NewsCard from "../../Cards/News-Card";
import { useInfiniteFetch } from "../../../api/custom-hooks";
import previous from "../../../resource/previous-button.svg";
import next from "../../../resource/next-button.svg";

function RecentNews({ toFetchedData = {} }) {
  const [pageIndex, setPageIndex] = useState(0);
  const recentNewsQuery = useInfiniteFetch({
    id: toFetchedData.id,
    url: toFetchedData.url,
    pageSize: toFetchedData.pageSize,
  });
  const { data, isLoading, isError, fetchNextPage, fetchPreviousPage } =
    recentNewsQuery;
  const topic = data ? Object.keys(data.pages[0][0])[0] : undefined;

  const handleNextPage = () => {
    console.log("Next button clicked");
    console.log("data.pages.length", data.pages.length);
    if (data && data.pages.length > pageIndex + 1) {
      fetchNextPage().then(() => setPageIndex(pageIndex + 1));
    }
  };

  const handlePreviousPage = () => {
    console.log("Previous button clicked");
    console.log("data.pages.length", data.pages.length);

    if (pageIndex > 0) {
      fetchPreviousPage().then(() => setPageIndex(pageIndex - 1));
    }
  };

  return (
    <section className="flex overflow-hidden flex-col px-16 py-28 w-full bg-gray-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
      <div className="flex flex-wrap gap-10 justify-between items-end w-full max-md:max-w-full">
        <div className="flex flex-col text-gray-800 min-w-[240px] w-[768px] max-md:max-w-full">
          <h2 className="text-5xl font-bold leading-tight max-md:max-w-full max-md:text-4xl">
            Latest News
          </h2>
          <p className="mt-6 text-lg max-md:max-w-full">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </p>
        </div>
        <button className="flex flex-col text-base text-gray-800 w-[104px]">
          <span className="gap-2 self-stretch px-6 py-3 max-w-full bg-white rounded-xl border border-gray-300 hover:bg-gray-200 transition max-md:px-5">
            View all
          </span>
        </button>
      </div>
      <div className="flex flex-col mt-16 w-full max-md:mt-10 max-md:max-w-full">
        <div className="box-border flex relative flex-col shrink-0">
          <div className="flex gap-8 items-start w-full max-md:max-w-full">
            {!isLoading ? (
              data.pages[pageIndex].map((item, index) => {
                const topicData = item[topic];
                const resolvedID =
                  topic === "News"
                    ? topicData.NID
                    : topic === "Laboratory"
                    ? topicData.LID
                    : topic === "Research"
                    ? topicData.RID
                    : null;

                return (
                  <NewsCard
                    key={`${index}`}
                    {...item[topic]}
                    type={`${topic}`}
                    ID={resolvedID}
                  />
                );
              })
            ) : (
              <div>Loading...</div>
            )}
          </div>
        </div>
        <div className="flex flex-wrap gap-10 justify-between items-center mt-12 w-full max-md:mt-10 max-md:max-w-full">
          <div className="flex gap-2 items-start self-stretch my-auto"></div>
          <div className="flex gap-4 items-start self-stretch my-auto">
            <button
              className="flex gap-2 justify-center items-center px-3 w-12 h-12 bg-white border border-gray-300 border-solid rounded-full"
              onClick={() => {
                console.log("Previous button clicked");
                handlePreviousPage();
              }}
              disabled={pageIndex === 0}
            >
              <img
                loading="lazy"
                src={previous}
                alt="Previous"
                className="object-contain self-stretch my-auto w-6 aspect-square"
              />
            </button>
            {!isError ? (
              <button
                className="flex gap-2 justify-center items-center px-3 w-12 h-12 bg-white border border-gray-300 border-solid rounded-full"
                onClick={() => {
                  console.log("Next button clicked");
                  handleNextPage();
                }}
                disabled={data && data.pages.length <= pageIndex + 1}
              >
                <img
                  loading="lazy"
                  src={next}
                  alt="Next"
                  className="object-contain self-stretch my-auto w-6 aspect-square"
                />
              </button>
            ) : (
              <button
                className="flex gap-2 justify-center items-center px-3 w-12 h-12 bg-white border border-gray-300 border-solid rounded-full"
                disabled
              >
                <img
                  loading="lazy"
                  src={next}
                  alt="Next"
                  className="object-contain self-stretch my-auto w-6 aspect-square"
                />
              </button>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}

export default RecentNews;
