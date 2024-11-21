import { useParams } from "react-router-dom";
import Description from "../../component/Description/Description";
import RecentNews from "../../component/News/Recent-News/Recent-News";
import TopicAndImage from "../../component/others/Big-Image/Topic-And-Image";

import { getData } from "api/api-method";
import { exampleToFetchData } from "PlaceHolder-Data/toFetch";
import { useNormalQueryGet, useQueryGetImg } from "api/custom-hooks";

function DynamicNewsPage() {
  const { id } = useParams(); // Access the id from the route
  const { data, isLoading } = useNormalQueryGet(
    `http://127.0.0.1:8000/user/news/thumbnail/${id}?amount=1&page=1`,
    "News",
    id
  );
  const { data: img, isLoading: isLoading2 } = useQueryGetImg(
    `http://127.0.0.1:8000/user`,
    "news",
    id
  );
  //related research , related news, related lab
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
        toFetchedData={exampleToFetchData.recentNewsResearch}
        filter={{ news_id: id }}
        componentTitle="Related Research"
      />
      <RecentNews
        toFetchedData={exampleToFetchData.recentNewsLaboratory}
        filter={{ news_id: id }}
        componentTitle="Related Laboratory"
      /> */}
      <RecentNews
        toFetchedData={exampleToFetchData.relatedNews}
        filter={{ news_id: id }}
        componentTitle="Other Related News"
      />
    </>
  );
}
export default DynamicNewsPage;

//fetch lab info, fetch image, then fetch projects etc...
