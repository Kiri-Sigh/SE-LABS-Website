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
    case "/":
      return (
        <>
          <Modals />
          <TableComponent />
          <HeroBox />
          <DividingRows />

          <RecentNews
            toFetchedData={exampleToFetchData.recentNews}
            topic="news"
            rowData={newsItems}
          />
          <RecentEvents listData={eventItems} topic="events" />
        </>
      );
    case "/about":
      return (
        <>
          <TopicAndImage />
          <AboutDescription />
          <RecentNews rowData={newsItems} topic="news" />
          <RecentEvents listData={eventItems} topic="events" />
        </>
      );
    case "/events":
      return (
        <>
          <TopicHeaderText topic="Events" />
          <GridCards rowData={newsItems} />
        </>
      );
    case "/news":
      return (
        <>
          <TopicHeaderText topic="News" />
          <GridCards rowData={newsItems} />
        </>
      );
    case "/publications":
      return (
        <>
          <TopicHeaderText topic="Publications" />
          <GridCards rowData={newsItems} />
        </>
      );
    case "/research":
      return (
        <>
          <TopicHeaderText topic="Research" />
          <GridCards rowData={newsItems} />
        </>
      );
    case "/labs":
      return (
        <>
          <TopicHeaderText topic="Labs" />
          <GridCards rowData={newsItems} />
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
