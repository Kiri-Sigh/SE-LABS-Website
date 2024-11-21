import React from "react";
import HeroBox from "../../component/others/Hero/Hero-box";
import RecentNews from "../../component/News/Recent-News/Recent-News";
import RecentEvents from "../../component/Events/Recent-Events/Recent-Events";
import { useLocation } from "react-router-dom";
import AboutDescription from "../../component/Description/About-Description/About-Description";
import About_Title from "component/Description/About-Description/About-Title";
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

import { useDispatch, useSelector } from "react-redux";
import { useNormalQueryGet } from "api/custom-hooks";
import { mainAction } from "../../store/main-slice.js";

function MainPages() {
  const dispatch = useDispatch();

  let fetchedLabData = useSelector((state) => state.mainSlice.fetchedLabData);

  const { data } = useNormalQueryGet(
    "http://127.0.0.1:8000/user/laboratory/thumbnail?amount=10",
    "laboratory"
  );
  // const { data: data2 } = useNormalQueryGet(
  //   "http://127.0.0.1:8000/user/news/thumbnail/a163c610-7d14-47c0-8748-a8fea6bc36ee",
  //   "news",
  //   "a163c610-7d14-47c0-8748-a8fea6bc36ee"
  //   );
  React.useEffect(() => {
    if (data) {
      dispatch(mainAction.setLabData(data));
    }
    // if (data2) {
    //   console.log("data2", data2);
    // }
  }, [data, dispatch]);
  const labData = useSelector((state) => state.mainSlice.labData);
  console.log(labData);
  const location = useLocation();
  switch (location.pathname) {
    case "/":
      return (
        <>
          {/* <Modals />
          <LoginComp />
          <MyFormComponent />
          <TableComponent /> */}
          <HeroBox />
          {/* <DividingRows /> */}
          <RecentNews toFetchedData={exampleToFetchData.recentNews} />
          <RecentEvents toFetchedData={exampleToFetchData.recentEvents} />
        </>
      );
    case "/about":
      return (
        <>
          <About_Title />
          <AboutDescription />
          <RecentNews toFetchedData={exampleToFetchData.recentNews} />
          <RecentEvents toFetchedData={exampleToFetchData.recentEvents} />
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
            fetchedLabData={labData}
            useFilterButton={true}
          />
        </>
      );
    case "/news":
      return (
        <>
          <TopicHeaderText topic="News" />
          <GridCards
            toFetchedData={exampleToFetchData.recentGridNews}
            url="http://127.0.0.1:8000/user/news/thumbnail?"
            fetchedLabData={labData}
            useFilterButton={true}
          />
        </>
      );
    case "/publications":
      return (
        <>
          <TopicHeaderText topic="Publications" />
          <GridCards
            toFetchedData={exampleToFetchData.recentGridPublication}
            url="http://127.0.0.1:8000/user/publication/thumbnail?"
            fetchedLabData={labData}
            useFilterButton={true}
            publicationLink={"https://www.se.kmitl.ac.th/"}
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
            fetchedLabData={labData}
            useFilterButton={true}
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
            fetchedLabData={labData}
            useFilterButton={true}
          />
        </>
      );
    case "/people":
      return (
        <>
          <TopicHeaderText topic="People" />
          <GridCards
            toFetchedData={exampleToFetchData.recentGridResearcher}
            url="http://127.0.0.1:8000/user/researcher/thumbnail?"
            fetchedLabData={labData}
            useFilterButton={true}
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
