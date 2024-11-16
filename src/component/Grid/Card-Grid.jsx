import React from "react";
import NewsCard from "../Cards/News-Card.jsx";
import previous from "../../resource/previous-button.svg";
import next from "../../resource/next-button.svg";
import ViewAllButton from "../Buttons/View-All-Btn.jsx";
import FilterButton from "../Buttons/Filter-Btn.jsx";
import { useInfiniteFetch } from "api/custom-hooks.js";
import EventCard from "component/Cards/Event-Card.jsx";

function GridCards({ toFetchedData = {}, url = "" }) {
    const recentNewsGridQuery = useInfiniteFetch({
        id: toFetchedData.id,
        url: url,
        pageSize: toFetchedData.pageSize,
    });
    const { data, isLoading, isError } = recentNewsGridQuery;
    const topic = data ? Object.keys(data.pages[0][0])[0] : undefined;

    // Helper function to chunk array into groups of 5
    const chunkArray = (arr, size) => {
        const result = [];
        for (let i = 0; i < arr.length; i += size) {
            result.push(arr.slice(i, i + size));
        }
        return result;
    };

    // Calculate total number of items
    const totalItems = data
        ? data.pages.reduce((acc, page) => acc + page.length, 0)
        : 0;

    return (
        <section className="flex overflow-hidden flex-col px-16 w-full bg-gray-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
            <div className="flex flex-wrap gap-10 justify-between items-end w-full max-md:max-w-full">
                <div className="flex flex-col text-black min-w-[240px] w-[768px] max-md:max-w-full"></div>
                <div className="flex items-center gap-4">
                    <FilterButton className="hover:bg-gray-200 " />
                    <ViewAllButton className="hover:bg-gray-200" />
                </div>
            </div>
            <div className="flex flex-col mt-6 w-full max-md:mt-5 max-md:max-w-full items-center">
                {/* Reduced margin-top */}
                <div className="box-border flex relative flex-col shrink-0">
                    <div className="w-full max-md:max-w-full mt-4">
                        {!isLoading ? (
                            data.pages.map((itemArr, pageIndex) =>
                                chunkArray(itemArr, 4).map((row, rowIndex) => (
                                    <div
                                        key={`${pageIndex}-${rowIndex}`}
                                        className="flex gap-6 mb-6 flex-wrap "
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
                                            return topic !== "Event" ? (
                                                <NewsCard
                                                    key={`${pageIndex}-${rowIndex}-${itemIndex}`}
                                                    {...item[topic]}
                                                    type={topic}
                                                    ID={resolvedID}
                                                    className="shadow-lg rounded-lg p-4"
                                                />
                                            ) : topic === "Event" ? (
                                                <EventCard
                                                    key={`${pageIndex}-${rowIndex}-${itemIndex}`}
                                                    {...item[topic]}
                                                    ID={resolvedID}
                                                    className="shadow-lg rounded-lg p-4"
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
            {!isError && totalItems >= 8 && (
                <button className="px-8 py-5 mt-8 w-full text-lg bg-blue-500 text-white border rounded-2xl  border-solid max-md:px-5 max-md:max-w-full hover:bg-blue-600 transition duration-300 ease-in-out transform hover:scale-105">
                    Load More
                </button>
            )}
            {/* Pagination and navigation controls */}
        </section>
    );
}

export default GridCards;
