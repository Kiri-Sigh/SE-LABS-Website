import { useParams } from "react-router-dom";
import Description from "../../component/Description/Description";
import RecentEvents from "../../component/Events/Recent-Events/Recent-Events";
import RecentNews from "../../component/News/Recent-News/Recent-News";
import TopicAndImage from "../../component/others/Big-Image/Topic-And-Image";

import { getData } from "api/api-method";
import { exampleToFetchData } from "PlaceHolder-Data/toFetch";
import { useQueryGetImg } from "api/custom-hooks";

function DynamicEventPage() {
  const { id } = useParams(); // Access the id from the route
  const { data } = getData(
    `http://127.0.0.1:8000/user/event/thumbnail?event_id=${id}&amount=1&page=1`
  );
  const { data: img } = useQueryGetImg(
    `http://127.0.0.1:8000/user`,
    "event",
    id
  );
  //lab news,lab event,lab people,lab publication,lab research
  return (
    <>
      <TopicAndImage data={data} image={img} />
      <Description data={data} />
    </>
  );
}
export default DynamicEventPage;

//fetch lab info, fetch image, then fetch projects etc...
