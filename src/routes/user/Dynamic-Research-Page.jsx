import { useParams } from "react-router-dom";
import Description from "../../component/Description/Description";
import RecentEvents from "../../component/Events/Recent-Events/Recent-Events";
import RecentNews from "../../component/News/Recent-News/Recent-News";
import TopicAndImage from "../../component/others/Big-Image/Topic-And-Image";

import { getData } from "api/api-method";
import { exampleToFetchData } from "PlaceHolder-Data/toFetch";

import { useNormalQueryGet, useQueryGetImg } from "api/custom-hooks";

function DynamicResearchPage() {
  const { id } = useParams(); // Access the id from the route
  console.log(id);
  const { data, isLoading } = useNormalQueryGet(
    `http://10.125.2.83:8000/user/research/thumbnail/${id}`,
    "research",
    id
  );
  if (data) console.log(data);
  const { data: img, isLoading: isLoading2 } = useQueryGetImg(
    `http://10.125.2.83:8000/user`,
    "research",
    id
  );
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

      {/* <RecentNews
        toFetchedData={exampleToFetchData.recentResearchResearcher}
        filter={{ research_id: id }}
        componentTitle="Reseachers"
      /> */}
      <RecentNews
        toFetchedData={exampleToFetchData.recentResearchNews}
        filter={{ research_id: id }}
        componentTitle="Research News"
      />
      <RecentEvents
        // toFetchedData={exampleToFetchData.recentResearchEvent}
        toFetchedData={exampleToFetchData.recentResearchEvent}
        filter={{ research_id: id }}
        componentTitle="Research Events"
      />
    </>
  );
}
export default DynamicResearchPage;

//fetch lab info, fetch image, then fetch projects etc...
