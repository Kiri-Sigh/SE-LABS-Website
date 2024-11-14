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
const CSSTailwind = () => {
  return (
    <>
      <Modals />
      {/* <LoginComp /> */}
      {/* <MyFormComponent /> */}
      {/* <TableComponent /> */}
      <TopicAndImage />

      <AboutDescription />

      <HeroBox />
      {/* <DividingRows /> */}
      <RecentNews toFetchedData={exampleToFetchData.recentNews} />
      <RecentEvents
        toFetchedData={exampleToFetchData.recentEvents}
        topic="events"
      />
      <TopicHeaderText topic="Events" />
      <GridCards
        toFetchedData={exampleToFetchData.recentGridEvents}
        topic="events"
        url="http://127.0.0.1:8000/user/event/thumbnail?"
      />
      <TopicHeaderText topic="News" />
      <GridCards
        toFetchedData={exampleToFetchData.recentGridNews}
        topic="news"
        url="http://127.0.0.1:8000/user/news/thumbnail?"
      />
      <TopicHeaderText topic="Publications" />
      <GridCards
        toFetchedData={exampleToFetchData.recentGridNews}
        url="http://127.0.0.1:8000/user/publication/thumbnail?"
      />
      <TopicHeaderText topic="Laboratory" />
      <GridCards
        toFetchedData={exampleToFetchData.recentGridLaboratory}
        url="http://127.0.0.1:8000/user/laboratory/thumbnail?"
      />
    </>
  );
};
export default CSSTailwind;
