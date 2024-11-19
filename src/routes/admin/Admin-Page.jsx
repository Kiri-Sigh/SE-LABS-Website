import React, { useEffect } from "react";
import HeroBox from "../../component/others/Hero/Hero-box";
import RecentNews from "../../component/News/Recent-News/Recent-News";
import RecentEvents from "../../component/Events/Recent-Events/Recent-Events";
import { useLocation, useNavigate } from "react-router-dom";
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
import { useDispatch, useSelector } from "react-redux";
import { useAutoLogin, useGetData, useNormalQueryGet } from "api/custom-hooks";
import { mainAction } from "../../store/main-slice.js";
import { getDataDynamic, postAutoLogin } from "api/api-method";
import Spinner1 from "component/others/spinner";
import DynamicForm from "component/admin-Component/try-form";
import {
  createFrame,
  editFrame,
  submitFrame,
  deleteFrame,
} from "component/admin-Component/Modal/input/frame";

function AdminPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  useEffect(() => {
    dispatch(mainAction.setIsAdminPage());
  }, [dispatch]);
  let highestRole = useSelector((state) => state.mainSlice.highestRole);

  // dispatch(mainAction.setIsAdminPage(true));

  // let fetchedLabData = useSelector((state) => state.mainSlice.fetchedLabData);
  // let isAdmin = useSelector((state) => state.mainSlice.isAdmin);
  // let adminData = useSelector((state) => state.mainSlice.adminData);
  // if (adminData.length === 0) {
  //   //fetch data using token, if not work then send back to login page
  //   //if token expire while create/edit/commit , then will save data bf go to login page
  // }
  // const token = localStorage.getItem("token");
  // const url = "http://127.0.0.1:8000/researcher/researcher/auto_login";
  // const { data, loading, error } = useGetData(url, token);

  const { mutate, isLoading, isError, error, isSuccess, data } = useAutoLogin();

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (token) {
      mutate(token); // Trigger the auto login with the token
    }
  }, [mutate]);
  useEffect(
    () => console.log("autologindata", data),
    [data, isLoading, isError]
  );
  if (!isLoading) console.log("autologindata", data);
  useEffect(() => {
    if (isSuccess) {
      dispatch(mainAction.setAdminData(data));
      dispatch(mainAction.setHighestRole(data?.Researcher.position));
    }
  }, [isSuccess, data, dispatch]);

  useEffect(() => {
    if (error) {
      navigate("/login");
    }
  }, [error, navigate]);

  const { data: labData2 } = useNormalQueryGet(
    "http://127.0.0.1:8000/user/research/thumbnail?amount=3",
    "research"
  );
  const { data: labData3 } = useNormalQueryGet(
    "http://127.0.0.1:8000/user/laboratory/thumbnail?amount=3",
    "laboratory"
  );
  const { data: labData4 } = useNormalQueryGet(
    "http://127.0.0.1:8000/user/news/thumbnail?amount=3",
    "news"
  );
  const { data: labData5 } = useNormalQueryGet(
    "http://127.0.0.1:8000/user/researcher/thumbnail?amount=3",
    "researcher"
  );
  const { data: labData6 } = useNormalQueryGet(
    "http://127.0.0.1:8000/user/publication/thumbnail?amount=3",
    "publication"
  );
  const { data: labData7 } = useNormalQueryGet(
    "http://127.0.0.1:8000/user/event/thumbnail?amount=3",
    "event"
  );
  const { data: labData9 } = useNormalQueryGet(
    "http://127.0.0.1:8000/user/event/thumbnail?event_id=0c186d37-45f8-4767-80bc-c304dfdcc355",
    "event"
  );
  const labData8 = getDataDynamic(
    "http://127.0.0.1:8000/lead_researcher/event/commit",
    localStorage.getItem("token")
  );
  useEffect(() => {
    if (labData2) {
      console.log("research", labData2);
    }
    if (labData3) {
      console.log("lab", labData3);
    }
    if (labData4) {
      console.log("news", labData4);
    }
    if (labData5) {
      console.log("people", labData5);
    }
    if (labData6) {
      console.log("publication", labData6);
    }
    // if (labData8) {
    //   console.log("eventCommit", labData8);
    // }
    if (labData7) {
      console.log("event", labData7);
    }
    if (labData9) {
      console.log("an event", labData9);
    }
  }, [labData2, labData3, labData5, labData4, labData6, labData7, labData9]);
  // const { data: data2 } = useNormalQueryGet(
  //   "http://127.0.0.1:8000/user/news/thumbnail/a163c610-7d14-47c0-8748-a8fea6bc36ee",
  //   "news",
  //   "a163c610-7d14-47c0-8748-a8fea6bc36ee"
  // );
  // React.useEffect(() => {
  //   if (data) {
  //     dispatch(mainAction.setLabData(data));
  //   }
  //   // if (data2) {
  //   //   console.log("data2", data2);
  //   // }
  // }, [data, dispatch]);
  // const labData = useSelector((state) => state.mainSlice.labData);
  // console.log(labData);

  const location = useLocation();
  switch (location.pathname) {
    case "/admin":
      if (highestRole === "Admin") {
        return (
          <>
            <p>admin</p>

            {/* <DynamicForm frame={createFrame.createEvent} />
            <DynamicForm frame={createFrame.createResearch} /> */}
            <DynamicForm frame={submitFrame.submitEvent} />

            {/* <RecentNews toFetchedData={exampleToFetchData.recentNews} />
            <RecentNews toFetchedData={exampleToFetchData.recentResearch} />
            <RecentNews toFetchedData={exampleToFetchData.recentLab} />
            <RecentNews toFetchedData={exampleToFetchData.recentPeople} />
            <RecentNews toFetchedData={exampleToFetchData.recentPublication} />
            <RecentEvents toFetchedData={exampleToFetchData.recentEvents} /> */}
          </>
        );
      } else if (highestRole === "Researcher") {
        return (
          <>
            <p>rsearcher</p>
            <RecentNews
              toFetchedData={exampleToFetchData.recentResearcherResearch}
            />
          </>
        );
      } else if (highestRole === "LeadResearcher") {
        return (
          <>
            <p>leadR</p>
            <RecentNews
              toFetchedData={exampleToFetchData.recentResearcherLab}
            />
            <RecentEvents
              toFetchedData={exampleToFetchData.recentResearcherResearch}
            />
          </>
        );
      } else if (highestRole === "Free") {
        return (
          <>
            <p>no affiliation</p>
          </>
        );
      } else {
        return <Spinner1 />;
      }

    case "/admin/about":
      return (
        <>
          <TopicAndImage />
          <AboutDescription />
          <RecentNews toFetchedData={exampleToFetchData.recentNews} />
          <RecentEvents toFetchedData={exampleToFetchData.recentEvents} />
        </>
      );
    case "/admin/events":
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
    case "/admin/news":
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
    case "/admin/publications":
      return (
        <>
          <TopicHeaderText topic="Publications" />
          <GridCards
            toFetchedData={exampleToFetchData.recentGridNews}
            url="http://127.0.0.1:8000/user/publication/thumbnail?"
            fetchedLabData={labData}
            useFilterButton={true}
            publicationLink={"https://www.se.kmitl.ac.th/"}
          />
        </>
      );
    case "/admin/research":
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
    case "/admin/laboratory":
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
    case "/admin/people":
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
    case "/admin/commit":
      return (
        <>
          <TopicHeaderText topic="Commit" />
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
export default AdminPage;
