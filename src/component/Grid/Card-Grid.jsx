import React, { useEffect } from "react";
import NewsCard from "../Cards/News-Card.jsx";
import ViewAllButton from "../Buttons/View-All-Btn.jsx";
import FilterButton from "../Buttons/Filter-Btn.jsx";
import { useInfiniteFetch } from "api/custom-hooks.js";
import EventCard from "component/Cards/Event-Card.jsx";
import TeamCard from "component/Cards/Team-Card.jsx";

function GridCards({
  toFetchedData = {},
  url = "",
  filter = null,
  useFilterButton = false,
  fetchedLabData = [],
  publicationLink = null,
}) {
  const [selectedLab, setSelectedLab] = React.useState(null);

  if (selectedLab) filter = { laboratory_id: selectedLab.Laboratory.LID };

  const recentNewsGridQuery = useInfiniteFetch({
    id: toFetchedData.id,
    url: url,
    pageSize: toFetchedData.pageSize,
    filter,
  });

  const {
    data,
    isLoading,
    isError,
    fetchNextPage,
    isFetchingNextPage,
    hasNextPage,
  } = recentNewsGridQuery;

  useEffect(() => {
    if (data) {
      console.log("Fetched data:", data);
    }
  }, [data]);

  const topic = data?.pages?.[0]?.[0]
    ? Object.keys(data.pages[0][0])[0]
    : undefined;
  const hasData =
    data?.pages?.some((page) => Array.isArray(page) && page.length > 0) ||
    false;

  const handleLabChange = (event) => {
    setSelectedLab(event);
  };

  const isDataEmpty =
    !data || data.pages.length === 0 || data.pages[0].length === 0;

  return (
    <section className="flex overflow-hidden flex-col px-16 py-28 w-full -mt-40 bg-gray-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
      <div className="flex flex-wrap gap-10 justify-between items-end w-full max-md:max-w-full">
        <div className="flex flex-col text-black min-w-[240px] w-[325px] max-md:max-w-full"></div>
        <div className="flex items-center gap-4">
          {useFilterButton && (
            <FilterButton
              fetchedLabData={fetchedLabData}
              setSelectedLab={handleLabChange}
            />
          )}
        </div>
      </div>
      <div className="flex flex-col mt-6 w-full max-md:mt-5 max-md:max-w-full">
        <div className="box-border flex relative flex-col shrink-0">
          <div className="w-full max-md:max-w-full mt-4">
            {!isLoading ? (
              isDataEmpty ? (
                <div>No data available</div>
              ) : (
                <div
                  key="card-grid"
                  className={`grid grid-flow-row auto-rows-auto my-10 justify-center ${
                    topic == "Researcher" || topic == "Publication"
                      ? "gap-y-10"
                      : "gap-y-20"
                  }`}
                  style={{
                    gridTemplateColumns:
                      "repeat(auto-fill, minmax(270px, 1fr))",
                  }}
                >
                  {data.pages.flatMap((itemArr, pageIndex) =>
                    itemArr.map((item, itemIndex) => {
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
                          : null;

                      return topic !== "Event" && topic !== "Researcher" ? (
                        <NewsCard
                          key={`${pageIndex}-${itemIndex}`}
                          {...item[topic]}
                          type={topic}
                          ID={resolvedID}
                          publicationLink={publicationLink}
                          fullData={item[topic]}
                        />
                      ) : topic === "Researcher" ? (
                        <TeamCard
                          key={`${pageIndex}-${itemIndex}`}
                          {...item[topic]}
                          fullData={item[topic]}
                        />
                      ) : topic === "Event" ? (
                        <div
                          key={`${pageIndex}-${itemIndex}`}
                          className="col-span-full w-full -my-10"
                        >
                          <EventCard {...item[topic]} ID={resolvedID} fullData={item[topic]}/>
                        </div>
                      ) : null;
                    })
                  )}
                </div>
              )
            ) : (
              <div>Loading...</div>
            )}
          </div>
        </div>
      </div>
      {!isError && hasData && hasNextPage && (
        <button
          onClick={() => {
            if (hasNextPage) {
              fetchNextPage();
            }
          }}
          disabled={isFetchingNextPage}
          className={`px-8 py-5 mt-8 w-full text-lg border rounded-2xl border-solid max-md:px-5 max-md:max-w-full transition duration-300 ease-in-out transform ${
            isFetchingNextPage
              ? "bg-gray-400 text-gray-700 cursor-not-allowed"
              : "bg-blue-500 text-white hover:bg-blue-600 hover:scale-105"
          }`}
        >
          {isFetchingNextPage ? "Loading more..." : "Load More"}
        </button>
      )}
    </section>
  );
}

export default GridCards;
