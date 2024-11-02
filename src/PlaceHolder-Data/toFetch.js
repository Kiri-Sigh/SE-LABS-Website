export const exampleToFetchData = {
  recentNews: {
    id: "abc",
    url: "http://127.0.0.1:8000/user/event/thumbnail",
    // type: "n",
    pageSize: 3,
  },
  recentEvents: {
    id: "abc",
    url: "http://127.0.0.1:8000/user/event/thumbnail",
    pageSize: 3,
  },
  recentLabNews: {
    id: "abc",
    url: "http://127.0.0.1:8000/user/new/thumbnail",
    pageSize: 3,
    param: { laboratory_id: "" },
  },
  recentLabEvents: {
    id: "abc",
    url: "http://127.0.0.1:8000/user/event/thumbnail",
    pageSize: 3,
    param: { laboratory_id: "", research_id: "" },
  },
};
