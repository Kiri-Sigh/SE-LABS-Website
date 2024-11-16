import { useParams } from "react-router-dom";
import Description from "../../component/Description/Description";
import RecentEvents from "../../component/Events/Recent-Events/Recent-Events";
import RecentNews from "../../component/News/Recent-News/Recent-News";
import TopicAndImage from "../../component/others/Big-Image/Topic-And-Image";

import { getData } from "api/api-method";
import { exampleToFetchData } from "PlaceHolder-Data/toFetch";
import { useQueryGetImg } from "api/custom-hooks";

function DynamicPeoplePage() {
  const { id } = useParams(); // Access the id from the route
  const { data } = getData(
    `http://127.0.0.1:8000/user/researcher/thumbnail?researcher_id=${id}&amount=1&page=1`
  );
  if (data) console.log("dat?", data);
  const { data: img } = useQueryGetImg(
    `http://127.0.0.1:8000/user`,
    "researcher",
    id
  );
  //lab news,lab event,lab people,lab publication,lab research
  return (
    <>
      <TopicAndImage data={data} image={img} />
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
