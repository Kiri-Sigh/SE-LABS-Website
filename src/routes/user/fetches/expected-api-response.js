import { DataFetcherQueue } from "./fetch-dynamic-page";
import { useParallelData, useInfiniteFetch } from "../../../api/custom-hooks";

//api || code
//amount || pageSize

//type: n = normal , np = normal+img , inf = infinite query , infp = infinite query+img

//request --response
//laboratory_id --LID
//researcher_id --UID
//

//np -> append ID to new arr to process and get img and assign to according obj
const dynamicLabPageTemplate = [
  //lab info,team,research,news, publication,events
  [
    {
      ID: "abc",
      url: "user/laboratory/thumbnail/LID",
      type: "np",
      imgType: ["LID"],
      imgSize: ["high"],
    },
  ],
  [
    {
      ID: "xyz",
      url: "user/researcher/LID/",
      type: "infp",
      pageSize: 5,
      imgType: ["UID", "LID"],
      imgSize: ["high", "low"],
    },
  ],
  [
    {
      ID: "xyz",
      url: "user/researc/LID/",
      type: "infp",
      pageSize: 5,
      imgType: ["UID", "LID"],
      imgSize: ["high", "low"],
    },
  ],

  // [
  //   {
  //     ID: "abc",
  //     url: "https://jsonplaceholder.typicode.com/posts/1",
  //     type: "inf",
  //     pageSize: 5,
  //   },
  // ],
];

////////////////////////////////
//Dynamic Lab page

const dynamicLabPage = DataFetcherQueue(dynamicLabPageTemplate);
