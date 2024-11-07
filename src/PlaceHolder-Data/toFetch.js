export const exampleToFetchData = {
  recentNews: {
    id: "recentNews",
    url: "http://127.0.0.1:8000/user/news/thumbnail?",
    // type: "n",
    pageSize: 5,
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
  postNews: {
    title: "str",
    body: "str",
    related_laboratory: {
      LID: "str",
      related_research: {
        RID: "str",
      },
    },
  },
};
