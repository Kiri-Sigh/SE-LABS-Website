import { RouterProvider, createBrowserRouter } from "react-router-dom";
import RootLayout from "./routes/root";
import LeadResearcherPage from "./routes/admin/Lead-Researcher-page";
import ResearcherPage from "./routes/admin/Researcher-Page";
import AdminPage from "./routes/admin/Admin-Page";
import DynamicLabPage from "./routes/user/Dynamic-Lab-Page";
import MainPages from "./routes/user/Landing-Page";
import AdminLayout from "./routes/admin/Admin-Layout";
import ErrorPage from "routes/user/Error-Page";
import DynamicNewsPage from "routes/user/Dynamic-News-Page";
import DynamicPeoplePage from "routes/user/Dynamic-People-Page";
import DynamicEventPage from "routes/user/Dynamic-Event-Page";
import DynamicResearchPage from "routes/user/Dynamic-Research-Page";
import Signin from "component/etc/tailgrid/Login_Page";
import ScrollToTop from "component/scroll-to-top";
import OverlayButton from "component/admin-Component/overlay";

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      { index: true, element: <MainPages /> },
      { path: "about", element: <MainPages /> },
      { path: "events", element: <MainPages /> },
      { path: "laboratory", element: <MainPages /> },
      { path: "news", element: <MainPages /> },
      { path: "publications", element: <MainPages /> },
      { path: "research", element: <MainPages /> },
      { path: "people", element: <MainPages /> },
      { path: "laboratory/:id", element: <DynamicLabPage /> },
      { path: "news/:id", element: <DynamicNewsPage /> },
      { path: "event/:id", element: <DynamicEventPage /> },
      { path: "people/:id", element: <DynamicPeoplePage /> },
      { path: "research/:id", element: <DynamicResearchPage /> },
    ],
  },
  {
    path: "/admin",
    element: <AdminLayout />,
    children: [{ index: true, element: <AdminPage /> }],
  },
  { path: "login", element: <Signin /> },
]);

function App() {
  return <RouterProvider router={router}></RouterProvider>;
}

export default App;
//
//add cursor pointer  CSS for link to paths
//
//login
//main page
//when in modal, can preview what it would look like on user page
//modal when create / create commit
//modal when edit (lab only)
//modal when LeadR check commit ()
//
//main page show all related items
//admin-show all lab,research,event,publication,
//leadR-related lab
//normal-related research
//
//create
//admin-create all assign all
//leadR -create all (no assign leadresearcher to UID and no creating lab)
//researcher-create news& event
//
//commit component for admin and leadR
//add a commit navBox
//
//can save progress for create/edit/commit
//when get progress from a floating button on tr , check permission with cached redux UID, if same then show on modal
//when close modal -> immediately cache the closed data to local storage
