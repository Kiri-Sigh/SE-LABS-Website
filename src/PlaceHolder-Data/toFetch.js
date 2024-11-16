export const exampleToFetchData = {
  recentNews: {
    id: "recentNews",
    url: "http://127.0.0.1:8000/user/news/thumbnail?",
    // type: "n",
    pageSize: 5,
  },
  recentEvents: {
    id: "recentEvents",
    url: "http://127.0.0.1:8000/user/event/thumbnail?",
    pageSize: 3,
  },
  recentLabNews: {
    id: "labNews",
    url: "http://127.0.0.1:8000/user/news/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id
  },
  recentLabEvent: {
    id: "labEvent",
    url: "http://127.0.0.1:8000/user/event/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id,research_id
  },
  recentLabPublication: {
    id: "labPublication",
    url: "http://127.0.0.1:8000/user/publication/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentLabResearch: {
    id: "labResearch",
    url: "http://127.0.0.1:8000/user/research/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentNewsLaboratory: {
    id: "newsLaboratory",
    url: "http://127.0.0.1:8000/user/laboratory/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentNewsResearch: {
    id: "newsResearch",
    url: "http://127.0.0.1:8000/user/research/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentLabResearcher: {
    id: "labResearcher",
    url: "http://127.0.0.1:8000/user/researcher/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentResearcherLab: {
    id: "researcherLab",
    url: "http://127.0.0.1:8000/user/laboratory/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentResearcherResearch: {
    id: "researcherResearch",
    url: "http://127.0.0.1:8000/user/research/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentResearchResearcher: {
    id: "researchResearcher",
    url: "http://127.0.0.1:8000/user/researcher/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentResearchNews: {
    id: "researchNews",
    url: "http://127.0.0.1:8000/user/news/thumbnail?",
    pageSize: 4,
    param: {}, //laboratory_id, maybe research_id
  },
  recentResearchEvent: {
    id: "researchEvent",
    url: "http://127.0.0.1:8000/user/event/thumbnail?",
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
    pageSize: 6,
  },
  recentGridResearch: {
    id: "recentGridResearch",
    // type: "n",
    pageSize: 6,
  },
  relatedNews: {
    id: "relatedNews",
    url: "http://127.0.0.1:8000/user/news/related_news?",
    // type: "n",
    pageSize: 4,
  },
};
