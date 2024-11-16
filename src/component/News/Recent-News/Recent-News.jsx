import React, { useState } from "react";
import NewsCard from "../../Cards/News-Card";
import { useInfiniteFetch } from "../../../api/custom-hooks";
import previous from "../../../resource/previous-button.svg";
import next from "../../../resource/next-button.svg";

import { getData, getImgData } from "../../../api/api-method";
import TeamCard from "component/Cards/Team-Card";
import { useSelector } from "react-redux";
function RecentNews({
    toFetchedData = {},
    filter = {},
    componentTitle = "recentNewsComp",
    useFilterButton = false,
    fetchedLabData = null,
    publicationLink = null,
}) {
    //main data = { data, fetchNextPage, hasNextPage, isFetchingNextPage, isLoading, error }

    const recentNewsQuery = useInfiniteFetch({
        id: toFetchedData.id,
        url: toFetchedData.url,
        pageSize: toFetchedData.pageSize,
        filter,
    });

    // const recentLabQuery = useInfiniteFetch({
    //   id: "labResearchers",
    //   url: "http://127.0.0.1:8000/user/researcher/thumbnail?",
    //   pageSize: 4,
    //   filter: { laboratory_id: "a45a9657-34db-40b7-98bf-b5f2764055b4" },
    // });
    // const { data: data2 } = recentLabQuery;

    // if (data2) console.log("labnesdata=", data2);

    // async function testGetData() {
    //   try {
    //     const url = "http://127.0.0.1:8000/user/researcher/thumbnail"; // Replace with your actual API
    //     const data = await getData(url);
    //     console.log("Fetched test Data:", data);
    //   } catch (error) {
    //     console.error("Error fetching data:", error);
    //   }
    // }

    // testGetData();

    const { data, isLoading, isError } = recentNewsQuery;
    if (data) console.log("data:", data);
    const topic = data?.pages?.[0]?.[0]
        ? Object.keys(data.pages[0][0])[0]
        : null;
    // const topic = firstItem ? Object.keys(firstItem)[0] : [];
    // const [imgs, setImg] = useState(null);
    // const img = getData(
    //   "http://127.0.0.1:8000/user/news/image-high?news_id=f6eb2c3f-efcd-4cd0-842f-05f746bf4b7b"
    // );

    const [pageIndex, setPageIndex] = useState(0);

    const fetchPreviousPage = async () => {
        // Implement the logic to fetch the previous page
    };

    const handleNextPage = async () => {
        // Implement the logic to fetch the next page
        setPageIndex(pageIndex + 1);
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
                        {componentTitle}
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
                            data.pages[0].map((item, index) => {
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

                                return topic !== "Event" &&
                                    topic !== "Researcher" ? (
                                    <NewsCard
                                        key={`${index}`}
                                        {...item[topic]}
                                        type={`${topic}`}
                                        ID={resolvedID}
                                        publicationLink={publicationLink}
                                    />
                                ) : topic === "Researcher" ? (
                                    <TeamCard
                                        key={`researcher-${index}-${filter.laboratory_id}`}
                                        {...item[topic]}
                                    />
                                ) : null;
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
                                disabled={
                                    data && data.pages.length <= pageIndex + 1
                                }
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
