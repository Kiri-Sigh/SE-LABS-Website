import React from "react";
import NewsCard from "../../Cards/News-Card";
import { useInfiniteFetch } from "../../../api/custom-hooks";
import previous from "../../../resource/previous-button.svg";
import next from "../../../resource/next-button.svg";
import TeamCard from "component/Cards/Team-Card";

function RecentNews({
  toFetchedData = {},
  filter = {},
  componentTitle = "recentNewsComp",
  useFilterButton = false,
  publicationLink = null,
}) {
  const recentNewsQuery = useInfiniteFetch({
    id: toFetchedData.id,
    url: toFetchedData.url,
    pageSize: toFetchedData.pageSize,
    filter,
  });

  const { data, isLoading, isError } = recentNewsQuery;
  const topic = data?.pages?.[0]?.[0] ? Object.keys(data.pages[0][0])[0] : null;

  // Check if there's any data
  const hasData = data?.pages?.some((page) => page.length > 0);

  return (
    <section className="flex overflow-hidden flex-col px-16 py-28 w-full bg-sky-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
      <div className="flex flex-wrap gap-10 justify-between items-end w-full max-md:max-w-full">
        <div className="flex flex-col text-black min-w-[240px] w-[768px] max-md:max-w-full">
          <h2 className="text-5xl font-bold leading-tight max-md:max-w-full max-md:text-4xl">
            {componentTitle}
          </h2>
          <p className="mt-6 text-lg max-md:max-w-full">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </p>
        </div>
        <button className="flex flex-col text-base text-black w-[104px]">
          <span className="gap-2 self-stretch px-6 py-3 max-w-full bg-white rounded-xl border border-black border-solid w-[104px] max-md:px-5">
            View all
          </span>
        </button>
      </div>
      <div className="flex flex-col mt-16 w-full max-md:mt-10 max-md:max-w-full">
        <div className="box-border flex relative flex-col shrink-0">
          <div className="flex gap-8 items-start w-full max-md:max-w-full">
            {!isLoading && hasData ? (
              data.pages.map((page, pageIndex) =>
                page.map((item, itemIndex) => {
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
                      key={`${pageIndex}-${itemIndex}`}
                      {...item[topic]}
                      type={`${topic}`}
                      ID={resolvedID}
                      publicationLink={publicationLink}
                    />
                  ) : topic === "Researcher" ? (
                    <TeamCard
                      key={`researcher-${pageIndex}-${itemIndex}`}
                      {...item[topic]}
                    />
                  ) : null;
                })
              )
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
          <div className="flex gap-2 items-start self-stretch my-auto"></div>
          <div className="flex gap-4 items-start self-stretch my-auto">
            <button className="flex gap-2 justify-center items-center px-3 w-12 h-12 bg-white border border-black border-solid rounded-[50px]">
              <img
                loading="lazy"
                src={previous}
                alt="Previous"
                className="object-contain self-stretch my-auto w-6 aspect-square"
              />
            </button>
            {!isError ? (
              <button className="flex gap-2 justify-center items-center px-3 w-12 h-12 bg-white border border-black border-solid rounded-[50px]">
                <img
                  loading="lazy"
                  src={next}
                  alt="Next"
                  className="object-contain self-stretch my-auto w-6 aspect-square"
                />
              </button>
            ) : (
              <button
                className="flex gap-2 justify-center items-center px-3 w-12 h-12 bg-white border border-black border-solid rounded-[50px]"
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
