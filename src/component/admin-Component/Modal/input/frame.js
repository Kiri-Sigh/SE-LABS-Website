//u = textArea
//research-free = research with null key of LabID
//global = global news/events with no relation with any labs/research

export const editFrame = {
  //ok
  editLab: {
    type: "patch",
    param: [
      { key: "laboratory", LID: "text", title: "text", body: "textArea" },
      { laboratory_id: "text" },
    ],
    body: [{ image: "file" }],
    url: "http://10.125.2.83:8000/lead_researcher/laboratory",
  },
  //ok
  editResearch: {
    type: "patch",
    param: [{ laboratory_id: "text" }],
    body: [
      {
        key: "research",
        RID: "text",
        title: "text",
        body: "textArea",
        related_laboratory: true,
      },
      { image: "file" },
    ],
    url: "http://10.125.2.83:8000/lead_researcher/research",
  },
  //ok
  putResearchToPublication: {
    type: "put",
    param: [
      { research_id: "text" },
      { url: "text" },
      { laboratory_id: "text" },
    ],

    url: "http://10.125.2.83:8000/lead_researcher/research",
  },
  //ok
  assignToResearch: {
    type: "patch",
    param: [
      { researcher_id: "text" },
      { research_id: "text" },
      { laboratory_id: "text" },
    ],

    url: "http://10.125.2.83:8000/lead_researcher/researcher",
  },
  //ok
  assignAsLeadR: {
    type: "patch",
    param: [{ researcher_id: "text" }, { laboratory_id: "text" }],

    url: "http://10.125.2.83:8000/admin/researcher",
  },
  //ok
  editPublication: {
    type: "patch",
    param: [
      {
        key: "publication",
        PID: "research_id",
        title: "text",
        body: "text",
        link: "text",
      },
      { laboratory_id: "text" },
    ],
    body: [{ image: "file" }],
    url: "http://10.125.2.83:8000/lead_researcher/publication",
  },
};

export const createFrame = {
  //ok
  createLab: {
    type: "post",
    param: [
      {
        key: "laboratory",
        title: "text",

        body: "textArea",
      },
    ],
    body: [{ image: "file" }],
    url: "http://10.125.2.83:8000/admin/laboratory",
  },
  //ok
  createNews: {
    type: "post",
    param: [{ research_id: "text" }, { laboratory_id: "text" }],

    body: [
      {
        key: "news",
        title: "text",

        body: "textArea",
        related_laboratory: true,
      },
      { image: "file" },
    ],
    url: "http://10.125.2.83:8000/researcher/news",
  },
  //ok
  createEvent: {
    type: "post",
    param: [{ research_id: "text" }, { laboratory_id: "text" }],

    body: [
      {
        key: "event",
        title: "text",
        body: "textArea",
        location: "text",
        start: "text",
        end: "text",
        related_laboratory: "huh",
      },
      { image: "file" },
    ],
    url: "http://10.125.2.83:8000/researcher/event",
  },
  //ok
  createResearch: {
    type: "post",
    param: [{ laboratory_id: "text" }],

    body: [
      {
        key: "research",
        title: "text",
        body: "textArea",

        related_laboratory: true,
      },
      { image: "file" },
    ],
    url: "http://10.125.2.83:8000/lead_researcher/research",
  },
  //ok
  createPeople: {
    type: "post",
    param: [
      { key: "researcher", password: "text", name: "text", mail: "string" },
      { laboratory_id: "text" },
    ],

    body: [{ image: "file" }],
    url: "http://10.125.2.83:8000/lead_researcher/researcher",
  },
};

export const submitFrame = {
  //unautherized
  submitEvent: {
    type: "patch",
    param: [{ event_id: "text" }, { is_approved: "checkbox" }],

    url: "http://10.125.2.83:8000/lead_researcher/event",
  },
  submitNews: {
    type: "patch",
    param: [{ news_id: "text" }, { is_approved: "checkbox" }],

    url: "http://10.125.2.83:8000/lead_researcher/news",
  },
};
export const deleteFrame = {
  deleteEvent: {
    type: "delete",
    param: [{ event_id: "text" }],

    url: "http://10.125.2.83:8000/lead_researcher/event",
  },
  deleteNews: {
    type: "delete",
    param: [{ news_id: "text" }],

    url: "http://10.125.2.83:8000/lead_researcher/news",
  },
  deleteLab: {
    type: "delete",
    param: [{ laboratory_id: "text" }],

    url: "http://10.125.2.83:8000/admin/laboratory",
  },
  deletePublication: {
    type: "delete",
    param: [{ publication_id: "text" }],

    url: "http://10.125.2.83:8000/lead_researcher/publication",
  },
  deleteResearch: {
    type: "delete",
    param: [{ research_id: "text" }],

    url: "http://10.125.2.83:8000/lead_researcher/research",
  },
  kickFromResearch: {
    type: "delete",
    param: [{ researcher_id: "text" }, { research_id: "text" }],

    url: "http://10.125.2.83:8000/lead_researcher/researcher",
  },
  removeLeadResearcher: {
    type: "delete",
    param: [{ researcher_id: "text" }],

    url: "http://10.125.2.83:8000/admin/researcher",
  },
};
