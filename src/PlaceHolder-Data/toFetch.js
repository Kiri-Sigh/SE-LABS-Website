export const exampleToFetchData = {
  recentNewsCommit: {
    id: "recentNewsCommit",
    url: "http://10.125.2.83:8000/lead_researcher/news/commit?",
    // type: "n",
    pageSize: 5,
  },
  recentEventCommit: {
    id: "recentEventCommit",
    url: "http://10.125.2.83:8000/lead_researcher/event/commit?",
    // type: "n",
    pageSize: 3,
  },
  recentNews: {
    id: "recentNews",
    url: "http://10.125.2.83:8000/user/news/thumbnail?",
    // type: "n",
    pageSize: 5,
  },
  recentEvents: {
    id: "recentEvents",
    url: "http://10.125.2.83:8000/user/event/thumbnail?",
    pageSize: 3,
  },
  recentLab: {
    id: "recentLab",
    url: "http://10.125.2.83:8000/user/laboratory/thumbnail?",
    pageSize: 5,
  },
  recentPublication: {
    id: "recentPublication",
    url: "http://10.125.2.83:8000/user/publication/thumbnail?",
    pageSize: 5,
  },
  recentResearch: {
    id: "recentResearch",
    url: "http://10.125.2.83:8000/user/research/thumbnail?",
    pageSize: 5,
  },
  recentPeople: {
    id: "recentPeople",
    url: "http://10.125.2.83:8000/user/researcher/thumbnail?",
    pageSize: 5,
  },
  recentLabNews: {
    id: "labNews",
    url: "http://10.125.2.83:8000/user/news/thumbnail?",
    pageSize: 5,
    param: {}, //laboratory_id
  },
  recentLabEvent: {
    id: "labEvent",
    url: "http://10.125.2.83:8000/user/event/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id,research_id
  },
  recentLabPublication: {
    id: "labPublication",
    url: "http://10.125.2.83:8000/user/publication/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentLabResearch: {
    id: "labResearch",
    url: "http://10.125.2.83:8000/user/research/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentNewsLaboratory: {
    id: "newsLaboratory",
    url: "http://10.125.2.83:8000/user/laboratory/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentNewsResearch: {
    id: "newsResearch",
    url: "http://10.125.2.83:8000/user/research/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentLabResearcher: {
    id: "labResearcher",
    url: "http://10.125.2.83:8000/user/researcher/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentResearcherLab: {
    id: "researcherLab",
    url: "http://10.125.2.83:8000/user/laboratory/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentResearcherResearch: {
    id: "researcherResearch",
    url: "http://10.125.2.83:8000/user/research/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentResearchResearcher: {
    id: "researchResearcher",
    url: "http://10.125.2.83:8000/user/researcher/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentResearchNews: {
    id: "researchNews",
    url: "http://10.125.2.83:8000/user/news/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentResearchEvent: {
    id: "researchEvent",
    url: "http://10.125.2.83:8000/user/event/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
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
  recentGridNews: {
    id: "recentGridNews",
    // type: "n",
    pageSize: 8,
  },
  recentGridEvents: {
    id: "recentGridEvents",
    // type: "n",
    pageSize: 8,
  },
  recentGridLaboratory: {
    id: "recentGridLaboratory",
    // type: "n",
    pageSize: 4,
  },
  recentGridResearcher: {
    id: "recentGridResearcher",
    // type: "n",
    pageSize: 8,
  },
  recentGridPublication: {
    id: "recentGridPublication",
    // type: "n",
    pageSize: 8,
  },
  recentGridResearch: {
    id: "recentGridResearch",
    // type: "n",
    pageSize: 8,
  },
  relatedNews: {
    id: "relatedNews",
    url: "http://10.125.2.83:8000/user/news/related_news?",
    // type: "n",
    pageSize: 4,
  },
  editLab: {},
  createNews: {},
  createResearch: {},
};
