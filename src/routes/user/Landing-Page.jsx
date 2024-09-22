import React from "react";
import HeroBox from "../../component/others/Hero/Hero-box";
import RecentNews from "../../component/News/Recent-News/Recent-News";
import RecentEvents from "../../component/Events/Recent-Events/Recent-Events";
import { useLocation } from "react-router-dom";
import AboutDescription from "../../component/Description/About-Description/About-Description";
import TopicAndImage from "../../component/others/Big-Image/Topic-And-Image";
import { eventItems, newsItems } from "../../PlaceHolder-Data/data";
function MainPages() {
  const location = useLocation();
  switch (location.pathname) {
    case "/":
      return (
        <>
          <HeroBox />
          <RecentNews newsItems={newsItems} />
          <RecentEvents eventItems={eventItems} />
        </>
      );
    case "/about":
      return (
        <>
          <TopicAndImage />
          <AboutDescription />
          <RecentNews newsItems={newsItems} />
          <RecentEvents eventItems={eventItems} />
        </>
      );
    case "/events":
      return <></>;
    case "/news":
      return <></>;
    case "/publications":
      return <></>;
    case "/research":
      return <></>;
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
