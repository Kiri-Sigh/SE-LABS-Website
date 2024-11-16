import { useParams } from "react-router-dom";
import Description from "../../component/Description/Description";
import RecentEvents from "../../component/Events/Recent-Events/Recent-Events";
import RecentNews from "../../component/News/Recent-News/Recent-News";
import TopicAndImage from "../../component/others/Big-Image/Topic-And-Image";

import { getData } from "api/api-method";
import { exampleToFetchData } from "PlaceHolder-Data/toFetch";

import { useQueryGetImg } from "api/custom-hooks";

function DynamicResearchPage() {
  const { id } = useParams(); // Access the id from the route
  const { data } = getData(
    `http://127.0.0.1:8000/user/research/thumbnail?research_id=${id}&amount=1&page=1`
  );
  const { data: img } = useQueryGetImg(
    `http://127.0.0.1:8000/user`,
    "research",
    id
  );
  //lab news,lab event,lab people,lab publication,lab research
  return (
    <>
      <TopicAndImage data={data} image={img} />
      <Description data={data} />

      <RecentNews
        toFetchedData={exampleToFetchData.recentResearchResearcher}
        filter={{ research_id: id }}
        componentTitle="Reseachers"
      />
      <RecentNews
        toFetchedData={exampleToFetchData.recentResearchNews}
        filter={{ research_id: id }}
        componentTitle="Research News"
      />
      <RecentEvents
        toFetchedData={exampleToFetchData.recentResearchEvent}
        filter={{ research_id: id }}
        componentTitle="Research Events"
      />
    </>
  );
}
export default DynamicResearchPage;

//fetch lab info, fetch image, then fetch projects etc...
