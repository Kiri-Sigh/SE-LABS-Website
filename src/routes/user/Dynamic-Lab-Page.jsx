import { useParams } from "react-router-dom";
import Description from "../../component/Description/Description";
import RecentEvents from "../../component/Events/Recent-Events/Recent-Events";
import RecentNews from "../../component/News/Recent-News/Recent-News";
import TopicAndImage from "../../component/others/Big-Image/Topic-And-Image";

import { getData } from "api/api-method";
import TeamCard from "component/Cards/Team-Card";
import { exampleToFetchData } from "PlaceHolder-Data/toFetch";
import { useNormalQueryGet, useQueryGetImg } from "api/custom-hooks";

function DynamicLabPage() {
  const { id } = useParams(); // Access the id from the route
  const { data, isLoading } = useNormalQueryGet(
    `http://10.125.2.83:8000/user/laboratory/thumbnail?laboratory_id=${id}&amount=1&page=1`,
    "Laboratory",
    id
  );
  if (data) console.log("dat?", data);
  const { data: img, isLoading: isLoading2 } = useQueryGetImg(
    `http://10.125.2.83:8000/user`,
    "laboratory",
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
        isLab={true}
      />
      <Description data={data} isLab={true} isLoading={isLoading} />
      <RecentNews
        toFetchedData={exampleToFetchData.recentLabResearch}
        filter={{ laboratory_id: id }}
        componentTitle="Lab Research"
      />
      <RecentNews
        toFetchedData={exampleToFetchData.recentLabResearcher}
        filter={{ laboratory_id: id }}
        componentTitle="Lab People"
      />
      <RecentNews
        toFetchedData={exampleToFetchData.recentLabPublication}
        filter={{ laboratory_id: id }}
        componentTitle="Lab Publication"
        publicationLink={"https://www.se.kmitl.ac.th/"}
      />
      <RecentNews
        toFetchedData={exampleToFetchData.recentLabNews}
        filter={{ laboratory_id: id }}
        componentTitle="Lab News"
      />
      <RecentEvents
        toFetchedData={exampleToFetchData.recentLabEvent}
        filter={{ laboratory_id: id }}
        componentTitle="Lab Events"
      />
    </>
  );
}
export default DynamicLabPage;

//fetch lab info, fetch image, then fetch projects etc...
