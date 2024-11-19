import { useParams } from "react-router-dom";
import Description from "../../component/Description/Description";
import RecentEvents from "../../component/Events/Recent-Events/Recent-Events";
import RecentNews from "../../component/News/Recent-News/Recent-News";
import TopicAndImage from "../../component/others/Big-Image/Topic-And-Image";

import { getData } from "api/api-method";
import { exampleToFetchData } from "PlaceHolder-Data/toFetch";
import { useNormalQueryGet, useQueryGetImg } from "api/custom-hooks";

function DynamicPeoplePage() {
  const { id } = useParams(); // Access the id from the route
  const { data, isLoading } = useNormalQueryGet(
    `http://127.0.0.1:8000/user/researcher/thumbnail/${id}`,
    "researcher",
    id
  );
  if (data) console.log("dat?", data);
  const { data: img, isLoading: isLoading2 } = useQueryGetImg(
    `http://127.0.0.1:8000/user`,
    "researcher",
    id
  );
  if (isLoading2) console.log("isloading?", isLoading2);

  //lab news,lab event,lab people,lab publication,lab research
  return (
    <>
      <TopicAndImage
        data={data}
        image={img}
        isLoading={isLoading}
        isLoading2={isLoading2}
      />
      <Description data={data} />
      <RecentNews
        toFetchedData={exampleToFetchData.recentResearcherResearch}
        filter={{ researcher_id: id }}
        componentTitle="Researcher Research"
      />
      <RecentNews
        toFetchedData={exampleToFetchData.recentResearcherLab}
        filter={{ researcher_id: id }}
        componentTitle="Researcher Laboratory"
      />
    </>
  );
}
export default DynamicPeoplePage;

//fetch lab info, fetch image, then fetch projects etc...
