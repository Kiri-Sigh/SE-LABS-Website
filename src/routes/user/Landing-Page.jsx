import React from "react";
import HeroBox from "../../component/others/Hero/Hero-box";
import RecentNews from "../../component/News/Recent-News/Recent-News";
import RecentEvents from "../../component/Events/Recent-Events/Recent-Events";
import { useLocation } from "react-router-dom";
import AboutDescription from "../../component/Description/About-Description/About-Description";
import TopicAndImage from "../../component/others/Big-Image/Topic-And-Image";
import { eventItems, labData, newsItems } from "../../PlaceHolder-Data/data";
import TopicHeaderText from "../../component/Topic-Header";
import GridCards from "../../component/Grid/Card-Grid";
import DividingRows from "../../component/admin-Component/tables/proto1/table";
import Modals from "../../component/admin-Component/Modal/Modal";
import TableComponent from "../../component/admin-Component/tables/proto2/table-try";
// import { getData } from "../../api/api-method";
// import axios from "axios";
// import { DataFetcherQueue } from "./fetches/fetch-dynamic-page";
import { exampleToFetchData } from "../../PlaceHolder-Data/toFetch";
import MyFormComponent from "../../component/etc/exampleForm";
import LoginComp from "component/etc/example-login";
import CSSTailwind from "./CSS-Tailwind-Page";
function MainPages() {
    // axios
    //   .get(
    //     "http://127.0.0.1:8000/user/event/thumbnail?laboratory_id=ad7edead-e775-48df-bde7-7f334c8c0980"
    //   )
    //   .then((response) => {
    //     console.log(response.data);
    //   });

    // console.log(
    //   getData(
    //     "http://localhost:8000/user/event/thumbnail?laboratory_id=ad7edead-e775-48df-bde7-7f334c8c0980"
    //   )
    // );
    // const a = [
    //   [
    //     {
    //       id: "abc",
    //       url: "http://127.0.0.1:8000/user/event/thumbnail?laboratory_id=ad7edead-e775-48df-bde7-7f334c8c0980",
    //       type: "n",
    //     },
    //     {
    //       id: "jsf",
    //       url: "http://127.0.0.1:8000/user/event/thumbnail?laboratory_id=ad7edead-e775-48df-bde7-7f334c8c0980",
    //       type: "n",
    //     },
    //     {
    //       id: "jpj",
    //       url: "http://127.0.0.1:8000/user/event/thumbnail?laboratory_id=ad7edead-e775-48df-bde7-7f334c8c0980",
    //       type: "n",
    //     },
    //   ],
    //   [
    //     {
    //       id: "oijf",
    //       url: "http://127.0.0.1:8000/user/event/thumbnail?laboratory_id=ad7edead-e775-48df-bde7-7f334c8c0980",
    //       type: "n",
    //     },
    //     {
    //       id: "asd",
    //       url: "http://127.0.0.1:8000/user/event/thumbnail?laboratory_id=ad7edead-e775-48df-bde7-7f334c8c0980",
    //       type: "n",
    //     },
    //   ],
    // ];
    // console.log(DataFetcherQueue(a));
    const location = useLocation();
    switch (location.pathname) {
        // case "/":
        //   return (
        //     <>
        //       <Modals />
        //       <LoginComp />
        //       <MyFormComponent />
        //       <TableComponent />
        //       <HeroBox />
        //       <DividingRows />
        //       <RecentNews
        //         toFetchedData={exampleToFetchData.recentNews}
        //         topic="news"
        //       />
        //       <RecentEvents
        //         toFetchedData={exampleToFetchData.recentEvents}
        //         topic="events"
        //       />
        //     </>
        //   );
        case "/":
            return (
                <>
                    <CSSTailwind />
                </>
            );

        case "/about":
            return (
                <>
                    <TopicAndImage />
                    <AboutDescription />
                    <RecentNews toFetchedData={exampleToFetchData.recentNews} />
                    <RecentEvents
                        toFetchedData={exampleToFetchData.recentEvents}
                        listData={eventItems}
                        topic="events"
                    />
                </>
            );
        case "/events":
            return (
                <>
                    <TopicHeaderText topic="Events" />
                    <GridCards
                        toFetchedData={exampleToFetchData.recentGridEvents}
                        topic="events"
                        url="http://127.0.0.1:8000/user/event/thumbnail?"
                    />
                </>
            );
        case "/news":
            return (
                <>
                    <TopicHeaderText topic="News" />
                    <GridCards
                        toFetchedData={exampleToFetchData.recentGridNews}
                        topic="news"
                        url="http://127.0.0.1:8000/user/news/thumbnail?"
                    />
                </>
            );
        case "/publications":
            return (
                <>
                    <TopicHeaderText topic="Publications" />
                    <GridCards
                        toFetchedData={exampleToFetchData.recentGridNews}
                        url="http://127.0.0.1:8000/user/publication/thumbnail?"
                    />
                </>
            );
        case "/research":
            return (
                <>
                    <TopicHeaderText topic="Research" />
                    <GridCards
                        toFetchedData={exampleToFetchData.recentGridResearch}
                        url="http://127.0.0.1:8000/user/research/thumbnail?"
                    />
                </>
            );
        case "/laboratory":
            return (
                <>
                    <TopicHeaderText topic="Laboratory" />
                    <GridCards
                        toFetchedData={exampleToFetchData.recentGridLaboratory}
                        url="http://127.0.0.1:8000/user/laboratory/thumbnail?"
                    />
                </>
            );
        default:
            <></>;
    }
    // { index: true, element: <MainPages /> },
    // { path: "about", element: <MainPages /> },
    // { path: "events", element: <MainPages /> },
    // { path: "labs", element: <MainPages /> },
    // { path: "news", element: <MainPages /> },
    // { path: "publications", element: <MainPages /> },
    // { path: "research", element: <MainPages /> },
    // { path: "events", element: <MainPages /> },
    // { path: "people", element: <MainPages /> },
    // { path: "labs/:labID", element: <DynamicLabPage /> },
}
export default MainPages;
