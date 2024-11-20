import { useParams } from "react-router-dom";
import Description from "../../component/Description/Description";
import RecentEvents from "../../component/Events/Recent-Events/Recent-Events";
import RecentNews from "../../component/News/Recent-News/Recent-News";
import TopicAndImage from "../../component/others/Big-Image/Topic-And-Image";

import { getData } from "api/api-method";
import { exampleToFetchData } from "PlaceHolder-Data/toFetch";
import { useNormalQueryGet, useQueryGetImg } from "api/custom-hooks";

function DynamicEventPage() {
    const { id } = useParams(); // Access the id from the route
    const { data, isLoading } = useNormalQueryGet(
        `http://127.0.0.1:8000/user/event/thumbnail/${id}?amount=1&page=1`,
        "Event",
        id
    );
    const { data: img, isLoading: isLoading2 } = useQueryGetImg(
        `http://127.0.0.1:8000/user`,
        "event",
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
            />{" "}
            <Description data={data} />
        </>
    );
}
export default DynamicEventPage;

//fetch lab info, fetch image, then fetch projects etc...
