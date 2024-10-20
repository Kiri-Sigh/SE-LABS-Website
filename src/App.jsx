import { RouterProvider, createBrowserRouter } from "react-router-dom";
import RootLayout from "./routes/root";
import LeadResearcherPage from "./routes/admin/Lead-Researcher-page";
import ResearcherPage from "./routes/admin/Researcher-Page";
import AdminPage from "./routes/admin/Admin-Page";
import DynamicLabPage from "./routes/user/Dynamic-Lab-Page";
import MainPages from "./routes/user/Landing-Page";
import AdminLayout from "./routes/admin/Admin-Layout";
const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    //errorElement: <ErrorPage />,
    children: [
      { index: true, element: <MainPages /> },
      { path: "about", element: <MainPages /> },
      { path: "events", element: <MainPages /> },
      { path: "labs", element: <MainPages /> },
      { path: "news", element: <MainPages /> },
      { path: "publications", element: <MainPages /> },
      { path: "research", element: <MainPages /> },
      { path: "events", element: <MainPages /> },
      { path: "people", element: <MainPages /> },
      { path: "labs/:labID", element: <DynamicLabPage /> },
    ],
  },
  {
    path: "admin",
    element: <AdminLayout />,
    children: [
      { index: true, element: <AdminPage /> },
      // { path: "researcher", element: <ResearcherPage /> },
      // { path: "lead-researcher", element: <LeadResearcherPage /> },
    ],
  },
  // { path: "login", element:<LoginPage/>},
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
