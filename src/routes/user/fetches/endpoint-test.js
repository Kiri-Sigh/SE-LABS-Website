const token = "abc";
const everyEndpointREquestResponse = [
  {
    url: "http://localhost/8000/user/event/thumbnail?laboratory_id=LID&amount=4&page=2",
    header: null,
    body: null,
    response: [
      {
        Event: {
          EID: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          title: "string",
          body: "string",
          location: "string",
          start: "2024-10-20T05:01:56.852Z",
          end: "2024-10-20T05:01:56.852Z",
          status: "Coming",
          related_laboratory: {
            LID: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            title: "string",
            related_research: {
              RID: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              title: "string",
            },
            related_publication: {
              PID: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              title: "string",
            },
          },
        },
      },
    ],
  },
  {
    url: "http://localhost/8000/user/event/thumbnail?research_id=RID&amount=4",
    header: "",
    body: {},
    response: {},
  },
  {
    url: "http://localhost/8000/token",
    header: null,
    body: { username: "string", password: "string" },
    response: {
      access_token: "string",
      token_type: "string",
    },
  },
  { url: "http://localhost/8000/", header: "", body: {}, response: {} },
  { url: "http://localhost/8000/", header: "", body: {}, response: {} },
  { url: "http://localhost/8000/", header: "", body: {}, response: {} },
  { url: "http://localhost/8000/", header: "", body: {}, response: {} },
  { url: "http://localhost/8000/", header: "", body: {}, response: {} },
  { url: "http://localhost/8000/", header: "", body: {}, response: {} },
  { url: "http://localhost/8000/", header: "", body: {}, response: {} },
];
