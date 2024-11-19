import React from "react";
import NewsCard from "../Cards/News-Card.jsx";
import ViewAllButton from "../Buttons/View-All-Btn.jsx";
import FilterButton from "../Buttons/Filter-Btn.jsx";
import { useInfiniteFetch } from "api/custom-hooks.js";
import EventCard from "component/Cards/Event-Card.jsx";
import TeamCard from "component/Cards/Team-Card.jsx";
import WhiteRoundedButton from "component/etc/tailgrid/buttonX.jsx";

function GridCards({
  toFetchedData = {},
  url = "",
  filter = null,
  useFilterButton = false,
  fetchedLabData = [],
  publicationLink = null,
}) {
  const [selectedLab, setSelectedLab] = React.useState(null);
  console.log("selected", selectedLab);
  if (selectedLab) filter = { laboratory_id: selectedLab.Laboratory.LID };
  const recentNewsGridQuery = useInfiniteFetch({
    id: toFetchedData.id,
    url: url,
    pageSize: toFetchedData.pageSize,
    filter,
  });

  const { data, isLoading, isError, fetchNextPage, isFetchingNextPage } =
    recentNewsGridQuery;

  const topic = data?.pages?.[0]?.[0]
    ? Object.keys(data.pages[0][0])[0]
    : undefined;
  const hasData =
    data && data.pages && data.pages.some((page) => page.length > 0);

  const handleLabChange = (event) => {
    setSelectedLab(event);
  };

  const chunkArray = (arr, size) => {
    const result = [];
    for (let i = 0; i < arr.length; i += size) {
      result.push(arr.slice(i, i + size));
    }
    return result;
  };

  const isDataEmpty =
    !data || data.pages.length === 0 || data.pages[0].length === 0;

  return (
    <section className="flex overflow-hidden flex-col px-16 py-28 w-full bg-gray-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
      <div className="flex flex-wrap gap-10 justify-between items-end w-full max-md:max-w-full">
        <div className="flex flex-col text-black min-w-[240px] w-[768px] max-md:max-w-full"></div>
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
                data.pages.map((itemArr, pageIndex) =>
                  chunkArray(itemArr, 4).map((row, rowIndex) => (
                    <div
                      key={`${pageIndex}-${rowIndex}`}
                      className="flex gap-4 mb-6 flex-wrap"
                    >
                      {row.map((item, itemIndex) => {
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
                            key={`${pageIndex}-${rowIndex}-${itemIndex}`}
                            {...item[topic]}
                            type={topic}
                            ID={resolvedID}
                            publicationLink={publicationLink}
                          />
                        ) : topic === "Researcher" ? (
                          <TeamCard
                            key={`${pageIndex}-${rowIndex}-${itemIndex}`}
                            {...item[topic]}
                          />
                        ) : topic === "Event" ? (
                          <EventCard
                            key={`${pageIndex}-${rowIndex}-${itemIndex}`}
                            {...item[topic]}
                            ID={resolvedID}
                          />
                        ) : null;
                      })}
                    </div>
                  ))
                )
              )
            ) : (
              <div>Loading...</div>
            )}
          </div>
        </div>
      </div>
      {!isError && hasData && (
        <button
          onClick={() => {
            console.log("clicked");
            fetchNextPage();
          }}
          disabled={isFetchingNextPage}
          className="px-8 py-5 mt-8 w-full text-lg bg-blue-500 text-white border rounded-2xl border-solid max-md:px-5 max-md:max-w-full hover:bg-blue-600 transition duration-300 ease-in-out transform hover:scale-105"
        >
          {isFetchingNextPage ? "Loading more..." : "Load More"}
        </button>
      )}
    </section>
  );
}

export default GridCards;
