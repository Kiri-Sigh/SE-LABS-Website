import { RouterProvider, createBrowserRouter } from "react-router-dom";
import RootLayout from "./routes/user/root";
import LandingPage from "./routes/user/Landing-Page";
import AboutPage from "./routes/user/About-Page";
import LeadResearcherPage from "./routes/admin/Lead-Researcher-page";
import ResearcherPage from "./routes/admin/Researcher-Page";
import AdminPage from "./routes/admin/Admin-Page";
import "./App.css";
import PublicationsPage from "./routes/user/Publications-Page";
const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    //errorElement: <ErrorPage />,
    children: [
      { index: true, element: <LandingPage /> },
      { path: "about", element: <AboutPage /> },
      { path: "events" },
      { path: "labs" },
      { path: "news" },
      { path: "publications", element: <PublicationsPage /> },
      { path: "research" },
      { path: "events" },
      { path: "people" },
    ],
  },
  { path: "admin", element: <AdminPage /> },
  { path: "researcher", element: <ResearcherPage /> },
  { path: "lead-researcher", element: <LeadResearcherPage /> },
  { path: "login" },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;

// const router = createBrowserRouter([
//   {
//     path: "/",
//     element: <RootLayout />,
//     errorElement: <ErrorPage />,
//     children: [
//       { index: true, element: <HomePage /> },
//       {
//         path: "events",
//         element: <EventsRootLayout />,
//         children: [
//           {
//             index: true,
//             element: <EventsPage />,
//             loader: eventsLoader,
//           },
//           {
//             path: ":eventId",
//             id: "event-detail",
//             loader: eventDetailLoader,
//             children: [
//               {
//                 index: true,
//                 element: <EventDetailPage />,
//                 action: deleteEventAction,
//               },
//               {
//                 path: "edit",
//                 element: <EditEventPage />,
//                 action: manipulateEventAction,
//               },
//             ],
//           },
//           {
//             path: "new",
//             element: <NewEventPage />,
//             action: manipulateEventAction,
//           },
//         ],
//       },
//       {
//         path: "newsletter",
//         element: <NewsletterPage />,
//         action: newsletterAction,
//       },
//     ],
//   },
// ]);
